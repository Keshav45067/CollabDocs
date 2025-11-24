import React, { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogFooter, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Input } from "@/components/ui/input";
import { Avatar } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";
import { cn } from "@/lib/utils";

/**
 * Simplified CollaboratorPermissions
 * - Only two access levels: "view" and "write"
 * - No per‑section configuration
 * - Admin can change permissions for all collaborators
 */

type Access = "view" | "write";

type Collaborator = {
  id: string;
  name: string;
  email?: string;
  avatarUrl?: string;
  access: Access;
};

export default function CollaboratorPermissionsDialog({
  open,
  onOpenChange,
  collaborators,
  isAdmin,
  onSave,
}: {
  open: any;
  onOpenChange: any;
  collaborators: any;
  isAdmin: boolean;
  onSave: any;
}
) {
  const [local, setLocal] = useState<Collaborator[]>([]);
  const [saving, setSaving] = useState(false);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    setLocal(JSON.parse(JSON.stringify(collaborators || [])));
  }, [collaborators, open]);

  function setAccess(id: string, access: Access) {
    setLocal(prev => prev.map(c => c.id === id ? { ...c, access } : c));
  }

  function reset() {
    setLocal(JSON.parse(JSON.stringify(collaborators || [])));
  }

  async function handleSave() {
    setSaving(true);
    try {
      await onSave(local);
      onOpenChange(false);
    } finally {
      setSaving(false);
    }
  }

  const filtered = local.filter(c => c.name.toLowerCase().includes(filter.toLowerCase()) || c.email?.toLowerCase().includes(filter.toLowerCase()));

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-xl">
        <DialogHeader>
          <DialogTitle>Manage collaborator access</DialogTitle>
          <DialogDescription>Assign write or view-only access to collaborators.</DialogDescription>
        </DialogHeader>

        <div className="mt-4 flex items-center gap-4">
          <Input placeholder="Search collaborators..." value={filter} onChange={(e) => setFilter(e.target.value)} />
          <div className="text-sm text-muted-foreground">{filtered.length} results</div>
        </div>

        <Separator className="my-4" />

        <ScrollArea className="h-[48vh] border rounded">
          <div className="p-3 space-y-3">
            {filtered.map((c) => (
              <div key={c.id} className="flex items-center justify-between p-2 rounded hover:bg-slate-50">
                <div className="flex items-center gap-3 min-w-0">
                  <Avatar className="h-8 w-8">
                    <div className="w-8 h-8 rounded-full flex items-center justify-center bg-slate-100 text-xs font-medium text-slate-800">
                      {c.name.charAt(0)}
                    </div>
                  </Avatar>
                  <div className="min-w-0">
                    <div className="text-sm font-medium truncate">{c.name}</div>
                    <div className="text-xs text-slate-500 truncate">{c.email || "—"}</div>
                  </div>
                </div>

                <select
                  value={c.access}
                  onChange={(e) => setAccess(c.id, e.target.value as Access)}
                  disabled={!isAdmin}
                  className="text-sm border rounded px-2 py-1"
                >
                  <option value="view">View</option>
                  <option value="write">Write</option>
                </select>
              </div>
            ))}
          </div>
        </ScrollArea>

        <DialogFooter className="mt-4 flex justify-end gap-2">
          <Button variant="ghost" onClick={() => { reset(); onOpenChange(false); }}>Cancel</Button>
          <Button onClick={handleSave} disabled={!isAdmin || saving}>{saving ? "Saving…" : "Save changes"}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
