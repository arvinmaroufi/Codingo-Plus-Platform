// app/providers/ClientProviders.tsx
"use client";

import { ReactNode } from "react";
import { SessionProvider } from "next-auth/react";
import Theme from "@/providers/ThemeProvider";
import Navbar from "@/components/Navbar";

export default function ClientProviders({
  children,
  session,
}: {
  children: ReactNode;
  session?: any;
}) {
  return (
    <SessionProvider session={session} basePath="/api/auth">
      <Theme>
        {children}
      </Theme>
    </SessionProvider>
  );
}
