"use client"
import { useState, FormEvent } from "react"
import { signIn } from "next-auth/react"
import { useRouter, useSearchParams } from "next/navigation"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/Input"
import { cn } from "@/lib/utils"



export default function LoginForm() {
  const [phone, setPhone] = useState("")
  const [password, setPassword] = useState("")
  const [errorMsg, setErrorMsg] = useState("")
  const [loading, setLoading] = useState(false)

  const router = useRouter()
  const params = useSearchParams()
  const callbackUrl = params.get("callbackUrl") || "/"

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setErrorMsg("")
    setLoading(true)

    const res = await signIn("credentials", {
      redirect: false,
      phone,
      password,
      callbackUrl,
    })

    setLoading(false)
    if (res?.error) return setErrorMsg(res.error)
    router.push(res?.url || callbackUrl)
  }

  return (
    <form className="my-8" onSubmit={handleSubmit}>
      {errorMsg && (
        <p className="mb-4 text-sm text-red-600">{errorMsg}</p>
      )}

      <LabelInputContainer className="mb-4">
        <Label htmlFor="phone">شماره تلفن</Label>
        <Input
          id="phone"
          type="tel"
          placeholder="0912123456789"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          required
        />
      </LabelInputContainer>

      <LabelInputContainer className="mb-4">
        <Label htmlFor="password">رمز</Label>
        <Input
          id="password"
          type="password"
          placeholder="••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </LabelInputContainer>

      <button
        type="submit"
        disabled={loading}
        className="group/btn relative block h-10 w-full rounded-md bg-gradient-to-br from-base-dark to-primary-light font-medium text-highlight-text-light shadow-[0px_1px_0px_0px_#ffffff40_inset,0px_-1px_0px_0px_#ffffff40_inset] dark:bg-base-light dark:from-base-light dark:to-primary-dark dark:text-main-text-light dark:shadow-[0px_1px_0px_0px_#27272a_inset,0px_-1px_0px_0px_#27272a_inset]"
      >
        {loading ? "ورود…" : "ورود"}
        <BottomGradient />
      </button>

      <div className="my-8 h-[1px] w-full bg-gradient-to-r from-transparent via-neutral-300 to-transparent dark:via-primary-dark" />

      <div className="flex flex-row gap-10">
        <button
            className="group/btn shadow-input relative flex h-10 w-full justify-center items-center space-x-2 rounded-md bg-secondary-light px-4 font-medium text-main-text-light dark:bg-secondary-dark dark:shadow-[0px_0px_1px_1px_#262626]"
            type="submit"
        >
            <span className="text-sm font-bold text-center text-main-text-light">ثبت نام</span>
            <BottomGradient />
        </button>
        <button
            className="group/btn shadow-input relative flex h-10 w-full justify-center items-center space-x-2 rounded-md bg-secondary-light px-4 font-medium text-main-text-light dark:bg-secondary-dark dark:shadow-[0px_0px_1px_1px_#262626]"
            type="submit"
        >
            <span className="text-sm font-bold text-center text-main-text-light">بازیابی رمزعبور</span>
            <BottomGradient />
        </button>
      </div>
    </form>
  )
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
