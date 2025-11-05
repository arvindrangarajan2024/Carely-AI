// API configuration and utilities

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  date_of_birth: string; // ISO date string (YYYY-MM-DD)
  phone_number?: string;
  address?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  blood_type?: string;
  allergies?: string;
  medical_conditions?: string;
  medications?: string;
  insurance_provider?: string;
  insurance_policy_number?: string;
  preferred_language?: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface PatientResponse {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  phone_number?: string;
  address?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ApiError {
  detail: string;
}

export interface ChatMessageRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatMessageResponse {
  response: string;
  message_id?: string;
  conversation_id: string;
}

// Get stored access token
export const getAccessToken = (): string | null => {
  return localStorage.getItem('access_token');
};

// Set access token
export const setAccessToken = (token: string): void => {
  localStorage.setItem('access_token', token);
};

// Remove access token
export const removeAccessToken = (): void => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('isLoggedIn');
};

// Helper function for API requests
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getAccessToken();
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error: ApiError = await response.json().catch(() => ({
      detail: 'An error occurred',
    }));
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }

  return response.json();
}

// Authentication API calls
export const authApi = {
  // Login endpoint - uses form data format
  async login(credentials: LoginRequest): Promise<TokenResponse> {
    // OAuth2PasswordRequestForm expects form data with username and password
    const formData = new URLSearchParams();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData.toString(),
    });

    if (!response.ok) {
      const error: ApiError = await response.json().catch(() => ({
        detail: 'Incorrect email or password',
      }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    const data: TokenResponse = await response.json();
    setAccessToken(data.access_token);
    localStorage.setItem('isLoggedIn', 'true');
    return data;
  },

  // Register endpoint
  async register(userData: SignupRequest): Promise<PatientResponse> {
    return apiRequest<PatientResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },

  // Get current user info
  async getCurrentUser(): Promise<PatientResponse> {
    return apiRequest<PatientResponse>('/auth/me');
  },

  // Logout
  logout(): void {
    removeAccessToken();
  },
};

// Chat API calls
export const chatApi = {
  // Send chat message
  async sendMessage(message: string, conversationId?: string): Promise<ChatMessageResponse> {
    const requestBody: ChatMessageRequest = { message };
    if (conversationId) {
      requestBody.conversation_id = conversationId;
    }
    
    const response = await apiRequest<ChatMessageResponse>('/chat/', {
      method: 'POST',
      body: JSON.stringify(requestBody),
    });
    return response;
  },
};

