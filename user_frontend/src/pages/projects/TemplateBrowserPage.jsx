// Updated user_frontend/src/pages/projects/TemplateBrowserPage.jsx
// Integration with Real-Time AI Editor

import React, { useEffect, useRef, useState } from 'react';
import apiClient from '../../services/api'; 
import RealtimeAIEditor from './RealtimeAIEditor';

const TemplateBrowserPage = () => {
  const [generating, setGenerating] = useState(false);
  const [projectName, setProjectName] = useState('');
  const [templateType, setTemplateType] = useState('blog_site');
  const [result, setResult] = useState(null);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [showRealtimeEditor, setShowRealtimeEditor] = useState(false);
  const [customizations, setCustomizations] = useState({
    company_name: '',
    primary_color: '#3b82f6',
    description: ''
  });
  
  // WebSocket for preview updates
  const wsRef = useRef(null);
  const [isConnected, setIsConnected] = useState(false);
  
  // Generation tracking
  const [generationId, setGenerationId] = useState(null);
  const [pollingInterval, setPollingInterval] = useState(null);

  const templateOptions = [
    { 
      id: 'blog_site', 
      name: 'Blog Website', 
      description: 'Complete blog with articles, comments, and admin panel',
      icon: '📝',
      features: ['Article Management', 'Comments System', 'SEO Optimized', 'Admin Dashboard']
    },
    { 
      id: 'business_site', 
      name: 'Business Website', 
      description: 'Professional business site with services and contact forms',
      icon: '💼',
      features: ['Service Pages', 'Contact Forms', 'Team Profiles', 'Portfolio Gallery']
    },
    { 
      id: 'restaurant_site', 
      name: 'Restaurant Website', 
      description: 'Restaurant site with menu, reservations, and online ordering',
      icon: '🍽️',
      features: ['Digital Menu', 'Reservation System', 'Online Ordering', 'Location Map']
    },
    { 
      id: 'portfolio_site', 
      name: 'Portfolio Website', 
      description: 'Creative portfolio with project showcase and client testimonials',
      icon: '🎨',
      features: ['Project Gallery', 'Client Testimonials', 'Skills Display', 'Contact Integration']
    },
    { 
      id: 'ecommerce_site', 
      name: 'E-commerce Website', 
      description: 'Full online store with product catalog and shopping cart',
      icon: '🛒',
      features: ['Product Catalog', 'Shopping Cart', 'Payment Integration', 'Order Management']
    }
  ];

  const selectedTemplate = templateOptions.find(t => t.id === templateType);

  //    WebSocket connection for preview updates
  useEffect(() => {
    if (!result?.generation_id) return;

    const token = localStorage.getItem('auth_token');
    if (!token) return;

    // Connect to    preview updates WebSocket
    const wsUrl = `ws://localhost:8000/api/v1/ws/preview-updates/${result.generation_id}?token=${token}`;
    
    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onopen = () => {
      console.log('🔄    preview WebSocket connected');
      setIsConnected(true);
      
      // Send initial subscription
      wsRef.current.send(JSON.stringify({
        type: 'subscribe_to_edits'
      }));
    };

    wsRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('📨    WebSocket message:', data);

        if (data.type === 'preview_update') {
          handlePreviewUpdate(data.data);
        } else if (data.type === 'edit_session_started') {
          showNotification('🤖 AI is editing your website...', 'info');
        } else if (data.type === 'edit_session_completed') {
          handleEditSessionComplete(data.data);
        } else if (data.type === 'connection_established') {
          console.log('✅    connection established:', data.data);
        }
      } catch (error) {
        console.error('WebSocket message parse error:', error);
      }
    };

    wsRef.current.onclose = () => {
      console.log('🔌    preview WebSocket disconnected');
      setIsConnected(false);
    };

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [result?.generation_id]);

  const handleEditSessionComplete = (sessionData) => {
    if (sessionData.success) {
      showNotification(`✨ ${sessionData.instruction} - Changes applied successfully!`, 'success');
      
      // Auto-refresh preview window if open
      if (window.previewWindow && !window.previewWindow.closed) {
        setTimeout(() => {
          window.previewWindow.location.reload();
        }, 1000);
      }
    } else {
      showNotification('❌ Edit failed - please try again', 'error');
    }
  };

  const handlePreviewUpdate = (data) => {
    console.log('🔄 Preview update received:', data);
    
    if (data.action === 'reload_preview') {
      showNotification('🔄 Preview updated with latest changes', 'success');
      
      // Auto-refresh any open preview windows
      if (window.previewWindow && !window.previewWindow.closed) {
        setTimeout(() => {
          window.previewWindow.location.reload();
        }, 500);
      }
    }
  };

  const generateWebsite = async () => {
    if (!projectName.trim()) {
      alert('Please enter a project name');
      return;
    }

    setGenerating(true);
    setResult(null);

    try {
      console.log(`🚀 Starting async generation of ${templateType} with name: ${projectName}`);
      
      const requestData = {
        project_name: projectName,
        customizations: {
          company_name: customizations.company_name || projectName,
          primary_color: customizations.primary_color,
          description: customizations.description
        },
        include_docker: true,
        include_readme: true
      };

      const response = await apiClient.post(
        `/api/v1/templates/${templateType}/generate`,
        requestData
      );

      console.log('✅ Generation started:', response);
      
      if (response.generation_id) {
        setGenerationId(response.generation_id);
        showNotification('Generation started! Checking progress...', 'info');
        startStatusPolling(response.generation_id);
      } else {
        throw new Error('No generation ID returned');
      }

    } catch (error) {
      console.error('❌ Generation start failed:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Generation failed to start';
      
      setResult({
        success: false,
        message: errorMessage,
        error_details: error.response?.data || error
      });

      showNotification('Generation failed to start: ' + errorMessage, 'error');
      setGenerating(false);
    }
  };

  const startStatusPolling = (genId) => {
    if (pollingInterval) {
      clearInterval(pollingInterval);
    }
    
    const interval = setInterval(async () => {
      try {
        const statusResponse = await apiClient.get(
          `/api/v1/templates/${templateType}/status/${genId}`
        );
        
        console.log('📊 Status update:', statusResponse);
        
        if (statusResponse.status === 'completed') {
          clearInterval(interval);
          setPollingInterval(null);
          setGenerating(false);
          
          setResult({
            success: true,
            message: statusResponse.message,
            files_count: statusResponse.file_count,
            project_name: statusResponse.project_name,
            generation_id: genId,
            template_type: templateType,
            project_id: statusResponse.project_id,
            generated_at: statusResponse.completed_at,
            raw_response: statusResponse
          });

          showNotification('Website generated successfully! 🎉', 'success');
          
          // Enable real-time editor
          setShowRealtimeEditor(true);
          
        } else if (statusResponse.status === 'failed') {
          clearInterval(interval);
          setPollingInterval(null);
          setGenerating(false);
          
          setResult({
            success: false,
            message: statusResponse.message,
            error_details: statusResponse.error
          });

          showNotification('Generation failed: ' + statusResponse.message, 'error');
        }
        
      } catch (error) {
        console.error('❌ Status check failed:', error);
        if (error.response?.status === 404) {
          clearInterval(interval);
          setPollingInterval(null);
          setGenerating(false);
          showNotification('Generation session expired', 'error');
        }
      }
    }, 3000);
    
    setPollingInterval(interval);
    
    // Auto-stop after 15 minutes
    setTimeout(() => {
      if (interval) {
        clearInterval(interval);
        setPollingInterval(null);
        setGenerating(false);
        showNotification('Generation timed out after 15 minutes', 'error');
      }
    }, 15 * 60 * 1000);
  };

  React.useEffect(() => {
    return () => {
      if (pollingInterval) {
        clearInterval(pollingInterval);
      }
    };
  }, [pollingInterval]);

  const openBuiltPreview = () => {
    if (!result || !result.generation_id) {
      showNotification('No generated website to preview', 'error');
      return;
    }

    const builtUrl = `${apiClient.baseURL}/api/v1/templates/${result.template_type}/preview-built/${result.generation_id}/`;
    console.log('🌐 Opening built preview:', builtUrl);
    
    // Store reference for live updates
    window.previewWindow = window.open(
      builtUrl, 
      `preview_${result.generation_id}`, 
      'width=1200,height=800,scrollbars=yes,resizable=yes'
    );
    
    showNotification('Opening built website preview', 'info');
  };

  const downloadWebsite = async () => {
    if (!result || !result.generation_id) {
      showNotification('No generated website to download', 'error');
      return;
    }

    try {
      showNotification('Starting download...', 'info');
      
      const downloadUrl = `${apiClient.baseURL}/api/v1/templates/${result.template_type}/download-generated`;
      console.log('📥 Downloading from:', downloadUrl);
      
      const token = localStorage.getItem('auth_token');
      const response = await fetch(downloadUrl, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Accept': 'application/zip'
        }
      });
      
      if (!response.ok) {
        throw new Error(`Download failed: ${response.status} ${response.statusText}`);
      }
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${projectName.replace(/\s+/g, '-').toLowerCase()}-website.zip`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      console.log('✅ Download completed');
      showNotification('Website downloaded successfully!', 'success');
      
    } catch (error) {
      console.error('❌ Download failed:', error);
      showNotification('Download failed: ' + error.message, 'error');
    }
  };

  const resetForm = () => {
    setResult(null);
    setProjectName('');
    setShowRealtimeEditor(false);
    setCustomizations({
      company_name: '',
      primary_color: '#3b82f6',
      description: ''
    });
    showNotification('Form reset - ready for new generation', 'info');
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
    
    notification.className = `fixed top-4 right-4 z-50 ${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg transition-all duration-300 max-w-md`;
    
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

  const GenerationProgress = ({ generationId, templateType }) => {
    const [status, setStatus] = useState(null);

    React.useEffect(() => {
      if (!generationId) return;

      const interval = setInterval(async () => {
        try {
          const response = await apiClient.get(`/api/v1/templates/${templateType}/status/${generationId}`);
          setStatus(response);
        } catch (error) {
          console.error('Status update failed:', error);
        }
      }, 2000);

      return () => clearInterval(interval);
    }, [generationId, templateType]);

    if (!status) return null;

    return (
      <div className="mt-6 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
        <div className="flex items-center mb-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mr-3"></div>
          <h4 className="font-medium text-blue-800 text-lg">Generation Progress</h4>
        </div>
        
        <div className="w-full bg-blue-200 rounded-full h-3 mb-4">
          <div 
            className="bg-blue-600 h-3 rounded-full transition-all duration-500"
            style={{ width: `${status.progress || 0}%` }}
          ></div>
        </div>
        
        <div className="flex justify-between text-sm text-blue-700 mb-3">
          <span>{status.progress || 0}% Complete</span>
          <span>Status: {status.status}</span>
        </div>
        
        <p className="text-sm text-blue-600">{status.message}</p>
        
        {status.status === 'generating' && (
          <div className="mt-4 space-y-2 text-xs text-blue-600">
            <div className="flex items-center">
              <div className="animate-pulse w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
              This may take 5-10 minutes for npm install and build
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            SEVDO Website Generator
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Create complete full-stack applications with React frontend, FastAPI backend, 
            and real-time AI editing - ready in minutes!
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          
          {/* Left Column: Generation */}
          <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            
            {/* Template Selection */}
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Choose Your Website Type</h2>
              
              <div className="grid gap-4">
                {templateOptions.map((template) => (
                  <div
                    key={template.id}
                    onClick={() => setTemplateType(template.id)}
                    className={`cursor-pointer border-2 rounded-lg p-4 transition-all duration-200 ${
                      templateType === template.id
                        ? 'border-blue-500 bg-blue-50 shadow-md'
                        : 'border-gray-200 hover:border-gray-300 hover:shadow-sm'
                    }`}
                  >
                    <div className="flex items-center">
                      <div className="text-2xl mr-3">{template.icon}</div>
                      <div className="flex-1">
                        <h3 className="font-medium text-gray-900 mb-1">{template.name}</h3>
                        <p className="text-sm text-gray-600 mb-2">{template.description}</p>
                        <div className="flex flex-wrap gap-1">
                          {template.features.slice(0, 2).map((feature, index) => (
                            <span key={index} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                              {feature}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Project Configuration */}
            <div className="p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Project Configuration</h2>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Project Name *
                  </label>
                  <input
                    type="text"
                    value={projectName}
                    onChange={(e) => setProjectName(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="My Awesome Website"
                    disabled={generating}
                  />
                </div>

                <div className="pt-2">
                  <button
                    onClick={() => setShowAdvanced(!showAdvanced)}
                    className="text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors"
                  >
                    {showAdvanced ? 'Hide' : 'Show'} Advanced Options
                  </button>
                </div>

                {showAdvanced && (
                  <div className="space-y-4 p-4 bg-gray-50 rounded-lg border">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Company Name
                      </label>
                      <input
                        type="text"
                        value={customizations.company_name}
                        onChange={(e) => setCustomizations({
                          ...customizations, 
                          company_name: e.target.value
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                        placeholder="Your Company Name"
                        disabled={generating}
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Primary Color
                      </label>
                      <div className="flex items-center space-x-3">
                        <input
                          type="color"
                          value={customizations.primary_color}
                          onChange={(e) => setCustomizations({
                            ...customizations, 
                            primary_color: e.target.value
                          })}
                          className="w-16 h-10 rounded border border-gray-300 cursor-pointer"
                          disabled={generating}
                        />
                        <span className="text-sm text-gray-600">{customizations.primary_color}</span>
                      </div>
                    </div>
                  </div>
                )}

                <div className="pt-4">
                  <button
                    onClick={generateWebsite}
                    disabled={generating || !projectName.trim()}
                    className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-4 px-6 rounded-lg font-medium text-lg hover:from-blue-700 hover:to-blue-800 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center transition-all duration-200 shadow-lg hover:shadow-xl"
                  >
                    {generating ? (
                      <>
                        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                        Generating Your Website...
                      </>
                    ) : (
                      <>
                        <span className="mr-2">🚀</span>
                        Generate Complete Website
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>

            {/* Generation Progress */}
            {generating && generationId && (
              <GenerationProgress generationId={generationId} templateType={templateType} />
            )}

            {/* Generation Result */}
            {result && (
              <div className={`p-6 border-t ${
                result.success 
                  ? 'bg-gradient-to-r from-green-50 to-emerald-50' 
                  : 'bg-gradient-to-r from-red-50 to-pink-50'
              }`}>
                {result.success ? (
                  <div>
                    <div className="flex items-center mb-4">
                      <span className="text-3xl mr-3">✅</span>
                      <div>
                        <h3 className="text-xl font-medium text-green-800">
                          Website Generated Successfully!
                        </h3>
                        <p className="text-green-700">{result.message}</p>
                      </div>
                    </div>
                    
                    <div className="flex flex-wrap gap-3 mb-4">
                      <button
                        onClick={openBuiltPreview}
                        className="bg-gradient-to-r from-purple-600 to-purple-700 text-white px-6 py-3 rounded-lg hover:from-purple-700 hover:to-purple-800 font-medium flex items-center transition-all duration-200 shadow-md hover:shadow-lg"
                      >
                        <span className="mr-2">🌐</span>
                        Open Preview
                      </button>
                      
                      <button
                        onClick={downloadWebsite}
                        className="bg-gradient-to-r from-green-600 to-green-700 text-white px-6 py-3 rounded-lg hover:from-green-700 hover:to-green-800 font-medium flex items-center transition-all duration-200 shadow-md hover:shadow-lg"
                      >
                        <span className="mr-2">📥</span>
                        Download ZIP
                      </button>
                      
                      <button
                        onClick={resetForm}
                        className="bg-gradient-to-r from-gray-600 to-gray-700 text-white px-6 py-3 rounded-lg hover:from-gray-700 hover:to-gray-800 font-medium transition-all duration-200 shadow-md hover:shadow-lg"
                      >
                        <span className="mr-2">🔄</span>
                        Generate Another
                      </button>
                    </div>
                  </div>
                ) : (
                  <div>
                    <div className="flex items-center mb-4">
                      <span className="text-3xl mr-3">❌</span>
                      <div>
                        <h3 className="text-xl font-medium text-red-800">Generation Failed</h3>
                        <p className="text-red-700">{result.message}</p>
                      </div>
                    </div>
                    <button
                      onClick={() => setResult(null)}
                      className="bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 font-medium transition-colors"
                    >
                      Try Again
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Right Column: Real-Time AI Editor */}
          {showRealtimeEditor && result?.success && (
            <div className="lg:sticky lg:top-8">
              <RealtimeAIEditor
                generationId={result.generation_id}
                templateType={result.template_type}
                previewUrl={`${apiClient.baseURL}/api/v1/templates/${result.template_type}/preview-built/${result.generation_id}/`}
              />
            </div>
          )}

          {/* Placeholder when no editor */}
          {!showRealtimeEditor && (
            <div className="bg-white rounded-xl shadow-lg p-8 flex items-center justify-center">
              <div className="text-center text-gray-500">
                <div className="text-6xl mb-4">🤖</div>
                <h3 className="text-lg font-medium mb-2">AI Editor</h3>
                <p className="text-sm">
                  Generate your website first to unlock the real-time AI editor
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Connection Status Indicator */}
        {showRealtimeEditor && (
          <div className="fixed bottom-4 right-4 z-50">
            <div className={`flex items-center px-4 py-2 rounded-lg shadow-lg text-white text-sm ${
              isConnected ? 'bg-green-500' : 'bg-red-500'
            }`}>
              <div className={`w-2 h-2 rounded-full mr-2 ${
                isConnected ? 'bg-green-200' : 'bg-red-200'
              }`}></div>
              {isConnected ? 'Real-time Connected' : 'Connection Lost'}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TemplateBrowserPage;