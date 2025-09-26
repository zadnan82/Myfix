import React from 'react';
import { Link } from 'react-router-dom';

export default function Fitness_SiteClassesPage() {
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
      <p>Choose from our wide variety of expert-led group fitness classes designed for all fitness levels</p>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <p>Weekly schedule - book your spot today</p>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex justify-between items-start mb-4">
    <div>
      <h3 className="text-xl font-bold text-gray-900 mb-2">HIIT Intensity</h3>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
        Intermediate
      </span>
    </div>
    <div className="text-right">
      <div className="text-sm text-gray-500">Available Spots</div>
      <div className="text-lg font-bold text-blue-600">12</div>
    </div>
  </div>
  
  <div className="space-y-3 mb-4">
    <div className="flex items-center text-sm text-gray-600">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      Mon/Wed/Fri 6:00 AM • 45 minutes
    </div>
    
    <div className="flex items-center text-sm text-gray-600">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
      </svg>
      Instructor: Sarah Johnson
    </div>
    
    
        <div className="flex items-center text-sm text-gray-600 mb-2">
            <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.781 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 9.172V5L8 4z"></path>
            </svg>
            Equipment: [kettlebells
        </div>
  </div>
  
  <p className="text-gray-600 text-sm mb-4">High-intensity interval training for maximum calorie burn</p>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
    Book Class
  </button>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex justify-between items-start mb-4">
    <div>
      <h3 className="text-xl font-bold text-gray-900 mb-2">Strength & Conditioning</h3>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
        All Levels
      </span>
    </div>
    <div className="text-right">
      <div className="text-sm text-gray-500">Available Spots</div>
      <div className="text-lg font-bold text-blue-600">8</div>
    </div>
  </div>
  
  <div className="space-y-3 mb-4">
    <div className="flex items-center text-sm text-gray-600">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      Mon/Wed/Fri 7:30 AM • 60 minutes
    </div>
    
    <div className="flex items-center text-sm text-gray-600">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
      </svg>
      Instructor: Mike Rodriguez
    </div>
    
    
        <div className="flex items-center text-sm text-gray-600 mb-2">
            <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.781 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 9.172V5L8 4z"></path>
            </svg>
            Equipment: [barbells
        </div>
  </div>
  
  <p className="text-gray-600 text-sm mb-4">Build lean muscle and increase overall strength</p>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
    Book Class
  </button>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex justify-between items-start mb-4">
    <div>
      <h3 className="text-xl font-bold text-gray-900 mb-2">Power Yoga Flow</h3>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
        Beginner
      </span>
    </div>
    <div className="text-right">
      <div className="text-sm text-gray-500">Available Spots</div>
      <div className="text-lg font-bold text-blue-600">15</div>
    </div>
  </div>
  
  <div className="space-y-3 mb-4">
    <div className="flex items-center text-sm text-gray-600">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      Tue/Thu 12:00 PM • 75 minutes
    </div>
    
    <div className="flex items-center text-sm text-gray-600">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
      </svg>
      Instructor: Emma Chen
    </div>
    
    
        <div className="flex items-center text-sm text-gray-600 mb-2">
            <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.781 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 9.172V5L8 4z"></path>
            </svg>
            Equipment: [yoga mats
        </div>
  </div>
  
  <p className="text-gray-600 text-sm mb-4">Dynamic yoga sequences to improve flexibility and mindfulness</p>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
    Book Class
  </button>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex justify-between items-start mb-4">
    <div>
      <h3 className="text-xl font-bold text-gray-900 mb-2">CrossFit Challenge</h3>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
        Advanced
      </span>
    </div>
    <div className="text-right">
      <div className="text-sm text-gray-500">Available Spots</div>
      <div className="text-lg font-bold text-blue-600">10</div>
    </div>
  </div>
  
  <div className="space-y-3 mb-4">
    <div className="flex items-center text-sm text-gray-600">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      Mon/Wed/Fri 6:00 PM • 50 minutes
    </div>
    
    <div className="flex items-center text-sm text-gray-600">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
      </svg>
      Instructor: Jake Thompson
    </div>
    
    
        <div className="flex items-center text-sm text-gray-600 mb-2">
            <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.781 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 9.172V5L8 4z"></path>
            </svg>
            Equipment: [pull-up bars
        </div>
  </div>
  
  <p className="text-gray-600 text-sm mb-4">Functional fitness combining cardio</p>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
    Book Class
  </button>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex justify-between items-start mb-4">
    <div>
      <h3 className="text-xl font-bold text-gray-900 mb-2">Spin Cycle</h3>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
        Intermediate
      </span>
    </div>
    <div className="text-right">
      <div className="text-sm text-gray-500">Available Spots</div>
      <div className="text-lg font-bold text-blue-600">20</div>
    </div>
  </div>
  
  <div className="space-y-3 mb-4">
    <div className="flex items-center text-sm text-gray-600">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      Tue/Thu/Sat 7:00 AM • 45 minutes
    </div>
    
    <div className="flex items-center text-sm text-gray-600">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
      </svg>
      Instructor: Lisa Park
    </div>
    
    
        <div className="flex items-center text-sm text-gray-600 mb-2">
            <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.781 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 9.172V5L8 4z"></path>
            </svg>
            Equipment: [spin bikes
        </div>
  </div>
  
  <p className="text-gray-600 text-sm mb-4">High-energy cycling workout with motivating music</p>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
    Book Class
  </button>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex justify-between items-start mb-4">
    <div>
      <h3 className="text-xl font-bold text-gray-900 mb-2">Pilates Core</h3>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
        Beginner
      </span>
    </div>
    <div className="text-right">
      <div className="text-sm text-gray-500">Available Spots</div>
      <div className="text-lg font-bold text-blue-600">12</div>
    </div>
  </div>
  
  <div className="space-y-3 mb-4">
    <div className="flex items-center text-sm text-gray-600">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      Tue/Thu 6:30 PM • 50 minutes
    </div>
    
    <div className="flex items-center text-sm text-gray-600">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
      </svg>
      Instructor: Emma Chen
    </div>
    
    
        <div className="flex items-center text-sm text-gray-600 mb-2">
            <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.781 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 9.172V5L8 4z"></path>
            </svg>
            Equipment: [reformers
        </div>
  </div>
  
  <p className="text-gray-600 text-sm mb-4">Core-focused workout for stability and posture</p>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
    Book Class
  </button>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex justify-between items-start mb-4">
    <div>
      <h3 className="text-xl font-bold text-gray-900 mb-2">Boxing Bootcamp</h3>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
        Intermediate
      </span>
    </div>
    <div className="text-right">
      <div className="text-sm text-gray-500">Available Spots</div>
      <div className="text-lg font-bold text-blue-600">16</div>
    </div>
  </div>
  
  <div className="space-y-3 mb-4">
    <div className="flex items-center text-sm text-gray-600">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      Sat 9:00 AM • 60 minutes
    </div>
    
    <div className="flex items-center text-sm text-gray-600">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
      </svg>
      Instructor: Carlos Martinez
    </div>
    
    
        <div className="flex items-center text-sm text-gray-600 mb-2">
            <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.781 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 9.172V5L8 4z"></path>
            </svg>
            Equipment: [gloves
        </div>
  </div>
  
  <p className="text-gray-600 text-sm mb-4">Boxing techniques combined with cardio conditioning</p>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
    Book Class
  </button>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex justify-between items-start mb-4">
    <div>
      <h3 className="text-xl font-bold text-gray-900 mb-2">Zumba Dance Fitness</h3>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
        All Levels
      </span>
    </div>
    <div className="text-right">
      <div className="text-sm text-gray-500">Available Spots</div>
      <div className="text-lg font-bold text-blue-600">25</div>
    </div>
  </div>
  
  <div className="space-y-3 mb-4">
    <div className="flex items-center text-sm text-gray-600">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      Wed/Fri 7:00 PM • 45 minutes
    </div>
    
    <div className="flex items-center text-sm text-gray-600">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
      </svg>
      Instructor: Maria Santos
    </div>
    
    
        <div className="flex items-center text-sm text-gray-600 mb-2">
            <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.781 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 9.172V5L8 4z"></path>
            </svg>
            Equipment: [none required]
        </div>
  </div>
  
  <p className="text-gray-600 text-sm mb-4">Fun dance workout that feels like a party</p>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
    Book Class
  </button>
</div>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Cardio Classes</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Burn calories, improve heart health, and boost endurance with our high-energy cardio workouts</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Strength Training</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Build muscle, increase bone density, and enhance metabolism with progressive resistance training</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Flexibility & Recovery</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Improve mobility, reduce injury risk, and enhance recovery with yoga and stretching classes</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Functional Fitness</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Train movements that translate to real-life activities and sports performance</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <p>Important information for all members</p>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Booking Required</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Reserve your spot up to 7 days in advance through our app or website</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Cancellation Policy</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Cancel at least 2 hours before class start time to avoid late fees</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">What to Bring</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Water bottle, towel, and appropriate workout attire. Equipment provided for all classes</p>
    </div>
  </div>
</section>
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
  <div className="max-w-4xl mx-auto px-4 text-center">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">Ready to Join a Class?</h2>
    <p className="text-xl text-blue-100 mb-8">Book your first class today and experience the PowerFit difference</p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Book Now
      </Link>
    </div>
  </div>
</section>
    </>
  );
}
