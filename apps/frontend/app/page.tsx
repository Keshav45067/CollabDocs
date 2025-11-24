// app/page.tsx
"use client"
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-white">
      <div className="w-full max-w-4xl px-6 py-28">
        <div className="mx-auto max-w-3xl text-center">
          {/* Title */}
          <h1 className="text-5xl md:text-6xl font-extrabold text-slate-900 leading-tight mb-4 animate-fade-up">
            Collab<span className="text-red-500">D</span>ocs
          </h1>

          {/* Description */}
          <p className="text-lg text-slate-600 mb-8 animate-fade-up animation-delay-100">
            A fast, minimal, real-time collaborative editor built on CRDT principles and a modern
            distributed backend. Seamless editing, robust persistence, and zero merge drama —
            designed for engineers and teams who want to move fast.
          </p>

          {/* CTA */}
          <div className="flex items-center justify-center gap-4 mb-10 animate-fade-up animation-delay-200">
            <Link href="/auth" passHref>
              <Button asChild>
                <div className="px-6 py-3">Log in</div>
              </Button>
            </Link>

            <Link href="/auth?register=t" passHref>
              <Button variant="outline" asChild>
                <div className="px-6 py-3">Register</div>
              </Button>
            </Link>
          </div>

          {/* Small footer */}
          <p className="text-xs text-slate-400 mb-8">Built with precision. Designed for teams.</p>

          {/* Decorative hero card (right column visual in compact single-column layout) */}
          <div className="mx-auto max-w-xl">
            <div className="bg-white border border-slate-100 rounded-2xl shadow-lg overflow-hidden transform transition-all duration-300 hover:scale-[1.01]">
              {/* Use exact local path below; your CI/tooling should convert it to a served URL */}
              <img
                src={"https://images.unsplash.com/photo-1603796846097-bee99e4a601f?q=80&w=2574&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"}
                alt="CollabDocs preview"
                className="w-full h-56 object-cover"
              />
              <div className="p-4">
                <div className="text-sm font-medium text-slate-800">Realtime collaboration</div>
                <div className="text-xs text-slate-500 mt-1">
                  Low-latency edits · CRDT-backed state · Durable snapshots
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes fadeUp {
          from {
            opacity: 0;
            transform: translateY(8px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fade-up {
          animation: fadeUp 520ms cubic-bezier(0.2, 0.9, 0.2, 1) both;
        }
        .animation-delay-100 {
          animation-delay: 100ms;
        }
        .animation-delay-200 {
          animation-delay: 200ms;
        }
      `}</style>
    </main>
  );
}
