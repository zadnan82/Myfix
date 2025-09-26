import React from 'react';
import { Link } from 'react-router-dom';

export default function Blog_SiteAdminPage() {
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
  <header className="bg-white shadow-sm border-b">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex justify-between items-center py-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="text-sm text-gray-500">Welcome back, Admin</p>
        </div>
        <div className="flex items-center space-x-4">
          <button 
            onClick={() => window.location.href = '/admin/editor'}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors flex items-center space-x-2"
          >
            <span>➕</span>
            <span>New Post</span>
          </button>
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
            <span>System Online</span>
          </div>
        </div>
      </div>
    </div>
  </header>

  <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
              <span className="text-blue-600 text-sm">📝</span>
            </div>
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-500">Total Posts</p>
            <p className="text-2xl font-bold text-gray-900" id="total-posts">Loading...</p>
          </div>
        </div>
      </div>
      
      <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
              <span className="text-green-600 text-sm">✅</span>
            </div>
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-500">Published</p>
            <p className="text-2xl font-bold text-gray-900" id="published-posts">Loading...</p>
          </div>
        </div>
      </div>
      
      <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
              <span className="text-yellow-600 text-sm">📄</span>
            </div>
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-500">Drafts</p>
            <p className="text-2xl font-bold text-gray-900" id="draft-posts">Loading...</p>
          </div>
        </div>
      </div>
      
      <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
              <span className="text-purple-600 text-sm">🏷️</span>
            </div>
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-500">Total Tags</p>
            <p className="text-2xl font-bold text-gray-900" id="total-tags">Loading...</p>
          </div>
        </div>
      </div>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div className="lg:col-span-2">
        <div className="bg-white rounded-xl shadow-sm border border-gray-100">
          <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Recent Posts</h2>
            <button 
              onClick={() => window.location.href = '/admin/posts'}
              className="text-sm text-blue-600 hover:text-blue-700"
            >
              View All
            </button>
          </div>
          <div className="p-6">
            <div id="recent-posts" className="space-y-4">
              <div className="text-center py-8 text-gray-500">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
                Loading recent posts...
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="lg:col-span-1">
        <div className="bg-white rounded-xl shadow-sm border border-gray-100">
          <div className="px-6 py-4 border-b border-gray-100">
            <h2 className="text-lg font-semibold text-gray-900">Quick Actions</h2>
          </div>
          <div className="p-6 space-y-4">
            <button 
              onClick={() => window.location.href = '/admin/editor'}
              className="w-full bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 px-4 py-3 rounded-lg transition-colors flex items-center space-x-3"
            >
              <span>✏️</span>
              <span>Create New Post</span>
            </button>
            
            <button 
              onClick={() => window.location.href = '/admin/posts?published=false'}
              className="w-full bg-yellow-50 hover:bg-yellow-100 text-yellow-700 border border-yellow-200 px-4 py-3 rounded-lg transition-colors flex items-center space-x-3"
            >
              <span>📄</span>
              <span>View Drafts</span>
            </button>
            
            <button 
              onClick={() => window.location.href = '/admin/tags'}
              className="w-full bg-purple-50 hover:bg-purple-100 text-purple-700 border border-purple-200 px-4 py-3 rounded-lg transition-colors flex items-center space-x-3"
            >
              <span>🏷️</span>
              <span>Manage Tags</span>
            </button>
            
            <button 
              onClick={() => window.location.href = '/admin/settings'}
              className="w-full bg-gray-50 hover:bg-gray-100 text-gray-700 border border-gray-200 px-4 py-3 rounded-lg transition-colors flex items-center space-x-3"
            >
              <span>⚙️</span>
              <span>Settings</span>
            </button>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-100 mt-6">
          <div className="px-6 py-4 border-b border-gray-100">
            <h2 className="text-lg font-semibold text-gray-900">System Status</h2>
          </div>
          <div className="p-6 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Database</span>
              <div className="flex items-center space-x-2">
                <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                <span className="text-sm text-green-600">Online</span>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">API Server</span>
              <div className="flex items-center space-x-2">
                <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                <span className="text-sm text-green-600">Running</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <img 
    src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=" 
    className="hidden"
    onLoad={() => {
      // Simple data loading without complex JavaScript
      fetch('/api/admin/blog/posts?limit=5')
        .then(response => response.json())
        .then(data => {
          const totalElement = document.getElementById('total-posts');
          const publishedElement = document.getElementById('published-posts');
          const draftElement = document.getElementById('draft-posts');
          
          if (totalElement && data.total !== undefined) {
            totalElement.textContent = data.total;
          }
          
          if (data.posts && Array.isArray(data.posts)) {
            const published = data.posts.filter(p => p.published).length;
            const drafts = data.posts.filter(p => !p.published).length;
            
            if (publishedElement) publishedElement.textContent = published;
            if (draftElement) draftElement.textContent = drafts;
          }
        })
        .catch(error => {
          console.log('Dashboard data load failed:', error);
        });
    }}
    alt=""
  />
</div>
    </>
  );
}
