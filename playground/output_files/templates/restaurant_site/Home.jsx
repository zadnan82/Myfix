import React from 'react';
import { Link } from 'react-router-dom';

export default function Restaurant_SiteHomePage() {
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
      Bella Vista Ristorante
    </h1>
    <h2 className="text-xl md:text-2xl font-light mb-8 text-blue-100 max-w-3xl mx-auto">
      Authentic Italian cuisine in the heart of the city since 1985
    </h2>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-semibold px-8 py-4 rounded-lg text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        View Our Menu
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
      <p>Handcrafted dishes made with the finest imported ingredients</p>
      <div className="relative bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200">
    
        <div className="absolute top-3 right-3">
            <span className="bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full">Popular</span>
        </div>
    <div className="flex flex-col md:flex-row">
        
        <div className="flex-1">
            
            <div className="flex justify-between items-start mb-2">
                <h3 className="text-lg font-semibold text-gray-900">Osso Buco Milanese</h3>
                <span className="text-lg font-bold text-red-600 ml-4">$32.95</span>
            </div>
            <p className="text-gray-600 text-sm leading-relaxed">Fresh Atlantic salmon grilled to perfection, served with seasonal vegetables and lemon butter sauce</p>
        </div>
    </div>
</div>
      <div className="relative bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200">
    
    <div className="flex flex-col md:flex-row">
        
        <div className="flex-1">
            
            <div className="flex justify-between items-start mb-2">
                <h3 className="text-lg font-semibold text-gray-900">Homemade Truffle Ravioli</h3>
                <span className="text-lg font-bold text-red-600 ml-4">$28.95</span>
            </div>
            <p className="text-gray-600 text-sm leading-relaxed">Fresh Atlantic salmon grilled to perfection, served with seasonal vegetables and lemon butter sauce</p>
        </div>
    </div>
</div>
      <div className="relative bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200">
    
    <div className="flex flex-col md:flex-row">
        
        <div className="flex-1">
            
            <div className="flex justify-between items-start mb-2">
                <h3 className="text-lg font-semibold text-gray-900">Grilled Branzino</h3>
                <span className="text-lg font-bold text-red-600 ml-4">$29.95</span>
            </div>
            <p className="text-gray-600 text-sm leading-relaxed">Fresh Atlantic salmon grilled to perfection, served with seasonal vegetables and lemon butter sauce</p>
        </div>
    </div>
</div>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Why Choose Bella Vista</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Experience that sets us apart from the rest</p>
    </div>
  </div>
</section>
      <section className="py-12 bg-gray-50">
  <div className="max-w-6xl mx-auto px-4">
    <div className="text-center mb-8">
      <h2 className="text-3xl font-bold text-gray-900">What Our Guests Say</h2>
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
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <div className="bg-white border border-gray-200 rounded-lg p-6">
    <h3 className="text-xl font-bold text-gray-900 mb-4">Hours of Operation</h3>
    
    
    <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
        <div className="flex items-center">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
            <span className="font-semibold text-green-900">Currently Open</span>
            <span className="text-green-700 ml-2">• Closes at 11:00 PM</span>
        </div>
    </div>
    
    <div className="space-y-3">
        
        <div className="bg-white border-gray-200 border rounded-lg p-4 flex justify-between items-center">
            <span className="font-medium text-gray-900">Monday</span>
            <span className="text-gray-700 font-medium">11:00 AM - 10:00 PM</span>
        </div>
        <div className="bg-white border-gray-200 border rounded-lg p-4 flex justify-between items-center">
            <span className="font-medium text-gray-900">Tuesday</span>
            <span className="text-gray-700 font-medium">11:00 AM - 10:00 PM</span>
        </div>
        <div className="bg-white border-gray-200 border rounded-lg p-4 flex justify-between items-center">
            <span className="font-medium text-gray-900">Wednesday</span>
            <span className="text-gray-700 font-medium">11:00 AM - 10:00 PM</span>
        </div>
        <div className="bg-white border-gray-200 border rounded-lg p-4 flex justify-between items-center">
            <span className="font-medium text-gray-900">Thursday</span>
            <span className="text-gray-700 font-medium">11:00 AM - 10:00 PM</span>
        </div>
        <div className="bg-blue-50 border-blue-200 border rounded-lg p-4 flex justify-between items-center">
            <span className="font-semibold text-blue-900">Friday</span>
            <span className="text-gray-700 font-medium">11:00 AM - 11:00 PM</span>
        </div>
        <div className="bg-white border-gray-200 border rounded-lg p-4 flex justify-between items-center">
            <span className="font-medium text-gray-900">Saturday</span>
            <span className="text-gray-700 font-medium">10:00 AM - 11:00 PM</span>
        </div>
        <div className="bg-white border-gray-200 border rounded-lg p-4 flex justify-between items-center">
            <span className="font-medium text-gray-900">Sunday</span>
            <span className="text-gray-700 font-medium">10:00 AM - 9:00 PM</span>
        </div>
    </div>
    
    <div className="mt-6 pt-4 border-t border-gray-200">
        <p className="text-sm text-gray-600 flex items-center">
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            All times are in EST
        </p>
        <p className="text-sm text-gray-600 mt-2">
            Kitchen closes 30 minutes before closing time
        </p>
    </div>
    
    
</div>
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
  <div className="max-w-4xl mx-auto px-4 text-center">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">Reserve Your Table</h2>
    <p className="text-xl text-blue-100 mb-8">Join us for an unforgettable dining experience</p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Make Reservation
      </Link>
    </div>
  </div>
</section>
    </>
  );
}
