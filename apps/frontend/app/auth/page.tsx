"use client"
import React, { useEffect, useState } from "react";
import Field from "../utils/field";
import { useRouter, useSearchParams } from "next/navigation";

// Minimal Next.js-style preview with two pages (Login and Register)
// Uses shadcn/ui primitives (Card, Input, Button). You'll need to have
// the shadcn/ui components available at the paths used below, and TailwindCSS enabled.

// Example component imports used by shadcn installations. Adjust paths if your project differs.
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

// Minimalistic form field component


export default function PreviewApp() {
  const [route, setRoute] = useState<'login' | 'register'>('login');
  const isRegister = useSearchParams().get("register");
  useEffect(()=>{
    if(isRegister) setRoute("register");
  },[])

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
      <div className="w-full max-w-md">
        <nav className="flex items-center justify-between mb-2">
          <div className="text-xl font-bold">CollabDocs — Auth</div>
          <div className="flex gap-2">
            <button
              className={`px-3 py-1 rounded-md text-sm ${route === 'login' ? 'bg-slate-900 text-white' : 'text-slate-600'}`}
              onClick={() => setRoute('login')}
            >
              Login
            </button>
            <button
              className={`px-3 py-1 rounded-md text-sm ${route === 'register' ? 'bg-slate-900 text-white' : 'text-slate-600'}`}
              onClick={() => setRoute('register')}
            >
              Register
            </button>
          </div>
        </nav>

        {route === 'login' ? <LoginCard /> : <RegisterCard />}
      </div>
    </div>
  );
}

function LoginCard() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      // Replace with real API call
      await new Promise((r) => setTimeout(r, 600));
      // mock validation
      if (!email || !password) throw new Error('Please provide email and password');
      // success — in a real app you'd store the JWT, redirect, etc.
      alert('Logged in (mock)');
    } catch (err: any) {
      setError(err?.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-2xl">Sign in</CardTitle>
      </CardHeader>
      <CardContent>
        <form className="space-y-4" onSubmit={onSubmit}>
          <Field label="Email">
            <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
          </Field>

          <Field label="Password">
            <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" />
          </Field>

          {error && <div className="text-sm text-red-600">{error}</div>}

          <div className="flex items-center justify-end">
            <Button type="submit" disabled={loading}>{loading ? 'Signing in...' : 'Sign in'}</Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}

function RegisterCard() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [sentOtp, setSentOtp] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const sendOtp = async () => {
    setError(null);
    if (!email) return setError('Enter a valid email');
    setLoading(true);
    try {
      // simulate API call to send OTP
      await new Promise((r) => setTimeout(r, 700));
      setSentOtp(true);
      router.push("/otp")
    } catch (err: any) {
      setError('Unable to send OTP');
    } finally {
      setLoading(false);
    }
  };


  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-2xl">Create account</CardTitle>
      </CardHeader>
      <CardContent>
          <form className="space-y-4" onSubmit={(e) => { e.preventDefault(); sendOtp(); }}>
            <Field label="Full name">
              <Input value={name} onChange={(e) => setName(e.target.value)} placeholder="Your name" />
            </Field>

            <Field label="Email">
              <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />
            </Field>

            <Field label="Password">
              <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Choose a secure password" />
            </Field>

            {error && <div className="text-sm text-red-600">{error}</div>}

            <div className="flex items-center justify-end">
              <Button type="submit" disabled={loading}>{loading ? 'Sending...' : 'Send OTP'}</Button>
            </div>
          </form>

        
      </CardContent>
    </Card>
  );
}
