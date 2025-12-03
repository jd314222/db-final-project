'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface AuthContextType {
  userId: number | null;
  isAuthenticated: boolean;
  login: (id: number) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  userId: null,
  isAuthenticated: false,
  login: () => {},
  logout: () => {},
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [userId, setUserId] = useState<number | null>(null);

  useEffect(() => {
    // Check localStorage for saved user ID
    const savedUserId = localStorage.getItem('userId');
    if (savedUserId) {
      setUserId(Number(savedUserId));
    }
  }, []);

  const login = (id: number) => {
    setUserId(id);
    localStorage.setItem('userId', id.toString());
  };

  const logout = () => {
    setUserId(null);
    localStorage.removeItem('userId');
  };

  return (
    <AuthContext.Provider value={{ 
      userId, 
      isAuthenticated: userId !== null, 
      login, 
      logout 
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
