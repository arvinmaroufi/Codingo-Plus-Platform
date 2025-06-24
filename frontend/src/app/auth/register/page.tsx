"use client";
import React from "react";
import { Label } from "@/components/ui/Label";
import { Input } from "@/components/ui/Input";
import { cn } from "@/lib/utils";

import { MdLockReset } from "react-icons/md";
import { IoLogIn } from "react-icons/io5";
import HeroSection from "@/components/HeroSection";




export default function RegisterPage() {

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log("Form submitted");
    };


    return (
        <main className="flex justify-evenly items-center gap-6 flex-col mx-auto sm:px-10 px-5">
          <HeroSection
            title="ثبت نام"
            mainText="با ثبت نام در مجموعه کدینگو می توانید به دوره های ما دسترسی داشته باشید"
            subText="اگر حساب کاربری دارید می توانید وارد شوید"

            buttonTitle="ورود"
            buttonIcon={<IoLogIn />}
            buttonPosition="right"
            buttonUrl="/courses"
            buttonClasses="font-bold"
          />
          <div className="flex items-center justify-between shadow-input mx-auto max-w-lg bg-slate-50 p-4 rounded-2xl md:p-8 dark:bg-slate-800 w-[80vw]">
            <form className="w-full" onSubmit={handleSubmit}>
              {/* phone */}
              <LabelInputContainer className="mb-4">
                <Label htmlFor="phone">شماره تلفن</Label>
                <Input id="phone" placeholder="0912123456789" type="phone" />
              </LabelInputContainer>

              {/* email */}
              <LabelInputContainer className="mb-4">
                <Label htmlFor="email">ایمیل</Label>
                <Input id="email" placeholder="codingo-plus@gmail.com" type="email" />
              </LabelInputContainer>

              {/* username */}
              <LabelInputContainer className="mb-4">
                <Label htmlFor="username">نام کاربری</Label>
                <Input id="username" placeholder="Codingo-Plus" type="username" />
              </LabelInputContainer>

              {/* password */}
              <LabelInputContainer className="mb-4">
                <Label htmlFor="password">رمز عبور</Label>
                <Input id="password" placeholder="••••••••" type="password" />
              </LabelInputContainer>

              {/* password_conf */}
              <LabelInputContainer className="mb-4">
                <Label htmlFor="password_conf">تکرار رمز عبور</Label>
                <Input id="password_conf" placeholder="••••••••" type="password" />
              </LabelInputContainer>
      
              <button
                className="group/btn relative block h-10 w-full rounded-md bg-gradient-to-br from-base-dark to-primary-light font-bold text-highlight-text-light shadow-[0px_1px_0px_0px_#ffffff40_inset,0px_-1px_0px_0px_#ffffff40_inset] dark:bg-base-light dark:from-base-light dark:to-primary-dark dark:text-main-text-light dark:shadow-[0px_1px_0px_0px_#27272a_inset,0px_-1px_0px_0px_#27272a_inset]"
                type="submit"
              >
                ثبت نام
              <BottomGradient />
              </button>
            
              <div className="my-8 h-[1px] w-full bg-gradient-to-r from-transparent via-neutral-300 to-transparent dark:via-primary-dark" />
        
              <div className="flex flex-row gap-6">
                <button className="group/btn shadow-input relative flex h-10 w-full items-center justify-evenly space-x-2 rounded-md bg-primary-light px-4 font-bold dark:bg-primary-dark dark:shadow-[0px_0px_1px_1px_#262626]">
                    <IoLogIn className="h-4 w-4 text-main-text-light dark:text-highlight-text-dark" />
                    <span className="text-sm text-main-text-light dark:text-highlight-text-dark">ورود با حساب کاربری</span>
                    <BottomGradient />
                </button>
                <button className="group/btn shadow-input relative flex h-10 w-full items-center justify-evenly space-x-2 rounded-md bg-primary-light px-4 font-bold dark:bg-primary-dark dark:shadow-[0px_0px_1px_1px_#262626]">
                    <MdLockReset className="h-4 w-4 text-main-text-light dark:text-highlight-text-dark" />
                    <span className="text-sm text-main-text-light dark:text-highlight-text-dark">بازیابی رمز عبور</span>
                    <BottomGradient />
                </button>
              </div>
            </form>
          </div>
        </main>
    )
}

const BottomGradient = () => {
  return (
    <>
      <span className="absolute inset-x-0 -bottom-px block h-px w-full bg-gradient-to-r from-transparent via-primary-dark dark:via-primary-light to-transparent opacity-0 transition duration-500 group-hover/btn:opacity-100" />
      <span className="absolute inset-x-10 -bottom-px mx-auto block h-px w-1/2 bg-gradient-to-r from-transparent via-base-dark dark:via-base-light to-transparent opacity-0 blur-sm transition duration-500 group-hover/btn:opacity-100" />
    </>
  );
};
 
const LabelInputContainer = ({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) => {
  return (
    <div className={cn("flex w-full flex-col space-y-2", className)}>
      {children}
    </div>
  );
};