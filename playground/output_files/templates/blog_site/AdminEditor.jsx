import React from 'react';
import { Link } from 'react-router-dom';

export default function Blog_SiteAdmineditorPage() {
  return (
    <>
      <nav className="bg-white shadow-sm border-b border-gray-200">
  <div className="max-w-6xl mx-auto px-4">
    <div className="flex justify-between items-center py-4">
      <div className="flex items-center">
        <Link to="/" className="text-xl font-bold text-gray-800 hover:text-blue-600 transition-colors duration-200">DevInsights</Link>
      </div>
      <div className="hidden md:flex space-x-1">
        <Link to="/" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">Home</Link>
        <Link to="/blog" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">Blog</Link>
        <Link to="/about" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">About</Link>
        <Link to="/contact" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">Contact</Link>
        <Link to="/admin" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">Admin</Link>
      </div>
      <div className="md:hidden">
        <button className="text-gray-700 hover:text-blue-600 focus:outline-none">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
        </button>
      </div>
    </div>
  </div>
</nav>
      <div className="min-h-screen bg-gray-50">
  <header className="bg-white shadow-sm border-b sticky top-0 z-10">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex justify-between items-center py-4">
        <div className="flex items-center space-x-4">
          <button 
            onClick={() => window.location.href = '/admin'}
            className="text-gray-500 hover:text-gray-700 p-2 rounded-lg hover:bg-gray-100"
            title="Back to dashboard"
          >
            ←
          </button>
          <div>
            <h1 className="text-xl font-bold text-gray-900">Create New Post</h1>
            <p className="text-sm text-gray-500" id="post-status">Ready to edit</p>
          </div>
        </div>
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <span id="word-count">0 words</span>
            <span>•</span>
            <span id="read-time">0 min read</span>
          </div>
          <button 
            id="save-draft-btn"
            className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            onClick={() => {
              const title = document.getElementById('post-title').value.trim();
              if (!title) {
                alert('Please enter a post title');
                return;
              }
              const postData = {
                title: title,
                content: document.getElementById('post-content').value,
                excerpt: document.getElementById('post-excerpt').value || null,
                featured_image: document.getElementById('featured-image').value || null,
                published: false,
                tags: []
              };
              fetch('/api/admin/blog/posts', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(postData)
              }).then(response => response.json()).then(data => {
                document.getElementById('post-status').textContent = 'Draft saved successfully!';
              }).catch(error => {
                document.getElementById('post-status').textContent = 'Failed to save draft';
              });
            }}
          >
            Save Draft
          </button>
          <button 
            id="publish-btn"
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            onClick={() => {
              const title = document.getElementById('post-title').value.trim();
              if (!title) {
                alert('Please enter a post title');
                return;
              }
              const postData = {
                title: title,
                content: document.getElementById('post-content').value,
                excerpt: document.getElementById('post-excerpt').value || null,
                featured_image: document.getElementById('featured-image').value || null,
                published: true,
                tags: []
              };
              fetch('/api/admin/blog/posts', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(postData)
              }).then(response => response.json()).then(data => {
                document.getElementById('post-status').textContent = 'Post published successfully!';
              }).catch(error => {
                document.getElementById('post-status').textContent = 'Failed to publish post';
              });
            }}
          >
            Publish
          </button>
        </div>
      </div>
    </div>
  </header>

  <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
      <div className="lg:col-span-3">
        <div className="bg-white rounded-xl shadow-sm border border-gray-100">
          <div className="p-6 space-y-6">
            <div>
              <input
                type="text"
                id="post-title"
                placeholder="Enter your post title..."
                className="w-full text-3xl font-bold border-none outline-none resize-none placeholder-gray-400 focus:ring-0 p-0"
                onInput={() => {
                  const title = document.getElementById('post-title').value;
                  const content = document.getElementById('post-content').value;
                  const words = content.trim() ? content.trim().split(/\s+/).length : 0;
                  const readTime = Math.max(1, Math.round(words / 225));
                  
                  document.getElementById('word-count').textContent = words + ' words';
                  document.getElementById('read-time').textContent = readTime + ' min read';
                  
                  if (title) {
                    const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
                    document.getElementById('slug-preview').textContent = slug || 'your-post-title';
                  }
                }}
              />
            </div>
            
            <div className="flex items-center space-x-2 text-sm text-gray-500 border-t pt-4">
              <span>URL:</span>
              <code id="slug-preview" className="bg-gray-100 px-2 py-1 rounded text-xs">your-post-title</code>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">Content</label>
              <textarea
                id="post-content"
                placeholder="Write your post content here..."
                className="w-full h-96 border border-gray-300 rounded-lg p-4 resize-y focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                onInput={() => {
                  const content = document.getElementById('post-content').value;
                  const words = content.trim() ? content.trim().split(/\s+/).length : 0;
                  const readTime = Math.max(1, Math.round(words / 225));
                  
                  document.getElementById('word-count').textContent = words + ' words';
                  document.getElementById('read-time').textContent = readTime + ' min read';
                }}
              ></textarea>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">Excerpt (Optional)</label>
              <textarea
                id="post-excerpt"
                placeholder="Brief description of your post..."
                className="w-full h-24 border border-gray-300 rounded-lg p-4 resize-y focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              ></textarea>
            </div>
          </div>
        </div>
      </div>

      <div className="lg:col-span-1">
        <div className="space-y-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Publication</h3>
            
            <div className="space-y-4">
              <div>
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="post-published"
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="text-sm text-gray-700">Publish immediately</span>
                </label>
              </div>
              
              <div className="text-sm text-gray-500">
                <div className="flex justify-between">
                  <span>Created:</span>
                  <span id="created-date">-</span>
                </div>
                <div className="flex justify-between mt-1">
                  <span>Modified:</span>
                  <span id="modified-date">-</span>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Featured Image</h3>
            
            <div className="space-y-4">
              <div>
                <input
                  type="url"
                  id="featured-image"
                  placeholder="Image URL..."
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  onInput={() => {
                    const url = document.getElementById('featured-image').value;
                    const preview = document.getElementById('image-preview');
                    const img = preview.querySelector('img');
                    
                    if (url) {
                      img.src = url;
                      img.onload = () => preview.classList.remove('hidden');
                      img.onerror = () => preview.classList.add('hidden');
                    } else {
                      preview.classList.add('hidden');
                    }
                  }}
                />
              </div>
              <div id="image-preview" className="hidden">
                <img className="w-full h-32 object-cover rounded-lg border" alt="Featured image preview" />
              </div>
              <p className="text-xs text-gray-500">Recommended size: 1200x630px</p>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Actions</h3>
            
            <div className="space-y-3">
              <button 
                onClick={() => {
                  const title = document.getElementById('post-title').value;
                  const content = document.getElementById('post-content').value;
                  
                  if (!title || !content) {
                    alert('Please add title and content to preview');
                    return;
                  }
                  
                  const previewWindow = window.open('', '_blank');
                  previewWindow.document.write('<html><head><title>Preview: ' + title + '</title><meta charset="utf-8"><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-gray-50"><div class="max-w-4xl mx-auto py-8 px-4"><article class="bg-white rounded-xl shadow-sm p-8"><h1 class="text-4xl font-bold text-gray-900 mb-6">' + title + '</h1><div class="prose max-w-none">' + content.replace(/\n/g, '<br>') + '</div></article></div></body></html>');
                }}
                className="w-full bg-gray-50 hover:bg-gray-100 text-gray-700 border border-gray-200 px-4 py-2 rounded-lg transition-colors flex items-center justify-center space-x-2"
              >
                <span>👁️</span>
                <span>Preview</span>
              </button>
              
              <button 
                onClick={() => window.location.href = '/admin'}
                className="w-full bg-gray-50 hover:bg-gray-100 text-gray-700 border border-gray-200 px-4 py-2 rounded-lg transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</div>
    </>
  );
}
