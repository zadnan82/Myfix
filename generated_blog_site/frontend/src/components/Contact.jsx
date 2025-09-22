import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

export default function Contact() {
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
      <section className="py-8">
  <div className="mx-auto px-4 max-w-4xl">
    <div className="text-left">
      <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
        Get In Touch
      </h2>
      <p className="text-lg text-gray-600 leading-relaxed">
        Have a question, suggestion, or just want to say hello? I'd love to hear from you!
      </p>
    </div>
  </div>
</section>
      <section className="py-8">
  <div className="mx-auto px-4 max-w-4xl">
    <div className="text-left">
      <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
        Contact Information
      </h2>
      <p className="text-lg text-gray-600 leading-relaxed">
        Section content goes here.
      </p>
    </div>
  </div>
</section>
      <section className="py-8">
  <div className="mx-auto px-4 max-w-4xl">
    <div className="text-left">
      <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
        Section Title
      </h2>
      <p className="text-lg text-gray-600 leading-relaxed">
        📧 Email: alex@devinsights.com
      </p>
    </div>
  </div>
</section>
      <section className="py-8">
  <div className="mx-auto px-4 max-w-4xl">
    <div className="text-left">
      <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
        Section Title
      </h2>
      <p className="text-lg text-gray-600 leading-relaxed">
        📱 Twitter: @devinsights
      </p>
    </div>
  </div>
</section>
      <section className="py-8">
  <div className="mx-auto px-4 max-w-4xl">
    <div className="text-left">
      <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
        Section Title
      </h2>
      <p className="text-lg text-gray-600 leading-relaxed">
        💼 LinkedIn: /in/alex-developer
      </p>
    </div>
  </div>
</section>
      <section className="py-8">
  <div className="mx-auto px-4 max-w-4xl">
    <div className="text-left">
      <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
        Section Title
      </h2>
      <p className="text-lg text-gray-600 leading-relaxed">
        🌍 Location: San Francisco, CA
      </p>
    </div>
  </div>
</section>
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
    <h2 className="text-4xl md:text-5xl font-bold mb-6">Ready to Transform Your Business?</h2>
    <p className="text-xl text-blue-100 mb-4">Join 10,000+ companies already using our platform</p>
    <p className="text-lg text-blue-100 mb-8">Start your free trial today. No credit card required. Cancel anytime.</p>
    
        <div className="flex items-center justify-center space-x-6 mb-8 text-sm">
            <div className="flex items-center text-green-600">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                14-day free trial
            </div>
            <div className="flex items-center text-green-600">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                No credit card required
            </div>
            <div className="flex items-center text-green-600">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Cancel anytime
            </div>
        </div>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-8">
      <button className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Start Free Trial
      </button>
      <button className="border-2 border-white text-white hover:bg-white hover:text-blue-600 font-semibold px-8 py-4 rounded-xl text-lg transition-all duration-300">
        Book a Demo
      </button>
    </div>
    <div className="bg-white bg-opacity-10 rounded-2xl p-6 backdrop-blur-sm">
      <p className="text-blue-100 italic mb-3">"This platform increased our productivity by 300%"</p>
      <p className="text-blue-200 font-semibold">Sarah Chen, CEO at TechCorp</p>
    </div>
  </div>
</section>
    </>
  );
}
