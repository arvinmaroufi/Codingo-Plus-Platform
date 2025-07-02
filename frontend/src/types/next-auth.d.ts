import NextAuth, { DefaultSession, DefaultUser } from "next-auth";
import { JWT as NextAuthJWT } from "next-auth/jwt";

export type UserType = "AD" | "TE" | "ST" | "SU";



declare module "next-auth" {
  interface Session extends DefaultSession {
    user: {
      id: number;
      phone: string;
      email: string;
      full_name: string;
      username: string;
      user_type: UserType;
      profile: string;
      is_admin: boolean;
    } & DefaultSession["user"];
    accessToken: string;
  }



  interface User extends DefaultUser {
    id: number;
    phone: string;
    email: string;
    full_name: string;
    username: string;
    user_type: UserType;
    profile: string;
    is_admin: boolean;
  }
}



declare module "next-auth/jwt" {
  interface JWT extends NextAuthJWT {
    id: number;
    phone: string;
    email: string;
    full_name: string;
    username: string;
    user_type: UserType;
    profile: string;
    is_admin: boolean;
    accessToken: string;
    refreshToken: string;
    accessTokenExpires: number;
    error?: "RefreshAccessTokenError";
  }
}
