import { Label } from "@/components/ui/label";
export default function Field({ label, children }: { label: string; children: React.ReactNode }) {
    return (
      <div className="space-y-1">
        <Label className="text-sm text-slate-600">{label}</Label>
        {children}
      </div>
    );
  }