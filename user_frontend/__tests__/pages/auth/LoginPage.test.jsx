import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import LoginPage from '../../../src/pages/auth/LoginPage';

// Mock props
const mockOnSwitchToRegister = jest.fn();
const mockOnSwitchToForgot = jest.fn();
const mockOnLoginSuccess = jest.fn();

describe('LoginPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders the login form', () => {
    render(
      <LoginPage 
        onSwitchToRegister={mockOnSwitchToRegister}
        onSwitchToForgot={mockOnSwitchToForgot}
        onLoginSuccess={mockOnLoginSuccess}
      />
    );
    
    expect(screen.getByRole('heading', { name: 'Welcome Back' })).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter your email address')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter your password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Sign In' })).toBeInTheDocument();
  });

  test('allows typing email and password', () => {
    render(
      <LoginPage 
        onSwitchToRegister={mockOnSwitchToRegister}
        onSwitchToForgot={mockOnSwitchToForgot}
        onLoginSuccess={mockOnLoginSuccess}
      />
    );
    
    const emailInput = screen.getByPlaceholderText('Enter your email address');
    const passwordInput = screen.getByPlaceholderText('Enter your password');
    
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    
    expect(emailInput.value).toBe('test@example.com');
    expect(passwordInput.value).toBe('password123');
  });

  test('calls onSwitchToForgot when forgot password is clicked', () => {
    render(
      <LoginPage 
        onSwitchToRegister={mockOnSwitchToRegister}
        onSwitchToForgot={mockOnSwitchToForgot}
        onLoginSuccess={mockOnLoginSuccess}
      />
    );
    
    const forgotPasswordLink = screen.getByText('Forgot your password?');
    fireEvent.click(forgotPasswordLink);
    
    expect(mockOnSwitchToForgot).toHaveBeenCalled();
  });

  test('calls onSwitchToRegister when sign up is clicked', () => {
    render(
      <LoginPage 
        onSwitchToRegister={mockOnSwitchToRegister}
        onSwitchToForgot={mockOnSwitchToForgot}
        onLoginSuccess={mockOnLoginSuccess}
      />
    );
    
    const signUpLink = screen.getByText('Sign up');
    fireEvent.click(signUpLink);
    
    expect(mockOnSwitchToRegister).toHaveBeenCalled();
  });
});