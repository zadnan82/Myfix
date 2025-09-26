import React from 'react';
import { Link } from 'react-router-dom';

export default function Fitness_SiteTrainersPage() {
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
      <p>Our certified fitness professionals are here to guide you on your journey to better health and fitness</p>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex flex-col items-center text-center mb-4">
    <div className="w-24 h-24 rounded-full bg-gray-200 mb-4 overflow-hidden">
      <img src="/images/sarah-trainer.jpg" alt="Sarah Johnson" className="w-full h-full object-cover" 
           onError="this.src='https://via.placeholder.com/96x96?text=Trainer'" />
    </div>
    <h3 className="text-xl font-bold text-gray-900 mb-1">Sarah Johnson</h3>
    <p className="text-blue-600 font-semibold mb-2">Lead HIIT Instructor</p>
    <div className="flex items-center text-sm text-gray-600 mb-2">
      <svg className="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
      </svg>
      HIIT & Cardio Training
    </div>
    <div className="flex items-center text-sm text-gray-600 mb-3">
      <svg className="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      8 years experience
    </div>
  </div>
  
  <p className="text-gray-600 text-sm mb-4">Sarah's high-energy approach to fitness has helped hundreds of members achieve their weight loss and conditioning goals. Her HIIT classes are legendary for their intensity and results.</p>
  
  
        <div className="mb-4">
            <h4 className="text-sm font-semibold text-gray-700 mb-2">Certifications</h4>
            <div className="flex flex-wrap">
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 mr-2 mb-2">[NASM-CPT</span>
            </div>
        </div>
  
  <div className="text-center border-t border-gray-200 pt-4">
    <div className="text-lg font-bold text-green-600 mb-3">$75/hour</div>
    <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
      Book Session
    </button>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex flex-col items-center text-center mb-4">
    <div className="w-24 h-24 rounded-full bg-gray-200 mb-4 overflow-hidden">
      <img src="/images/mike-trainer.jpg" alt="Mike Rodriguez" className="w-full h-full object-cover" 
           onError="this.src='https://via.placeholder.com/96x96?text=Trainer'" />
    </div>
    <h3 className="text-xl font-bold text-gray-900 mb-1">Mike Rodriguez</h3>
    <p className="text-blue-600 font-semibold mb-2">Strength Training Director</p>
    <div className="flex items-center text-sm text-gray-600 mb-2">
      <svg className="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
      </svg>
      Powerlifting & Strength
    </div>
    <div className="flex items-center text-sm text-gray-600 mb-3">
      <svg className="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      12 years experience
    </div>
  </div>
  
  <p className="text-gray-600 text-sm mb-4">Former competitive powerlifter Mike brings serious strength training expertise. He specializes in helping members build muscle and achieve personal records safely.</p>
  
  
        <div className="mb-4">
            <h4 className="text-sm font-semibold text-gray-700 mb-2">Certifications</h4>
            <div className="flex flex-wrap">
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 mr-2 mb-2">[CSCS</span>
            </div>
        </div>
  
  <div className="text-center border-t border-gray-200 pt-4">
    <div className="text-lg font-bold text-green-600 mb-3">$85/hour</div>
    <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
      Book Session
    </button>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex flex-col items-center text-center mb-4">
    <div className="w-24 h-24 rounded-full bg-gray-200 mb-4 overflow-hidden">
      <img src="/images/emma-trainer.jpg" alt="Emma Chen" className="w-full h-full object-cover" 
           onError="this.src='https://via.placeholder.com/96x96?text=Trainer'" />
    </div>
    <h3 className="text-xl font-bold text-gray-900 mb-1">Emma Chen</h3>
    <p className="text-blue-600 font-semibold mb-2">Yoga & Wellness Instructor</p>
    <div className="flex items-center text-sm text-gray-600 mb-2">
      <svg className="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
      </svg>
      Yoga & Flexibility
    </div>
    <div className="flex items-center text-sm text-gray-600 mb-3">
      <svg className="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      6 years experience
    </div>
  </div>
  
  <p className="text-gray-600 text-sm mb-4">Emma's mindful approach to movement helps members find balance in body and mind. Her classes focus on flexibility</p>
  
  
        <div className="mb-4">
            <h4 className="text-sm font-semibold text-gray-700 mb-2">Certifications</h4>
            <div className="flex flex-wrap">
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 mr-2 mb-2">[RYT-500</span>
            </div>
        </div>
  
  <div className="text-center border-t border-gray-200 pt-4">
    <div className="text-lg font-bold text-green-600 mb-3">$70/hour</div>
    <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
      Book Session
    </button>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex flex-col items-center text-center mb-4">
    <div className="w-24 h-24 rounded-full bg-gray-200 mb-4 overflow-hidden">
      <img src="/images/jake-trainer.jpg" alt="Jake Thompson" className="w-full h-full object-cover" 
           onError="this.src='https://via.placeholder.com/96x96?text=Trainer'" />
    </div>
    <h3 className="text-xl font-bold text-gray-900 mb-1">Jake Thompson</h3>
    <p className="text-blue-600 font-semibold mb-2">CrossFit Coach</p>
    <div className="flex items-center text-sm text-gray-600 mb-2">
      <svg className="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
      </svg>
      Functional Fitness
    </div>
    <div className="flex items-center text-sm text-gray-600 mb-3">
      <svg className="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      10 years experience
    </div>
  </div>
  
  <p className="text-gray-600 text-sm mb-4">Jake's athletic background and coaching expertise make him perfect for members looking to improve sports performance and functional movement.</p>
  
  
        <div className="mb-4">
            <h4 className="text-sm font-semibold text-gray-700 mb-2">Certifications</h4>
            <div className="flex flex-wrap">
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 mr-2 mb-2">[CrossFit Level 3</span>
            </div>
        </div>
  
  <div className="text-center border-t border-gray-200 pt-4">
    <div className="text-lg font-bold text-green-600 mb-3">$80/hour</div>
    <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
      Book Session
    </button>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex flex-col items-center text-center mb-4">
    <div className="w-24 h-24 rounded-full bg-gray-200 mb-4 overflow-hidden">
      <img src="/images/lisa-trainer.jpg" alt="Lisa Park" className="w-full h-full object-cover" 
           onError="this.src='https://via.placeholder.com/96x96?text=Trainer'" />
    </div>
    <h3 className="text-xl font-bold text-gray-900 mb-1">Lisa Park</h3>
    <p className="text-blue-600 font-semibold mb-2">Cycling Instructor</p>
    <div className="flex items-center text-sm text-gray-600 mb-2">
      <svg className="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
      </svg>
      Indoor Cycling & Cardio
    </div>
    <div className="flex items-center text-sm text-gray-600 mb-3">
      <svg className="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      5 years experience
    </div>
  </div>
  
  <p className="text-gray-600 text-sm mb-4">Lisa's infectious energy and carefully curated playlists make her cycling classes the most popular at PowerFit. She focuses on endurance and fat burning.</p>
  
  
        <div className="mb-4">
            <h4 className="text-sm font-semibold text-gray-700 mb-2">Certifications</h4>
            <div className="flex flex-wrap">
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 mr-2 mb-2">[Spinning Certified</span>
            </div>
        </div>
  
  <div className="text-center border-t border-gray-200 pt-4">
    <div className="text-lg font-bold text-green-600 mb-3">$65/hour</div>
    <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
      Book Session
    </button>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  <div className="flex flex-col items-center text-center mb-4">
    <div className="w-24 h-24 rounded-full bg-gray-200 mb-4 overflow-hidden">
      <img src="/images/carlos-trainer.jpg" alt="Carlos Martinez" className="w-full h-full object-cover" 
           onError="this.src='https://via.placeholder.com/96x96?text=Trainer'" />
    </div>
    <h3 className="text-xl font-bold text-gray-900 mb-1">Carlos Martinez</h3>
    <p className="text-blue-600 font-semibold mb-2">Boxing Coach</p>
    <div className="flex items-center text-sm text-gray-600 mb-2">
      <svg className="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
      </svg>
      Boxing & Combat Sports
    </div>
    <div className="flex items-center text-sm text-gray-600 mb-3">
      <svg className="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      9 years experience
    </div>
  </div>
  
  <p className="text-gray-600 text-sm mb-4">Former amateur boxer Carlos teaches proper technique while delivering an incredible workout. His classes build confidence and conditioning.</p>
  
  
        <div className="mb-4">
            <h4 className="text-sm font-semibold text-gray-700 mb-2">Certifications</h4>
            <div className="flex flex-wrap">
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 mr-2 mb-2">[USA Boxing Coach</span>
            </div>
        </div>
  
  <div className="text-center border-t border-gray-200 pt-4">
    <div className="text-lg font-bold text-green-600 mb-3">$75/hour</div>
    <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300">
      Book Session
    </button>
  </div>
</div>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">One-on-One Training</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Personalized workout plans and dedicated attention to help you reach your specific goals faster</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Small Group Training</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Train with 2-4 friends for a more affordable option while still getting personalized coaching</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Specialized Programs</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Sport-specific training, injury rehabilitation, and competition preparation with expert guidance</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Nutrition Coaching</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Complement your training with personalized meal planning and nutrition education</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <p>Choose the personal training option that fits your needs and budget</p>
      <div className="relative bg-white rounded-2xl shadow-xl border-2 border-blue-500 p-6 transition-all duration-300 hover:shadow-2xl transform hover:-translate-y-1">
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
            <div className="bg-blue-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                Most Popular
            </div>
        </div>
  <div className="text-center mb-6">
    <h3 className="text-2xl font-bold text-gray-900 mb-2">Single Session</h3>
    <div className="mb-2">
      <span className="text-4xl font-bold text-gray-900">$75-85</span>
      <span className="text-gray-600">/session</span>
    </div>
    
    <div className="text-sm text-blue-600 font-medium">No Contract</div>
  </div>
  
  <ul className="mb-8 space-y-3">
                <li className="flex items-center text-gray-600 mb-3">
                    <svg className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    [1-hour personal training
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
    <h3 className="text-2xl font-bold text-gray-900 mb-2">4-Session Package</h3>
    <div className="mb-2">
      <span className="text-4xl font-bold text-gray-900">$280-320</span>
      <span className="text-gray-600">/month</span>
    </div>
    
    <div className="text-sm text-blue-600 font-medium">No Contract</div>
  </div>
  
  <ul className="mb-8 space-y-3">
                <li className="flex items-center text-gray-600 mb-3">
                    <svg className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    [4 personal training sessions
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
    <h3 className="text-2xl font-bold text-gray-900 mb-2">Monthly Unlimited</h3>
    <div className="mb-2">
      <span className="text-4xl font-bold text-gray-900">$800-1000</span>
      <span className="text-gray-600">/month</span>
    </div>
    
    <div className="text-sm text-blue-600 font-medium">No Contract</div>
  </div>
  
  <ul className="mb-8 space-y-3">
                <li className="flex items-center text-gray-600 mb-3">
                    <svg className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    [Unlimited personal training
                </li>
  </ul>
  
  <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 transform hover:scale-105">
    Choose Plan
  </button>
</div>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <p>Ready to work with one of our expert trainers?</p>
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
  <div className="max-w-4xl mx-auto px-4 text-center">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">Start Personal Training</h2>
    <p className="text-xl text-blue-100 mb-8">Schedule a complimentary consultation to discuss your goals and find the perfect trainer match</p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Book Consultation
      </Link>
    </div>
  </div>
</section>
    </>
  );
}
