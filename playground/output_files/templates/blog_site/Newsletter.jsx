import React from 'react';
import { Link } from 'react-router-dom';

export default function Blog_SiteNewsletterPage() {
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
      <section className="py-12 bg-gradient-to-br from-blue-50 to-indigo-100">
  <div className="max-w-2xl mx-auto px-4">
    <div className="bg-white rounded-2xl shadow-xl p-8">
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
          </svg>
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-4">Subscribe to DevInsights Newsletter</h2>
        <p className="text-lg text-gray-600">Get the latest articles and updates delivered directly to your inbox</p>
      </div>
      
      <form className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Email Address *</label>
          <input 
            id="ns-email"
            name="email"
            type="email" 
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
            placeholder="Enter your email address" 
            required 
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Name (Optional)</label>
          <input 
            id="ns-name"
            name="name"
            type="text" 
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
            placeholder="Enter your name (optional)" 
          />
        </div>
        
        <button 
          type="button" 
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl"
           onClick={(event) => {const emailInput = document.getElementById('ns-email');const nameInput = document.getElementById('ns-name');const email = emailInput.value.trim();const name = nameInput.value.trim();if (!email) { alert('Please enter your email address'); return; }const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;if (!emailRegex.test(email)) { alert('Please enter a valid email address'); return; }const formData = { email: email, name: name || null };const btn = event.target; btn.disabled = true; btn.textContent = 'Subscribing...';fetch('http://localhost:8000/api/newsletter', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(formData)}).then(response => response.json()).then(result => {console.log('Newsletter response:', result);if (result.msg || result.message) {alert(result.msg || result.message);if (result.status === 'subscribed' || result.status === 'reactivated') {emailInput.value = ''; nameInput.value = '';}}btn.disabled = false; btn.textContent = 'Subscribe';}).catch(error => {console.error('Newsletter error:', error);alert('Error: Could not subscribe. Please try again.');btn.disabled = false; btn.textContent = 'Subscribe';});}}
        >
          <div className="flex items-center justify-center">
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
            </svg>
            Subscribe
          </div>
        </button>
      </form>
      
      <div className="mt-6 text-center">
        <p className="text-sm text-gray-500 flex items-center justify-center">
          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
          </svg>
          We respect your privacy. Unsubscribe at any time.
        </p>
      </div>
      
      
      <div className="mt-8 pt-6 border-t border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">What you'll get:</h3>
        <div className="grid md:grid-cols-3 gap-4 text-center">
          <div className="flex flex-col items-center">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-2">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <p className="text-sm font-medium text-gray-700">Latest Articles</p>
          </div>
          <div className="flex flex-col items-center">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-2">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
            </div>
            <p className="text-sm font-medium text-gray-700">Exclusive Tips</p>
          </div>
          <div className="flex flex-col items-center">
            <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-2">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <p className="text-sm font-medium text-gray-700">Weekly Updates</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
      <section className="py-8">
  <div className="mx-auto px-4 max-w-4xl">
    <div className="text-left">
      <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
        What Our Subscribers Say
      </h2>
      <p className="text-lg text-gray-600 leading-relaxed">
        Join thousands of developers who rely on our newsletter for the latest trends and best practices in web development.
      </p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Newsletter Benefits</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Everything you need to stay ahead in web development</p>
    </div>
  </div>
</section>
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
  <div className="max-w-4xl mx-auto px-4 text-center">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">Ready to Level Up?</h2>
    <p className="text-xl text-blue-100 mb-8">Don't miss out on exclusive content and early access to new tutorials</p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Subscribe Today
      </Link>
    </div>
  </div>
</section>
    </>
  );
}
