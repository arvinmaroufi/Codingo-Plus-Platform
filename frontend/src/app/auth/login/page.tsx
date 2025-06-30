"use client";
import React from "react";
import { Label } from "@/components/ui/Label";
import { Input } from "@/components/ui/Input";
import { cn } from "@/lib/utils";

import {
  IconBrandGithub,
  IconBrandGoogle,
  IconBrandOnlyfans,
} from "@tabler/icons-react";
import HeroSection from "@/components/HeroSection";




export default function LoginPage() {

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log("Form submitted");
    };


    return (
        <main className="flex justify-between items-center gap-6 flex-col mx-auto sm:px-10 px-5">
          <HeroSection
            title="مجموعه ی کدینگو"
            mainText="آموزش توسعه و مهندسی نرم افزار"
            subText="به مجم.عه ی کدینگو خوش آمدید"

            buttonTitle="مشاهده ی دوره ها"
            buttonPosition="right"
            buttonUrl="/courses"
          />
          <div className="shadow-input mx-auto max-w-md rounded-none bg-highlight-text-dark  p-4 md:rounded-2xl md:p-8 dark:bg-main-text-light">
              <h2 className="text-xl font-bold text-main-text-light dark:text-main-text-dark">
                  به کدنیگو پلاس خوش آمدید
              </h2>
              <p className="mt-2 max-w-sm text-sm text-main-text-light dark:text-main-text-dark">
                برای ورود به دنیای عمیق و زیبای برنامه نویسی و مهدنسی نرم لافز ار به ما ملحق شوید
              </p>
          
              <form className="my-8" onSubmit={handleSubmit}>
                {/* phone */}
                <LabelInputContainer className="mb-4">
                  <Label htmlFor="phone">شماره تلفن</Label>
                  <Input id="phone" placeholder="0912123456789" type="phone" />
                </LabelInputContainer>

                {/* password */}
                <LabelInputContainer className="mb-4">
                  <Label htmlFor="password">رمز</Label>
                  <Input id="password" placeholder="••••••••" type="password" />
                </LabelInputContainer>
        
                <button
                  className="group/btn relative block h-10 w-full rounded-md bg-gradient-to-br from-base-dark to-primary-light font-medium text-highlight-text-light shadow-[0px_1px_0px_0px_#ffffff40_inset,0px_-1px_0px_0px_#ffffff40_inset] dark:bg-base-light dark:from-base-light dark:to-primary-dark dark:text-main-text-light dark:shadow-[0px_1px_0px_0px_#27272a_inset,0px_-1px_0px_0px_#27272a_inset]"
                  type="submit"
                >
                  ورود
                <BottomGradient />
                </button>
              
                <div className="my-8 h-[1px] w-full bg-gradient-to-r from-transparent via-neutral-300 to-transparent dark:via-primary-dark" />
          
                <div className="flex flex-col space-y-4">
                  <button
                      className="group/btn shadow-input relative flex h-10 w-full items-center justify-start space-x-2 rounded-md bg-gray-50 px-4 font-medium text-black dark:bg-zinc-900 dark:shadow-[0px_0px_1px_1px_#262626]"
                      type="submit"
                  >
                      <IconBrandGithub className="h-4 w-4 text-neutral-800 dark:text-neutral-300" />
                      <span className="text-sm text-neutral-700 dark:text-neutral-300">GitHub</span>
                      <BottomGradient />
                  </button>
                  <button
                      className="group/btn shadow-input relative flex h-10 w-full items-center justify-start space-x-2 rounded-md bg-gray-50 px-4 font-medium text-black dark:bg-zinc-900 dark:shadow-[0px_0px_1px_1px_#262626]"
                      type="submit"
                  >
                      <IconBrandGoogle className="h-4 w-4 text-neutral-800 dark:text-neutral-300" />
                      <span className="text-sm text-neutral-700 dark:text-neutral-300">Google</span>
                      <BottomGradient />
                  </button>
                  <button
                      className="group/btn shadow-input relative flex h-10 w-full items-center justify-start space-x-2 rounded-md bg-gray-50 px-4 font-medium text-black dark:bg-zinc-900 dark:shadow-[0px_0px_1px_1px_#262626]"
                      type="submit"
                  >
                      <IconBrandOnlyfans className="h-4 w-4 text-neutral-800 dark:text-neutral-300" />
                      <span className="text-sm text-neutral-700 dark:text-neutral-300">OnlyFans</span>
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