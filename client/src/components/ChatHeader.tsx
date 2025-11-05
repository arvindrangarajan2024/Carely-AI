import { MessageCircle } from "lucide-react";

export const ChatHeader = () => {
  return (
    <div className="border-b border-border bg-card px-6 py-4 shadow-sm">
      <div className="max-w-4xl mx-auto flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-md">
          <MessageCircle className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="text-lg font-semibold text-foreground">Friendly Assistant</h1>
          <p className="text-xs text-muted-foreground">Always here to help</p>
        </div>
      </div>
    </div>
  );
};
