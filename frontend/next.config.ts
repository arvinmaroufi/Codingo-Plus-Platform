import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactStrictMode: true,
  env: {
    DJANGO_API_URL: process.env.DJANGO_API_URL,
  },
};

export default nextConfig;
