"use client";
import React from "react";

export function LabelInputContainer({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={`${className ?? ""} flex flex-col space-y-2 w-full`}>
      {children}
    </div>
  );
}
