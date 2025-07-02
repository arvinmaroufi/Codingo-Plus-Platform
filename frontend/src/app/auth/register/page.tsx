import HeroSection from "@/components/HeroSection";
import RegisterForm from "@/components/auth/forms/RegisterForm";
import { CiLogin } from "react-icons/ci";


export default function RegisterPage() {
  return (
    <main className="px-5 sm:px-10 py-10 flex flex-col gap-8 items-center">
      <HeroSection
        title="ثبت نام"
        mainText="در کدینگو پلاس ثبت‌نام کنید"
        subText="و به بهترین محتوای آموزشی دسترسی پیدا کنید"
        buttonTitle="ورود"
        buttonUrl="/auth/login"
        buttonPosition={"right"}
        buttonIcon={<CiLogin />}
        />
      <div className="shadow-input mx-auto max-w-md rounded-none bg-highlight-text-dark p-4 md:rounded-2xl md:p-8 dark:bg-main-text-light">
        <h2 className="text-xl font-bold text-main-text-light dark:text-main-text-dark">
          به کدنیگو پلاس بپیوندید
        </h2>
        <p className="mt-2 mb-3 max-w-sm text-sm text-main-text-light dark:text-main-text-dark">
          برای ورود به دنیای عمیق و زیبای برنامه نویسی و مهندسی نرم‌افزار
          به ما ملحق شوید
        </p>

        <RegisterForm />
      </div>
    </main>
  );
}
