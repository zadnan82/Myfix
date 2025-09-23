// user_frontend/src/config/api.config.js

// Environment-based API configuration
const getApiBaseUrl = () => {
  // Check for explicit environment variable first - this should always take precedence
  if (import.meta.env.VITE_API_URL) {
    console.log('[CONFIG] Using explicit VITE_API_URL:', import.meta.env.VITE_API_URL);
    return import.meta.env.VITE_API_URL;
  }
  
  // Fallback based on build mode (only when no explicit API URL is set)
  // if (import.meta.env.PROD) {
  //   // In production with split architecture, use API subdomain
  //   if (typeof window !== 'undefined') {
  //     const hostname = window.location.hostname;
  //     const dynamicUrl = `https://api.${hostname}`;
  //     console.log('[CONFIG] Using dynamic API URL:', dynamicUrl);
  //     return dynamicUrl;
  //   }
  //   // Fallback for SSR or build time
  //   console.log('[CONFIG] Using fallback API URL: https://api.sevdo.se');
  //   return 'https://api.sevdo.se';
  // }
  
  console.log('[CONFIG] Using development API URL');
  return 'http://localhost:8000'; // Development default
};

const API_BASE_URL = getApiBaseUrl();

// Detect if we're in production environment
// Production is determined by build mode or non-localhost URLs
const isProduction = import.meta.env.PROD || (!API_BASE_URL.includes('localhost') && !API_BASE_URL.includes('127.0.0.1'));

// Debug logging
console.log(`[CONFIG] API_BASE_URL: ${API_BASE_URL}`);
console.log(`[CONFIG] isProduction: ${isProduction}`);
console.log(`[CONFIG] Build mode: ${import.meta.env.PROD ? 'production' : 'development'}`);
console.log(`[CONFIG] Window location: ${typeof window !== 'undefined' ? window.location.origin : 'server-side'}`);
console.log(`[CONFIG] VITE_API_URL env: ${import.meta.env.VITE_API_URL || 'not set'}`);

// Helper to create endpoint paths
// If VITE_API_URL already has /api, we shouldn't add it again
// In production environments where VITE_API_URL includes /api, remove the /api prefix from path
const createEndpoint = (path) => {
  // Check if VITE_API_URL ends with /api
  const apiUrlEndsWithApi = import.meta.env.VITE_API_URL && 
    import.meta.env.VITE_API_URL.endsWith('/api');
  
  if (apiUrlEndsWithApi && path.startsWith('/api/')) {
    console.log(`[CONFIG] API URL already has /api: ${path} -> ${path.substring(4)}`);
    return path.substring(4); // Remove '/api' prefix, leaving '/v1/...'
  }
  return path;
};

export const CONFIG = {
  // API Configuration
  API: {
    BASE_URL: API_BASE_URL,
    TIMEOUT: 30000,
    RETRY_ATTEMPTS: 3,
  },
  
  // ALL API ENDPOINTS - Complete with new backend endpoints
  ENDPOINTS: {
    // Auth endpoints
    LOGIN: createEndpoint('/api/v1/auth/token'),
    REGISTER: createEndpoint('/api/v1/auth/register'), 
    LOGOUT: createEndpoint('/api/v1/auth/logout'),
    LOGOUT_ALL: createEndpoint('/api/v1/auth/logout/all'), 
    ME: createEndpoint('/api/v1/auth/me'),
    UPDATE_PROFILE: createEndpoint('/api/v1/auth/me'),
    CHANGE_PASSWORD: createEndpoint('/api/v1/auth/change-password'),
    SESSIONS: createEndpoint('/api/v1/auth/sessions'),
    REVOKE_SESSION: createEndpoint('/api/v1/auth/sessions'),
    
    // User Preferences
    GET_PREFERENCES: createEndpoint('/api/v1/auth/profile/preferences'),
    UPDATE_PREFERENCES: createEndpoint('/api/v1/auth/profile/preferences'),
    USER_USAGE_STATS: createEndpoint('/api/v1/auth/profile/usage'),
    
    // Projects endpoints
    PROJECTS: createEndpoint('/api/v1/projects'),
    PROJECT_GENERATE: createEndpoint('/api/v1/projects/{id}/generate'),
    PROJECT_STATUS: createEndpoint('/api/v1/projects/{id}/status'),
    PROJECT_GENERATIONS: createEndpoint('/api/v1/projects/{id}/generations'),
    PROJECT_FILES: createEndpoint('/api/v1/projects/{id}/files'),
    
    // SEVDO endpoints (NEW)
    SEVDO_GENERATE_BACKEND: createEndpoint('/api/v1/sevdo/generate/backend'),
    SEVDO_GENERATE_FRONTEND: createEndpoint('/api/v1/sevdo/generate/frontend'),
    SEVDO_GENERATE_PROJECT: createEndpoint('/api/v1/sevdo/generate/project'),
    
    // Analytics endpoints
    DASHBOARD_ANALYTICS: createEndpoint('/api/v1/analytics/dashboard'),
    PROJECT_ANALYTICS: createEndpoint('/api/v1/analytics/projects'),
    USAGE_ANALYTICS: createEndpoint('/api/v1/analytics/usage'),
    PERFORMANCE_METRICS: createEndpoint('/api/v1/analytics/performance'),
    USER_ACTIVITY: createEndpoint('/api/v1/analytics/activity'),
    
    // File Management endpoints
    UPLOAD_FILE: createEndpoint('/api/v1/files/upload'),
    DOWNLOAD_FILE: createEndpoint('/api/v1/files/{id}'),
    DELETE_FILE: createEndpoint('/api/v1/files/{id}'),
    LIST_PROJECT_FILES: createEndpoint('/api/v1/files/project/{id}'),
    
    // System endpoints
    SYSTEM_HEALTH: createEndpoint('/api/v1/system/health'),
    SYSTEM_STATUS: createEndpoint('/api/v1/system/status'),
    SYSTEM_METRICS: createEndpoint('/api/v1/system/metrics'),
    REPORT_ERROR: createEndpoint('/api/v1/system/errors/report'),
    SUBMIT_FEEDBACK: createEndpoint('/api/v1/system/feedback'),
    
    // Notifications endpoints
    NOTIFICATIONS: createEndpoint('/api/v1/notifications'),
    MARK_NOTIFICATION_READ: createEndpoint('/api/v1/notifications/{id}/read'),
    MARK_ALL_READ: createEndpoint('/api/v1/notifications/mark-all-read'),
    DELETE_NOTIFICATION: createEndpoint('/api/v1/notifications/{id}'),
    UNREAD_COUNT: createEndpoint('/api/v1/notifications/unread-count'),
    
    // Tokens endpoints
    TOKENS: createEndpoint('/api/v1/tokens'),
    SEARCH_TOKENS: createEndpoint('/api/v1/tokens/search'),
    VALIDATE_TOKENS: createEndpoint('/api/v1/tokens/validate'),
    SUGGEST_TOKENS: createEndpoint('/api/v1/tokens/suggest'),
    TOKEN_ANALYTICS: createEndpoint('/api/v1/tokens/analytics'),
    
    // Templates endpoints
    TEMPLATES: createEndpoint('/api/v1/templates'),
    POPULAR_TEMPLATES: createEndpoint('/api/v1/templates/popular'),
    USE_TEMPLATE: createEndpoint('/api/v1/templates/{id}/use'),
    
    // AI endpoints
    AI_PROJECT_FROM_DESCRIPTION: createEndpoint('/api/v1/ai/project-from-description'),
    AI_CHAT: createEndpoint('/api/v1/ai/chat'),

    // LLM Editor
    LLM_EDITOR_EDIT_FILE: createEndpoint('/api/v1/llm-editor/edit-text-file'),
    LLM_EDITOR_EDIT_FILE_PUBLIC: createEndpoint('/api/v1/llm-editor/edit-text-file/public'),

    
    // WebSocket endpoints
    WS_NOTIFICATIONS: createEndpoint('/api/v1/ws/notifications'),
    WS_PROJECT_GENERATION: createEndpoint('/api/v1/ws/projects/{id}/generation'),
    
    // Future endpoints
    REFRESH: createEndpoint('/api/v1/auth/refresh'),
    FORGOT_PASSWORD: createEndpoint('/api/v1/auth/forgot-password'),
    RESET_PASSWORD: createEndpoint('/api/v1/auth/reset-password'),
  },
  
  // Request Headers
  HEADERS: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  
  // App Settings
  APP: {
    NAME: import.meta.env.VITE_APP_NAME || 'Sevdo',
    VERSION: '2.0.0',
  },
  
  // Storage Keys
  STORAGE_KEYS: {
    SESSION_TOKEN: 'auth_token',
    USER_DATA: 'user_data',
    USER_PREFERENCES: 'user_preferences',
  },
  
  // Feature Flags
  FEATURES: {
    REGISTRATION: true,
    PASSWORD_RESET: true,
    REMEMBER_ME: true,
    ANALYTICS: true,
    FILE_MANAGEMENT: true,
    NOTIFICATIONS: true,
    WEBSOCKETS: true,
    AI_FEATURES: true,
    SEVDO_INTEGRATION: true, // NEW
  },
  
  // Error Messages
  ERRORS: {
    NETWORK_ERROR: 'Network error. Please check your connection.',
    UNAUTHORIZED: 'Session expired. Please login again.',
    FORBIDDEN: 'You do not have permission to perform this action.',
    NOT_FOUND: 'The requested resource was not found.',
    CONFLICT: 'A conflict occurred. Please try again.',
    SERVER_ERROR: 'Server error. Please try again later.',
    TIMEOUT: 'Request timed out. Please try again.',
    VALIDATION_ERROR: 'Please check your input and try again.',
    GENERATION_ERROR: 'Code generation failed. Please try again.'
  }
};

// Helper functions
export const getApiUrl = (endpoint) => {
  // Make sure we don't have double slashes between base URL and endpoint
  let baseUrl = CONFIG.API.BASE_URL;
  let modifiedEndpoint = endpoint;
  
  // If base URL ends with a slash and endpoint starts with one, remove one
  if (baseUrl.endsWith('/') && modifiedEndpoint.startsWith('/')) {
    modifiedEndpoint = modifiedEndpoint.substring(1);
  }
  
  const fullUrl = `${baseUrl}${modifiedEndpoint}`;
  
  // Log URLs in production to help with debugging
  if (isProduction || import.meta.env.VITE_DEBUG_API === 'true') {
    console.log(`[CONFIG] Final URL: ${fullUrl}`);
  }
  
  return fullUrl;
};
export const getEndpoint = (key) => CONFIG.ENDPOINTS[key] || '';

// Helper to replace URL parameters
export const buildEndpoint = (endpointKey, params = {}) => {
  let endpoint = getEndpoint(endpointKey);
  
  // Replace URL parameters like {id} with actual values
  Object.keys(params).forEach(key => {
    endpoint = endpoint.replace(`{${key}}`, params[key]);
  });
  
  return endpoint;
};

export default CONFIG;
