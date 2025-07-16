import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactStrictMode: true,
  env: {
    DJANGO_API_URL: process.env.DJANGO_API_URL,
    MEDIA_URL: process.env.MEDIA_URL,
  },
  images: {
    domains: ['127.0.0.1', 'localhost'],
  }
};

export default nextConfig;
