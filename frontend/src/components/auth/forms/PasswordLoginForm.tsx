"use client";
import React, { FormEvent } from "react";
import { BottomGradient } from "./BottomGradient";
import { LabelInputContainer } from "./LabelInputContainer";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/Input";



export function PasswordLoginForm({
  password,
  setPassword,
  loading,
  onSubmit,
}: {
  password: string;
  setPassword: (val: string) => void;
  loading: boolean;
  onSubmit: (e: FormEvent) => void;
}) {
  return (
    <form onSubmit={onSubmit} className="space-y-4 w-full">
      <LabelInputContainer>
        <Label htmlFor="password">رمز عبور</Label>
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
        className="block w-full py-2 bg-gradient-to-br from-base-dark to-primary-light text-white rounded disabled:opacity-50 group/btn"
      >
        {loading ? "در حال ورود…" : "ورود"}
        <BottomGradient />
      </button>
    </form>
  );
}
