import { Message, Thread, User } from "@/types";
import { ENV } from "./env";

export const API_BASE_URL = ENV.IS_DEVELOPMENT ? "http://localhost:8000/api/v1" : "/api/v1";
// export const API_BASE_URL = "http://localhost:8000/api/v1"

export async function fetchThreads(): Promise<Thread[]> {
  const response = await fetch(`${API_BASE_URL}/threads`, {
    method: "GET",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    throw new Error("Failed to fetch threads");
  }
  const data = await response.json();

  if (!Array.isArray(data)) {
    console.error("Invalid threads format:", data);
    return [];
  }

  return data.map((thread: Thread) => ({
    ...thread,
    title: thread.title || "새로운 대화",
  }));
}

export async function createThread(): Promise<Thread> {
  const response = await fetch(`${API_BASE_URL}/threads/create`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    throw new Error("Failed to create thread");
  }
  return response.json();
}

export async function fetchMessages(threadId: number): Promise<Message[]> {
  const response = await fetch(`${API_BASE_URL}/threads/${threadId}/messages`, {
    method: "GET",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    throw new Error("Failed to fetch messages");
  }
  const data = await response.json();

  if (!Array.isArray(data)) {
    console.error("Invalid messages format:", data);
    return [];
  }

  return data.map((msg: any) => ({
    id: msg.id ? msg.id.toString() : Date.now().toString(), // ID가 없으면 임시 ID 생성
    role: msg.role,
    content: msg.content,
    created_at: msg.created_at,
  }));
}

export async function fetchUserInfo(): Promise<User | null> {
  const response = await fetch(`${API_BASE_URL}/user/info`, {
    method: "GET",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    throw new Error("Failed to fetch user info");
  }
  const data = await response.json();
  if (data.status_code === 200) {
    return data.data;
  }
  return null;
}

/**
 * Sends a message to the chat API and returns a stream reader.
 */
export async function sendMessage(
  message: string,
  sessionId: number
): Promise<ReadableStreamDefaultReader<Uint8Array>> {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    },
    body: JSON.stringify({
      message,
      session_id: sessionId,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to send message");
  }

  if (!response.body) {
    throw new Error("No response body");
  }

  return response.body.getReader();
}

export async function sendMessageNonStreaming(
  message: string,
  sessionId: number
): Promise<string> {
  const response = await fetch(`${API_BASE_URL}/chat/non-streaming`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      session_id: sessionId,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to send message");
  }

  const data = await response.json();
  // The backend returns a string directly or an object with a response field depending on implementation.
  // Based on previous backend code: return response_text (which is a string)
  // Wait, let me double check the backend implementation in chat.py
  // It returns response_text directly.
  return data;
}
