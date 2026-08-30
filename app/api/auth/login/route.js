import { NextResponse } from "next/server";

const apiUrl = process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function POST(request) {
  try {
    const upstream = await fetch(`${apiUrl}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(await request.json()),
    });
    const body = await upstream.text();
    let data = {};
    try { data = body ? JSON.parse(body) : {}; } catch { data = { detail: body }; }
    if (!upstream.ok) return NextResponse.json(data, { status: upstream.status });
    if (!data.access_token) return NextResponse.json({ detail: "The API did not return a login token." }, { status: 502 });

    const response = NextResponse.json({ message: "Logged in." });
    response.cookies.set("stockflow_token", data.access_token, {
      httpOnly: true, sameSite: "lax", secure: process.env.NODE_ENV === "production", maxAge: 60 * 60, path: "/",
    });
    return response;
  } catch {
    return NextResponse.json({ detail: "Could not reach the FastAPI server at port 8000." }, { status: 503 });
  }
}
