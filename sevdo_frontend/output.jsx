import React from 'react';
import { Link } from 'react-router-dom';

export default function GeneratedComponent() {
  return (
    <>
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
  <div className="max-w-4xl mx-auto px-4 text-center">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">Ready to Start?</h2>
    <p className="text-xl text-blue-100 mb-8">Join 10,000+ companies already using our platform</p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Start Free Trial
      </Link>
    </div>
  </div>
</section>
    </>
  );
}
