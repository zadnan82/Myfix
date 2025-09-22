import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import RegisterPage from '../../../src/pages/auth/RegisterPage';

// Mock props
const mockOnSwitchToLogin = jest.fn();
const mockOnRegisterSuccess = jest.fn();

describe('RegisterPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders the registration form', () => {
    render(
      <RegisterPage 
        onSwitchToLogin={mockOnSwitchToLogin}
        onRegisterSuccess={mockOnRegisterSuccess}
      />
    );
    
    // Use more specific queries to avoid multiple elements issue
    expect(screen.getByRole('heading', { name: 'Create Account' })).toBeInTheDocument();
    expect(screen.getByPlaceholderText('First name')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Last name')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter your email address')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Create a strong password')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Confirm your password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Create Account' })).toBeInTheDocument();
  });

  test('allows typing form fields', () => {
    render(
      <RegisterPage 
        onSwitchToLogin={mockOnSwitchToLogin}
        onRegisterSuccess={mockOnRegisterSuccess}
      />
    );
    
    const firstNameInput = screen.getByPlaceholderText('First name');
    const lastNameInput = screen.getByPlaceholderText('Last name');
    const emailInput = screen.getByPlaceholderText('Enter your email address');
    const passwordInput = screen.getByPlaceholderText('Create a strong password');
    
    fireEvent.change(firstNameInput, { target: { value: 'John' } });
    fireEvent.change(lastNameInput, { target: { value: 'Doe' } });
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'Password123!' } });
    
    expect(firstNameInput.value).toBe('John');
    expect(lastNameInput.value).toBe('Doe');
    expect(emailInput.value).toBe('test@example.com');
    expect(passwordInput.value).toBe('Password123!');
  });

  test('calls onSwitchToLogin when sign in is clicked', () => {
    render(
      <RegisterPage 
        onSwitchToLogin={mockOnSwitchToLogin}
        onRegisterSuccess={mockOnRegisterSuccess}
      />
    );
    
    const signInLink = screen.getByText('Sign in');
    fireEvent.click(signInLink);
    
    expect(mockOnSwitchToLogin).toHaveBeenCalled();
  });
});