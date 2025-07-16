"use client";

import React, { FormEvent } from "react";
import { LabelInputContainer } from "./LabelInputContainer";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/label";
import { BottomGradient } from "./BottomGradient";



export function RegisterFieldsForm({
  phone, setPhone,
  email, setEmail,
  username, setUsername,
  fullName, setFullName,
  password, setPassword,
  passwordConf, setPasswordConf,
  loading,
  onSubmit,
}: {
  phone: string; setPhone: (s:string)=>void;
  email: string; setEmail: (s:string)=>void;
  username: string; setUsername: (s:string)=>void;
  fullName: string; setFullName: (s:string)=>void;
  password: string; setPassword: (s:string)=>void;
  passwordConf: string; setPasswordConf: (s:string)=>void;
  loading: boolean;
  onSubmit: (e: FormEvent) => void;
}) {
  return (
    <form onSubmit={onSubmit} className="space-y-4 w-full">
      <LabelInputContainer>
        <Label htmlFor="phone">شماره تلفن</Label>
        <Input id="phone" type="tel" required
          value={phone} onChange={e=>setPhone(e.target.value)} />
      </LabelInputContainer>

      <LabelInputContainer>
        <Label htmlFor="email">ایمیل</Label>
        <Input id="email" type="email" required
          value={email} onChange={e=>setEmail(e.target.value)} />
      </LabelInputContainer>

      <LabelInputContainer>
        <Label htmlFor="username">نام کاربری</Label>
        <Input id="username" type="text" required
          value={username} onChange={e=>setUsername(e.target.value)} />
      </LabelInputContainer>

      <LabelInputContainer>
        <Label htmlFor="fullName">نام کامل</Label>
        <Input id="fullName" type="text" required
          value={fullName} onChange={e=>setFullName(e.target.value)} />
      </LabelInputContainer>

      <LabelInputContainer>
        <Label htmlFor="password">رمز عبور</Label>
        <Input id="password" type="password" required
          value={password} onChange={e=>setPassword(e.target.value)} />
      </LabelInputContainer>

      <LabelInputContainer>
        <Label htmlFor="passwordConf">تکرار رمز عبور</Label>
        <Input id="passwordConf" type="password" required
          value={passwordConf} onChange={e=>setPasswordConf(e.target.value)} />
      </LabelInputContainer>

      <button
        type="submit"
        disabled={loading}
        className="group/btn relative block w-full py-2 bg-blue-600 text-white rounded disabled:opacity-50"
      >
        {loading ? "در حال ارسال…" : "دریافت کد OTP"}
        <BottomGradient />
      </button>
    </form>
  );
}
