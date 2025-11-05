import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { MessageSquare, Shield, Clock, Heart } from "lucide-react";

const Landing = () => {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    const isLoggedIn = localStorage.getItem("isLoggedIn");
    if (isLoggedIn === "true") {
      navigate("/chat");
    } else {
      navigate("/auth");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-primary/5 to-secondary/10">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <header className="text-center mb-16 animate-fade-in">
          <div className="flex items-center justify-center mb-4">
            <Heart className="w-12 h-12 text-primary mr-3" />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
              Carely AI
            </h1>
          </div>
          <p className="text-xl text-muted-foreground mt-4">
            Your trusted medical assistant, available 24/7
          </p>
        </header>

        {/* Hero Section */}
        <section className="text-center mb-20 animate-fade-in" style={{ animationDelay: "0.1s" }}>
          <h2 className="text-4xl font-bold mb-6 text-foreground">
            Ask Your Medical Questions From Us
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
            Get reliable medical information and guidance instantly. Our AI-powered chatbot
            is here to help you understand your health concerns better. Available anytime,
            anywhere.
          </p>
          <Button 
            onClick={handleGetStarted}
            size="lg"
            className="text-lg px-8 py-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
          >
            Start Chatting Now
          </Button>
        </section>

        {/* Features */}
        <section className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div className="bg-card p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow animate-fade-in" style={{ animationDelay: "0.2s" }}>
            <MessageSquare className="w-12 h-12 text-primary mb-4" />
            <h3 className="text-xl font-semibold mb-3">Instant Responses</h3>
            <p className="text-muted-foreground">
              Get immediate answers to your medical questions with our advanced AI technology.
            </p>
          </div>
          
          <div className="bg-card p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow animate-fade-in" style={{ animationDelay: "0.3s" }}>
            <Shield className="w-12 h-12 text-primary mb-4" />
            <h3 className="text-xl font-semibold mb-3">Private & Secure</h3>
            <p className="text-muted-foreground">
              Your health information is kept confidential and secure with our encrypted platform.
            </p>
          </div>
          
          <div className="bg-card p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow animate-fade-in" style={{ animationDelay: "0.4s" }}>
            <Clock className="w-12 h-12 text-primary mb-4" />
            <h3 className="text-xl font-semibold mb-3">24/7 Availability</h3>
            <p className="text-muted-foreground">
              Access medical guidance whenever you need it, day or night, from anywhere.
            </p>
          </div>
        </section>

        {/* Disclaimer */}
        <section className="mt-16 text-center max-w-3xl mx-auto">
          <p className="text-sm text-muted-foreground italic">
            <strong>Medical Disclaimer:</strong> This chatbot provides general health information
            and should not replace professional medical advice, diagnosis, or treatment. Always
            consult with a qualified healthcare provider for medical concerns.
          </p>
        </section>
      </div>
    </div>
  );
};

export default Landing;
