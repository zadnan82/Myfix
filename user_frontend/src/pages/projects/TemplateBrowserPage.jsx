import React, { useEffect, useRef, useState } from 'react';
import apiClient from '../../services/api';

const TemplateBrowserPage = () => {
  const [generating, setGenerating] = useState(false);
  const [projectName, setProjectName] = useState('');
  const [templateType, setTemplateType] = useState('blog_site');
  const [result, setResult] = useState(null);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editPrompt, setEditPrompt] = useState('');
  const [editHistory, setEditHistory] = useState([]);
  const [customizations, setCustomizations] = useState({
    company_name: '',
    primary_color: '#3b82f6',
    description: ''
  });
  const wsRef = useRef(null);
  const [isConnected, setIsConnected] = useState(false);
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

  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (!token) return;

    const wsUrl = `ws://localhost:8000/api/v1/ws/notifications?token=${token}`;
    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onopen = () => {
      console.log('WebSocket connected for live updates');
      setIsConnected(true);
    };

    wsRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('WebSocket message received:', data);

        if (data.type === 'preview_update' && result?.generation_id === data.data.generation_id) {
          handlePreviewUpdate(data.data);
        }
      } catch (error) {
        console.error('WebSocket message parse error:', error);
      }
    };

    wsRef.current.onclose = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    };

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [result]);

  const handlePreviewUpdate = (data) => {
    console.log('Handling preview update:', data);
    
    if (data.status === 'building') {
      showNotification(`${data.message} (${data.progress}%)`, 'info');
      setIsEditing(true);
    } 
    else if (data.status === 'completed') {
      showNotification(data.message, 'success');
      setIsEditing(false);
      
      if (window.previewWindow && !window.previewWindow.closed) {
        setTimeout(() => {
          window.previewWindow.location.reload();
          showNotification('Preview refreshed with your changes!', 'success');
        }, 500);
      }
      
      setEditHistory(prev => [...prev, {
        instruction: data.changes?.join(', ') || 'Build completed',
        timestamp: data.timestamp,
        success: true,
        changes: data.changes || []
      }]);
    } 
    else if (data.status === 'error') {
      showNotification(`Build failed: ${data.message}`, 'error');
      setIsEditing(false);
      
      setEditHistory(prev => [...prev, {
        instruction: 'Build failed',
        timestamp: data.timestamp,
        success: false,
        error: data.message
      }]);
    }
  };

  const openBuiltPreview = () => {
    if (!result || !result.generation_id) {
      showNotification('No generated website to preview', 'error');
      return;
    }

    const builtUrl = `${apiClient.baseURL}/api/v1/templates/${result.template_type}/preview-built/${result.generation_id}/`;
    console.log('Opening built preview:', builtUrl);
    window.previewWindow = window.open(builtUrl, `preview_${result.generation_id}`, 'width=1200,height=800,scrollbars=yes,resizable=yes');
    showNotification('Opening built website preview', 'info');
  };

  const generateWebsite = async () => {
    if (!projectName.trim()) {
      alert('Please enter a project name');
      return;
    }

    setGenerating(true);
    setResult(null);

    try {
      console.log(`Starting async generation of ${templateType} with name: ${projectName}`);
      
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

      console.log('Generation started:', response);
      
      if (response.generation_id) {
        setGenerationId(response.generation_id);
        showNotification('Generation started! Checking progress...', 'info');
        startStatusPolling(response.generation_id);
      } else {
        throw new Error('No generation ID returned');
      }

    } catch (error) {
      console.error('Generation start failed:', error);
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
        
        console.log('Status update:', statusResponse);
        
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

          showNotification('Website generated successfully!', 'success');
          
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
          
        } else {
          console.log(`Progress: ${statusResponse.progress}% - ${statusResponse.message}`);
        }
        
      } catch (error) {
        console.error('Status check failed:', error);
        if (error.response?.status === 404) {
          clearInterval(interval);
          setPollingInterval(null);
          setGenerating(false);
          showNotification('Generation session expired', 'error');
        }
      }
    }, 3000);
    
    setPollingInterval(interval);
    
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

  const downloadWebsite = async () => {
    if (!result || !result.generation_id) {
      showNotification('No generated website to download', 'error');
      return;
    }

    try {
      showNotification('Starting download...', 'info');
      
      const downloadUrl = `${apiClient.baseURL}/api/v1/templates/${result.template_type}/download-generated`;
      console.log('Downloading from:', downloadUrl);
      
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
      
      console.log('Download completed');
      showNotification('Website downloaded successfully!', 'success');
      
    } catch (error) {
      console.error('Download failed:', error);
      showNotification('Download failed: ' + error.message, 'error');
    }
  };

  const applyAIEdit = async () => {
    if (!result || !result.generation_id || !editPrompt.trim()) {
      showNotification('Please enter an editing instruction', 'error');
      return;
    }

    setIsEditing(true);
    
    try {
      console.log(`Applying AI edit: ${editPrompt}`);
      
      const response = await apiClient.post('/api/v1/ai/change-project-from-description', {
        description: editPrompt,
        project_name: result.generation_id,
      });

      console.log('AI edit response:', response);
      
      const successCount = response.results?.filter(r => r.compilation?.success).length || 0;
      const totalCount = response.results?.length || 0;
      
      if (successCount > 0) {
        setEditHistory(prev => [...prev, {
          instruction: editPrompt,
          timestamp: new Date().toISOString(),
          success: true,
          status: 'completed',
          summary: `${successCount}/${totalCount} changes applied`
        }]);

        setTimeout(() => {
    showNotification('Build should be complete. Click Refresh Preview now!', 'success');
  }, 30000); // 30 seconds
        
        setEditPrompt('');
        showNotification(`Changes applied successfully! (${successCount}/${totalCount})`, 'success');
        showNotification('Click "Refresh Preview" to see your changes', 'info');
      } else {
        throw new Error('No successful changes applied');
      }
      
    } catch (error) {
      console.error('AI edit failed:', error);
      
      setEditHistory(prev => [...prev, {
        instruction: editPrompt,
        timestamp: new Date().toISOString(),
        success: false,
        error: error.response?.data?.detail || error.message
      }]);
      
      showNotification('Edit failed: ' + (error.response?.data?.detail || error.message), 'error');
    } finally {
      setIsEditing(false);
    }
  };

  const refreshPreview = () => {
    if (!result || !result.generation_id) {
      showNotification('No preview window to refresh', 'error');
      return;
    }

    const builtUrl = `${apiClient.baseURL}/api/v1/templates/${result.template_type}/preview-built/${result.generation_id}/`;

    if (window.previewWindow && !window.previewWindow.closed) {
      try {
        // Use postMessage to trigger refresh (cross-origin safe)
        // Or just reopen the window with the same URL to force refresh
        window.previewWindow.location.href = builtUrl;
        showNotification('Preview refreshed successfully!', 'success');
      } catch (e) {
        console.error('Failed to refresh preview:', e);
        // If that fails, close and reopen
        window.previewWindow.close();
        window.previewWindow = window.open(
          builtUrl, 
          `preview_${result.generation_id}`, 
          'width=1200,height=800,scrollbars=yes,resizable=yes'
        );
        showNotification('Preview window reopened', 'success');
      }
    } else {
      // No preview window open - open a new one
      window.previewWindow = window.open(
        builtUrl, 
        `preview_${result.generation_id}`, 
        'width=1200,height=800,scrollbars=yes,resizable=yes'
      );
      showNotification('Preview window opened', 'success');
    }
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

  const resetForm = () => {
    setResult(null);
    setProjectName('');
    setCustomizations({
      company_name: '',
      primary_color: '#3b82f6',
      description: ''
    });
    showNotification('Form reset - ready for new generation', 'info');
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            SEVDO Website Generator
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Create complete full-stack applications with React frontend, FastAPI backend, 
            and Docker deployment - ready in minutes with live preview!
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Choose Your Website Type</h2>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
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
                  <div className="text-3xl mb-2">{template.icon}</div>
                  <h3 className="font-medium text-gray-900 mb-1">{template.name}</h3>
                  <p className="text-sm text-gray-600 mb-3">{template.description}</p>
                  <div className="flex flex-wrap gap-1">
                    {template.features.slice(0, 2).map((feature, index) => (
                      <span key={index} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                        {feature}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {selectedTemplate && (
            <div className="p-6 bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-gray-200">
              <div className="flex items-center mb-3">
                <span className="text-2xl mr-3">{selectedTemplate.icon}</span>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{selectedTemplate.name}</h3>
                  <p className="text-gray-600">{selectedTemplate.description}</p>
                </div>
              </div>
              <div className="flex flex-wrap gap-2 mb-3">
                {selectedTemplate.features.map((feature, index) => (
                  <span key={index} className="bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full">
                    {feature}
                  </span>
                ))}
              </div>
            </div>
          )}

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

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Description
                    </label>
                    <textarea
                      value={customizations.description}
                      onChange={(e) => setCustomizations({
                        ...customizations, 
                        description: e.target.value
                      })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                      placeholder="Brief description of your website"
                      rows="3"
                      disabled={generating}
                    />
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
                    'Generate Complete Website'
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>

        {generating && (
          <div className="mt-6 bg-gradient-to-r from-yellow-50 to-orange-50 border border-yellow-200 rounded-lg p-6">
            <div className="flex items-center mb-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-yellow-500 mr-3"></div>
              <h4 className="font-medium text-yellow-800 text-lg">Generation in Progress</h4>
            </div>
            <div className="space-y-3 text-sm text-yellow-700">
              <div className="flex items-center">
                <div className="animate-pulse w-2 h-2 bg-yellow-500 rounded-full mr-3"></div>
                Running SEVDO integrator with your project settings
              </div>
              <div className="flex items-center">
                <div className="animate-pulse w-2 h-2 bg-yellow-500 rounded-full mr-3"></div>
                Generating React frontend components from templates
              </div>
              <div className="flex items-center">
                <div className="animate-pulse w-2 h-2 bg-yellow-500 rounded-full mr-3"></div>
                Creating FastAPI backend with database models
              </div>
              <div className="flex items-center">
                <div className="animate-pulse w-2 h-2 bg-yellow-500 rounded-full mr-3"></div>
                Setting up Docker configuration and project files
              </div>
            </div>
          </div>
        )}

        {result && (
          <div className={`mt-6 p-6 rounded-lg border shadow-lg ${
            result.success 
              ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-200' 
              : 'bg-gradient-to-r from-red-50 to-pink-50 border-red-200'
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
                
                <div className="bg-white rounded-lg p-4 mb-6 shadow-sm">
                  <div className="grid md:grid-cols-4 gap-4 text-center">
                    <div className="p-3">
                      <div className="text-3xl font-bold text-blue-600">{result.files_count}</div>
                      <div className="text-sm text-gray-600">Files Generated</div>
                    </div>
                    <div className="p-3">
                      <div className="text-3xl font-bold text-green-600">✓</div>
                      <div className="text-sm text-gray-600">React Frontend</div>
                    </div>
                    <div className="p-3">
                      <div className="text-3xl font-bold text-purple-600">✓</div>
                      <div className="text-sm text-gray-600">FastAPI Backend</div>
                    </div>
                    <div className="p-3">
                      <div className="text-3xl font-bold text-orange-600">🐳</div>
                      <div className="text-sm text-gray-600">Docker Ready</div>
                    </div>
                  </div>
                </div>

                <div className="flex flex-wrap gap-3 mb-4">
                  <button
                    onClick={openBuiltPreview}
                    className="bg-gradient-to-r from-green-600 to-green-700 text-white px-6 py-3 rounded-lg hover:from-green-700 hover:to-green-800 font-medium flex items-center transition-all duration-200 shadow-md hover:shadow-lg"
                  >
                    View Website
                  </button>
                  
                  <button
                    onClick={downloadWebsite}
                    className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-3 rounded-lg hover:from-blue-700 hover:to-blue-800 font-medium flex items-center transition-all duration-200 shadow-md hover:shadow-lg"
                  >
                    Download ZIP
                  </button>
                  
                  <button
                    onClick={resetForm}
                    className="bg-gradient-to-r from-gray-600 to-gray-700 text-white px-6 py-3 rounded-lg hover:from-gray-700 hover:to-gray-800 font-medium transition-all duration-200 shadow-md hover:shadow-lg"
                  >
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

        {result && result.success && (
          <div className="mt-6 p-6 bg-gradient-to-r from-purple-50 to-indigo-50 border border-purple-200 rounded-lg">
            <h4 className="text-lg font-medium text-purple-900 mb-4">
              AI Website Editor
            </h4>
            
            {isEditing && (
              <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-center mb-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600 mr-3"></div>
                  <span className="text-blue-800 font-medium">Building your changes...</span>
                </div>
                <div className="w-full bg-blue-200 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full animate-pulse" style={{width: '60%'}}></div>
                </div>
              </div>
            )}
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Editing Instruction
                </label>
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={editPrompt}
                    onChange={(e) => setEditPrompt(e.target.value)}
                    placeholder="e.g., 'Change the primary color to green', 'Add a contact button to the header'"
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                    disabled={isEditing}
                    onKeyPress={(e) => e.key === 'Enter' && !isEditing && applyAIEdit()}
                  />
                  <button
                    onClick={applyAIEdit}
                    disabled={isEditing || !editPrompt.trim()}
                    className="bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white px-6 py-2 rounded-lg font-medium transition-colors"
                  >
                    {isEditing ? 'Processing...' : 'Apply Edit'}
                  </button>
                  <button
                    onClick={refreshPreview}
                    disabled={isEditing}
                    className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-6 py-2 rounded-lg font-medium transition-colors flex items-center gap-2"
                  >
                    <span>🔄</span>
                    Refresh Preview
                  </button>
                </div>
              </div>
              
              <div>
                <p className="text-sm text-gray-600 mb-2">Quick suggestions:</p>
                <div className="flex flex-wrap gap-2">
                  {[
                    'Change the primary color to red',
                    'Add a signup button',
                    'Make the header larger',
                    'Add social media links',
                    'Change the background color'
                  ].map((suggestion, index) => (
                    <button
                      key={index}
                      onClick={() => !isEditing && setEditPrompt(suggestion)}
                      disabled={isEditing}
                      className="text-xs bg-purple-100 hover:bg-purple-200 text-purple-700 px-3 py-1 rounded-full transition-colors disabled:opacity-50"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
                <p className="text-xs text-gray-500 mt-2">Tip: After applying edits, click "Refresh Preview" to see your changes</p>
              </div>
              
              {editHistory.length > 0 && (
                <div>
                  <h5 className="text-sm font-medium text-gray-700 mb-2">Recent Edits</h5>
                  <div className="max-h-32 overflow-y-auto space-y-1">
                    {editHistory.slice(-5).reverse().map((edit, index) => (
                      <div key={index} className={`text-xs p-2 rounded border ${
                        edit.status === 'processing' ? 'bg-blue-50 border-blue-200' :
                        edit.success ? 'bg-white border-gray-200' : 'bg-red-50 border-red-200'
                      }`}>
                        <div className="flex items-center justify-between">
                          <span className={
                            edit.status === 'processing' ? 'text-blue-600 flex items-center' :
                            edit.success ? 'text-green-600' : 'text-red-600'
                          }>
                            {edit.status === 'processing' && (
                              <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-blue-600 mr-2"></div>
                            )}
                            {edit.success ? '✓' : '✗'} {edit.instruction}
                          </span>
                          <span className="text-gray-500">
                            {new Date(edit.timestamp).toLocaleTimeString()}
                          </span>
                        </div>
                        {edit.error && (
                          <p className="text-red-500 text-xs mt-1">{edit.error}</p>
                        )}
                        {edit.summary && (
                          <p className="text-gray-500 text-xs mt-1">{edit.summary}</p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">What You'll Get</h3>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-3 flex items-center">
                <span className="mr-2">⚛️</span>
                Frontend Package
              </h4>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Complete React application with routing
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Responsive design with Tailwind CSS
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Interactive components and forms
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Ready for npm start and deployment
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-3 flex items-center">
                <span className="mr-2">🔧</span>
                Backend Package
              </h4>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  FastAPI server with REST endpoints
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Database models and migrations
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Authentication and security
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Docker configuration included
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TemplateBrowserPage;