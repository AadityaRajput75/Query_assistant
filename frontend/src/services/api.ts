import axios from 'axios';
import { ChatRequest, ChatResponse } from '../types/chat';

const API_BASE_URL = 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatService = {
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>('/chat', request);
    return response.data;
  },

  getSessionMessages: async (sessionId: string) => {
    const response = await api.get(`/sessions/${sessionId}/messages`);
    return response.data;
  },

  getAllSessions: async () => {
    const response = await api.get('/sessions');
    return response.data;
  },

  getSessionInfo: async (sessionId: string) => {
    const response = await api.get(`/sessions/${sessionId}`);
    return response.data;
  },

  deleteSession: async (sessionId: string) => {
    const response = await api.delete(`/sessions/${sessionId}`);
    return response.data;
  },

  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;