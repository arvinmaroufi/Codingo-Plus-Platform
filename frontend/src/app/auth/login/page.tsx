import type { Metadata } from "next"
import HeroSection from "@/components/HeroSection"
import LoginForm from "@/components/auth/forms/LoginForm"

export const metadata: Metadata = {
  title: "ورود | Codingo Plus",
}

export default function LoginPage() {
  return (
    <main className="flex justify-between items-center gap-6 flex-col mx-auto sm:px-10 px-5">
      <HeroSection
        title="مجموعه ی کدینگو"
        mainText="آموزش توسعه و مهندسی نرم افزار"
        subText="به مجموعه ی کدینگو خوش آمدید"
        buttonTitle="مشاهده دوره ها"
        buttonPosition="right"
        buttonUrl="/courses"
      />

      <div className="shadow-input mx-auto max-w-md rounded-none bg-highlight-text-dark p-4 md:rounded-2xl md:p-8 dark:bg-main-text-light">
        <h2 className="text-xl font-bold text-main-text-light dark:text-main-text-dark">
          به کدنیگو پلاس خوش آمدید
        </h2>
        <p className="mt-2 max-w-sm text-sm text-main-text-light dark:text-main-text-dark">
          برای ورود به دنیای عمیق و زیبای برنامه نویسی و مهندسی نرم‌افزار
          به ما ملحق شوید
        </p>

        <LoginForm />
      </div>
    </main>
  )
}
