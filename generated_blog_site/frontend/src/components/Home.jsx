import React from 'react';
import { Link } from 'react-router-dom';

export default function Home() {
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
      <section className="relative bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 text-white min-h-screen flex items-center">
  <div className="absolute inset-0 bg-black opacity-20"></div>
  <div className="relative z-10 max-w-6xl mx-auto px-4 py-20 text-center">
    <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
      Welcome to DevInsights
    </h1>
    <h2 className="text-xl md:text-2xl font-light mb-8 text-blue-100 max-w-3xl mx-auto">
      Sharing knowledge about web development, programming, and technology
    </h2>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-semibold px-8 py-4 rounded-lg text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Read Latest Posts
      </Link>
    </div>

  </div>
  <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
    </svg>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Why Read This Blog</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Insights and tutorials from real-world development experience</p>
    </div>
  </div>
</section>
      <section className="py-12 bg-gray-50 min-h-screen">
  <div className="max-w-7xl mx-auto px-4">
    
    
    <div className="text-center mb-12">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">Latest Articles</h1>
      <p className="text-xl text-gray-600 max-w-2xl mx-auto">Thoughts, tutorials, and insights</p>
    </div>

    
    

    
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-8">
      
            <article className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden">
                <div className="w-full h-48 bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white font-semibold">
                    Featured Image
                </div>
                <div className="p-6">
                    <div className="flex items-center text-sm text-gray-500 mb-3">
                        <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium mr-3">#React</span>
                        <time>March 15, 2024</time>
                    </div>
                    <h2 className="text-xl font-bold text-gray-900 mb-3 hover:text-blue-600 transition-colors cursor-pointer line-clamp-2">
                        Getting Started with React Hooks
                    </h2>
                    <p className="text-gray-600 text-sm mb-4 leading-relaxed line-clamp-3">
                        Learn how to use React Hooks to build more efficient and cleaner functional components in your applications.
                    </p>
                    <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-500">5 min read</span>
                        <span className="text-gray-500">by Jane Smith</span>
                    </div>
                </div>
            </article>
            <article className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden">
                <div className="w-full h-48 bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white font-semibold">
                    Featured Image
                </div>
                <div className="p-6">
                    <div className="flex items-center text-sm text-gray-500 mb-3">
                        <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium mr-3">#Design</span>
                        <time>March 12, 2024</time>
                    </div>
                    <h2 className="text-xl font-bold text-gray-900 mb-3 hover:text-blue-600 transition-colors cursor-pointer line-clamp-2">
                        CSS Grid vs Flexbox: When to Use What
                    </h2>
                    <p className="text-gray-600 text-sm mb-4 leading-relaxed line-clamp-3">
                        A comprehensive guide to understanding the differences between CSS Grid and Flexbox and when to use each layout method.
                    </p>
                    <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-500">7 min read</span>
                        <span className="text-gray-500">by John Doe</span>
                    </div>
                </div>
            </article>
            <article className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden">
                <div className="w-full h-48 bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white font-semibold">
                    Featured Image
                </div>
                <div className="p-6">
                    <div className="flex items-center text-sm text-gray-500 mb-3">
                        <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium mr-3">#Tutorial</span>
                        <time>March 10, 2024</time>
                    </div>
                    <h2 className="text-xl font-bold text-gray-900 mb-3 hover:text-blue-600 transition-colors cursor-pointer line-clamp-2">
                        Building REST APIs with Node.js
                    </h2>
                    <p className="text-gray-600 text-sm mb-4 leading-relaxed line-clamp-3">
                        Step-by-step tutorial on creating robust and scalable REST APIs using Node.js, Express, and MongoDB.
                    </p>
                    <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-500">12 min read</span>
                        <span className="text-gray-500">by Mike Johnson</span>
                    </div>
                </div>
            </article>
            <article className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden">
                <div className="w-full h-48 bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white font-semibold">
                    Featured Image
                </div>
                <div className="p-6">
                    <div className="flex items-center text-sm text-gray-500 mb-3">
                        <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium mr-3">#JavaScript</span>
                        <time>March 8, 2024</time>
                    </div>
                    <h2 className="text-xl font-bold text-gray-900 mb-3 hover:text-blue-600 transition-colors cursor-pointer line-clamp-2">
                        Modern JavaScript ES6+ Features
                    </h2>
                    <p className="text-gray-600 text-sm mb-4 leading-relaxed line-clamp-3">
                        Explore the latest JavaScript features including arrow functions, destructuring, async/await, and more.
                    </p>
                    <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-500">8 min read</span>
                        <span className="text-gray-500">by Sarah Wilson</span>
                    </div>
                </div>
            </article>
            <article className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden">
                <div className="w-full h-48 bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white font-semibold">
                    Featured Image
                </div>
                <div className="p-6">
                    <div className="flex items-center text-sm text-gray-500 mb-3">
                        <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium mr-3">#Web Development</span>
                        <time>March 5, 2024</time>
                    </div>
                    <h2 className="text-xl font-bold text-gray-900 mb-3 hover:text-blue-600 transition-colors cursor-pointer line-clamp-2">
                        Responsive Web Design Best Practices
                    </h2>
                    <p className="text-gray-600 text-sm mb-4 leading-relaxed line-clamp-3">
                        Learn the fundamental principles of responsive web design and how to create websites that work on all devices.
                    </p>
                    <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-500">6 min read</span>
                        <span className="text-gray-500">by Alex Brown</span>
                    </div>
                </div>
            </article>
            <article className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden">
                <div className="w-full h-48 bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white font-semibold">
                    Featured Image
                </div>
                <div className="p-6">
                    <div className="flex items-center text-sm text-gray-500 mb-3">
                        <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium mr-3">#Tutorial</span>
                        <time>March 2, 2024</time>
                    </div>
                    <h2 className="text-xl font-bold text-gray-900 mb-3 hover:text-blue-600 transition-colors cursor-pointer line-clamp-2">
                        Introduction to TypeScript
                    </h2>
                    <p className="text-gray-600 text-sm mb-4 leading-relaxed line-clamp-3">
                        Discover how TypeScript can improve your JavaScript development with static typing and better tooling.
                    </p>
                    <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-500">10 min read</span>
                        <span className="text-gray-500">by Emma Davis</span>
                    </div>
                </div>
            </article>
    </div>

    
    <div className="flex items-center justify-center space-x-2 mt-12">
        <button className="px-3 py-2 text-sm font-medium text-gray-500 hover:text-blue-600 transition-colors" disabled>
            ← Previous
        </button>
        <button className="px-3 py-2 text-sm font-medium bg-blue-600 text-white rounded-md">1</button>
        <button className="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600 transition-colors">2</button>
        <button className="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600 transition-colors">3</button>
        <span className="px-3 py-2 text-sm text-gray-500">...</span>
        <button className="px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600 transition-colors">10</button>
        <button className="px-3 py-2 text-sm font-medium text-blue-600 hover:text-blue-700 transition-colors">
            Next →
        </button>
    </div>

    
    <div className="hidden text-center py-12">
      <div className="text-gray-400 mb-4">
        <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
      </div>
      <h3 className="text-lg font-medium text-gray-900 mb-2">No articles found</h3>
      <p className="text-gray-500">Try adjusting your search or filter criteria.</p>
    </div>
  </div>
</section>
      <section className="py-12 bg-gray-50">
  <div className="max-w-6xl mx-auto px-4">
    <div className="text-center mb-8">
      <h2 className="text-3xl font-bold text-gray-900">What Readers Say</h2>
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
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
  <div className="max-w-4xl mx-auto px-4 text-center">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">Never Miss a Post</h2>
    <p className="text-xl text-blue-100 mb-8">Subscribe to get the latest articles delivered to your inbox</p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      <button className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Subscribe Now
      </button>
    </div>
  </div>
</section>
    </>
  );
}
