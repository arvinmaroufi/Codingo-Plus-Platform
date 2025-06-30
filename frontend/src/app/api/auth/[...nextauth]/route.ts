import NextAuth, { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import { jwtDecode } from "jwt-decode";
import { JWT } from "next-auth/jwt";
import { UserType } from "@/types/next-auth";


interface TokenPayload {
  user_id: number;
  phone: string;
  email: string;
  full_name: string;
  user_type: string;
  profile: string;
  exp: number;
}


export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        phone: { label: "Phone", type: "phone" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        // 1) Hit Django /api/token/
        const res = await fetch(
          `${process.env.DJANGO_API_URL}auth/login-password/`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(credentials),
          }
        );
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Invalid credentials");

        console.log(data)

        // 2) Decode JWT to extract user info & expiry
        const payload = jwtDecode<TokenPayload>(data.access);

        console.log(payload)

        // 3) Return a “user” object that NextAuth will persist into its JWT
        return {
          id: payload.user_id,
          phone: payload.phone,
          email: payload.email,
          full_name: payload.full_name,
          user_type: payload.user_type,
          profile: payload.profile,
          accessToken: data.access,
          refreshToken: data.refresh,
          accessTokenExpires: payload.exp * 1000,
        };
      },
    }),
  ],

  session: { strategy: "jwt", maxAge: 60 * 60 },

  callbacks: {
    // Persist tokens in the NextAuth JWT
    async jwt({ token, user }) {
      // First time signing in
      if (user) {
        return {
          ...token,
          userId: user.id,
          user_type: user.user_type,
          phone: user.phone,
          email: user.email,
          full_name: user.full_name,
          profile: user.profile,
          accessToken: (user as any).accessToken,
          refreshToken: (user as any).refreshToken,
          accessTokenExpires: (user as any).accessTokenExpires,
        } as JWT;
      }
      // If token still valid, just return it
      if (Date.now() < (token.accessTokenExpires as number)) {
        return token;
      }
      // Otherwise, refresh it
      try {
        const res = await fetch(
          `${process.env.DJANGO_API_URL}auth/refresh/`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh: token.refreshToken }),
          }
        );
        const refreshed = await res.json();
        if (!res.ok) throw refreshed;
        const newPayload = jwtDecode<TokenPayload>(refreshed.access);
        return {
          ...token,
          accessToken: refreshed.access,
          accessTokenExpires: newPayload.exp * 1000,
          refreshToken: refreshed.refresh ?? token.refreshToken,
        } as JWT;
      } catch {
        return { ...token, error: "RefreshAccessTokenError" } as JWT;
      }
    },

    // Make token props available in `useSession()`
    async session({ session, token }) {
      return {
        ...session,
        user: {
          ...session.user!,
          id: token.userId as number,
          phone: token.phone as string,
          email: token.email as string,
          full_name: token.full_name as string,
          profile: token.profile as string,
          user_type: token.user_type as UserType,
        },
        accessToken: token.accessToken as string,
      };
    },
  },

  secret: process.env.NEXTAUTH_SECRET,
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
