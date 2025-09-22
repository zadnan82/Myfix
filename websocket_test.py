#!/usr/bin/env python3
"""
WebSocket Connection Test Script for SEVDO Backend

This script tests the WebSocket endpoints to verify they're working correctly.
Usage: python websocket_test.py [server_url] [token]

Examples:
  python websocket_test.py wss://api.sevdo.se test-token
  python websocket_test.py ws://localhost:8000 your-auth-token
"""

import asyncio
import websockets
import json
import sys
from datetime import datetime


async def test_notifications_websocket(server_url, token):
    """Test the notifications WebSocket endpoint"""
    uri = f"{server_url}/api/v1/ws/notifications?token={token}"
    
    print(f"🔗 Connecting to: {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connection established!")
            
            # Send a test message to mark a notification as read
            test_message = {
                "type": "mark_read",
                "notification_id": 1
            }
            
            await websocket.send(json.dumps(test_message))
            print("📤 Sent test message:", test_message)
            
            # Wait for responses for 10 seconds
            print("⏳ Waiting for messages for 10 seconds...")
            
            timeout = 10
            start_time = asyncio.get_event_loop().time()
            
            while asyncio.get_event_loop().time() - start_time < timeout:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(message)
                    print(f"📥 Received: {data}")
                except asyncio.TimeoutError:
                    print(".", end="", flush=True)
                except websockets.exceptions.ConnectionClosed:
                    print("\n❌ Connection closed by server")
                    break
                except json.JSONDecodeError as e:
                    print(f"\n⚠️  Invalid JSON received: {message}")
            
            print(f"\n✅ Test completed successfully!")
            
    except websockets.exceptions.InvalidStatusCode as e:
        if e.status_code == 426:
            print(f"❌ 426 Upgrade Required - WebSocket endpoint not available")
            print(f"   This means the server doesn't support WebSocket on this endpoint")
        else:
            print(f"❌ HTTP {e.status_code}: {e}")
    except websockets.exceptions.InvalidURI:
        print(f"❌ Invalid WebSocket URI: {uri}")
    except websockets.exceptions.ConnectionRefused:
        print(f"❌ Connection refused - server not running or not accessible")
    except Exception as e:
        print(f"❌ Connection failed: {e}")


async def test_project_websocket(server_url, token, project_id=1):
    """Test the project generation WebSocket endpoint"""
    uri = f"{server_url}/api/v1/ws/projects/{project_id}/generation?token={token}"
    
    print(f"🔗 Connecting to project WebSocket: {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Project WebSocket connection established!")
            
            # Wait for project status messages
            print("⏳ Waiting for project messages for 5 seconds...")
            
            timeout = 5
            start_time = asyncio.get_event_loop().time()
            
            while asyncio.get_event_loop().time() - start_time < timeout:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(message)
                    print(f"📥 Project update: {data}")
                except asyncio.TimeoutError:
                    print(".", end="", flush=True)
                except websockets.exceptions.ConnectionClosed:
                    print("\n❌ Project connection closed by server")
                    break
                except json.JSONDecodeError as e:
                    print(f"\n⚠️  Invalid JSON received: {message}")
            
            print(f"\n✅ Project WebSocket test completed!")
            
    except websockets.exceptions.InvalidStatusCode as e:
        if e.status_code == 426:
            print(f"❌ 426 Upgrade Required - Project WebSocket endpoint not available")
        else:
            print(f"❌ HTTP {e.status_code}: {e}")
    except Exception as e:
        print(f"❌ Project WebSocket connection failed: {e}")


async def test_system_status_websocket(server_url):
    """Test the system status WebSocket endpoint (no auth required)"""
    uri = f"{server_url}/api/v1/ws/system-status"
    
    print(f"🔗 Connecting to system status WebSocket: {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ System status WebSocket connection established!")
            
            # Wait for system status messages
            print("⏳ Waiting for system status messages for 5 seconds...")
            
            timeout = 5
            start_time = asyncio.get_event_loop().time()
            
            while asyncio.get_event_loop().time() - start_time < timeout:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(message)
                    print(f"📥 System status: {data}")
                except asyncio.TimeoutError:
                    print(".", end="", flush=True)
                except websockets.exceptions.ConnectionClosed:
                    print("\n❌ System status connection closed by server")
                    break
                except json.JSONDecodeError as e:
                    print(f"\n⚠️  Invalid JSON received: {message}")
            
            print(f"\n✅ System status WebSocket test completed!")
            
    except websockets.exceptions.InvalidStatusCode as e:
        if e.status_code == 426:
            print(f"❌ 426 Upgrade Required - System status WebSocket endpoint not available")
        else:
            print(f"❌ HTTP {e.status_code}: {e}")
    except Exception as e:
        print(f"❌ System status WebSocket connection failed: {e}")


async def main():
    if len(sys.argv) < 2:
        print("Usage: python websocket_test.py <server_url> [token]")
        print("Examples:")
        print("  python websocket_test.py wss://api.sevdo.se test-token")
        print("  python websocket_test.py ws://localhost:8000 your-auth-token")
        sys.exit(1)
    
    server_url = sys.argv[1]
    token = sys.argv[2] if len(sys.argv) > 2 else "test-token"
    
    print(f"🚀 Starting WebSocket tests")
    print(f"   Server: {server_url}")
    print(f"   Token: {token}")
    print(f"   Time: {datetime.now().isoformat()}")
    print("=" * 50)
    
    # Test all WebSocket endpoints
    await test_notifications_websocket(server_url, token)
    print("\n" + "-" * 50)
    
    await test_project_websocket(server_url, token, project_id=1)
    print("\n" + "-" * 50)
    
    await test_system_status_websocket(server_url)
    
    print("\n" + "=" * 50)
    print("🏁 All WebSocket tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
