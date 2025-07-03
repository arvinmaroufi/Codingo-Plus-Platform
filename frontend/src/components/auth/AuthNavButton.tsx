"use client";

import { MouseEvent } from "react";
import { useSession } from "next-auth/react";
import { signOut } from "next-auth/react";
import Link from "next/link";


interface Props {
  callbackUrl?: string;
}

export default function AuthNavButton({ callbackUrl = "/auth/login" }: Props) {
    const { data: session } = useSession()

    const handleLogout = (e: MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();
        // This will clear the session cookie and redirect the browser.
        signOut({ callbackUrl });
    };

    if (session) {
        return (
            <button className="border text-sm font-medium relative border-neutral-200 dark:border-white/[0.2] text-main-text-light dark:text-main-text-dark px-4 py-2 rounded-full" onClick={handleLogout}>
                <span>خروج</span>
                <span className="absolute inset-x-0 w-1/2 mx-auto -bottom-px bg-gradient-to-r from-transparent via-primary-light dark:via-primary-dark to-transparent  h-px" />
            </button>
        )
    }
    else {
        return (
            <Link className="border text-sm font-medium relative border-neutral-200 dark:border-white/[0.2] text-main-text-light dark:text-main-text-dark px-4 py-2 rounded-full" href='/auth/login'>
                <span>ورود</span>
                <span className="absolute inset-x-0 w-1/2 mx-auto -bottom-px bg-gradient-to-r from-transparent via-primary-light dark:via-primary-dark to-transparent  h-px" />
            </Link>
        )
    }
}
