"use client";
import React, { FormEvent } from "react";
import OTPInput from "../OtpInput";
import { BottomGradient } from "./BottomGradient";
import { Label } from "@/components/ui/label";


export function OTPLoginForm({
  phone,
  devOtp,
  otpCode,
  setOtpCode,
  loading,
  onSubmit,
}: {
  phone: string;
  devOtp: string;
  otpCode: string;
  setOtpCode: (val: string) => void;
  loading: boolean;
  onSubmit: (e: FormEvent) => void;
}) {
  return (
    <form onSubmit={onSubmit} className="space-y-4 w-full">
      <p className="text-sm">
        کد به <strong>{phone}</strong> ارسال شد:{" "}
        <code className="bg-gray-100 px-1 rounded">{devOtp || "----"}</code>
      </p>

      <div className="space-y-1">
        <Label>کد OTP</Label>
        <OTPInput length={6} onChange={setOtpCode} onComplete={setOtpCode} />
      </div>

      <button
        type="submit"
        disabled={loading || otpCode.length < 4}
        className="block w-full py-2 bg-gradient-to-br from-base-dark to-primary-light text-white rounded disabled:opacity-50 group/btn"
      >
        {loading ? "در حال تایید…" : "ورود با OTP"}
        <BottomGradient />
      </button>
    </form>
  );
}
