// user_frontend/src/components/RealtimeAIEditor.jsx

import React, { useState, useRef, useEffect } from 'react';
import apiClient from '../../services/api';

const RealtimeAIEditor = ({ generationId, templateType, previewUrl }) => {
  const [instruction, setInstruction] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [editHistory, setEditHistory] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const [previewFrame, setPreviewFrame] = useState(null);
  
  const wsRef = useRef(null);
  const previewRef = useRef(null);

  // WebSocket connection for real-time updates
  useEffect(() => {
    if (!generationId) return;

    const token = localStorage.getItem('auth_token'); 
     const wsUrl = `ws://localhost:8000/api/v1/ws/preview-updates/${generationId}?token=${token}`;
    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onopen = () => {
      console.log('🔄 Real-time editor WebSocket connected');
      setIsConnected(true);
    };

    wsRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('📨 WebSocket message:', data);

        if (data.type === 'edit_result') {
          handleEditResult(data.data);
        } else if (data.type === 'preview_status') {
          console.log('📊 Preview status:', data.data);
        } else if (data.type === 'error') {
          showNotification('Error: ' + data.data.message, 'error');
        }
      } catch (error) {
        console.error('WebSocket message parse error:', error);
      }
    };

    wsRef.current.onclose = () => {
      console.log('🔌 Real-time editor WebSocket disconnected');
      setIsConnected(false);
    };

    wsRef.current.onerror = (error) => {
      console.error('🚨 WebSocket error:', error);
    };

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [generationId]);

  const applyRealtimeEdit = async () => {
    if (!instruction.trim() || !generationId) {
      showNotification('Please enter an editing instruction', 'warning');
      return;
    }

    setIsEditing(true);

    try {
      // Method 1: WebSocket real-time editing (preferred)
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        console.log('🚀 Applying real-time edit via WebSocket:', instruction);
        
        wsRef.current.send(JSON.stringify({
          type: 'apply_edit',
          instruction: instruction,
          template_type: templateType,
          target_component: 'auto'
        }));
        
        // WebSocket will handle the response via handleEditResult()
      } else {
        // Method 2: HTTP API fallback
        console.log('🔄 WebSocket not available, using HTTP API');
        
        const response = await apiClient.post('/api/v1/realtime-ai-edit/realtime-edit', {
          generation_id: generationId,
          template_type: templateType,
          instruction: instruction,
          target_component: 'auto',
          preview_mode: 'live'
        });

        handleEditResult(response);
      }

    } catch (error) {
      console.error('❌ Real-time edit failed:', error);
      showNotification('Edit failed: ' + error.message, 'error');
      setIsEditing(false);
    }
  };

  const handleEditResult = (result) => {
    console.log('✅ Edit result received:', result);
    
    setIsEditing(false);
    
    // Add to edit history
    setEditHistory(prev => [...prev, {
      instruction: instruction,
      timestamp: new Date().toISOString(),
      success: result.success,
      changes: result.changes || [],
      modified_files: result.modified_files || [],
      message: result.message
    }]);

    if (result.success) {
      setInstruction(''); // Clear instruction after successful edit
      showNotification('✨ Changes applied! Preview will update automatically.', 'success');
      
      // Auto-refresh the preview iframe after a short delay
      setTimeout(() => {
        refreshPreview();
      }, 2000);
      
    } else {
      showNotification('Edit failed: ' + result.message, 'error');
    }
  };

  const refreshPreview = () => {
    if (previewRef.current) {
      console.log('🔄 Refreshing preview iframe');
      const currentSrc = previewRef.current.src;
      previewRef.current.src = '';
      setTimeout(() => {
        previewRef.current.src = currentSrc + '?t=' + Date.now();
      }, 100);
      showNotification('🔄 Preview refreshed with latest changes', 'info');
    }
  };

  const openExternalPreview = () => {
    const builtUrl = `${apiClient.baseURL}/api/v1/templates/${templateType}/preview-built/${generationId}/`;
    window.open(builtUrl, '_blank', 'width=1200,height=800');
  };

  const showNotification = (message, type = 'info') => {
    const notification = document.createElement('div');
    notification.textContent = message;
    
    const colors = {
      success: 'bg-green-500',
      error: 'bg-red-500', 
      info: 'bg-blue-500',
      warning: 'bg-yellow-500'
    };
    
    notification.className = `fixed top-4 right-4 z-50 ${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg transition-all duration-300 max-w-md text-sm`;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.style.opacity = '0';
      setTimeout(() => {
        if (notification.parentNode) {
          notification.remove();
        }
      }, 300);
    }, 4000);
  };

  const quickEditSuggestions = [
    'Change the primary color to red',
    'Make the header text larger',
    'Add a signup button to the navigation',
    'Change the background color to light blue',
    'Make all buttons rounded',
    'Add social media icons to the footer',
    'Change the font to bold',
    'Add a contact form'
  ];

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden border">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <span className="text-2xl mr-3">🤖</span>
            <div>
              <h3 className="text-lg font-semibold">Real-Time AI Editor</h3>
              <p className="text-purple-200 text-sm">Edit your website with natural language</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'}`}></div>
            <span className="text-sm">{isConnected ? 'Connected' : 'Disconnected'}</span>
          </div>
        </div>
      </div>

      {/* Editor Interface */}
      <div className="p-6">
        <div className="space-y-4">
          
          {/* Instruction Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              What would you like to change?
            </label>
            <div className="flex gap-3">
              <input
                type="text"
                value={instruction}
                onChange={(e) => setInstruction(e.target.value)}
                placeholder="e.g., 'Change the primary color to green', 'Add a contact button to the header'"
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                disabled={isEditing}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && !isEditing) {
                    applyRealtimeEdit();
                  }
                }}
              />
              <button
                onClick={applyRealtimeEdit}
                disabled={isEditing || !instruction.trim()}
                className="bg-purple-600 hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center min-w-[120px] justify-center"
              >
                {isEditing ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Editing...
                  </>
                ) : (
                  <>
                    <span className="mr-2">✨</span>
                    Apply
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Quick Suggestions */}
          <div>
            <p className="text-sm font-medium text-gray-700 mb-2">Quick suggestions:</p>
            <div className="flex flex-wrap gap-2">
              {quickEditSuggestions.map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => setInstruction(suggestion)}
                  disabled={isEditing}
                  className="text-xs bg-purple-100 hover:bg-purple-200 disabled:opacity-50 text-purple-700 px-3 py-1 rounded-full transition-colors"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>

          {/* Preview Controls */}
          <div className="flex gap-3 pt-4 border-t">
            <button
              onClick={refreshPreview}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center"
            >
              <span className="mr-2">🔄</span>
              Refresh Preview
            </button>
            <button
              onClick={openExternalPreview}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center"
            >
              <span className="mr-2">🌐</span>
              Open in New Tab
            </button>
          </div>
        </div>
      </div>

      {/* Live Preview */}
      <div className="border-t bg-gray-50 p-4">
        <div className="flex justify-between items-center mb-3">
          <h4 className="font-medium text-gray-900">Live Preview</h4>
          <span className="text-xs text-gray-500">Updates automatically after edits</span>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border overflow-hidden" style={{ height: '500px' }}>
          <iframe
            ref={previewRef}
            src={previewUrl}
            className="w-full h-full border-0"
            title="Live Preview"
            sandbox="allow-scripts allow-same-origin allow-forms"
          />
        </div>
      </div>

      {/* Edit History */}
      {editHistory.length > 0 && (
        <div className="border-t bg-gray-50 p-4">
          <h4 className="font-medium text-gray-900 mb-3">Recent Edits</h4>
          <div className="space-y-2 max-h-40 overflow-y-auto">
            {editHistory.slice(-5).reverse().map((edit, index) => (
              <div key={index} className="bg-white p-3 rounded-lg border text-sm">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className={edit.success ? 'text-green-600 font-bold' : 'text-red-600 font-bold'}>
                        {edit.success ? '✅' : '❌'}
                      </span>
                      <span className="text-gray-900 font-medium">{edit.instruction}</span>
                    </div>
                    {edit.success && edit.changes.length > 0 && (
                      <div className="text-gray-600 text-xs">
                        Changes: {edit.changes.join(', ')}
                      </div>
                    )}
                    {!edit.success && edit.message && (
                      <div className="text-red-600 text-xs">
                        Error: {edit.message}
                      </div>
                    )}
                  </div>
                  <span className="text-gray-400 text-xs">
                    {new Date(edit.timestamp).toLocaleTimeString()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default RealtimeAIEditor;