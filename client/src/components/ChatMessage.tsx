import { cn } from "@/lib/utils";
import { Bot, User, Calendar, Clock, MapPin, CheckCircle2 } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface AppointmentData {
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
}

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  isLoading?: boolean;
  appointmentData?: AppointmentData;
}

export const ChatMessage = ({ message, isUser, isLoading, appointmentData }: ChatMessageProps) => {
  return (
    <div
      className={cn(
        "flex gap-3 mb-4 animate-fade-in",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center">
          <Bot className="w-5 h-5 text-primary-foreground" />
        </div>
      )}
      
      <div
        className={cn(
          "max-w-[75%] rounded-2xl px-4 py-3 shadow-sm",
          isUser
            ? "bg-secondary text-secondary-foreground rounded-br-md"
            : "bg-card text-card-foreground rounded-bl-md border border-border"
        )}
      >
        {isLoading ? (
          <div className="flex gap-1 items-center py-1">
            <div className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce [animation-delay:-0.3s]"></div>
            <div className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce [animation-delay:-0.15s]"></div>
            <div className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce"></div>
          </div>
        ) : (
          <>
            <p className="text-sm leading-relaxed whitespace-pre-wrap">{message}</p>
            
            {/* Display appointment confirmation */}
            {appointmentData?.success && appointmentData.appointment_id && (
              <Card className="mt-3 border-green-200 bg-green-50">
                <CardHeader className="pb-3">
                  <CardTitle className="text-base flex items-center gap-2 text-green-700">
                    <CheckCircle2 className="w-5 h-5" />
                    Appointment Booked
                  </CardTitle>
                </CardHeader>
                <CardContent className="text-sm space-y-2">
                  <div className="flex items-center gap-2">
                    <Calendar className="w-4 h-4 text-green-600" />
                    <span className="font-medium">Appointment #{appointmentData.appointment_id}</span>
                  </div>
                  {appointmentData.appointment_details && (
                    <>
                      <div className="flex items-center gap-2">
                        <User className="w-4 h-4 text-green-600" />
                        <span>{appointmentData.appointment_details.doctor_name}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Clock className="w-4 h-4 text-green-600" />
                        <span>{appointmentData.appointment_details.duration_minutes} minutes</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <MapPin className="w-4 h-4 text-green-600" />
                        <span>{appointmentData.appointment_details.is_virtual ? 'Virtual' : 'In-Person'}</span>
                      </div>
                      <Badge variant="outline" className="mt-2">
                        {appointmentData.appointment_details.appointment_type}
                      </Badge>
                    </>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Display available time slots */}
            {appointmentData?.action === 'show_slots' && appointmentData.slots && (
              <Card className="mt-3 border-blue-200 bg-blue-50">
                <CardHeader className="pb-3">
                  <CardTitle className="text-base text-blue-700">Available Time Slots</CardTitle>
                </CardHeader>
                <CardContent className="text-sm">
                  <div className="space-y-2">
                    {appointmentData.slots.slice(0, 5).map((slot, index) => (
                      <div
                        key={index}
                        className="p-2 rounded bg-white border border-blue-100 hover:border-blue-300 transition-colors"
                      >
                        <div className="flex items-center gap-2">
                          <Calendar className="w-4 h-4 text-blue-600" />
                          <span>{slot.formatted}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Display error if any */}
            {appointmentData?.error && (
              <Card className="mt-3 border-red-200 bg-red-50">
                <CardContent className="pt-4 text-sm text-red-700">
                  <p>Error: {appointmentData.error}</p>
                </CardContent>
              </Card>
            )}
          </>
        )}
      </div>
      
      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-accent flex items-center justify-center">
          <User className="w-5 h-5 text-accent-foreground" />
        </div>
      )}
    </div>
  );
};
