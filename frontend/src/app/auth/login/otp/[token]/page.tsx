"use client";

import React, { useState } from "react";
import MainHeroSection from "@/components/main/hero-section";
import OTPInput from "@/components/auth/otp-input";




export default function ValidateLoginOtpPage() {
  // Track the OTP code in state.
  const [otpCode, setOtpCode] = useState("");

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // For debugging, we log immediately whether or not the length is complete.
    console.log("Submit clicked, current OTP:", otpCode);
    
    // If you still want to enforce the length, you can do so.
    if (otpCode.length !== 6) {
      alert("لطفاً کد تایید را به طور کامل وارد کنید.");
      return;
    }
    
    // Now log the OTP before sending it to the server.
    console.log("Submitting OTP:", otpCode);
    // Here you can call your API
  };

  return (
    <main className="flex justify-between items-center gap-6 flex-col mx-auto sm:px-10 px-5">
      <MainHeroSection />
      <div className="shadow-input mx-auto max-w-md rounded-none bg-highlight-text-dark p-4 md:rounded-2xl md:p-8 dark:bg-main-text-light">
        <h2 className="text-xl font-bold text-main-text-light dark:text-main-text-dark">
          به کدنیگو پلاس خوش آمدید
        </h2>
        <p className="mt-2 max-w-sm text-sm text-main-text-light dark:text-main-text-dark">
          برای ورود به دنیای عمیق و زیبای برنامه نویسی و مهدنسی نرم لافز ار به ما ملحق شوید
        </p>
        <form className="my-8" onSubmit={handleSubmit}>
          <div className="flex flex-col space-y-2 mb-4">
            <label
              htmlFor="otp"
              className="text-sm font-medium text-black dark:text-white"
            >
              کد تایید
            </label>
            <OTPInput
              length={6}
              onChange={(code) => {
                setOtpCode(code);
                console.log("OTP updated:", code);
              }}
            />
          </div>
          <button
            className="group/btn relative block h-10 w-full rounded-md bg-gradient-to-br from-base-dark to-primary-light font-medium text-highlight-text-light shadow-[0px_1px_0px_0px_#ffffff40_inset, 0px_-1px_0px_0px_#ffffff40_inset] dark:bg-base-light dark:from-base-light dark:to-primary-dark dark:text-main-text-light dark:shadow-[0px_1px_0px_0px_#27272a_inset, 0px_-1px_0px_0px_#27272a_inset]"
            type="submit"
          >
            ورود
            <BottomGradient />
          </button>
          <div className="my-8 h-[1px] w-full bg-gradient-to-r from-transparent via-neutral-300 to-transparent dark:via-primary-dark" />
          <div className="flex flex-col space-y-4">
            <button
              className="group/btn shadow-input relative flex h-10 w-full items-center justify-center rounded-md bg-gray-50 px-4 font-medium text-black dark:bg-zinc-900 dark:shadow-[0px_0px_1px_1px_#262626]"
              type="button"
              onClick={() => console.log("Resend OTP")}
            >
              <span className="text-sm text-neutral-700 dark:text-neutral-300">
                ارسال مجدد کد تایید
              </span>
              <BottomGradient />
            </button>
          </div>
        </form>
      </div>
    </main>
  );
}

const BottomGradient = () => {
  return (
    <>
      <span className="absolute inset-x-0 -bottom-px block h-px w-full bg-gradient-to-r from-transparent via-primary-dark dark:via-primary-light to-transparent opacity-0 transition duration-500 group-hover/btn:opacity-100" />
      <span className="absolute inset-x-10 -bottom-px mx-auto block h-px w-1/2 bg-gradient-to-r from-transparent via-base-dark dark:via-base-light to-transparent opacity-0 blur-sm transition duration-500 group-hover/btn:opacity-100" />
    </>
  );
};
