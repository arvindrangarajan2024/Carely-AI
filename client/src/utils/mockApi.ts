// Mock API responses for chatbot

const mockResponses = [
  "That's a great question! Let me help you with that.",
  "I understand what you're asking. Here's what I think...",
  "Interesting! Based on what you've told me, I'd suggest...",
  "Thanks for sharing that with me. Here's my perspective...",
  "I'm here to help! Let me break that down for you.",
];

export const mockChatResponse = async (message: string): Promise<string> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1500 + Math.random() * 1000));
  
  const randomResponse = mockResponses[Math.floor(Math.random() * mockResponses.length)];
  return `${randomResponse} You said: "${message}"`;
};

export const mockVoiceToText = async (audioBlob: Blob): Promise<string> => {
  // Simulate voice-to-text processing
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  const mockTranscriptions = [
    "Hello, how are you today?",
    "Can you help me with something?",
    "What's the weather like?",
    "Tell me more about this feature.",
    "I need assistance with my account.",
  ];
  
  return mockTranscriptions[Math.floor(Math.random() * mockTranscriptions.length)];
};
