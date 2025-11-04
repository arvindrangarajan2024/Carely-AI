import { useState, FormEvent } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Mic, Send, Square } from "lucide-react";
import { useVoiceRecording } from "@/hooks/useVoiceRecording";
import { mockVoiceToText } from "@/utils/mockApi";
import { useToast } from "@/hooks/use-toast";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

export const ChatInput = ({ onSendMessage, disabled }: ChatInputProps) => {
  const [input, setInput] = useState("");
  const { toast } = useToast();
  const {
    isRecording,
    audioBlob,
    startRecording,
    stopRecording,
    resetRecording,
  } = useVoiceRecording();

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSendMessage(input.trim());
      setInput("");
    }
  };

  const handleVoiceRecord = async () => {
    if (isRecording) {
      stopRecording();
    } else {
      await startRecording();
    }
  };

  const handleAudioProcessed = async () => {
    if (audioBlob) {
      try {
        toast({
          title: "Processing voice...",
          description: "Converting your voice to text",
        });
        const text = await mockVoiceToText(audioBlob);
        setInput(text);
        resetRecording();
        toast({
          title: "Voice recognized!",
          description: "You can now edit or send the message",
        });
      } catch (error) {
        toast({
          title: "Error",
          description: "Failed to process voice recording",
          variant: "destructive",
        });
      }
    }
  };

  if (audioBlob) {
    handleAudioProcessed();
  }

  return (
    <form onSubmit={handleSubmit} className="border-t border-border bg-card p-4">
      <div className="flex gap-2 items-end max-w-4xl mx-auto">
        <Button
          type="button"
          size="icon"
          variant={isRecording ? "destructive" : "outline"}
          onClick={handleVoiceRecord}
          disabled={disabled}
          className="flex-shrink-0 h-10 w-10"
        >
          {isRecording ? (
            <Square className="h-4 w-4" />
          ) : (
            <Mic className="h-4 w-4" />
          )}
        </Button>
        
        <Textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={disabled || isRecording}
          className="min-h-[40px] max-h-[120px] resize-none"
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e);
            }
          }}
        />
        
        <Button
          type="submit"
          size="icon"
          disabled={!input.trim() || disabled}
          className="flex-shrink-0 h-10 w-10"
        >
          <Send className="h-4 w-4" />
        </Button>
      </div>
    </form>
  );
};
