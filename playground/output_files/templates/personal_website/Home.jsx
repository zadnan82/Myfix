import React from 'react';
import { Link } from 'react-router-dom';

export default function Personal_WebsiteHomePage() {
  return (
    <>
      <section className="relative bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 text-white min-h-screen flex items-center">
  <div className="absolute inset-0 bg-black opacity-20"></div>
  <div className="relative z-10 max-w-6xl mx-auto px-4 py-20 text-center">
    <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
      Sevdo
    </h1>
    <h2 className="text-xl md:text-2xl font-light mb-8 text-blue-100 max-w-3xl mx-auto">
      Sevdo langugage is a langugage made for tokenoptimizations
    </h2>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-semibold px-8 py-4 rounded-lg text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Save 4 million tokens
      </Link>
    </div>

  </div>
  <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
    </svg>
  </div>
</section>
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
  <div className="max-w-4xl mx-auto px-4 text-center">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">Stop overspending on tokens now</h2>
    <p className="text-xl text-blue-100 mb-8">Our agents are ready to go</p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Order a demo now
      </Link>
    </div>
  </div>
</section>
      <div className="max-w-2xl mx-auto p-4 border rounded-lg">
  <h2 className="text-xl font-bold mb-4">Chat</h2>
  <div className="chat-container" style={{height: '400px'}}>
    <div id="ch-messages" className="chat-messages bg-gray-50 p-4 rounded-lg mb-4 overflow-y-auto" style={{height: 'calc(400px - 100px)'}}>
      <div className="message mb-2">
        <div className="bg-blue-500 text-white p-2 rounded-lg max-w-xs">
          Hello! How can I help you today?
        </div>
      </div>
      <div className="message mb-2 flex justify-end">
        <div className="bg-gray-300 text-black p-2 rounded-lg max-w-xs">
          Hi there! I'm looking for some information.
        </div>
      </div>
    </div>
    <div className="chat-input flex gap-2">
      <input id="ch-input" className="flex-1 border rounded-lg px-3 py-2" placeholder="Type your message..." type="text" />
      <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-lg">
        Send
      </button>
    </div>
  </div>
</div>
    </>
  );
}
