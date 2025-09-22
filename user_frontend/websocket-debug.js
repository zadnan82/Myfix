// WebSocket Debug Script for Production
// Run this in browser console to test WebSocket URL construction

console.log('=== WEBSOCKET DEBUG TEST ===');

// Test URL construction manually
const testApiBase = 'https://80.216.194.14';
const testEndpoint = '/api/v1/ws/notifications';
const testToken = 'test-token-123';

// Convert to WebSocket URL
const wsBase = testApiBase.replace('https://', 'wss://').replace('http://', 'ws://');
const finalUrl = `${wsBase}${testEndpoint}?token=${testToken}`;

console.log('Manual URL construction test:');
console.log('  API Base:', testApiBase);
console.log('  WebSocket Base:', wsBase);
console.log('  Endpoint:', testEndpoint);
console.log('  Final URL:', finalUrl);

// Test actual WebSocket connection (will fail but shows the URL being used)
console.log('\nTesting actual WebSocket connection:');
try {
  const testWs = new WebSocket(finalUrl);
  console.log('WebSocket object created successfully');
  
  testWs.onopen = () => console.log('Test WebSocket opened (unexpected)');
  testWs.onerror = (error) => console.log('Test WebSocket error (expected):', error);
  testWs.onclose = (event) => console.log('Test WebSocket closed:', event.code, event.reason);
  
  // Close immediately
  setTimeout(() => {
    testWs.close();
    console.log('Test WebSocket manually closed');
  }, 1000);
  
} catch (error) {
  console.error('Failed to create test WebSocket:', error);
}

// Check current environment
console.log('\nEnvironment info:');
console.log('  Current URL:', window.location.href);
console.log('  Protocol:', window.location.protocol);
console.log('  Host:', window.location.host);
console.log('  Is HTTPS:', window.location.protocol === 'https:');

console.log('=== END WEBSOCKET DEBUG ===');
