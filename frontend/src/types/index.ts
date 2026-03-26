// User types
export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

// Resume types
export interface School {
  name: string;
  course: string;
  cgpa?: number;
  start_year?: number;
  end_year?: number;
}

export interface Certification {
  title: string;
  issuer?: string;
  year?: number;
}

export interface Project {
  name: string;
  description: string;
  tech_stack: string[];
  start_year?: number;
  end_year?: number;
}

export interface Company {
  name: string;
  designation: string;
  responsibilities: string[];
  start_month?: number;
  start_year?: number;
  end_month?: number;
  end_year?: number;
  duration_string?: string;
}

export interface Resume {
  name: string;
  phone?: string;
  email: string;
  github?: string;
  linkedin?: string;
  education: School[];
  skills: string[];
  projects: Project[];
  experience: Company[];
  certificates: Certification[];
  summary: string;
  career_level: string;
}

// Chat types
export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

// API types
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

export interface LoginResponse {
  msg: string;
  token: string;
}

export interface SignupResponse {
  msg: string;
}

export interface ChatResponse {
  msg: string;
}

export interface UploadResponse {
  message: string;
}
