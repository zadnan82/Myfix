import React from 'react';
import { Link } from 'react-router-dom';

export default function Blog_SiteAdminloginPage() {
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
      <form className="max-w-md mx-auto p-6">
  <h1 className="text-xl font-bold mb-4">Login to Your Account</h1>
  <div className="flex flex-col gap-4">
    <label className="block">
      <span className="mb-1 block">Username</span>
      <input id="lf-email" name="username" className="border rounded px-3 py-2 w-full" placeholder="Enter your username" />
    </label>
    <label className="block">
      <span className="mb-1 block">Password</span>
      <input id="lf-password" name="password" className="border rounded px-3 py-2 w-full" type="password" placeholder="Enter your password" />
    </label>
    <div className="flex flex-row gap-2 mt-4">
      <button type="button" className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded"
 onClick={(e) => {
   e.preventDefault();
   const username = document.getElementById('lf-email').value;
   const password = document.getElementById('lf-password').value;
   
   if (!username || !password) {
     alert('Please enter both username and password');
     return;
   }
   
   console.log('Attempting login...');
   
   fetch('/api/login', {
     method: 'POST',
     headers: {'Content-Type': 'application/json'},
     body: JSON.stringify({username: username, password: password, remember_me: false})
   })
   .then(response => {
     console.log('Response status:', response.status);
     return response.json();
   })
   .then(data => {
     console.log('Login response:', data);
     if (data.session_token) {
       localStorage.setItem('authToken', data.session_token);
       console.log('Token saved, redirecting to admin...');
       window.location.href = '/admin';
     } else {
       alert(data.detail || 'Login failed');
     }
   })
   .catch(error => {
     console.error('Login error:', error);
     alert('Login failed. Please try again.');
   });
 }}>Sign In</button>
      <button type="button" className="bg-gray-500 hover:bg-gray-600 text-white font-medium px-4 py-2 rounded">Forgot Password?</button>
    </div>
  </div>
</form>
    </>
  );
}
