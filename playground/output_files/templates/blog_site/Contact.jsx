import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';

export default function Blog_SiteContactPage() {
  const navigate = useNavigate();

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
      <section className="py-12 bg-gray-50">
  <div className="max-w-2xl mx-auto px-4">
    <div className="text-center mb-8">
      <h2 className="text-3xl font-bold text-gray-900 mb-4">Send Me a Message</h2>
      <p className="text-gray-600">We'd love to hear from you. Send us a message and we'll respond as soon as possible.</p>
    </div>
    
    <form className="bg-white rounded-lg shadow-md p-8">
      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
          <input 
            id="cf-name"
            name="name"
            type="text" 
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter your full name" 
            required 
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
          <input 
            id="cf-email"
            name="email"
            type="email" 
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter your email address" 
            required 
          />
        </div>
      </div>
      
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">Subject</label>
        <input 
          id="cf-subject"
          name="subject"
          type="text" 
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="What is this about?" 
          required 
        />
      </div>
      
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">Message</label>
        <textarea 
          id="cf-message"
          name="message"
          rows="5" 
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-vertical"
          placeholder="Tell us more about your inquiry..." 
          required
        ></textarea>
      </div>
      
      <button 
        type="button" 
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-md transition-colors duration-200"
         onClick={(event) => {const formData = {name: document.getElementById('cf-name').value, email: document.getElementById('cf-email').value, subject: document.getElementById('cf-subject').value, message: document.getElementById('cf-message').value}; const btn = event.target; btn.disabled = true; btn.textContent = 'Sending...';fetch('http://localhost:8000/api/contact', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(formData)}).then(response => response.json()).then(result => {console.log('Contact form response:', result); if (result.msg || result.message) {alert(result.msg || result.message); setTimeout(() => { navigate('/'); }, 2000);} btn.disabled = false; btn.textContent = 'Send Message';}).catch(error => {console.error('Contact form error:', error); alert('Error: Could not send message. Please try again.'); btn.disabled = false; btn.textContent = 'Send Message';});}}
      >
        Send Message
      </button>
    </form>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Get In Touch</h2>
      <p className="text-xl text-gray-600 max-w-2xl mx-auto">Have a question, suggestion, or just want to say hello? I'd love to hear from you!</p>
    </div>

    <div className="max-w-3xl mx-auto">
      <div className="bg-white shadow-lg rounded-xl p-8 md:p-10">

        <div className="mb-8">
          <h3 className="text-2xl font-semibold text-gray-900 mb-3">Contact Information</h3>
          <p className="text-gray-600">Section content goes here.</p>
        </div>

        <div className="grid gap-6 md:grid-cols-1">

          <div className="flex items-center space-x-4 p-4 rounded-lg hover:bg-gray-50 transition-colors duration-200">
            <div className="flex-shrink-0">
              <span className="text-2xl" role="img" aria-label="Email">📧</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 mb-1">Email</p>
              <a className="text-lg text-gray-900 hover:text-blue-600 transition-colors duration-200 font-medium" href="mailto:john@company.com">
                john@company.com
              </a>
            </div>
          </div>

          <div className="flex items-center space-x-4 p-4 rounded-lg hover:bg-gray-50 transition-colors duration-200">
            <div className="flex-shrink-0">
              <span className="text-2xl" role="img" aria-label="Twitter">🐦</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 mb-1">Twitter</p>
              <a className="text-lg text-gray-900 hover:text-blue-600 transition-colors duration-200 font-medium" href="https://twitter.com/johnsmith" target="_blank" rel="noopener noreferrer">
                @johnsmith
              </a>
            </div>
          </div>

          <div className="flex items-center space-x-4 p-4 rounded-lg hover:bg-gray-50 transition-colors duration-200">
            <div className="flex-shrink-0">
              <span className="text-2xl" role="img" aria-label="LinkedIn">💼</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 mb-1">LinkedIn</p>
              <a className="text-lg text-gray-900 hover:text-blue-600 transition-colors duration-200 font-medium" href="https://linkedin.com/in/johnsmith" target="_blank" rel="noopener noreferrer">
                /in/johnsmith
              </a>
            </div>
          </div>

          <div className="flex items-center space-x-4 p-4 rounded-lg hover:bg-gray-50 transition-colors duration-200">
            <div className="flex-shrink-0">
              <span className="text-2xl" role="img" aria-label="Location">🌍</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 mb-1">Location</p>
              <span className="text-lg text-gray-900 font-medium">
                New York
              </span>
            </div>
          </div>

        </div>

      </div>
    </div>
  </div>
</section>
      <section className="py-12 bg-white">
  <div className="max-w-3xl mx-auto px-4">
    <h2 className="text-3xl font-bold text-gray-900 mb-8">Frequently Asked Questions</h2>
  </div>
</section>
      <section className="py-8">
  <div className="mx-auto px-4 max-w-4xl">
    <div className="text-left">
      <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
        💬 How often do you publish new articles?
      </h2>
      <p className="text-lg text-gray-600 leading-relaxed">
        I aim to publish 2-3 new articles every week, usually on Tuesdays and Fridays.
      </p>
    </div>
  </div>
</section>
      <section className="py-8">
  <div className="mx-auto px-4 max-w-4xl">
    <div className="text-left">
      <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
        🎯 Can you write about specific topics?
      </h2>
      <p className="text-lg text-gray-600 leading-relaxed">
        Absolutely! I love suggestions from readers. Send me your ideas and I'll consider them for future posts.
      </p>
    </div>
  </div>
</section>
      <section className="py-8">
  <div className="mx-auto px-4 max-w-4xl">
    <div className="text-left">
      <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
        🤝 Are you available for consulting or collaboration?
      </h2>
      <p className="text-lg text-gray-600 leading-relaxed">
        Yes, I'm open to discussing freelance projects and collaborations. Use the contact form above to get in touch.
      </p>
    </div>
  </div>
</section>
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
  <div className="max-w-4xl mx-auto px-4 text-center">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">Stay Connected</h2>
    <p className="text-xl text-blue-100 mb-8">Join the community and never miss an update</p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Subscribe to Newsletter
      </Link>
    </div>
  </div>
</section>
    </>
  );
}
