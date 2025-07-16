"use client";

import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import { RegisterFieldsForm } from "./RegisterFieldsForm";
import { OTPRegisterForm } from "./OTPRegisterForm";
import { signIn } from "next-auth/react";



export default function RegisterForm() {
  const router = useRouter();

  // step 1 = form fields, step 2 = OTP
  const [step, setStep] = useState<1|2>(1);

  // form fields
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConf, setPasswordConf] = useState("");

  // OTP
  const [otpToken, setOtpToken] = useState("");
  const [otpCode, setOtpCode] = useState("");
  const [devOtp, setDevOtp] = useState("");

  // flags
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  // 1) request OTP
  async function handleInit(e: FormEvent) {
    e.preventDefault();
    setErrorMsg(""); setLoading(true);

    const res = await fetch(
      `${process.env.DJANGO_API_URL}auth/register-request-otp/`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          phone, email, username,
          full_name: fullName,
          password, password_conf: passwordConf,
          user_type: "ST",         // hard‐coded
        }),
      }
    );
    const data = await res.json();
    setLoading(false);

    if (!res.ok) {
      return setErrorMsg(data.detail.erorr || "خطا در ارسال OTP");
    }
    setOtpToken(data.detail.token);
    setDevOtp(data.detail.code || "");
    setStep(2);
  }

  // Step 2: verify OTP + token → finalize + auto-login
  async function handleVerify(e: FormEvent) {
    e.preventDefault();
    setErrorMsg("");
    setLoading(true);

    try {
      // 1) hit your validate-OTP endpoint
      console.log(otpCode)
      const res = await fetch(
        `${process.env.DJANGO_API_URL}auth/register-validate-otp/${otpToken}/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code: otpCode }),
        }
      );

      const data = await res.json();
      setLoading(false);

      if (!res.ok) {
        return setErrorMsg(data.detail.message || "کد صحیح نیست");
      }

      // 2) extract the tokens your backend returned
      const { access, refresh } = data.detail.token;

      // 3) seed NextAuth with those tokens via the "register-otp" provider
      const otpRes = await signIn("register-otp", {
        redirect: false,
        accessToken: access,
        refreshToken: refresh,
        callbackUrl: "/",
      });

      if (otpRes?.error) {
        setErrorMsg(otpRes.error);
      } else {
        // 4) push to your landing
        router.push("/");
      }
    } catch (err) {
      console.error(err);
      setLoading(false);
      setErrorMsg("خطای شبکه، دوباره تلاش کنید");
    }
  }

  return (
    <div className="max-w-md mx-auto space-y-6">
      {errorMsg && <p className="text-red-600">{errorMsg}</p>}

      {step === 1 && (
        <RegisterFieldsForm
          phone={phone} setPhone={setPhone}
          email={email} setEmail={setEmail}
          username={username} setUsername={setUsername}
          fullName={fullName} setFullName={setFullName}
          password={password} setPassword={setPassword}
          passwordConf={passwordConf} setPasswordConf={setPasswordConf}
          loading={loading}
          onSubmit={handleInit}
        />
      )}

      {step === 2 && (
        <OTPRegisterForm
          phone={phone}
          devOtp={devOtp}
          otpCode={otpCode}
          setOtpCode={setOtpCode}
          loading={loading}
          onSubmit={handleVerify}
        />
      )}
    </div>
  );
}
