import NextAuth, { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import { jwtDecode } from "jwt-decode";
import { JWT } from "next-auth/jwt";
import { UserType } from "@/types/next-auth";



interface TokenPayload {
  id: number;
  is_admin: boolean;
  phone: string;
  email: string;
  full_name: string;
  username: string;
  user_type: UserType;
  profile: string;
  exp: number;
}



export const authOptions: NextAuthOptions = {
  providers: [
    // 1) Your existing phone/password creds
    CredentialsProvider({
      id: "credentials",
      name: "Credentials",
      credentials: {
        phone: { label: "Phone", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_DJANGO_API_URL}/auth/login-password/`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(credentials),
          }
        );
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Invalid login");

        const payload = jwtDecode<TokenPayload>(data.access);
        return {
          id: payload.id,
          phone: payload.phone,
          email: payload.email,
          full_name: payload.full_name,
          username: payload.username,
          user_type: payload.user_type,
          profile: payload.profile,
          is_admin: payload.is_admin,
          accessToken: data.access,
          refreshToken: data.refresh,
          accessTokenExpires: payload.exp * 1000,
        };
      },
    }),

    // 2) New “otp” provider that seeds NextAuth from your reg-validate tokens
    CredentialsProvider({
      id: "otp",
      name: "OTP",
      credentials: {
        accessToken: { label: "Access Token", type: "text" },
        refreshToken: { label: "Refresh Token", type: "text" },
      },
      async authorize(credentials) {
        const { accessToken, refreshToken } = credentials!;
        if (!accessToken) return null;

        const payload = jwtDecode<TokenPayload>(accessToken);

        return {
          id: payload.id,
          phone: payload.phone,
          email: payload.email,
          full_name: payload.full_name,
          username: payload.username,
          user_type: payload.user_type,
          profile: payload.profile,
          is_admin: payload.is_admin,
          accessToken,
          refreshToken: refreshToken!,
          accessTokenExpires: payload.exp * 1000,
        };
      },
    }),
  ],

  session: { strategy: "jwt", maxAge: 60 * 60 },

  callbacks: {
    async jwt({ token, user }) {
      // on first sign-in from either provider
      if (user) {
        return {
          ...token,
          ...user,
        } as JWT;
      }

      // when token is still valid, just return it
      if (Date.now() < (token.accessTokenExpires as number)) {
        return token;
      }

      // otherwise refresh
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_DJANGO_API_URL}/auth/refresh/`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh: token.refreshToken }),
          }
        );
        const data = await res.json();
        if (!res.ok) throw data;

        const newPayload = jwtDecode<TokenPayload>(data.access);
        return {
          ...token,
          accessToken: data.access,
          refreshToken: data.refresh ?? token.refreshToken,
          accessTokenExpires: newPayload.exp * 1000,
        } as JWT;
      } catch {
        return { ...token, error: "RefreshAccessTokenError" } as JWT;
      }
    },

    async session({ session, token }) {
      session.user = {
        id: token.id as number,
        phone: token.phone as string,
        email: token.email as string,
        full_name: token.full_name as string,
        username: token.username as string,
        user_type: token.user_type as UserType,
        profile: token.profile as string,
        is_admin: token.is_admin as boolean,
        name: session.user?.name ?? token.email as string,
      };
      session.accessToken = token.accessToken as string;
      return session;
    },
  },

  secret: process.env.NEXTAUTH_SECRET,
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
