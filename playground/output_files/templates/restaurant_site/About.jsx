import React from 'react';
import { Link } from 'react-router-dom';

export default function Restaurant_SiteAboutPage() {
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
      <section className="relative bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 text-white min-h-screen flex items-center">
  <div className="absolute inset-0 bg-black opacity-20"></div>
  <div className="relative z-10 max-w-6xl mx-auto px-4 py-20 text-center">
    <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
      Our Story
    </h1>
    <h2 className="text-xl md:text-2xl font-light mb-8 text-blue-100 max-w-3xl mx-auto">
      Three generations of Italian tradition and passion for authentic cuisine
    </h2>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-semibold px-8 py-4 rounded-lg text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Meet Our Chef
      </Link>
    </div>

  </div>
  <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
    </svg>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <p>Bella Vista Ristorante opened its doors in 1985 when Giuseppe and Maria Rossini brought their family recipes from Naples to share with our community. Today, their grandson Marco continues the tradition, combining time-honored techniques with fresh, local ingredients.</p>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <p>Trained in the kitchens of Milan and inspired by his grandmother's cooking, Chef Marco brings authenticity and innovation to every dish. His commitment to traditional methods and seasonal ingredients has earned Bella Vista recognition as the city's premier Italian dining destination.</p>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Our Values</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">What guides us in everything we do</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <p>Winner of "Best Italian Restaurant" for three consecutive years. Featured in Food & Wine Magazine and recognized by the Italian Culinary Institute for authentic regional cuisine.</p>
      <section className="py-12 bg-gray-50">
  <div className="max-w-6xl mx-auto px-4">
    <div className="text-center mb-8">
      <h2 className="text-3xl font-bold text-gray-900">Guest Experiences</h2>
    </div>
    <div className="grid md:grid-cols-3 gap-8">
    <div className="bg-white p-6 rounded-lg shadow-md">
      <p className="text-gray-600 mb-4">"This product has transformed our workflow completely."</p>
      <div className="flex items-center">
        <div className="w-12 h-12 bg-gray-300 rounded-full mr-4"></div>
        <div>
          <h4 className="font-semibold text-gray-900">Sarah Johnson</h4>
          <p className="text-gray-600 text-sm">CEO, TechCorp</p>
        </div>
      </div>
    </div>
    <div className="bg-white p-6 rounded-lg shadow-md">
      <p className="text-gray-600 mb-4">"Amazing experience, highly recommended!"</p>
      <div className="flex items-center">
        <div className="w-12 h-12 bg-gray-300 rounded-full mr-4"></div>
        <div>
          <h4 className="font-semibold text-gray-900">Mike Chen</h4>
          <p className="text-gray-600 text-sm">Developer</p>
        </div>
      </div>
    </div>
    <div className="bg-white p-6 rounded-lg shadow-md">
      <p className="text-gray-600 mb-4">"The best tool I've used in years."</p>
      <div className="flex items-center">
        <div className="w-12 h-12 bg-gray-300 rounded-full mr-4"></div>
        <div>
          <h4 className="font-semibold text-gray-900">Anna Smith</h4>
          <p className="text-gray-600 text-sm">Designer</p>
        </div>
      </div>
    </div>
    </div>
  </div>
</section>
      <section className="py-20 bg-white">
  <div className="max-w-7xl mx-auto px-4">
    <div className="grid lg:grid-cols-2 gap-12 items-center">
      <div>
        <h2 className="text-4xl font-bold text-gray-900 mb-6">Ready to Transform Your Business?</h2>
        <p className="text-xl text-gray-600 mb-4">Join 10,000+ companies already using our platform</p>
        <p className="text-lg text-gray-600 mb-8">Start your free trial today. No credit card required. Cancel anytime.</p>
        
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
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <Link to="/blog" className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
            Start Free Trial
          </Link>
          <Link to="/contact" className="border-2 border-gray-300 text-gray-700 hover:bg-gray-100 font-semibold px-8 py-4 rounded-xl text-lg transition-all duration-300">
            Book a Demo
          </Link>
        </div>
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-200">
          <p className="text-gray-700 italic mb-3">"This platform increased our productivity by 300%"</p>
          <p className="text-gray-600 font-semibold">Sarah Chen, CEO at TechCorp</p>
        </div>
      </div>
      <div className="relative">
        <div className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-3xl p-8 text-white">
          <div className="text-center">
            <div className="text-6xl mb-4">🚀</div>
            <h3 className="text-2xl font-bold mb-4">Ready to Launch?</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div className="bg-white bg-opacity-20 rounded-lg p-3">
                <div className="font-bold text-2xl">10K+</div>
                <div>Happy Users</div>
              </div>
              <div className="bg-white bg-opacity-20 rounded-lg p-3">
                <div className="font-bold text-2xl">99.9%</div>
                <div>Uptime</div>
              </div>
              <div className="bg-white bg-opacity-20 rounded-lg p-3">
                <div className="font-bold text-2xl">24/7</div>
                <div>Support</div>
              </div>
              <div className="bg-white bg-opacity-20 rounded-lg p-3">
                <div className="font-bold text-2xl">5min</div>
                <div>Setup</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
    </>
  );
}
