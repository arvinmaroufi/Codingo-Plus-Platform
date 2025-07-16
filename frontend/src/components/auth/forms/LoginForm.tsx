"use client";

import { useState, useEffect, FormEvent } from "react";
import { signIn } from "next-auth/react";
import { useRouter, useSearchParams } from "next/navigation";

import { PhoneInput } from "./PhoneInput";
import { ModeSwitch } from "./ModeSwitch";
import { PasswordLoginForm } from "./PasswordLoginForm";
import { OTPLoginForm } from "./OTPLoginForm";



export default function LoginForm() {
  const router = useRouter();
  const params = useSearchParams();
  const callbackUrl = params.get("callbackUrl") || "/";

  // --- shared state ---
  const [phone, setPhone] = useState("");
  const [canProceed, setCanProceed] = useState(false);
  const [mode, setMode] = useState<"default" | "password" | "otp">("default");
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  // --- password state ---
  const [password, setPassword] = useState("");

  // --- OTP state ---
  const [otpToken, setOtpToken] = useState("");
  const [otpCode, setOtpCode] = useState("");
  const [devOtp, setDevOtp] = useState("");

  // enable only when phone length ≥11
  useEffect(() => {
    setCanProceed(/^\d{11,}$/.test(phone.trim()));
  }, [phone]);

  // 1) password login
  async function handlePasswordLogin(e: FormEvent) {
    e.preventDefault();
    setErrorMsg(""); setLoading(true);

    const res = await signIn("credentials", {
      redirect: false,
      phone, password,
      callbackUrl,
    });
    setLoading(false);
    if (res?.error) return setErrorMsg(res.error);
    router.push(res?.url || callbackUrl);
  }

  // 2) request OTP
  async function handleRequestOtp() {
    setErrorMsg(""); setLoading(true);

    try {
      const res = await fetch(
        `${process.env.DJANGO_API_URL}/auth/login-request-otp/`,
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
      console.log(data.detail);
      setOtpToken(data.detail.token);
      setDevOtp(data.detail.code || "");
      setMode("otp");
    } catch {
      setLoading(false);
      setErrorMsg("خطای شبکه، دوباره تلاش کنید");
    }
  }

  // 3) verify OTP
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
      {/* PHONE */}
      <PhoneInput phone={phone} setPhone={setPhone} />

      {/* MODE SWITCH OR ERROR */}
      {mode === "default" && (
        <ModeSwitch
          mode={mode}
          canProceed={canProceed}
          loading={loading}
          onOtpRequest={handleRequestOtp}
          onPasswordChoose={() => {
            setMode("password");
            setErrorMsg("");
          }}
        />
      )}
      {errorMsg && (
        <p className="mb-4 text-sm text-red-600">{errorMsg}</p>
      )}

      {/* PASSWORD */}
      {mode === "password" && (
        <PasswordLoginForm
          password={password}
          setPassword={setPassword}
          loading={loading}
          onSubmit={handlePasswordLogin}
        />
      )}

      {/* OTP */}
      {mode === "otp" && (
        <OTPLoginForm
          phone={phone}
          devOtp={devOtp}
          otpCode={otpCode}
          setOtpCode={setOtpCode}
          loading={loading}
          onSubmit={handleVerifyOtp}
        />
      )}
    </div>
  );
}
