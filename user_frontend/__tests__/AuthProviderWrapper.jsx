import React from 'react';
import { AuthProvider } from '../src/context/AuthContext';

// Create a simple test wrapper that provides AuthContext
const TestAuthProvider = ({ children }) => {
  const mockAuthValue = {
    login: jest.fn(),
    register: jest.fn(),
    isLoading: false,
    clearError: jest.fn(),
  };

  return (
    <AuthProvider value={mockAuthValue}>
      {children}
    </AuthProvider>
  );
};

export default TestAuthProvider;