// user_frontend/src/components/RealTemplateGallery.jsx

import React, { useState, useEffect } from 'react';
import { apiClient } from '../services/api';
import { getEndpoint, getApiUrl } from '../config/api.config';

const RealTemplateGallery = () => {
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [showCustomizer, setShowCustomizer] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [generationResult, setGenerationResult] = useState(null);
  const [customizations, setCustomizations] = useState({
    project_name: '',
    company_name: '',
    primary_color: '#3b82f6',
    description: '',
    contact_email: '',
    phone: ''
  });

  useEffect(() => {
    loadGeneratedTemplates();
  }, []);

  const loadGeneratedTemplates = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/api/v1/templates');
      
      // Filter only successfully generated templates
      const generatedTemplates = Array.isArray(response) 
        ? response.filter(t => t.preview_data?.has_frontend || t.preview_data?.has_backend)
        : response.templates?.filter(t => t.preview_data?.has_frontend || t.preview_data?.has_backend) || [];
      
      setTemplates(generatedTemplates);
      console.log('Loaded generated templates:', generatedTemplates);
    } catch (error) {
      console.error('Failed to load generated templates:', error);
      // Show error message to user
      setTemplates([]);
    } finally {
      setLoading(false);
    }
  };

  const openDemoPreview = (template) => {
    const demoUrl = getApiUrl(`/api/v1/templates/${template.id}/demo`);
    window.open(demoUrl, '_blank', 'width=1200,height=800,scrollbars=yes,resizable=yes');
  };

  const startCustomization = (template) => {
    setSelectedTemplate(template);
    setShowCustomizer(true);
    setCustomizations({
      ...customizations,
      project_name: `My ${template.name}`,
      description: template.description || `Custom ${template.name} website`
    });
  };

  const generateCustomTemplate = async () => {
    if (!selectedTemplate || !customizations.project_name.trim()) {
      alert('Please enter a project name');
      return;
    }

    setGenerating(true);
    try {
      const response = await apiClient.post(
        `/api/v1/templates/${selectedTemplate.id}/generate`,
        {
          project_name: customizations.project_name,
          customizations: customizations,
          include_docker: true,
          include_readme: true
        }
      );

      setGenerationResult(response);
      
      // Show success message
      const fileCount = response.files_count || 0;
      alert(`🎉 "${customizations.project_name}" generated successfully!\n\n` + 
            `✅ ${fileCount} files created\n` +
            `✅ Frontend: React application\n` + 
            `✅ Backend: FastAPI server\n` +
            `✅ Database: PostgreSQL\n` +
            `✅ Docker: Ready to deploy\n\n` +
            `You can now download your complete web application!`);

    } catch (error) {
      console.error('Template generation failed:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Unknown error';
      alert(`❌ Generation failed:\n\n${errorMessage}\n\nPlease try again or contact support.`);
    } finally {
      setGenerating(false);
    }
  };

  const downloadTemplate = async (template, isCustom = false) => {
    try {
      let downloadUrl;
      
      if (isCustom && generationResult) {
        // Download the custom generated version
        const customizationsJson = encodeURIComponent(JSON.stringify(customizations));
        downloadUrl = getApiUrl(`/api/v1/templates/${template.id}/download-generated?project_name=${encodeURIComponent(customizations.project_name)}&customizations=${customizationsJson}`);
      } else {
        // Download the base template
        downloadUrl = getApiUrl(`/api/v1/templates/${template.id}/download?project_name=${encodeURIComponent(template.name)}`);
      }
      
      // Create invisible link and trigger download
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = `${isCustom ? customizations.project_name : template.name}-webapp.zip`;
      
      // Add auth header by fetching manually
      const response = await fetch(downloadUrl, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
        }
      });
      
      if (!response.ok) {
        throw new Error(`Download failed: ${response.statusText}`);
      }
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      link.href = url;
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      // Show success message
      setTimeout(() => {
        alert('📥 Download started! Your webapp includes:\n\n' +
              '• Complete React frontend\n' +
              '• FastAPI backend with database\n' +
              '• Docker configuration\n' +
              '• Setup instructions\n' +
              '• Environment configuration\n\n' +
              'Extract the ZIP and follow the README to get started!');
      }, 1000);
      
    } catch (error) {
      console.error('Download failed:', error);
      alert('❌ Download failed: ' + error.message);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getTemplateIcon = (category) => {
    const icons = {
      restaurant: '🍽️',
      business: '💼', 
      ecommerce: '🛒',
      portfolio: '🎨',
      blog: '📝',
      saas: '💻',
      fitness: '💪',
      education: '📚',
      real_estate: '🏠',
      nonprofit: '❤️'
    };
    return icons[category] || '🌐';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Loading Generated Websites</h3>
          <p className="text-gray-600">Please wait while we load the ready-to-use templates...</p>
        </div>
      </div>
    );
  }

  if (showCustomizer && selectedTemplate) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto py-8 px-4">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <div>
              <button
                onClick={() => setShowCustomizer(false)}
                className="text-blue-600 hover:text-blue-800 mb-4 flex items-center"
              >
                ← Back to Gallery
              </button>
              <h1 className="text-3xl font-bold text-gray-900">
                Customize: {selectedTemplate.name}
              </h1>
              <p className="text-gray-600 mt-1">{selectedTemplate.description}</p>
            </div>
            
            <div className="text-right">
              <div className="text-sm text-gray-500">Template includes:</div>
              <div className="flex items-center space-x-4 mt-1">
                {selectedTemplate.preview_data?.has_frontend && (
                  <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    ✅ Frontend
                  </span>
                )}
                {selectedTemplate.preview_data?.has_backend && (
                  <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    ✅ Backend
                  </span>
                )}
                <span className="text-sm text-gray-500">
                  {formatFileSize(selectedTemplate.preview_data?.download_size || 0)}
                </span>
              </div>
            </div>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {/* Customization Panel */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow-lg p-6 sticky top-8">
                <h2 className="text-xl font-semibold mb-6">Customize Your Website</h2>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Project Name *
                    </label>
                    <input
                      type="text"
                      value={customizations.project_name}
                      onChange={(e) => setCustomizations({...customizations, project_name: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="My Awesome Website"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Company/Brand Name
                    </label>
                    <input
                      type="text"
                      value={customizations.company_name}
                      onChange={(e) => setCustomizations({...customizations, company_name: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Your Company Name"
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
                        onChange={(e) => setCustomizations({...customizations, primary_color: e.target.value})}
                        className="w-12 h-10 rounded border border-gray-300"
                      />
                      <input
                        type="text"
                        value={customizations.primary_color}
                        onChange={(e) => setCustomizations({...customizations, primary_color: e.target.value})}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Contact Email
                    </label>
                    <input
                      type="email"
                      value={customizations.contact_email}
                      onChange={(e) => setCustomizations({...customizations, contact_email: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="contact@yourcompany.com"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Description
                    </label>
                    <textarea
                      value={customizations.description}
                      onChange={(e) => setCustomizations({...customizations, description: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      rows={3}
                      placeholder="Describe your website or business..."
                    />
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="mt-8 space-y-3">
                  {!generationResult ? (
                    <button
                      onClick={generateCustomTemplate}
                      disabled={generating || !customizations.project_name.trim()}
                      className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                    >
                      {generating ? (
                        <>
                          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                          Generating Your Website...
                        </>
                      ) : (
                        <>
                          🚀 Generate Custom Website
                        </>
                      )}
                    </button>
                  ) : (
                    <button
                      onClick={() => downloadTemplate(selectedTemplate, true)}
                      className="w-full bg-green-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-green-700 flex items-center justify-center"
                    >
                      📥 Download Your Website
                    </button>
                  )}

                  <button
                    onClick={() => openDemoPreview(selectedTemplate)}
                    className="w-full bg-purple-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-purple-700"
                  >
                    👁️ View Live Demo
                  </button>
                  
                  <button
                    onClick={() => downloadTemplate(selectedTemplate, false)}
                    className="w-full bg-gray-200 text-gray-800 py-2 px-4 rounded-lg font-medium hover:bg-gray-300"
                  >
                    📥 Download Original Template
                  </button>
                </div>

                {/* Template Features */}
                {selectedTemplate.features && (
                  <div className="mt-6">
                    <h3 className="font-medium text-gray-900 mb-3">Included Features:</h3>
                    <div className="flex flex-wrap gap-2">
                      {selectedTemplate.features.slice(0, 8).map((feature, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                        >
                          {feature}
                        </span>
                      ))}
                      {selectedTemplate.features.length > 8 && (
                        <span className="px-3 py-1 bg-gray-100 text-gray-600 text-sm rounded-full">
                          +{selectedTemplate.features.length - 8} more
                        </span>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Preview Panel */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-lg shadow-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold">Live Preview</h2>
                  <button
                    onClick={() => openDemoPreview(selectedTemplate)}
                    className="text-blue-600 hover:text-blue-800 text-sm"
                  >
                    Open in New Tab →
                  </button>
                </div>
                
                {generationResult && (
                  <div className="mb-6 bg-green-50 border border-green-200 rounded-lg p-4">
                    <h3 className="font-medium text-green-800 mb-2">✅ Generation Successful!</h3>
                    <div className="text-green-700 text-sm space-y-1">
                      <p>Project "{generationResult.project_name}" has been generated</p>
                      <p>📁 {generationResult.files_count} files created</p>
                      <p>🎯 Ready for download and deployment</p>
                    </div>
                  </div>
                )}
                
                {/* Embedded Preview */}
                <div className="border rounded-lg overflow-hidden" style={{ height: '600px' }}>
                  <iframe
                    src={getApiUrl(`/api/v1/templates/${selectedTemplate.id}/demo`)}
                    className="w-full h-full"
                    title={`${selectedTemplate.name} Preview`}
                    loading="lazy"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-12 px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Ready-to-Deploy Websites
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
            Professional websites generated with <strong>SEVDO Integrator</strong>. 
            Complete with frontend, backend, database, and Docker - ready to customize and deploy in minutes.
          </p>
          
          <div className="flex justify-center space-x-8 text-sm text-gray-500">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-400 rounded-full mr-2"></div>
              Live Demos Available
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-blue-400 rounded-full mr-2"></div>
              Full Source Code
            </div>
            <div className="flex items-center">  
              <div className="w-3 h-3 bg-purple-400 rounded-full mr-2"></div>
              Docker Ready
            </div>
          </div>
        </div>

        {/* Templates Grid */}
        {templates.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {templates.map((template) => (
              <div key={template.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
                {/* Template Preview */}
                <div className="relative h-48 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="text-white text-6xl">
                      {getTemplateIcon(template.category)}
                    </div>
                  </div>
                  
                  {/* Status Badges */}
                  <div className="absolute top-3 left-3">
                    {template.is_featured && (
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                        ⭐ Featured
                      </span>
                    )}
                  </div>
                  
                  <div className="absolute top-3 right-3 space-y-1">
                    {template.preview_data?.has_frontend && (
                      <div className="bg-green-500 text-white px-2 py-1 rounded text-xs font-medium">
                        ✅ Frontend
                      </div>
                    )}
                    {template.preview_data?.has_backend && (
                      <div className="bg-blue-500 text-white px-2 py-1 rounded text-xs font-medium">
                        ✅ Backend
                      </div>
                    )}
                  </div>
                </div>

                {/* Template Info */}
                <div className="p-6">
                  <div className="flex items-start justify-between mb-3">
                    <h3 className="text-xl font-bold text-gray-900 line-clamp-1">
                      {template.name}
                    </h3>
                    <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                      v{template.version}
                    </span>
                  </div>
                  
                  <p className="text-gray-600 mb-4 line-clamp-3 text-sm">
                    {template.description}
                  </p>
                  
                  {/* Stats */}
                  <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                    <span>⭐ {template.rating?.toFixed(1) || '5.0'}</span>
                    <span>📦 {template.preview_data?.file_count || 0} files</span>
                    <span>{formatFileSize(template.preview_data?.download_size || 0)}</span>
                  </div>

                  {/* Tags */}
                  <div className="flex flex-wrap gap-1 mb-4">
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                      {template.category}
                    </span>
                    {template.tags?.slice(0, 2).map((tag, index) => (
                      <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                        {tag}
                      </span>
                    ))}
                  </div>

                  {/* Action Buttons */}
                  <div className="space-y-2">
                    <button
                      onClick={() => startCustomization(template)}
                      className="w-full bg-blue-600 text-white py-2.5 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center justify-center"
                    >
                      🚀 Customize & Generate
                    </button>
                    
                    <div className="grid grid-cols-2 gap-2">
                      <button
                        onClick={() => openDemoPreview(template)}
                        className="bg-purple-600 text-white py-2 px-3 rounded-lg text-sm font-medium hover:bg-purple-700 transition-colors"
                      >
                        👁️ Live Demo
                      </button>
                      <button
                        onClick={() => downloadTemplate(template)}
                        className="bg-green-600 text-white py-2 px-3 rounded-lg text-sm font-medium hover:bg-green-700 transition-colors"
                      >
                        📥 Download
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <div className="text-6xl mb-6">⏳</div>
            <h3 className="text-2xl font-semibold text-gray-900 mb-4">Templates are being generated...</h3>
            <p className="text-gray-600 mb-8 max-w-2xl mx-auto">
              Our SEVDO Integrator is creating complete web applications from templates. 
              This process may take a few minutes for each template.
            </p>
            <button
              onClick={loadGeneratedTemplates}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700"
            >
              🔄 Refresh Templates
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default RealTemplateGallery;