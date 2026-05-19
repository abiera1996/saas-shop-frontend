import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { logger } from "@/lib/logger";

const DJANGO_API_URL = "http://localhost:8000/api";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    
    const start = Date.now();
    const res = await fetch(`${DJANGO_API_URL}/auth/token/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const duration = Date.now() - start;
    logger.info(`[SSR LOGIN] POST /api/auth/login -> Django Status: ${res.status} (${duration}ms)`);

    const data = await res.json();

    if (!res.ok) {
      return NextResponse.json({ detail: data.detail || "Invalid credentials" }, { status: res.status });
    }

    // Set HttpOnly cookies
    const cookieStore = await cookies();
    cookieStore.set("access_token", data.access, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      maxAge: 60 * 60 * 24, // 1 day
      path: "/",
    });
    
    if (data.refresh) {
      cookieStore.set("refresh_token", data.refresh, {
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
        sameSite: "lax",
        maxAge: 60 * 60 * 24 * 7, // 7 days
        path: "/",
      });
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ detail: "Internal Server Error" }, { status: 500 });
  }
}
