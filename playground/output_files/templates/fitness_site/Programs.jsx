import React from 'react';
import { Link } from 'react-router-dom';

export default function Fitness_SiteProgramsPage() {
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
      <p>Structured training programs designed to help you achieve specific fitness goals</p>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex justify-between items-start mb-4">
    <div className="flex-1">
      <h3 className="text-xl font-bold text-gray-900 mb-2">12-Week Body Transformation</h3>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
        Intermediate
      </span>
    </div>
    <div className="text-right">
      <div className="text-2xl font-bold text-green-600">$599</div>
      <div className="text-sm text-gray-500">12 weeks</div>
    </div>
  </div>
  
  <div className="mb-4">
    <div className="flex items-center text-sm text-gray-600 mb-2">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
      </svg>
      Goal: Weight Loss & Muscle Gain
    </div>
    
    <div className="flex items-center text-sm text-gray-600 mb-3">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
      </svg>
      Trainer: Sarah Johnson & Mike Rodriguez
    </div>
  </div>
  
  <div className="mb-4"><h4 className="text-sm font-semibold text-gray-700 mb-2">Program Includes:</h4><ul className="space-y-1">
                <li className="flex items-center text-gray-600 mb-2">
                    <svg className="w-4 h-4 text-blue-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    [Personal Training Sessions
                </li></ul></div>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
    Enroll Now
  </button>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex justify-between items-start mb-4">
    <div className="flex-1">
      <h3 className="text-xl font-bold text-gray-900 mb-2">Strength Builder Program</h3>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
        Beginner
      </span>
    </div>
    <div className="text-right">
      <div className="text-2xl font-bold text-green-600">$299</div>
      <div className="text-sm text-gray-500">8 weeks</div>
    </div>
  </div>
  
  <div className="mb-4">
    <div className="flex items-center text-sm text-gray-600 mb-2">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
      </svg>
      Goal: Build Foundation Strength
    </div>
    
    <div className="flex items-center text-sm text-gray-600 mb-3">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
      </svg>
      Trainer: Mike Rodriguez
    </div>
  </div>
  
  <div className="mb-4"><h4 className="text-sm font-semibold text-gray-700 mb-2">Program Includes:</h4><ul className="space-y-1">
                <li className="flex items-center text-gray-600 mb-2">
                    <svg className="w-4 h-4 text-blue-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    [Progressive Workout Plan
                </li></ul></div>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
    Enroll Now
  </button>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex justify-between items-start mb-4">
    <div className="flex-1">
      <h3 className="text-xl font-bold text-gray-900 mb-2">Athletic Performance</h3>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
        Advanced
      </span>
    </div>
    <div className="text-right">
      <div className="text-2xl font-bold text-green-600">$799</div>
      <div className="text-sm text-gray-500">10 weeks</div>
    </div>
  </div>
  
  <div className="mb-4">
    <div className="flex items-center text-sm text-gray-600 mb-2">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
      </svg>
      Goal: Sports Performance
    </div>
    
    <div className="flex items-center text-sm text-gray-600 mb-3">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
      </svg>
      Trainer: Jake Thompson
    </div>
  </div>
  
  <div className="mb-4"><h4 className="text-sm font-semibold text-gray-700 mb-2">Program Includes:</h4><ul className="space-y-1">
                <li className="flex items-center text-gray-600 mb-2">
                    <svg className="w-4 h-4 text-blue-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    [Sport-Specific Training
                </li></ul></div>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
    Enroll Now
  </button>
</div>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex justify-between items-start mb-4">
    <div className="flex-1">
      <h3 className="text-xl font-bold text-gray-900 mb-2">Prenatal Fitness</h3>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
        Beginner
      </span>
    </div>
    <div className="text-right">
      <div className="text-2xl font-bold text-green-600">$149/month</div>
      <div className="text-sm text-gray-500">Ongoing</div>
    </div>
  </div>
  
  <div className="mb-4">
    <div className="flex items-center text-sm text-gray-600 mb-2">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
      </svg>
      Goal: Healthy Pregnancy
    </div>
    
    <div className="flex items-center text-sm text-gray-600 mb-3">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
      </svg>
      Trainer: Emma Chen
    </div>
  </div>
  
  <div className="mb-4"><h4 className="text-sm font-semibold text-gray-700 mb-2">Program Includes:</h4><ul className="space-y-1">
                <li className="flex items-center text-gray-600 mb-2">
                    <svg className="w-4 h-4 text-blue-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    [Safe Exercise Routines
                </li></ul></div>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
    Enroll Now
  </button>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex justify-between items-start mb-4">
    <div className="flex-1">
      <h3 className="text-xl font-bold text-gray-900 mb-2">Senior Fitness</h3>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
        Beginner
      </span>
    </div>
    <div className="text-right">
      <div className="text-2xl font-bold text-green-600">$99/month</div>
      <div className="text-sm text-gray-500">Ongoing</div>
    </div>
  </div>
  
  <div className="mb-4">
    <div className="flex items-center text-sm text-gray-600 mb-2">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
      </svg>
      Goal: Active Aging
    </div>
    
    <div className="flex items-center text-sm text-gray-600 mb-3">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
      </svg>
      Trainer: Emma Chen & Lisa Park
    </div>
  </div>
  
  <div className="mb-4"><h4 className="text-sm font-semibold text-gray-700 mb-2">Program Includes:</h4><ul className="space-y-1">
                <li className="flex items-center text-gray-600 mb-2">
                    <svg className="w-4 h-4 text-blue-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    [Low-Impact Workouts
                </li></ul></div>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
    Enroll Now
  </button>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex justify-between items-start mb-4">
    <div className="flex-1">
      <h3 className="text-xl font-bold text-gray-900 mb-2">Injury Recovery</h3>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
        Beginner
      </span>
    </div>
    <div className="text-right">
      <div className="text-2xl font-bold text-green-600">$199/month</div>
      <div className="text-sm text-gray-500">Variable</div>
    </div>
  </div>
  
  <div className="mb-4">
    <div className="flex items-center text-sm text-gray-600 mb-2">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
      </svg>
      Goal: Rehabilitation
    </div>
    
    <div className="flex items-center text-sm text-gray-600 mb-3">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
      </svg>
      Trainer: Jake Thompson
    </div>
  </div>
  
  <div className="mb-4"><h4 className="text-sm font-semibold text-gray-700 mb-2">Program Includes:</h4><ul className="space-y-1">
                <li className="flex items-center text-gray-600 mb-2">
                    <svg className="w-4 h-4 text-blue-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    [Physical Therapy Exercises
                </li></ul></div>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
    Enroll Now
  </button>
</div>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex justify-between items-start mb-4">
    <div className="flex-1">
      <h3 className="text-xl font-bold text-gray-900 mb-2">30-Day HIIT Challenge</h3>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
        Intermediate
      </span>
    </div>
    <div className="text-right">
      <div className="text-2xl font-bold text-green-600">$99</div>
      <div className="text-sm text-gray-500">30 days</div>
    </div>
  </div>
  
  <div className="mb-4">
    <div className="flex items-center text-sm text-gray-600 mb-2">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
      </svg>
      Goal: Cardiovascular Fitness
    </div>
    
    <div className="flex items-center text-sm text-gray-600 mb-3">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
      </svg>
      Trainer: Sarah Johnson
    </div>
  </div>
  
  <div className="mb-4"><h4 className="text-sm font-semibold text-gray-700 mb-2">Program Includes:</h4><ul className="space-y-1">
                <li className="flex items-center text-gray-600 mb-2">
                    <svg className="w-4 h-4 text-blue-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    [Daily HIIT Workouts
                </li></ul></div>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
    Enroll Now
  </button>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex justify-between items-start mb-4">
    <div className="flex-1">
      <h3 className="text-xl font-bold text-gray-900 mb-2">Powerlifting Prep</h3>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
        Advanced
      </span>
    </div>
    <div className="text-right">
      <div className="text-2xl font-bold text-green-600">$899</div>
      <div className="text-sm text-gray-500">16 weeks</div>
    </div>
  </div>
  
  <div className="mb-4">
    <div className="flex items-center text-sm text-gray-600 mb-2">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
      </svg>
      Goal: Competition Ready
    </div>
    
    <div className="flex items-center text-sm text-gray-600 mb-3">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
      </svg>
      Trainer: Mike Rodriguez
    </div>
  </div>
  
  <div className="mb-4"><h4 className="text-sm font-semibold text-gray-700 mb-2">Program Includes:</h4><ul className="space-y-1">
                <li className="flex items-center text-gray-600 mb-2">
                    <svg className="w-4 h-4 text-blue-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    [Competition Training
                </li></ul></div>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
    Enroll Now
  </button>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex justify-between items-start mb-4">
    <div className="flex-1">
      <h3 className="text-xl font-bold text-gray-900 mb-2">Yoga Journey</h3>
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
        All Levels
      </span>
    </div>
    <div className="text-right">
      <div className="text-2xl font-bold text-green-600">$199</div>
      <div className="text-sm text-gray-500">6 weeks</div>
    </div>
  </div>
  
  <div className="mb-4">
    <div className="flex items-center text-sm text-gray-600 mb-2">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
      </svg>
      Goal: Flexibility & Mindfulness
    </div>
    
    <div className="flex items-center text-sm text-gray-600 mb-3">
      <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
      </svg>
      Trainer: Emma Chen
    </div>
  </div>
  
  <div className="mb-4"><h4 className="text-sm font-semibold text-gray-700 mb-2">Program Includes:</h4><ul className="space-y-1">
                <li className="flex items-center text-gray-600 mb-2">
                    <svg className="w-4 h-4 text-blue-500 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    [Progressive Yoga Sequences
                </li></ul></div>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
    Enroll Now
  </button>
</div>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Meal Planning Service</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Custom meal plans designed around your goals, dietary preferences, and lifestyle</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Nutrition Coaching</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">One-on-one sessions with certified nutritionists to optimize your eating habits</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Supplement Guidance</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Evidence-based supplement recommendations to support your training and recovery</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Personalized Approach</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Every program is customized based on your fitness level, goals, and available time</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Progress Tracking</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Regular assessments and measurements to monitor your transformation journey</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Expert Support</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Direct access to certified trainers and nutritionists throughout your program</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Flexible Scheduling</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Programs designed to fit your schedule with options for busy lifestyles</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Community Support</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Connect with others in similar programs for motivation and accountability</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-12 bg-gray-50">
  <div className="max-w-6xl mx-auto px-4">
    <div className="text-center mb-8">
      <h2 className="text-3xl font-bold text-gray-900">Program Graduate Testimonials</h2>
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
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Results Guarantee</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Follow the program as designed and see results within 30 days or get your money back</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Lifetime Support</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Access to program materials and alumni community for ongoing support</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Program Modifications</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Programs can be adjusted based on your progress and changing needs</p>
    </div>
  </div>
</section>
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
  <div className="max-w-4xl mx-auto px-4 text-center">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">Ready to Transform Your Life?</h2>
    <p className="text-xl text-blue-100 mb-8">Choose a program that aligns with your goals and start your transformation today</p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Browse Programs
      </Link>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">1. Choose Your Program</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Select the program that best matches your goals and fitness level</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">2. Initial Assessment</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Complete a comprehensive fitness assessment and goal-setting session</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">3. Follow Your Plan</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Execute your personalized workout and nutrition plan with trainer guidance</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">4. Track Progress</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Regular check-ins and measurements to ensure you're on track for success</p>
    </div>
  </div>
</section>
    </>
  );
}
