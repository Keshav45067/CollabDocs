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

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
      <div className="w-full max-w-md">
        <nav className="flex items-center justify-between mb-2">
          <div className="text-xl font-bold">CollabDocs — Auth</div>
          <div className="flex gap-2">
          </div>
        </nav>
         <OtpCard/>
      </div>
    </div>
  );
}


function OtpCard() {
  const [step, setStep] = useState<'otp'|'done'>('otp');
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [sentOtp, setSentOtp] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isTimerActive, setIsTimerActive] = useState(true);
  const [timer, setTimer] = useState(60);



  const verifyOtpAndRegister = async () => {
    setError(null);
    if (!otp) return setError('Enter OTP');
    setLoading(true);
    try {
      // simulate verification & registration
      await new Promise((r) => setTimeout(r, 700));
      // simple mock: accept any 4-digit otp
      if (otp.length < 3) throw new Error('Invalid OTP');
      setStep('done');
      alert('Registered (mock)');
    } catch (err: any) {
      setError(err?.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    let countdown: any = null;
    if (isTimerActive && timer > 0) {
      countdown = setInterval(() => {
        setTimer((prev) => prev - 1);
      }, 1000);
    } else if (timer === 0) {
      setIsTimerActive(false);
    }
    return () => clearInterval(countdown);
  }, [isTimerActive, timer]);

  if (step === 'done') {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Registered</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-slate-700">Your account has been registered (mock). You can now sign in.</p>
        </CardContent>
      </Card>
    );
  }
  const router = useRouter();

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-2xl">Create account</CardTitle>
      </CardHeader>
      <CardContent>
        {step === 'otp' && (
          <div className="space-y-4">
            <p className="text-sm text-slate-700">We sent an OTP to <strong>Laud***@lelo.com</strong>. Enter it below to finish registration.</p>
            <Field label="OTP">
              <Input value={otp} onChange={(e) => setOtp(e.target.value)} placeholder="123456" />
            </Field>

            {error && <div className="text-sm text-red-600">{error}</div>}
            <p className="text-sm font-bold cursor-pointer">{isTimerActive?`Resend in ${timer}`:'Resend OTP' }</p>
            <div className="flex items-center justify-between">
              <Button variant="ghost" onClick={() => { router.push("/auth?register=t") }}>Edit details</Button>
              <div className="flex gap-2">
                <Button onClick={verifyOtpAndRegister} disabled={loading}>{loading ? 'Verifying...' : 'Verify & create'}</Button>
              </div>
            </div>

          </div>
        )}
      </CardContent>
    </Card>
  );
}
