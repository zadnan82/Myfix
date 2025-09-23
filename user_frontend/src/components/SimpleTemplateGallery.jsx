// user_frontend/src/components/SimpleTemplateGallery.jsx

import React, { useState, useEffect } from 'react';
import { apiClient } from '../services/api';

const SimpleTemplateGallery = () => {
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [showCustomizer, setShowCustomizer] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [customizations, setCustomizations] = useState({
    project_name: '',
    company_name: '',
    primary_color: '#3b82f6'
  });

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/api/v1/templates/generated');
      setTemplates(response);
    } catch (error) {
      console.error('Failed to load templates:', error);
      setTemplates([]);
    } finally {
      setLoading(false);
    }
  };

  const openDemo = (template) => {
    const demoUrl = `${apiClient.baseURL}/api/v1/templates/${template.id}/demo`;
    window.open(demoUrl, '_blank', 'width=1200,height=800');
  };

  const startCustomization = (template) => {
    setSelectedTemplate(template);
    setShowCustomizer(true);
    setCustomizations({
      ...customizations,
      project_name: `My ${template.name}`
    });
  };

  const generateTemplate = async () => {
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
          customizations: customizations
        }
      );

      alert(`🎉 Success!\n\n${response.message}\n\nFiles generated: ${response.files_count}`);
      
      // Auto-download
      downloadTemplate();

    } catch (error) {
      console.error('Generation failed:', error);
      alert(`❌ Generation failed: ${error.response?.data?.detail || error.message}`);
    } finally {
      setGenerating(false);
    }
  };

  const downloadTemplate = async () => {
    if (!selectedTemplate) return;
    
    try {
      const downloadUrl = `${apiClient.baseURL}/api/v1/templates/${selectedTemplate.id}/download`;
      
      const response = await fetch(downloadUrl, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
        }
      });
      
      if (!response.ok) throw new Error('Download failed');
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${selectedTemplate.name}-webapp.zip`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
    } catch (error) {
      console.error('Download failed:', error);
      alert('Download failed: ' + error.message);
    }
  };

  const formatSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <h3 className="text-xl font-semibold">Loading Templates...</h3>
          <p className="text-gray-600 mt-2">Preparing your website templates</p>
        </div>
      </div>
    );
  }

  if (showCustomizer && selectedTemplate) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4">
          <button
            onClick={() => setShowCustomizer(false)}
            className="text-blue-600 hover:text-blue-800 mb-6"
          >
            ← Back to Templates
          </button>

          <div className="bg-white rounded-lg shadow-lg p-8">
            <h1 className="text-3xl font-bold mb-2">{selectedTemplate.name}</h1>
            <p className="text-gray-600 mb-8">{selectedTemplate.description}</p>

            <div className="grid md:grid-cols-2 gap-8">
              {/* Customization Form */}
              <div>
                <h2 className="text-xl font-semibold mb-4">Customize Your Website</h2>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Project Name *</label>
                    <input
                      type="text"
                      value={customizations.project_name}
                      onChange={(e) => setCustomizations({
                        ...customizations, 
                        project_name: e.target.value
                      })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="My Awesome Website"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">Company Name</label>
                    <input
                      type="text"
                      value={customizations.company_name}
                      onChange={(e) => setCustomizations({
                        ...customizations, 
                        company_name: e.target.value
                      })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Your Company"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">Primary Color</label>
                    <input
                      type="color"
                      value={customizations.primary_color}
                      onChange={(e) => setCustomizations({
                        ...customizations, 
                        primary_color: e.target.value
                      })}
                      className="w-full h-10 rounded border border-gray-300"
                    />
                  </div>
                </div>

                <div className="mt-8 space-y-3">
                  <button
                    onClick={generateTemplate}
                    disabled={generating || !customizations.project_name.trim()}
                    className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 flex items-center justify-center"
                  >
                    {generating ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                        Generating...
                      </>
                    ) : (
                      '🚀 Generate My Website'
                    )}
                  </button>

                  <button
                    onClick={downloadTemplate}
                    className="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700"
                  >
                    📥 Download Original Template
                  </button>

                  <button
                    onClick={() => openDemo(selectedTemplate)}
                    className="w-full bg-purple-600 text-white py-2 px-4 rounded-lg hover:bg-purple-700"
                  >
                    👁️ View Demo
                  </button>
                </div>
              </div>

              {/* Preview */}
              <div>
                <h2 className="text-xl font-semibold mb-4">Template Preview</h2>
                <div className="border rounded-lg overflow-hidden" style={{ height: '400px' }}>
                  <iframe
                    src={`${apiClient.baseURL}/api/v1/templates/${selectedTemplate.id}/demo`}
                    className="w-full h-full"
                    title="Template Preview"
                  />
                </div>
                
                <div className="mt-4 text-sm text-gray-600">
                  <div className="flex justify-between">
                    <span>Files: {selectedTemplate.file_count}</span>
                    <span>Size: {formatSize(selectedTemplate.download_size)}</span>
                  </div>
                  <div className="flex justify-between mt-1">
                    <span>Frontend: {selectedTemplate.has_frontend ? '✅' : '❌'}</span>
                    <span>Backend: {selectedTemplate.has_backend ? '✅' : '❌'}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Ready-to-Deploy Websites
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Professional websites generated with SEVDO. Complete with React frontend, 
            FastAPI backend, and Docker deployment - ready in minutes.
          </p>
        </div>

        {/* Templates Grid */}
        {templates.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {templates.map((template) => (
              <div key={template.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300">
                {/* Template Icon */}
                <div className="h-48 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 flex items-center justify-center">
                  <div className="text-white text-6xl">
                    {template.category === 'restaurant' && '🍽️'}
                    {template.category === 'business' && '💼'}
                    {template.category === 'ecommerce' && '🛒'}
                    {template.category === 'portfolio' && '🎨'}
                    {template.category === 'blog' && '📝'}
                    {!['restaurant', 'business', 'ecommerce', 'portfolio', 'blog'].includes(template.category) && '🌐'}
                  </div>
                  
                  {template.is_featured && (
                    <div className="absolute top-3 left-3">
                      <span className="bg-yellow-400 text-yellow-900 px-2 py-1 rounded-full text-xs font-medium">
                        ⭐ Featured
                      </span>
                    </div>
                  )}
                </div>

                {/* Template Info */}
                <div className="p-6">
                  <h3 className="text-xl font-bold text-gray-900 mb-2">
                    {template.name}
                  </h3>
                  <p className="text-gray-600 mb-4 text-sm line-clamp-3">
                    {template.description}
                  </p>

                  {/* Stats */}
                  <div className="flex justify-between text-sm text-gray-500 mb-4">
                    <span>📁 {template.file_count} files</span>
                    <span>{formatSize(template.download_size)}</span>
                  </div>

                  {/* Features */}
                  <div className="flex justify-between items-center mb-4">
                    {template.has_frontend && (
                      <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs">
                        ✅ Frontend
                      </span>
                    )}
                    {template.has_backend && (
                      <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                        ✅ Backend
                      </span>
                    )}
                  </div>

                  {/* Action Buttons */}
                  <div className="space-y-2">
                    <button
                      onClick={() => startCustomization(template)}
                      className="w-full bg-blue-600 text-white py-2.5 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors"
                    >
                      🚀 Customize & Generate
                    </button>
                    
                    <div className="grid grid-cols-2 gap-2">
                      <button
                        onClick={() => openDemo(template)}
                        className="bg-purple-600 text-white py-2 px-3 rounded-lg text-sm hover:bg-purple-700"
                      >
                        👁️ Demo
                      </button>
                      <button
                        onClick={() => downloadTemplate(template)}
                        className="bg-green-600 text-white py-2 px-3 rounded-lg text-sm hover:bg-green-700"
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
            <h3 className="text-2xl font-semibold text-gray-900 mb-4">
              Templates are being generated...
            </h3>
            <p className="text-gray-600 mb-8 max-w-2xl mx-auto">
              Our SEVDO Integrator is creating complete web applications from templates. 
              This process may take a few minutes.
            </p>
            <div className="space-y-3">
              <button
                onClick={loadTemplates}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700"
              >
                🔄 Check Progress
              </button>
              <div>
                <button
                  onClick={() => window.open(`${apiClient.baseURL}/api/v1/templates/generation-status`, '_blank')}
                  className="text-blue-600 hover:text-blue-800 text-sm"
                >
                  View Generation Status →
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SimpleTemplateGallery;