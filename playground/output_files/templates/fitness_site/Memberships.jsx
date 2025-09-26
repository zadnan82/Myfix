import React from 'react';
import { Link } from 'react-router-dom';

export default function Fitness_SiteMembershipsPage() {
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
      <p>Choose the membership that fits your lifestyle and fitness goals</p>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <div className="relative bg-white rounded-2xl shadow-xl border-2 border-blue-500 p-6 transition-all duration-300 hover:shadow-2xl transform hover:-translate-y-1">
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
            <div className="bg-blue-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                Most Popular
            </div>
        </div>
  <div className="text-center mb-6">
    <h3 className="text-2xl font-bold text-gray-900 mb-2">Basic</h3>
    <div className="mb-2">
      <span className="text-4xl font-bold text-gray-900">$49</span>
      <span className="text-gray-600">/month</span>
    </div>
    <div className="text-sm text-gray-600 mb-2">Setup Fee: $25</div>
    <div className="text-sm text-blue-600 font-medium">No Contract</div>
  </div>
  
  <ul className="mb-8 space-y-3">
                <li className="flex items-center text-gray-600 mb-3">
                    <svg className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    [24/7 Gym Access
                </li>
  </ul>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 transform hover:scale-105">
    Choose Plan
  </button>
</div>
      <div className="relative bg-white rounded-2xl shadow-xl border-2 border-blue-500 p-6 transition-all duration-300 hover:shadow-2xl transform hover:-translate-y-1">
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
            <div className="bg-blue-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                Most Popular
            </div>
        </div>
  <div className="text-center mb-6">
    <h3 className="text-2xl font-bold text-gray-900 mb-2">Premium</h3>
    <div className="mb-2">
      <span className="text-4xl font-bold text-gray-900">$79</span>
      <span className="text-gray-600">/month</span>
    </div>
    <div className="text-sm text-gray-600 mb-2">Setup Fee: $25</div>
    <div className="text-sm text-blue-600 font-medium">No Contract</div>
  </div>
  
  <ul className="mb-8 space-y-3">
                <li className="flex items-center text-gray-600 mb-3">
                    <svg className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    [All Basic Features
                </li>
  </ul>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 transform hover:scale-105">
    Choose Plan
  </button>
</div>
      <div className="relative bg-white rounded-2xl shadow-xl border-2 border-blue-500 p-6 transition-all duration-300 hover:shadow-2xl transform hover:-translate-y-1">
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
            <div className="bg-blue-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                Most Popular
            </div>
        </div>
  <div className="text-center mb-6">
    <h3 className="text-2xl font-bold text-gray-900 mb-2">VIP</h3>
    <div className="mb-2">
      <span className="text-4xl font-bold text-gray-900">$129</span>
      <span className="text-gray-600">/month</span>
    </div>
    
    <div className="text-sm text-blue-600 font-medium">No Contract</div>
  </div>
  
  <ul className="mb-8 space-y-3">
                <li className="flex items-center text-gray-600 mb-3">
                    <svg className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    [All Premium Features
                </li>
  </ul>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 transform hover:scale-105">
    Choose Plan
  </button>
</div>
      <div className="relative bg-white rounded-2xl shadow-xl border-2 border-blue-500 p-6 transition-all duration-300 hover:shadow-2xl transform hover:-translate-y-1">
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
            <div className="bg-blue-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                Most Popular
            </div>
        </div>
  <div className="text-center mb-6">
    <h3 className="text-2xl font-bold text-gray-900 mb-2">Student</h3>
    <div className="mb-2">
      <span className="text-4xl font-bold text-gray-900">$35</span>
      <span className="text-gray-600">/month</span>
    </div>
    <div className="text-sm text-gray-600 mb-2">Setup Fee: $15</div>
    <div className="text-sm text-blue-600 font-medium">Semester Minimum</div>
  </div>
  
  <ul className="mb-8 space-y-3">
                <li className="flex items-center text-gray-600 mb-3">
                    <svg className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    [Basic Gym Access
                </li>
  </ul>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 transform hover:scale-105">
    Choose Plan
  </button>
</div>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">State-of-the-Art Equipment</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Access to the latest cardio machines, strength equipment, and functional training tools</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Expert-Led Classes</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Over 50 group fitness classes per week taught by certified instructors</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Flexible Scheduling</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">24/7 access for Basic+ members, early morning and late evening class options</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Community Support</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Join a supportive community of fitness enthusiasts and make lasting connections</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Clean & Safe Environment</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Regularly sanitized equipment, spacious workout areas, and professional maintenance</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">No Hidden Fees</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Transparent pricing with no enrollment fees for Premium and VIP memberships</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <p>Special rates for businesses and organizations</p>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Team Discounts</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">15% off monthly rates for groups of 10+ employees from the same company</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Wellness Programs</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Custom corporate wellness programs including lunch-and-learn sessions and fitness challenges</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Flexible Billing</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Direct corporate billing options and flexible payment terms available</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Guest Privileges</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Bring friends and family to experience PowerFit with monthly guest passes</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Nationwide Access</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Access to partner gyms when traveling - over 500 locations nationwide</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Member Events</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Exclusive workshops, fitness challenges, and social events throughout the year</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Referral Rewards</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Earn free months when you refer friends who join PowerFit</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Membership Freeze</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Freeze your membership for up to 3 months per year for medical or travel reasons</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Easy Cancellation</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Cancel anytime with 30-day notice - no cancellation fees or penalties</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Money-Back Guarantee</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Not satisfied? Get a full refund within your first 30 days</p>
    </div>
  </div>
</section>
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
  <div className="max-w-4xl mx-auto px-4 text-center">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">Ready to Join PowerFit?</h2>
    <p className="text-xl text-blue-100 mb-8">Start your fitness journey today with our 7-day free trial - no commitment required</p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Start Free Trial
      </Link>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">What's included in the free trial?</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Full access to gym equipment, 3 group classes, and a complimentary fitness assessment</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Can I change my membership plan?</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Yes, you can upgrade or downgrade your plan at any time with changes taking effect the next billing cycle</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Are there any long-term contracts?</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">No contracts required for Basic, Premium, and VIP memberships. Student memberships require a semester minimum</p>
    </div>
  </div>
</section>
    </>
  );
}
