// __tests__/setup.js
import '@testing-library/jest-dom';

// Simple mock for lucide icons
jest.mock('lucide-react', () => ({
  Mail: () => <span data-testid="mail-icon" />,
  ArrowLeft: () => <span data-testid="arrow-left-icon" />,
  CheckCircle: () => <span data-testid="check-circle-icon" />,
  Code: () => <span data-testid="code-icon" />,
  Lock: () => <span data-testid="lock-icon" />,
  Eye: () => <span data-testid="eye-icon" />,
  EyeOff: () => <span data-testid="eye-off-icon" />,
  User: () => <span data-testid="user-icon" />,
  UserPlus: () => <span data-testid="user-plus-icon" />,
  Check: () => <span data-testid="check-icon" />,
  X: () => <span data-testid="x-icon" />,
}));

// Mock UI components with simpler implementations
jest.mock('../src/components/ui/Button', () => ({ 
  children, onClick, loading, disabled, variant, className, type 
}) => (
  <button 
    onClick={onClick} 
    disabled={disabled || loading}
    data-testid="button"
    data-variant={variant}
    className={className}
    type={type}
  >
    {loading ? 'Loading...' : children}
  </button>
));

jest.mock('../src/components/ui/Input', () => ({ 
  label, name, type, icon, value, onChange, error, placeholder, required, disabled, autoComplete, autoFocus 
}) => (
  <div>
    {label && <label>{label}</label>}
    <input
      name={name}
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      required={required}
      disabled={disabled}
      autoComplete={autoComplete}
      autoFocus={autoFocus}
      data-testid={name ? `input-${name}` : 'input'}
    />
    {error && <span data-testid={name ? `error-${name}` : 'error'}>{error}</span>}
  </div>
));

jest.mock('../src/components/ui/Card', () => ({ children, className }) => (
  <div className={className} data-testid="card">{children}</div>
));

// Mock auth service
jest.mock('../src/services/auth.service', () => ({
  authService: {
    forgotPassword: jest.fn().mockResolvedValue({}),
    login: jest.fn(),
    register: jest.fn(),
    logout: jest.fn(),
    getCurrentUser: jest.fn(),
    getStoredToken: jest.fn(),
    isValidToken: jest.fn(),
    clearLocalSession: jest.fn(),
  }
}));

// Mock Toast components
jest.mock('../src/components/ui/Toast', () => ({
  useToast: () => ({
    success: jest.fn(),
    error: jest.fn(),
    info: jest.fn(),
    warning: jest.fn(),
  }),
  useErrorToast: () => jest.fn(),
}));

// Mock ErrorBoundary
jest.mock('../src/components/ErrorBoundary', () => ({
  useErrorHandler: () => jest.fn(),
}));

// Mock AuthContext with a simple implementation
jest.mock('../src/context/AuthContext', () => ({
  useAuth: () => ({
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
  }),
  AuthProvider: ({ children }) => <>{children}</>,
  AUTH_STATES: {
    LOADING: 'loading',
    AUTHENTICATED: 'authenticated',
    UNAUTHENTICATED: 'unauthenticated',
    ERROR: 'error'
  }
}));