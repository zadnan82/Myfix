// Complete TemplateBrowserPage with generation and live preview
import React, { useState } from 'react';
import apiClient from '../../services/api';

const TemplateBrowserPage = () => {
  const [generating, setGenerating] = useState(false);
  const [projectName, setProjectName] = useState('');
  const [templateType, setTemplateType] = useState('blog_site');
  const [result, setResult] = useState(null);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [customizations, setCustomizations] = useState({
    company_name: '',
    primary_color: '#3b82f6',
    description: ''
  });

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

  const generateWebsite = async () => {
    if (!projectName.trim()) {
      alert('Please enter a project name');
      return;
    }

    setGenerating(true);
    setResult(null);

    try {
      console.log(`Generating ${templateType} with name: ${projectName}`);
      
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

      console.log('Request data:', requestData);
      
      const response = await apiClient.post(
        `/api/v1/templates/${templateType}/generate`,
        requestData
      );

      console.log('Generation successful:', response);
      
      setResult({
        success: true,
        message: response.message,
        files_count: response.files_count,
        project_name: response.project_name,
        generation_id: response.generation_id,
        template_type: templateType
      });

      // Show success notification
      showNotification('Website generated successfully!', 'success');

    } catch (error) {
      console.error('Generation failed:', error);
      
      const errorMessage = error.response?.data?.detail || error.message || 'Generation failed';
      
      setResult({
        success: false,
        message: errorMessage
      });

      showNotification('Generation failed: ' + errorMessage, 'error');
    } finally {
      setGenerating(false);
    }
  };

  const downloadWebsite = async () => {
    if (!result || !result.generation_id) {
      alert('No generated website to download');
      return;
    }

    try {
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
        throw new Error(`Download failed: ${response.status}`);
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

  const openLivePreview = () => {
    if (!result || !result.generation_id) {
      alert('No generated website to preview');
      return;
    }

    const liveUrl = `${apiClient.baseURL}/api/v1/templates/${result.template_type}/live/${result.generation_id}`;
    console.log('Opening live preview:', liveUrl);
    window.open(liveUrl, '_blank', 'width=1200,height=800,scrollbars=yes,resizable=yes');
    showNotification('Opening live preview in new window', 'info');
  };

  const openDemo = () => {
    const demoUrl = `${apiClient.baseURL}/api/v1/templates/${templateType}/live-preview`;
    console.log('Opening demo:', demoUrl);
    window.open(demoUrl, '_blank', 'width=1200,height=800,scrollbars=yes,resizable=yes');
  };

  const showNotification = (message, type = 'info') => {
    // Create notification element
    const notification = document.createElement('div');
    notification.textContent = message;
    
    const colors = {
      success: 'bg-green-500',
      error: 'bg-red-500', 
      info: 'bg-blue-500'
    };
    
    notification.className = `fixed top-4 right-4 z-50 ${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg transition-all duration-300`;
    
    document.body.appendChild(notification);
    
    // Remove after 4 seconds
    setTimeout(() => {
      notification.style.opacity = '0';
      setTimeout(() => notification.remove(), 300);
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
  };


  const startLivePreview = async () => {
    if (!result || !result.generation_id) return;
    
    try {
        const response = await apiClient.post(
            `/api/v1/projects/${result.project_id}/preview`
        );
        
        // Open the preview in new tab
        window.open(`/preview/${result.project_id}/`, '_blank');
        
    } catch (error) {
        showNotification('Failed to start preview', 'error');
    }
};


  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Website Generator
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Create complete full-stack applications with React frontend, FastAPI backend, 
            and Docker deployment - ready in minutes.
          </p>
        </div>

        {/* Main Generation Form */}
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          
          {/* Template Selection */}
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Choose Your Website Type</h2>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {templateOptions.map((template) => (
                <div
                  key={template.id}
                  onClick={() => setTemplateType(template.id)}
                  className={`cursor-pointer border-2 rounded-lg p-4 transition-all ${
                    templateType === template.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
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

          {/* Selected Template Info */}
          {selectedTemplate && (
            <div className="p-6 bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-gray-200">
              <div className="flex items-center mb-3">
                <span className="text-2xl mr-3">{selectedTemplate.icon}</span>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{selectedTemplate.name}</h3>
                  <p className="text-gray-600">{selectedTemplate.description}</p>
                </div>
              </div>
              <div className="flex flex-wrap gap-2">
                {selectedTemplate.features.map((feature, index) => (
                  <span key={index} className="bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full">
                    {feature}
                  </span>
                ))}
              </div>
              <button
                onClick={openDemo}
                className="mt-3 text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                View Template Demo →
              </button>
            </div>
          )}

          {/* Project Configuration */}
          <div className="p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Project Configuration</h2>
            
            <div className="space-y-4">
              {/* Project Name */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Project Name *
                </label>
                <input
                  type="text"
                  value={projectName}
                  onChange={(e) => setProjectName(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="My Awesome Website"
                  disabled={generating}
                />
              </div>

              {/* Advanced Options Toggle */}
              <div className="pt-2">
                <button
                  onClick={() => setShowAdvanced(!showAdvanced)}
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  {showAdvanced ? 'Hide' : 'Show'} Advanced Options
                </button>
              </div>

              {/* Advanced Options */}
              {showAdvanced && (
                <div className="space-y-4 p-4 bg-gray-50 rounded-lg">
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
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Your Company Name"
                      disabled={generating}
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Primary Color
                    </label>
                    <input
                      type="color"
                      value={customizations.primary_color}
                      onChange={(e) => setCustomizations({
                        ...customizations, 
                        primary_color: e.target.value
                      })}
                      className="w-full h-10 rounded border border-gray-300"
                      disabled={generating}
                    />
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
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Brief description of your website"
                      rows="3"
                      disabled={generating}
                    />
                  </div>
                </div>
              )}

              {/* Generate Button */}
              <div className="pt-4">
                <button
                  onClick={generateWebsite}
                  disabled={generating || !projectName.trim()}
                  className="w-full bg-blue-600 text-white py-4 px-6 rounded-lg font-medium text-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center transition-all duration-200"
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
        </div>

        {/* Generation Progress */}
        {generating && (
          <div className="mt-6 bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <h4 className="font-medium text-yellow-800 mb-3">Generation in Progress</h4>
            <div className="space-y-2 text-sm text-yellow-700">
              <div className="flex items-center">
                <div className="animate-pulse w-2 h-2 bg-yellow-500 rounded-full mr-2"></div>
                Running SEVDO integrator with your project settings
              </div>
              <div className="flex items-center">
                <div className="animate-pulse w-2 h-2 bg-yellow-500 rounded-full mr-2"></div>
                Generating React frontend components from templates
              </div>
              <div className="flex items-center">
                <div className="animate-pulse w-2 h-2 bg-yellow-500 rounded-full mr-2"></div>
                Creating FastAPI backend with database models
              </div>
              <div className="flex items-center">
                <div className="animate-pulse w-2 h-2 bg-yellow-500 rounded-full mr-2"></div>
                Setting up Docker configuration and project files
              </div>
            </div>
          </div>
        )}

        {/* Generation Result */}
        {result && (
          <div className={`mt-6 p-6 rounded-lg border ${
            result.success 
              ? 'bg-green-50 border-green-200' 
              : 'bg-red-50 border-red-200'
          }`}>
            {result.success ? (
              <div>
                <div className="flex items-center mb-4">
                  <span className="text-2xl mr-3">✅</span>
                  <div>
                    <h3 className="text-lg font-medium text-green-800">
                      Website Generated Successfully!
                    </h3>
                    <p className="text-green-700">{result.message}</p>
                  </div>
                </div>
                
                <div className="bg-white rounded-lg p-4 mb-4">
                  <div className="grid md:grid-cols-3 gap-4 text-center">
                    <div>
                      <div className="text-2xl font-bold text-blue-600">{result.files_count}</div>
                      <div className="text-sm text-gray-600">Files Generated</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-green-600">✓</div>
                      <div className="text-sm text-gray-600">React Frontend</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-purple-600">✓</div>
                      <div className="text-sm text-gray-600">FastAPI Backend</div>
                    </div>
                  </div>
                </div>

                <div className="flex flex-wrap gap-3">
                  <button
                    onClick={openLivePreview}
                    className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 font-medium flex items-center transition-colors"
                  >
                    <span className="mr-2">🌐</span>
                    View Live Website
                  </button>

                  <button
    onClick={startLivePreview}
    className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
>
    <span className="mr-2">🚀</span>
    Start Live Preview
</button>
                  
                  <button
                    onClick={downloadWebsite}
                    className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 font-medium flex items-center transition-colors"
                  >
                    <span className="mr-2">📥</span>
                    Download ZIP
                  </button>
                  
                  <button
                    onClick={resetForm}
                    className="bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700 font-medium transition-colors"
                  >
                    Generate Another
                  </button>
                </div>
              </div>
            ) : (
              <div>
                <div className="flex items-center mb-4">
                  <span className="text-2xl mr-3">❌</span>
                  <div>
                    <h3 className="text-lg font-medium text-red-800">Generation Failed</h3>
                    <p className="text-red-700">{result.message}</p>
                  </div>
                </div>
                <button
                  onClick={() => setResult(null)}
                  className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
                >
                  Try Again
                </button>
              </div>
            )}
          </div>
        )}

        {/* What You Get Info */}
        <div className="mt-8 bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">What You'll Get</h3>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Frontend Package</h4>
              <ul className="space-y-1 text-sm text-gray-600">
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
              <h4 className="font-medium text-gray-900 mb-2">Backend Package</h4>
              <ul className="space-y-1 text-sm text-gray-600">
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