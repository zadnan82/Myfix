# Production Deployment Fix

## Problem
The frontend was getting 405 (Method Not Allowed) errors when trying to access API endpoints in production. The error occurred because:

1. **Missing NGINX proxy configuration**: The frontend's NGINX server wasn't configured to proxy API requests to the backend
2. **Incorrect API URL configuration**: The frontend was hardcoded to use a specific IP address instead of using relative URLs

## Solution Applied

### 1. Updated NGINX Configuration (`user_frontend/nginx.conf`)

Added proper proxy configuration to route API requests:

```nginx
# Upstream backend service with fallbacks
upstream backend {
    server user-backend:8000 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8000 backup max_fails=3 fail_timeout=30s;
    server localhost:8000 backup max_fails=3 fail_timeout=30s;
}

# Proxy /api/ requests to backend
location /api/ {
    proxy_pass http://backend;
    # ... proxy headers and CORS configuration
}

# Proxy /v1/ requests to backend/api/v1/ (for production frontend)
location /v1/ {
    proxy_pass http://backend/api/v1/;
    # ... proxy headers and CORS configuration
}
```

### 2. Updated Frontend API Configuration (`user_frontend/src/config/api.config.js`)

Changed the production API URL to use the same domain as the frontend:

```javascript
const getApiBaseUrl = () => {
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  
  if (import.meta.env.PROD) {
    // Use same domain as frontend - NGINX will proxy to backend
    return window.location.origin;
  }
  
  return 'http://localhost:8000'; // Development default
};
```

### 3. Created Production Docker Compose Override

Created `docker-compose.prod.yml` for production-specific settings:
- Frontend serves on port 80
- Backend services not exposed externally
- Production environment variables
- Removed development volumes

## How It Works

1. **Frontend requests**: `https://80.216.194.14/v1/auth/token`
2. **NGINX receives**: Request to `/v1/auth/token`
3. **NGINX proxies**: To `http://backend/api/v1/auth/token`
4. **Backend processes**: The request on `/api/v1/auth/token`
5. **Response**: Sent back through NGINX to frontend

## Deployment Commands

### For Production
```bash
# Use production overrides
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

# Or set environment variables
export FRONTEND_DOCKERFILE=Dockerfile
export FRONTEND_PORT=80
export SEVDO_ENV=production
docker compose up --build -d
```

### For Development
```bash
# Use development defaults
docker compose up --build
```

## Verification Steps

1. **Check frontend loads**: Visit `http://80.216.194.14`
2. **Check API proxy**: Network tab should show successful API requests
3. **Check backend connectivity**: NGINX logs should show successful proxy requests
4. **Test authentication**: Login should work without 405 errors

## Troubleshooting

### If still getting 405 errors:
1. Check NGINX logs: `docker compose logs user-frontend`
2. Check backend logs: `docker compose logs user-backend`
3. Verify backend is running: `docker compose ps`
4. Test backend directly: `curl http://localhost:8000/api/v1/auth/token` (should return 422, not 405)

### If backend connection fails:
1. Verify Docker network: `docker network ls`
2. Check service names: `docker compose ps`
3. Test internal connectivity: `docker compose exec user-frontend ping user-backend`

## Key Changes Made

- ✅ Added NGINX proxy configuration for `/api/` and `/v1/` routes
- ✅ Fixed frontend API URL to use `window.location.origin` in production
- ✅ Added CORS headers to NGINX configuration
- ✅ Created production Docker Compose override
- ✅ Added debugging logs to frontend configuration
- ✅ Configured upstream with fallback servers for resilience
