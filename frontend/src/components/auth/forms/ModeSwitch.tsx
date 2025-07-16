"use client";
import React from "react";
import { cn } from "@/lib/utils";

export function ModeSwitch({
  mode,
  canProceed,
  loading,
  onOtpRequest,
  onPasswordChoose,
}: {
  mode: "default" | "password" | "otp";
  canProceed: boolean;
  loading: boolean;
  onOtpRequest: () => void;
  onPasswordChoose: () => void;
}) {
  return (
    <div className="flex gap-4 mb-6 w-full">
      <button
        type="button"
        disabled={!canProceed || loading}
        onClick={onOtpRequest}
        className={cn(
          "flex-1 py-2 rounded",
          canProceed
            ? "bg-primary-light text-white"
            : "bg-gray-300 text-gray-600 cursor-not-allowed"
        )}
      >
        {loading ? "در حال پردازش…" : "درخواست کد"}
      </button>
      <button
        type="button"
        disabled={!canProceed || loading}
        onClick={onPasswordChoose}
        className={cn(
          "flex-1 py-2 rounded",
          canProceed
            ? "bg-secondary-light text-black"
            : "bg-gray-300 text-gray-600 cursor-not-allowed"
        )}
      >
        وارد کردن رمز عبور
      </button>
    </div>
  );
}
