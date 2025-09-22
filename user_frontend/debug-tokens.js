// Production Token Debug Script
// Run this in the browser console to debug token issues

console.log('=== TOKEN DEBUG INFORMATION ===');

// Check localStorage directly
const directToken = localStorage.getItem('auth_token');
console.log('Direct localStorage token:', directToken ? directToken.substring(0, 20) + '...' : 'null');

// Check all localStorage keys
console.log('All localStorage keys:', Object.keys(localStorage));

// Check sessionStorage
console.log('SessionStorage keys:', Object.keys(sessionStorage));

// Check if storage service is available
if (typeof storage !== 'undefined') {
  const storageToken = storage.get('auth_token');
  console.log('Storage service token:', storageToken ? storageToken.substring(0, 20) + '...' : 'null');
  console.log('Token match:', directToken === storageToken);
} else {
  console.log('Storage service not available in console');
}

// Check current page info
console.log('Current URL:', window.location.href);
console.log('Protocol:', window.location.protocol);
console.log('Host:', window.location.host);

// Check if WebSocket service is available
if (typeof websocketService !== 'undefined') {
  console.log('WebSocket service available');
  console.log('Should connect:', websocketService.shouldConnect());
  console.log('Is production:', websocketService.isProduction);
} else {
  console.log('WebSocket service not available in console');
}

// Environment info
console.log('Build mode (PROD):', import.meta?.env?.PROD || 'unknown');
console.log('API URL env:', import.meta?.env?.VITE_API_URL || 'unknown');

console.log('=== END TOKEN DEBUG ===');
