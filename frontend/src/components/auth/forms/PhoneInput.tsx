"use client";
import React from "react";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/Input";


export function PhoneInput({
  phone,
  setPhone,
}: {
  phone: string;
  setPhone: (val: string) => void;
}) {
  return (
    <div className="space-y-1 mb-6 w-full">
      <Label htmlFor="phone">شماره تلفن</Label>
      <Input
        id="phone"
        type="tel"
        placeholder="09121234567"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
        required
      />
    </div>
  );
}
