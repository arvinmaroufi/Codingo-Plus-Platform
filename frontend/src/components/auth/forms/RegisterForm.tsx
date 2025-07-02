// components/RegisterForm.tsx
"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/label";
import OTPInput from "../OtpInput";
import { cn } from "@/lib/utils";
import { signIn } from "next-auth/react";



export default function RegisterForm() {
  const router = useRouter();
  const API = process.env.DJANGO_API_URL!.replace(/\/+$/, "");
  const [step, setStep] = useState<1 | 2>(1);

  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConf, setPasswordConf] = useState("");

  const [token, setToken] = useState("");
  const [devOtp, setDevOtp] = useState(""); // for dev/testing
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Step 1: initiate registration → get token + otp
  async function handleInit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await fetch(
        `${API}/auth/register-request-otp/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            phone,
            email,
            username,
            user_type: 'ST',
            full_name: fullName,
            password,
            password_conf: passwordConf,
          }),
        }
      );
      const data = await res.json();
      setLoading(false);

      if (!res.ok) {
        return setError(data.detail || "خطا در ارسال OTP");
      }

      setToken(data.detail.token);
      setDevOtp(data.detail.code || "");
      setStep(2);

    } catch (err) {
      console.error(err);
      setLoading(false);
      setError("خطای شبکه، دوباره تلاش کنید");
    }
  }

  // Step 2: verify OTP + token → finalize + auto-login
  async function handleVerify(e: FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      // 1) hit your validate-OTP endpoint
      const res = await fetch(
        `${API}/auth/register-validate-otp/${token}/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code }),
        }
      );

      const data = await res.json();
      setLoading(false);

      if (!res.ok) {
        return setError(data.detail.message || "کد صحیح نیست");
      }

      // 2) extract the tokens your backend returned
      const { access, refresh } = data.detail.token;

      // 3) seed NextAuth with those tokens via the "otp" provider
      const otpRes = await signIn("otp", {
        redirect: false,
        accessToken: access,
        refreshToken: refresh,
        callbackUrl: "/",
      });

      if (otpRes?.error) {
        setError(otpRes.error);
      } else {
        // 4) push to your landing
        router.push("/");
      }
    } catch (err) {
      console.error(err);
      setLoading(false);
      setError("خطای شبکه، دوباره تلاش کنید");
    }
  }


  return (
    <div className="max-w-md mx-auto space-y-6">
      {error && <p className="text-red-600">{error}</p>}

      {step === 1 ? (
        <form onSubmit={handleInit} className="space-y-4">
          {/* phone */}
          <LabelInputContainer className="space-y-1">
            <Label htmlFor="phone">شماره تلفن</Label>
            <Input
              id="phone"
              type="tel"
              required
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
            />
          </LabelInputContainer>

          {/* email */}
          <LabelInputContainer className="space-y-1">
            <Label htmlFor="email">ایمیل</Label>
            <Input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </LabelInputContainer>

          {/* username */}
          <LabelInputContainer className="space-y-1">
            <Label htmlFor="username">نام کاربری</Label>
            <Input
              id="username"
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </LabelInputContainer>

          {/* full name */}
          <LabelInputContainer className="space-y-1">
            <Label htmlFor="fullName">نام کامل</Label>
            <Input
              id="fullName"
              type="text"
              required
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
            />
          </LabelInputContainer>

          {/* password */}
          <LabelInputContainer className="space-y-1">
            <Label htmlFor="password">رمز عبور</Label>
            <Input
              id="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </LabelInputContainer>

          {/* password confirm */}
          <LabelInputContainer className="space-y-1">
            <Label htmlFor="passwordConf">تکرار رمز عبور</Label>
            <Input
              id="passwordConf"
              type="password"
              required
              value={passwordConf}
              onChange={(e) => setPasswordConf(e.target.value)}
            />
          </LabelInputContainer>

          <button
            type="submit"
            disabled={loading}
            className="group/btn relative block h-10 w-full rounded-md bg-gradient-to-br from-base-dark to-primary-light font-medium text-highlight-text-light shadow-[0px_1px_0px_0px_#ffffff40_inset,0px_-1px_0px_0px_#ffffff40_inset] dark:bg-base-light dark:from-base-light dark:to-primary-dark dark:text-main-text-light dark:shadow-[0px_1px_0px_0px_#27272a_inset,0px_-1px_0px_0px_#27272a_inset]"
          >
            {loading ? "درحال برسیی" : "ثبت نام"}
            <BottomGradient />
          </button>

          <div className="my-8 h-[1px] w-full bg-gradient-to-r from-transparent via-neutral-300 to-transparent dark:via-primary-dark" />

          <div className="flex flex-row gap-10">
            <button
                className="group/btn shadow-input relative flex h-10 w-full justify-center items-center space-x-2 rounded-md bg-secondary-light px-4 font-medium text-main-text-light dark:bg-secondary-dark dark:shadow-[0px_0px_1px_1px_#262626]"
                type="button"
            >
                <span className="text-sm font-bold text-center text-main-text-light">ورود</span>
                <BottomGradient />
            </button>
            <button
                className="group/btn shadow-input relative flex h-10 w-full justify-center items-center space-x-2 rounded-md bg-secondary-light px-4 font-medium text-main-text-light dark:bg-secondary-dark dark:shadow-[0px_0px_1px_1px_#262626]"
                type="button"
            >
                <span className="text-sm font-bold text-center text-main-text-light">بازیابی رمزعبور</span>
                <BottomGradient />
            </button>
          </div>
        </form>
      ) : (
        <form onSubmit={handleVerify} className="space-y-4">
          <p>
            برای شماره <strong>{phone}</strong>، کد زیر ارسال شد:
            <code className="block mt-1 p-1 bg-gray-200 rounded">
              {devOtp || "----"}
            </code>
          </p>

          <LabelInputContainer className="space-y-1">
            <Label>کد OTP</Label>
            <OTPInput
              length={6}
              onChange={setCode}
              onComplete={(c) => setCode(c)}
            />
          </LabelInputContainer>

          <button
            type="submit"
            disabled={loading}
            className="group/btn relative block h-10 w-full rounded-md bg-gradient-to-br from-base-dark to-primary-light font-medium text-highlight-text-light shadow-[0px_1px_0px_0px_#ffffff40_inset,0px_-1px_0px_0px_#ffffff40_inset] dark:bg-base-light dark:from-base-light dark:to-primary-dark dark:text-main-text-light dark:shadow-[0px_1px_0px_0px_#27272a_inset,0px_-1px_0px_0px_#27272a_inset]"
          >
            {loading ? "در حال برسی" : "ارسال کد تایید"}
            <BottomGradient />
          </button>
        </form>
      )}
    </div>
  );
}


const BottomGradient = () => (
  <>
    <span className="absolute inset-x-0 -bottom-px block h-px w-full bg-gradient-to-r from-transparent via-primary-dark dark:via-primary-light to-transparent opacity-0 transition duration-500 group-hover/btn:opacity-100" />
    <span className="absolute inset-x-10 -bottom-px mx-auto block h-px w-1/2 bg-gradient-to-r from-transparent via-base-dark dark:via-base-light to-transparent opacity-0 blur-sm transition duration-500 group-hover/btn:opacity-100" />
  </>
)

const LabelInputContainer = ({
  children,
  className,
}: {
  children: React.ReactNode
  className?: string
}) => (
  <div className={cn("flex w-full flex-col space-y-2", className)}>
    {children}
  </div>
)