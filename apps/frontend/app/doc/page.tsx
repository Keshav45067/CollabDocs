// app/docs/[id]/page.tsx
"use client";

import React, { useEffect, useRef, useState } from "react";
import CollaboratorPermissionsDialog from './CollaboratorPermissionsDialog'
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

/**
 * Frontend-only Document Editor Page (no backend)
 *
 * - Professional minimal toolbar (formatting buttons act on contentEditable via execCommand for demo)
 * - Title editing (local state)
 * - Large contentEditable area with placeholder
 * - Presence / collaborators panel with animated avatars and typing indicator (simulated)
 * - Autosave indicator (simulated) and "Saved X ago" using timeAgo
 * - Decorative preview image using uploaded asset path (local path will be transformed by your toolchain)
 *
 * NOTE: This file intentionally contains NO backend calls. All "live" behaviors are simulated
 * to demonstrate the exact UX and feel of the editor.
 */

function timeAgo(iso?: string) {
  if (!iso) return "just now";
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

// small icon helpers (inline SVG)
const IconBold = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden>
    <path d="M7 6h6a3 3 0 0 1 0 6H7z" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M7 12h6a3 3 0 0 1 0 6H7z" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);
const IconItalic = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden>
    <path d="M10 4h8M6 20h8M15 4L9 20" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);
const IconUnderline = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden>
    <path d="M6 3v6a6 6 0 0 0 12 0V3" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
    <path d="M5 21h14" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

export default function DocEditorUI() {
  const [title, setTitle] = useState("Untitled document");
  const [content, setContent] = useState(
    "Start writing — your changes are captured locally. This demo shows the editor UI only."
  );
  const [lastSavedAt, setLastSavedAt] = useState<string | undefined>(new Date().toISOString());
  const [isSaving, setIsSaving] = useState(false);
  const [collaborators, setCollaborators] = useState([
    { id: "u1", name: "Aisha" },
    { id: "u2", name: "Ravi" },
    { id: "u3", name: "Maria" },
  ]);
  const [typingUser, setTypingUser] = useState<string | null>(null);
  const [sections, setSections] = useState<
    { id: string; title: string; content: string; order: number }[]
  >([
    { id: "s1", title: "Introduction", content: "Intro...", order: 0 },
    { id: "s2", title: "Body", content: "Main...", order: 1 },
  ]);
  const [open, setOpen] = useState(false);

  const [activeSectionId, setActiveSectionId] = useState<string | null>(sections[0]?.id ?? null);

  // UI state for section management
  const [isSectionModalOpen, setIsSectionModalOpen] = useState(false); // create/edit section
  const [sectionToDelete, setSectionToDelete] = useState<{ id: string; title: string } | null>(null);

  // collaborator permissions
  const [collaboratorsWithPermissions, setCollaboratorsWithPermissions] =
    useState<
      { id: string; name: string; globalRole: "viewer" | "editor" | "admin"; sectionRoles: Record<string, "none" | "view" | "edit"> }[]
    >([
      { id: "u1", name: "Aisha", globalRole: "editor", sectionRoles: {} },
      // ...
    ]);

  const [isCollabDialogOpen, setIsCollabDialogOpen] = useState(false);

  const editorRef = useRef<HTMLDivElement | null>(null);
  const autosaveTimer = useRef<number | null>(null);

  // simulate collaborator typing every now and then
  useEffect(() => {
    const t = setInterval(() => {
      const rnd = Math.random();
      if (rnd < 0.35) {
        const who = collaborators[Math.floor(Math.random() * collaborators.length)].name;
        setTypingUser(who);
        setTimeout(() => setTypingUser(null), 2000 + Math.floor(Math.random() * 2500));
      }
    }, 5000);
    return () => clearInterval(t);
  }, [collaborators]);

  // autosave simulation: debounce 1000ms after local edits
  function scheduleAutosave() {
    if (autosaveTimer.current) window.clearTimeout(autosaveTimer.current);
    autosaveTimer.current = window.setTimeout(() => {
      setIsSaving(true);
      // simulate save delay
      setTimeout(() => {
        setLastSavedAt(new Date().toISOString());
        setIsSaving(false);
      }, 700);
    }, 1000);
  }

  // update content state on input
  function handleInput() {
    if (!editorRef.current) return;
    const txt = editorRef.current.innerText;
    setContent(txt);
    scheduleAutosave();
  }

  // formatting buttons (uses simple document.execCommand for demo only)
  function applyFormat(command: "bold" | "italic" | "underline") {
    document.execCommand(command);
    // after formatting, reflect content state and schedule autosave
    if (editorRef.current) {
      setContent(editorRef.current.innerText);
      scheduleAutosave();
    }
  }

  // accessible avatar rendering
  function avatarFor(name: string) {
    const initial = name.charAt(0).toUpperCase();
    const palette = ["bg-rose-200", "bg-amber-200", "bg-lime-200", "bg-sky-200", "bg-violet-200"];
    let h = 0;
    for (let i = 0; i < name.length; i++) h = (h << 5) - h + name.charCodeAt(i);
    const color = palette[Math.abs(h) % palette.length];
    return (
      <div key={name} className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium text-slate-800 ${color}`}>
        {initial}
      </div>
    );
  }

  // small helper to show save label
  function saveLabel() {
    if (isSaving) return "Saving…";
    return lastSavedAt ? `Saved ${timeAgo(lastSavedAt)}` : "Not saved";
  }
  useEffect(()=>{
    if(editorRef && editorRef.current) editorRef.current.innerText = content;
  
  },[editorRef])

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col">
      {/* header */}
      <header className="bg-white border-b">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between gap-6">
          <div className="flex items-center gap-6">
            <div className="text-lg font-semibold">CollabDocs</div>

            <div className="flex flex-col">
              <Input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-[520px] text-xl font-semibold border-0 bg-transparent focus:ring-0 px-0"
                aria-label="Document title"
              />
              <div className="text-xs text-slate-500 -mt-1">Private to you — hit Save to persist (demo)</div>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="flex -space-x-2">{collaborators.map((c) => avatarFor(c.name))}</div>
              <div className="text-xs text-slate-600">
                {typingUser ? `${typingUser} is typing…` : `${collaborators.length} collaborators`}
              </div>
            </div>

            <div className="text-xs text-slate-500">{saveLabel()}</div>

            <Button onClick={() => { setIsSaving(true); setTimeout(() => { setIsSaving(false); setLastSavedAt(new Date().toISOString()); }, 600); }}>
              Save
            </Button>
          </div>
        </div>
      </header>

      {/* toolbar */}
      <div className="max-w-6xl mx-auto px-6 py-3">
        <div className="bg-white rounded-md border px-3 py-2 flex items-center gap-2 shadow-sm">
          <div className="flex items-center gap-1">
            <button
              aria-label="Bold"
              title="Bold"
              onClick={() => applyFormat("bold")}
              className="p-2 rounded hover:bg-slate-100 active:bg-slate-200"
            >
              <IconBold />
            </button>
            <button
              aria-label="Italic"
              title="Italic"
              onClick={() => applyFormat("italic")}
              className="p-2 rounded hover:bg-slate-100 active:bg-slate-200"
            >
              <IconItalic />
            </button>
            <button
              aria-label="Underline"
              title="Underline"
              onClick={() => applyFormat("underline")}
              className="p-2 rounded hover:bg-slate-100 active:bg-slate-200"
            >
              <IconUnderline />
            </button>
          </div>

          <div className="border-l h-6 mx-2" />

          <div className="text-xs text-slate-500">Formatting</div>

          <div className="flex-1" />

          <div className="text-xs text-slate-400">Shortcut keys available</div>
        </div>
      </div>

      {/* editor */}
      <main className="max-w-6xl mx-auto px-6 py-6 flex gap-6">
        <article className="flex-1">
          <div className="rounded-lg border bg-white shadow-sm min-h-[60vh] p-6">
            <div
              ref={editorRef}
              contentEditable
              suppressContentEditableWarning
              onInput={handleInput}
              className="prose prose-lg w-[50vw] min-w-[500px] min-h-[48vh] outline-none caret-slate-900"
              style={{ whiteSpace: "pre-wrap" }}
            >
            </div>
          </div>

          {/* footer controls */}
          <div className="flex items-center justify-between mt-3">
            <div className="text-xs text-slate-500">Last change: {timeAgo(lastSavedAt)}</div>
            {/* <div className="text-xs text-slate-400">Local edits only — no backend</div> */}
          </div>
        </article>

        {/* right rail */}
        <aside className="w-64 flex-shrink-0">
          <div className="space-y-4">

            <div className="bg-white rounded-lg border p-4 shadow-sm">
              <div className="flex justify-between w-full mb-2">
              <div className="text-sm font-medium ">Collaborators</div>
              <Button className="text-white font-semibold" onClick={()=>setOpen(true)}>Manage</Button>
              </div>
              <div className="space-y-2">
                {collaborators.map((c) => (
                  <div key={c.id} className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium text-slate-800 bg-slate-100">
                      {c.name.charAt(0).toUpperCase()}
                    </div>
                    <div>
                      <div className="text-sm">{c.name}</div>
                      <div className="text-xs text-slate-400">Active</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </aside>
      </main>

      <style jsx>{`
        /* subtle entrance animation */
        @keyframes fadeUp { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0);} }
        .prose { animation: fadeUp 360ms ease both; }
      `}</style>
    <CollaboratorPermissionsDialog
     open={open}
     onOpenChange={setOpen}
     collaborators={collaborators}
     isAdmin={true}
     onSave={()=>{}}
    />
    </div>
  );
}
