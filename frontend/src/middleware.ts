// src/middleware.ts
import { getToken } from "next-auth/jwt";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { UserType } from "@/types/next-auth";

/** Public‐only pages: signed-in users should never see */
const PUBLIC_PAGES = [
  "/auth/login",
  "/auth/register",
  "/auth/reset-password",
  "/courses",
  "/about",
  "/blogs",
];

/** Role‐based protected sections */
const ROLE_ROUTES: Record<UserType, string[]> = {
  AD: ["admin"],
  TE: ["teachers/dashboard"],
  ST: ["dashboard"],
  SU: ["supporters/dashboard"],
};

export async function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;

  // Skip Next.js internals and static assets
  if (
    pathname.startsWith("/_next/") ||
    pathname.startsWith("/api/") ||
    pathname.includes(".")
  ) {
    return NextResponse.next();
  }

  // grab the NextAuth JWT (if any)
  const token = await getToken({
    req,
    secret: process.env.NEXTAUTH_SECRET,
    // cookieName: "next-auth.session-token", // override if you changed it
  });

  // 1) Public pages: if already signed in, bounce to dashboard
  if (PUBLIC_PAGES.some((p) => pathname === p)) {
    if (token) {
      return NextResponse.redirect(new URL("/dashboard", req.url));
    }
    return NextResponse.next(); // guest can view
  }

  // 2) Everything else requires a session
  if (!token) {
    return NextResponse.redirect(new URL("/auth/login", req.url));
  }

  // 3) Role check
  const userRole = token.user_type as UserType;
  const allowedRoots = ROLE_ROUTES[userRole] ?? [];
  const isAllowed = allowedRoots.some((root) =>
    pathname.startsWith(`/${root}`)
  );
  if (!isAllowed) {
    return NextResponse.redirect(new URL("/403", req.url));
  }

  // 4) All good
  return NextResponse.next();
}

export const config = {
  matcher: [
    // PUBLIC_PAGES
    "/auth/:path*",
    "/courses",
    "/about",
    "/blogs",

    // ROLE_ROUTES, as literals with wildcards
    "/admin/:path*",
    "/teachers/dashboard/:path*",
    "/dashboard/:path*",
    "/supporters/dashboard/:path*",
  ],
};
