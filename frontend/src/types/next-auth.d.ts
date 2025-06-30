// types/next-auth.d.ts
import NextAuth, { DefaultSession, DefaultUser } from "next-auth";
import { JWT as NextAuthJWT } from "next-auth/jwt";

export type UserType = | "AD" | "TE" | "ST" | "SU"

declare module "next-auth" {
  interface Session extends DefaultSession {
    user: {
      id: number;
      phone: string;
      email: string;
      full_name: string;
      user_type: string;
      profile: string;
    } & DefaultSession["user"];
    accessToken: string;
  }

  interface User extends DefaultUser {
    user_id: number;
    phone: string;
    email: string;
    full_name: string;
    user_type: string;
    profile: string;
    user_type: UserType;
  }
}

declare module "next-auth/jwt" {
  interface JWT extends NextAuthJWT {
    user_id: number;
    phone: string;
    email: string;
    full_name: string;
    user_type: string;
    profile: string;
    accessToken: string;
    refreshToken: string;
    accessTokenExpires: number;
    error?: "RefreshAccessTokenError";
  }
}
