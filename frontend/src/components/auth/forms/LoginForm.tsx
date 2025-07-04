// components/auth/forms/LoginForm.tsx
"use client";

import { useState, useEffect, FormEvent } from "react";
import { signIn } from "next-auth/react";
import { useRouter, useSearchParams } from "next/navigation";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/Input";
import OTPInput from "../OtpInput";
import { cn } from "@/lib/utils";



export default function LoginForm() {
  const router = useRouter();
  const params = useSearchParams();
  const callbackUrl = params.get("callbackUrl") || "/";

  // fields + flags
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [otpToken, setOtpToken] = useState("");
  const [otpCode, setOtpCode] = useState("");
  const [devOtp, setDevOtp] = useState(""); // only for dev display

  const [mode, setMode] = useState<"default"|"password"|"otp">("default");
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  // buttons enabled once phone looks valid
  const [canProceed, setCanProceed] = useState(false);
  useEffect(() => {
    setCanProceed(/^\d{11,}$/.test(phone.trim()));
  }, [phone]);

  // 1) PHONE+PASSWORD login
  async function handlePasswordLogin(e: FormEvent) {
    e.preventDefault();
    setErrorMsg(""); setLoading(true);

    const res = await signIn("credentials", {
      redirect: false,
      phone, password, callbackUrl,
    });

    setLoading(false);
    if (res?.error) return setErrorMsg(res.error);
    router.push(res?.url || callbackUrl);
  }

  // 2) REQUEST OTP (single step)
  async function handleRequestOtp() {
    setErrorMsg(""); setLoading(true);

    try {
      const res = await fetch(
        `${process.env.DJANGO_API_URL}auth/login-request-otp/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ phone }),
        }
      );
      const data = await res.json();
      setLoading(false);

      if (!res.ok) {
        setErrorMsg(data.detail.message || "خطا در ارسال کد OTP");
        return;
      }

      setOtpToken(data.detail.token);
      setDevOtp(data.detail.code || "");
      setMode("otp");
    } catch {
      setLoading(false);
      setErrorMsg("خطای شبکه، دوباره تلاش کنید");
    }
  }

  // 3) VERIFY OTP + login-otp
  async function handleVerifyOtp(e: FormEvent) {
    e.preventDefault();
    setErrorMsg(""); setLoading(true);

    const res = await signIn("login-otp", {
      redirect: false,
      token: otpToken,
      code: otpCode,
      callbackUrl,
    });

    setLoading(false);
    if (res?.error) return setErrorMsg(res.error);
    router.push(res?.url || callbackUrl);
  }

  return (
    <div className="w-full max-w-md mx-auto">
      {/* PHONE INPUT (always visible) */}
      <div className="space-y-1 mb-6">
        <Label htmlFor="phone">شماره تلفن</Label>
        <Input
          id="phone"
          type="tel"
          placeholder="09121234567"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          required
        />
      </div>

      {/* MODE SWITCH */}
      {mode === "default" && (
        <div className="flex gap-4 mb-6">
          <button
            type="button"
            disabled={!canProceed || loading}
            onClick={handleRequestOtp}
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
            onClick={() => {
              setMode("password");
              setErrorMsg("");
            }}
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
      )}

      {/* ERROR MESSAGE */}
      {errorMsg && <p className="mb-4 text-sm text-red-600">{errorMsg}</p>}

      {/* PASSWORD FLOW */}
      {mode === "password" && (
        <form onSubmit={handlePasswordLogin} className="space-y-4">
          <div className="space-y-1">
            <Label htmlFor="password">رمز عبور</Label>
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 bg-gradient-to-br from-base-dark to-primary-light text-white rounded disabled:opacity-50"
          >
            {loading ? "در حال ورود…" : "ورود"}
          </button>
        </form>
      )}

      {/* OTP FLOW */}
      {mode === "otp" && (
        <form onSubmit={handleVerifyOtp} className="space-y-4">
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
            className="w-full py-2 bg-gradient-to-br from-base-dark to-primary-light text-white rounded disabled:opacity-50"
          >
            {loading ? "در حال تایید…" : "تایید"}
          </button>
        </form>
      )}
    </div>
  );
}
