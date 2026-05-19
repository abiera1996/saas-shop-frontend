import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  allowedDevOrigins: [
    "shopname.oursaas.com:3000",
    "oursaas.com:3000",
    "localhost:3000"
  ]
};

export default nextConfig;
