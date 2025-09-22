import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ForgotPasswordPage from '../../../src/pages/auth/ForgotPasswordPage';
import { authService } from '../../../src/services/auth.service';

// Mock the onSwitchToLogin prop
const mockOnSwitchToLogin = jest.fn();

describe('ForgotPasswordPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    authService.forgotPassword.mockClear();
  });

  test('renders the forgot password form', () => {
    render(<ForgotPasswordPage onSwitchToLogin={mockOnSwitchToLogin} />);
    
    expect(screen.getByText('Reset Password')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('your@email.com')).toBeInTheDocument();
    expect(screen.getByText('Send Reset Instructions')).toBeInTheDocument();
  });

  test('shows error when email is empty', async () => {
    render(<ForgotPasswordPage onSwitchToLogin={mockOnSwitchToLogin} />);
    
    const submitButton = screen.getByText('Send Reset Instructions');
    fireEvent.click(submitButton);
    
    // Use a more specific query to avoid the multiple elements issue
    const errorElements = await screen.findAllByText('Email is required');
    expect(errorElements.length).toBeGreaterThan(0);
  });

  test('shows error when email is invalid', async () => {
    render(<ForgotPasswordPage onSwitchToLogin={mockOnSwitchToLogin} />);
    
    const emailInput = screen.getByPlaceholderText('your@email.com');
    fireEvent.change(emailInput, { target: { value: 'invalid-email' } });
    
    const submitButton = screen.getByText('Send Reset Instructions');
    fireEvent.click(submitButton);
    
    // Use a more specific query
    const errorElements = await screen.findAllByText('Please enter a valid email address');
    expect(errorElements.length).toBeGreaterThan(0);
  });

  test('calls onSwitchToLogin when back button is clicked', () => {
    render(<ForgotPasswordPage onSwitchToLogin={mockOnSwitchToLogin} />);
    
    const backButton = screen.getByText('Back to Sign In');
    fireEvent.click(backButton);
    
    expect(mockOnSwitchToLogin).toHaveBeenCalled();
  });

  test('allows typing email address', () => {
    render(<ForgotPasswordPage onSwitchToLogin={mockOnSwitchToLogin} />);
    
    const emailInput = screen.getByPlaceholderText('your@email.com');
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    
    expect(emailInput.value).toBe('test@example.com');
  });
});