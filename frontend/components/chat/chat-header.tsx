"use client";

import { Menu } from "lucide-react";

interface ChatHeaderProps {
  tokenUsage: number;
  isSidebarOpen: boolean;
  onToggleSidebar: () => void;
}

export function ChatHeader({
  tokenUsage,
  isSidebarOpen,
  onToggleSidebar,
}: ChatHeaderProps) {
  return (
    <div className="h-14 border-b border-border flex items-center justify-between px-6 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <button
        onClick={onToggleSidebar}
        className="p-2 hover:bg-muted rounded-lg transition-colors text-muted-foreground hover:text-foreground cursor-pointer"
      >
        <Menu className="h-5 w-5" />
      </button>

      <div className="text-sm text-muted-foreground ml-auto">
        토큰: <span className="font-semibold text-blue-600">{tokenUsage}</span>
      </div>
    </div>
  );
}
