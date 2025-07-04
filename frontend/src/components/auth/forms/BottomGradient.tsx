"use client";
import React from "react";

export function BottomGradient() {
  return (
    <>
      <span className="absolute inset-x-0 -bottom-px h-px bg-gradient-to-r from-transparent via-primary-dark to-transparent opacity-0 group-hover/btn:opacity-100" />
      <span className="absolute inset-x-10 -bottom-px h-px w-1/2 bg-gradient-to-r from-transparent via-base-dark to-transparent opacity-0 blur-sm group-hover/btn:opacity-100" />
    </>
  );
}
