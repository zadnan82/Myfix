import React from 'react';
import { Link } from 'react-router-dom';

export default function Personal_WebsiteProjectsPage() {
  return (
    <>
      <nav className="bg-white shadow-sm border-b border-gray-200">
  <div className="max-w-6xl mx-auto px-4">
    <div className="flex justify-between items-center py-4">
      <div className="flex items-center">
        <Link to="/" className="text-xl font-bold text-gray-800 hover:text-blue-600 transition-colors duration-200">Brand</Link>
      </div>
      <div className="hidden md:flex space-x-1">
        <Link to="/" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">Home</Link>
        <Link to="/about" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">About</Link>
        <Link to="/services" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">Services</Link>
        <Link to="/contact" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">Contact</Link>
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
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <p>Here are some of the projects I've worked on recently. Each one represents a unique challenge and solution.</p>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <p>A full-featured online store with payment processing, inventory management, and admin dashboard.</p>
      <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium rounded px-4 py-2 text-sm">View Demo</button>
      <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium rounded px-4 py-2 text-sm">Source Code</button>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <p>Collaborative project management tool with real-time updates, team chat, and progress tracking.</p>
      <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium rounded px-4 py-2 text-sm">View Demo</button>
      <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium rounded px-4 py-2 text-sm">Source Code</button>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <p>This very website! Built with modern web technologies and responsive design.</p>
      <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium rounded px-4 py-2 text-sm">View Demo</button>
      <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium rounded px-4 py-2 text-sm">Source Code</button>
    </>
  );
}
