"use client";
import React, { FormEvent } from "react";
import { Label } from "@/components/ui/label";
import OTPInput from "../OtpInput";
import { BottomGradient } from "./BottomGradient";


export function OTPRegisterForm({
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
  setOtpCode: (s:string)=>void;
  loading: boolean;
  onSubmit: (e: FormEvent) => void;
}) {
  return (
    <form onSubmit={onSubmit} className="space-y-4 w-full">
      <p className="text-sm">
        برای شماره <strong>{phone}</strong> کد زیر ارسال شد:
      </p>
      <code className="block mt-1 p-1 bg-gray-200 rounded">
        {devOtp || "----"}
      </code>

      <div className="space-y-1">
        <Label>کد OTP</Label>
        <OTPInput length={6} onChange={setOtpCode} onComplete={setOtpCode} />
      </div>

      <button
        type="submit"
        disabled={loading || otpCode.length < 6}
        className="group/btn relative block w-full py-2 bg-green-600 text-white rounded disabled:opacity-50"
      >
        {loading ? "در حال تایید…" : "ثبت‌نام نهایی"}
        <BottomGradient />
      </button>
    </form>
  );
}
