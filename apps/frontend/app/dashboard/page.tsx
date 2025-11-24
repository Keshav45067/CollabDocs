// app/dashboard/page.tsx
"use client";

import React, { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogTrigger,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

/**
 * Updated Dashboard page:
 * - Removed Created column
 * - Shows "last edited" as relative time (e.g., "5 minutes ago", "3 hours ago")
 * - Table rows are selectable: click a row -> it becomes selected and displays a black border
 *
 * Decorative image uses local uploaded file path (will be transformed to a served URL by your toolchain):
 * "/mnt/data/Screenshot 2025-11-23 at 2.21.11 PM.png"
 */

type Doc = {
  id: string;
  name: string;
  createdAt: string; // ISO
  lastEditedAt: string; // ISO
};

function timeAgo(iso?: string) {
  if (!iso) return "—";
  const then = new Date(iso).getTime();
  const now = Date.now();
  const s = Math.floor((now - then) / 1000);
  if (s < 5) return "just now";
  if (s < 60) return `${s} ${s === 1 ? "second" : "seconds"} ago`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m} ${m === 1 ? "minute" : "minutes"} ago`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h} ${h === 1 ? "hour" : "hours"} ago`;
  const d = Math.floor(h / 24);
  if (d < 30) return `${d} ${d === 1 ? "day" : "days"} ago`;
  const mo = Math.floor(d / 30);
  if (mo < 12) return `${mo} ${mo === 1 ? "month" : "months"} ago`;
  const y = Math.floor(mo / 12);
  return `${y} ${y === 1 ? "year" : "years"} ago`;
}

export default function DashboardPage() {
  const [docs, setDocs] = useState<Doc[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [newName, setNewName] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    async function load() {
      setLoading(true);
      try {
        const res = await fetch("/api/docs");
        if (!res.ok) throw new Error("no-api");
        const json = await res.json();
        if (!mounted) return;
        setDocs(json);
      } catch (err) {
        if (!mounted) return;
        // fallback mock data for local dev / POC
        setDocs([
          {
            id: "doc-1",
            name: "Project Plan",
            createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 5).toISOString(),
            lastEditedAt: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
          },
          {
            id: "doc-2",
            name: "Research Notes",
            createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 20).toISOString(),
            lastEditedAt: new Date(Date.now() - 1000 * 60 * 60 * 25).toISOString(),
          },
          {
            id: "doc-3",
            name: "Meeting Minutes",
            createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 60).toISOString(),
            lastEditedAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 30).toISOString(),
          },
        ]);
      } finally {
        if (mounted) setLoading(false);
      }
    }
    load();
    return () => {
      mounted = false;
    };
  }, []);

  async function createDoc(e?: React.FormEvent) {
    e?.preventDefault();
    setError(null);
    if (!newName.trim()) {
      setError("Name is required");
      return;
    }
    setCreating(true);
    try {
      const payload = { name: newName.trim() };
      const res = await fetch("/api/docs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (res.ok) {
        const created: Doc = await res.json();
        setDocs((prev) => (prev ? [created, ...prev] : [created]));
        setNewName("");
        setDialogOpen(false);
      } else {
        // fallback local creation
        const local: Doc = {
          id: "local-" + Date.now(),
          name: newName.trim(),
          createdAt: new Date().toISOString(),
          lastEditedAt: new Date().toISOString(),
        };
        setDocs((prev) => (prev ? [local, ...prev] : [local]));
        setNewName("");
        setDialogOpen(false);
      }
    } catch (err: any) {
      setError(err?.message || "Failed to create");
    } finally {
      setCreating(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <header className="max-w-6xl mx-auto mb-8 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h1 className="text-2xl font-semibold text-slate-900">CollabDocs</h1>
          <p className="text-sm text-slate-600">Hello Keshav, let's collaborate ✨</p>
        </div>

        <div className="flex items-center gap-4">
          <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
            <DialogTrigger asChild>
              <Button>New document</Button>
            </DialogTrigger>

            <DialogContent className="sm:max-w-[420px]">
              <DialogHeader>
                <DialogTitle>Create document</DialogTitle>
              </DialogHeader>

              <form onSubmit={createDoc} className="space-y-4">
                <div>
                  <Label className="text-sm">Document name</Label>
                  <Input
                    value={newName}
                    onChange={(e) => setNewName(e.target.value)}
                    placeholder="Untitled document"
                    className="mt-2"
                    required
                  />
                </div>

                {error && <div className="text-sm text-red-600">{error}</div>}

                <div className="flex justify-end pt-2">
                  <Button type="submit" disabled={creating}>
                    {creating ? "Creating..." : "Create"}
                  </Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        </div>
      </header>

      <main className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Left: list */}
          <Card className="col-span-2">
            <CardHeader>
              <CardTitle>Documents</CardTitle>
            </CardHeader>

            <CardContent>
              {loading ? (
                <div className="py-8 text-center text-slate-500">Loading documents…</div>
              ) : docs && docs.length > 0 ? (
                <div className="space-y-2">
                  {docs.map((d) => {
                    const selected = selectedId === d.id;
                    return (
                      <div
                        key={d.id}
                        role="button"
                        tabIndex={0}
                        onClick={() => setSelectedId(d.id)}
                        onKeyDown={(e) => {
                          if (e.key === "Enter" || e.key === " ") setSelectedId(d.id);
                        }}
                        className={`flex items-center justify-between gap-4 p-4 rounded-lg cursor-pointer transition-shadow border ${
                          selected ? "border-black bg-white shadow" : "border-transparent hover:shadow-sm hover:bg-white"
                        }`}
                        aria-pressed={selected}
                      >
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-md bg-slate-100 flex items-center justify-center text-slate-700 font-medium">
                            {d.name.charAt(0).toUpperCase()}
                          </div>

                          <div>
                            <div className="font-medium text-slate-900">{d.name}</div>
                            <div className="text-xs text-slate-500">
                              {/* optional small subtitle */}
                              {d.id}
                            </div>
                          </div>
                        </div>

                        <div className="text-sm text-slate-500">{timeAgo(d.lastEditedAt)}</div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div className="py-8 text-center text-slate-500">
                  No documents yet. Create one to get started.
                </div>
              )}
            </CardContent>
          </Card>

          {/* Right: small profile / decorative */}
          <div className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Account</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-full bg-slate-200 flex items-center justify-center text-slate-700 font-medium">
                    K
                  </div>
                  <div>
                    <div className="font-medium">Keshav</div>
                    <div className="text-sm text-slate-500">keshav@example.com</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Preview</CardTitle>
              </CardHeader>
              <CardContent>
                <img
                  src={"/mnt/data/Screenshot 2025-11-23 at 2.21.11 PM.png"}
                  alt="Decorative preview"
                  className="w-full rounded-md border"
                />
                <Button className="mt-3 font-semibold text-m text-white">Edit</Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}
