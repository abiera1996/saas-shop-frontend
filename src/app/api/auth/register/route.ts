import { NextRequest, NextResponse } from "next/server";
import { logger } from "@/lib/logger";

const DJANGO_API_URL = "http://localhost:8000/api";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    
    const start = Date.now();
    const res = await fetch(`${DJANGO_API_URL}/auth/register/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const duration = Date.now() - start;
    logger.info(`[SSR REGISTER] POST /api/auth/register -> Django Status: ${res.status} (${duration}ms)`);

    const data = await res.json();

    if (!res.ok) {
      return NextResponse.json(data, { status: res.status });
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ detail: "Internal Server Error" }, { status: 500 });
  }
}
