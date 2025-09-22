// __tests__/test-utils.jsx
import React from 'react';
import { render } from '@testing-library/react';

// Create a simple mock for AuthContext
const mockAuthValue = {
  login: jest.fn(),
  register: jest.fn(),
  isLoading: false,
  clearError: jest.fn(),
  user: null,
  authState: 'unauthenticated',
  error: null,
  isAuthenticated: false,
  isError: false,
  isInitializing: false,
  userName: null,
  userEmail: null,
  userRole: null,
  logout: jest.fn(),
  updateProfile: jest.fn(),
  changePassword: jest.fn(),
  hasRole: jest.fn(),
  isAdmin: jest.fn(),
  getStoredToken: jest.fn(),
  retry: jest.fn(),
};

// Create a simple wrapper that doesn't depend on the actual AuthContext
const TestWrapper = ({ children }) => {
  return <>{children}</>;
};

const customRender = (ui, options = {}) => {
  return render(ui, { wrapper: TestWrapper, ...options });
};

// Re-export everything
export * from '@testing-library/react';

// Override the render method
export { customRender as render };