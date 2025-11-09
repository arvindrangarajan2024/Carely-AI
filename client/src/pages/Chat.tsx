import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { ChatHeader } from "@/components/ChatHeader";
import { ChatMessage } from "@/components/ChatMessage";
import { ChatInput } from "@/components/ChatInput";
import { chatApi } from "@/utils/api";

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  isLoading?: boolean;
  appointmentData?: {
    action?: string;
    appointment_id?: number;
    success?: boolean;
    error?: string;
    slots?: Array<{
      datetime: string;
      formatted: string;
      available: boolean;
    }>;
    appointment_details?: {
      appointment_type: string;
      doctor_name: string;
      scheduled_time: string;
      reason: string;
      is_virtual: boolean;
      duration_minutes: number;
    };
  };
}

const Chat = () => {
  const navigate = useNavigate();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      text: "Hello! I'm your medical assistant. How can I help you today?",
      isUser: false,
    },
  ]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Check authentication on mount
  useEffect(() => {
    const isLoggedIn = localStorage.getItem("isLoggedIn");
    if (isLoggedIn !== "true") {
      navigate("/");
    }
  }, [navigate]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (text: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      text,
      isUser: true,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsProcessing(true);

    // Add loading message
    const loadingMessage: Message = {
      id: `${Date.now()}-loading`,
      text: "",
      isUser: false,
      isLoading: true,
    };
    setMessages((prev) => [...prev, loadingMessage]);

    try {
      const response = await chatApi.sendMessage(text, conversationId || undefined);
      
      // Store conversation ID if we got one back
      if (response.conversation_id) {
        setConversationId(response.conversation_id);
      }
      
      // Remove loading message and add actual response
      setMessages((prev) => {
        const filtered = prev.filter((msg) => !msg.isLoading);
        return [
          ...filtered,
          {
            id: Date.now().toString(),
            text: response.response,
            isUser: false,
            appointmentData: response.appointment_data,
          },
        ];
      });
    } catch (error) {
      console.error("Error getting response:", error);
      setMessages((prev) => {
        const filtered = prev.filter((msg) => !msg.isLoading);
        return [
          ...filtered,
          {
            id: Date.now().toString(),
            text: error instanceof Error ? error.message : "Sorry, I encountered an error. Please try again.",
            isUser: false,
          },
        ];
      });
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-background">
      <ChatHeader />
      
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-4xl mx-auto">
          {messages.map((message) => (
            <ChatMessage
              key={message.id}
              message={message.text}
              isUser={message.isUser}
              isLoading={message.isLoading}
              appointmentData={message.appointmentData}
            />
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>
      
      <ChatInput onSendMessage={handleSendMessage} disabled={isProcessing} />
    </div>
  );
};

export default Chat;
