import React from 'react';
import { Link } from 'react-router-dom';

export default function Wedding_SiteGalleriPage() {
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
      <p>Se förvandlingen från vision till verklighet</p>
      <section className="relative bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 text-white min-h-screen flex items-center">
  <div className="absolute inset-0 bg-black opacity-20"></div>
  <div className="relative z-10 max-w-6xl mx-auto px-4 py-20 text-center">
    <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
      Före & Efter - Magiska förvandlingar
    </h1>
    <h2 className="text-xl md:text-2xl font-light mb-8 text-blue-100 max-w-3xl mx-auto">
      Upptäck hur vi förvandlar vanliga platser till drömscenarier för er stora dag
    </h2>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-semibold px-8 py-4 rounded-lg text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Se alla projekt
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
      <p>Romantiska vigselplatser</p>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
  <div className="relative">
    <div className="grid grid-cols-2 gap-0">
      
      <div className="relative group">
        <img src="/images/gallery/church-before.jpg" alt="Before - Klassisk kyrkceremoni" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=Before'" />
        <div className="absolute top-3 left-3 bg-black bg-opacity-70 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Före
        </div>
      </div>
      
      
      <div className="relative group">
        <img src="/images/gallery/church-after.jpg" alt="After - Klassisk kyrkceremoni" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=After'" />
        <div className="absolute top-3 right-3 bg-pink-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Efter
        </div>
      </div>
    </div>
    
    
    <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 bg-white bg-opacity-90 px-3 py-1 rounded-full text-sm font-medium text-gray-700">
      Wedding
    </div>
  </div>
  
  <div className="p-6">
    <h3 className="text-xl font-bold text-gray-900 mb-3">Klassisk kyrkceremoni</h3>
    <p className="text-gray-600 text-sm leading-relaxed">Traditionell kyrka förvandlad med vita rosor och ljus</p>
    
    <div className="flex justify-between items-center mt-4">
      <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
        Se fler bilder →
      </button>
      <button className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Inspireras
      </button>
    </div>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
  <div className="relative">
    <div className="grid grid-cols-2 gap-0">
      
      <div className="relative group">
        <img src="/images/gallery/garden-before.jpg" alt="Before - Trädgårdsbröllop" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=Before'" />
        <div className="absolute top-3 left-3 bg-black bg-opacity-70 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Före
        </div>
      </div>
      
      
      <div className="relative group">
        <img src="/images/gallery/garden-after.jpg" alt="After - Trädgårdsbröllop" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=After'" />
        <div className="absolute top-3 right-3 bg-pink-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Efter
        </div>
      </div>
    </div>
    
    
    <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 bg-white bg-opacity-90 px-3 py-1 rounded-full text-sm font-medium text-gray-700">
      Wedding
    </div>
  </div>
  
  <div className="p-6">
    <h3 className="text-xl font-bold text-gray-900 mb-3">Trädgårdsbröllop</h3>
    <p className="text-gray-600 text-sm leading-relaxed">Privat trädgård som blev en romantisk vigselplats</p>
    
    <div className="flex justify-between items-center mt-4">
      <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
        Se fler bilder →
      </button>
      <button className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Inspireras
      </button>
    </div>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
  <div className="relative">
    <div className="grid grid-cols-2 gap-0">
      
      <div className="relative group">
        <img src="/images/gallery/beach-before.jpg" alt="Before - Strandceremoni" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=Before'" />
        <div className="absolute top-3 left-3 bg-black bg-opacity-70 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Före
        </div>
      </div>
      
      
      <div className="relative group">
        <img src="/images/gallery/beach-after.jpg" alt="After - Strandceremoni" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=After'" />
        <div className="absolute top-3 right-3 bg-pink-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Efter
        </div>
      </div>
    </div>
    
    
    <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 bg-white bg-opacity-90 px-3 py-1 rounded-full text-sm font-medium text-gray-700">
      Wedding
    </div>
  </div>
  
  <div className="p-6">
    <h3 className="text-xl font-bold text-gray-900 mb-3">Strandceremoni</h3>
    <p className="text-gray-600 text-sm leading-relaxed">Vacker strandvy med elegant båge och blommor</p>
    
    <div className="flex justify-between items-center mt-4">
      <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
        Se fler bilder →
      </button>
      <button className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Inspireras
      </button>
    </div>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
  <div className="relative">
    <div className="grid grid-cols-2 gap-0">
      
      <div className="relative group">
        <img src="/images/gallery/castle-before.jpg" alt="Before - Slottsbröllop" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=Before'" />
        <div className="absolute top-3 left-3 bg-black bg-opacity-70 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Före
        </div>
      </div>
      
      
      <div className="relative group">
        <img src="/images/gallery/castle-after.jpg" alt="After - Slottsbröllop" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=After'" />
        <div className="absolute top-3 right-3 bg-pink-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Efter
        </div>
      </div>
    </div>
    
    
    <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 bg-white bg-opacity-90 px-3 py-1 rounded-full text-sm font-medium text-gray-700">
      Wedding
    </div>
  </div>
  
  <div className="p-6">
    <h3 className="text-xl font-bold text-gray-900 mb-3">Slottsbröllop</h3>
    <p className="text-gray-600 text-sm leading-relaxed">Historiskt slott med kunglig atmosfär</p>
    
    <div className="flex justify-between items-center mt-4">
      <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
        Se fler bilder →
      </button>
      <button className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Inspireras
      </button>
    </div>
  </div>
</div>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <p>Festlokaler som tar andan ur er</p>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
  <div className="relative">
    <div className="grid grid-cols-2 gap-0">
      
      <div className="relative group">
        <img src="/images/gallery/ballroom-before.jpg" alt="Before - Elegant ballsal" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=Before'" />
        <div className="absolute top-3 left-3 bg-black bg-opacity-70 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Före
        </div>
      </div>
      
      
      <div className="relative group">
        <img src="/images/gallery/ballroom-after.jpg" alt="After - Elegant ballsal" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=After'" />
        <div className="absolute top-3 right-3 bg-pink-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Efter
        </div>
      </div>
    </div>
    
    
    <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 bg-white bg-opacity-90 px-3 py-1 rounded-full text-sm font-medium text-gray-700">
      Wedding
    </div>
  </div>
  
  <div className="p-6">
    <h3 className="text-xl font-bold text-gray-900 mb-3">Elegant ballsal</h3>
    <p className="text-gray-600 text-sm leading-relaxed">Klassisk ballsal med kristallkronor och gulddetaljer</p>
    
    <div className="flex justify-between items-center mt-4">
      <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
        Se fler bilder →
      </button>
      <button className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Inspireras
      </button>
    </div>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
  <div className="relative">
    <div className="grid grid-cols-2 gap-0">
      
      <div className="relative group">
        <img src="/images/gallery/barn-before.jpg" alt="Before - Rustik lada" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=Before'" />
        <div className="absolute top-3 left-3 bg-black bg-opacity-70 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Före
        </div>
      </div>
      
      
      <div className="relative group">
        <img src="/images/gallery/barn-after.jpg" alt="After - Rustik lada" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=After'" />
        <div className="absolute top-3 right-3 bg-pink-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Efter
        </div>
      </div>
    </div>
    
    
    <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 bg-white bg-opacity-90 px-3 py-1 rounded-full text-sm font-medium text-gray-700">
      Wedding
    </div>
  </div>
  
  <div className="p-6">
    <h3 className="text-xl font-bold text-gray-900 mb-3">Rustik lada</h3>
    <p className="text-gray-600 text-sm leading-relaxed">Charmig lada förvandlad till modern festlokal</p>
    
    <div className="flex justify-between items-center mt-4">
      <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
        Se fler bilder →
      </button>
      <button className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Inspireras
      </button>
    </div>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
  <div className="relative">
    <div className="grid grid-cols-2 gap-0">
      
      <div className="relative group">
        <img src="/images/gallery/rooftop-before.jpg" alt="Before - Takrestaurang" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=Before'" />
        <div className="absolute top-3 left-3 bg-black bg-opacity-70 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Före
        </div>
      </div>
      
      
      <div className="relative group">
        <img src="/images/gallery/rooftop-after.jpg" alt="After - Takrestaurang" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=After'" />
        <div className="absolute top-3 right-3 bg-pink-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Efter
        </div>
      </div>
    </div>
    
    
    <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 bg-white bg-opacity-90 px-3 py-1 rounded-full text-sm font-medium text-gray-700">
      Wedding
    </div>
  </div>
  
  <div className="p-6">
    <h3 className="text-xl font-bold text-gray-900 mb-3">Takrestaurang</h3>
    <p className="text-gray-600 text-sm leading-relaxed">Spektakulär utsikt över staden med elegant inredning</p>
    
    <div className="flex justify-between items-center mt-4">
      <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
        Se fler bilder →
      </button>
      <button className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Inspireras
      </button>
    </div>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
  <div className="relative">
    <div className="grid grid-cols-2 gap-0">
      
      <div className="relative group">
        <img src="/images/gallery/vintage-before.jpg" alt="Before - Vintagesal" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=Before'" />
        <div className="absolute top-3 left-3 bg-black bg-opacity-70 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Före
        </div>
      </div>
      
      
      <div className="relative group">
        <img src="/images/gallery/vintage-after.jpg" alt="After - Vintagesal" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=After'" />
        <div className="absolute top-3 right-3 bg-pink-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Efter
        </div>
      </div>
    </div>
    
    
    <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 bg-white bg-opacity-90 px-3 py-1 rounded-full text-sm font-medium text-gray-700">
      Wedding
    </div>
  </div>
  
  <div className="p-6">
    <h3 className="text-xl font-bold text-gray-900 mb-3">Vintagesal</h3>
    <p className="text-gray-600 text-sm leading-relaxed">Nostalgisk charm med antika möbler och mjuk belysning</p>
    
    <div className="flex justify-between items-center mt-4">
      <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
        Se fler bilder →
      </button>
      <button className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Inspireras
      </button>
    </div>
  </div>
</div>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <p>Unika stilar för varje par</p>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
  <div className="relative">
    <div className="grid grid-cols-2 gap-0">
      
      <div className="relative group">
        <img src="/images/gallery/boho-before.jpg" alt="Before - Bohemisk stil" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=Before'" />
        <div className="absolute top-3 left-3 bg-black bg-opacity-70 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Före
        </div>
      </div>
      
      
      <div className="relative group">
        <img src="/images/gallery/boho-after.jpg" alt="After - Bohemisk stil" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=After'" />
        <div className="absolute top-3 right-3 bg-pink-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Efter
        </div>
      </div>
    </div>
    
    
    <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 bg-white bg-opacity-90 px-3 py-1 rounded-full text-sm font-medium text-gray-700">
      Wedding
    </div>
  </div>
  
  <div className="p-6">
    <h3 className="text-xl font-bold text-gray-900 mb-3">Bohemisk stil</h3>
    <p className="text-gray-600 text-sm leading-relaxed">Avslappnad elegans med naturliga material och jordnära färger</p>
    
    <div className="flex justify-between items-center mt-4">
      <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
        Se fler bilder →
      </button>
      <button className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Inspireras
      </button>
    </div>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
  <div className="relative">
    <div className="grid grid-cols-2 gap-0">
      
      <div className="relative group">
        <img src="/images/gallery/modern-before.jpg" alt="Before - Modern minimalism" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=Before'" />
        <div className="absolute top-3 left-3 bg-black bg-opacity-70 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Före
        </div>
      </div>
      
      
      <div className="relative group">
        <img src="/images/gallery/modern-after.jpg" alt="After - Modern minimalism" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=After'" />
        <div className="absolute top-3 right-3 bg-pink-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Efter
        </div>
      </div>
    </div>
    
    
    <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 bg-white bg-opacity-90 px-3 py-1 rounded-full text-sm font-medium text-gray-700">
      Wedding
    </div>
  </div>
  
  <div className="p-6">
    <h3 className="text-xl font-bold text-gray-900 mb-3">Modern minimalism</h3>
    <p className="text-gray-600 text-sm leading-relaxed">Ren design med fokus på geometriska former och neutrala toner</p>
    
    <div className="flex justify-between items-center mt-4">
      <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
        Se fler bilder →
      </button>
      <button className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Inspireras
      </button>
    </div>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
  <div className="relative">
    <div className="grid grid-cols-2 gap-0">
      
      <div className="relative group">
        <img src="/images/gallery/gatsby-before.jpg" alt="Before - Gatsby glamour" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=Before'" />
        <div className="absolute top-3 left-3 bg-black bg-opacity-70 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Före
        </div>
      </div>
      
      
      <div className="relative group">
        <img src="/images/gallery/gatsby-after.jpg" alt="After - Gatsby glamour" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=After'" />
        <div className="absolute top-3 right-3 bg-pink-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Efter
        </div>
      </div>
    </div>
    
    
    <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 bg-white bg-opacity-90 px-3 py-1 rounded-full text-sm font-medium text-gray-700">
      Wedding
    </div>
  </div>
  
  <div className="p-6">
    <h3 className="text-xl font-bold text-gray-900 mb-3">Gatsby glamour</h3>
    <p className="text-gray-600 text-sm leading-relaxed">Art deco-inspirerat med guld</p>
    
    <div className="flex justify-between items-center mt-4">
      <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
        Se fler bilder →
      </button>
      <button className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Inspireras
      </button>
    </div>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
  <div className="relative">
    <div className="grid grid-cols-2 gap-0">
      
      <div className="relative group">
        <img src="/images/gallery/scandi-before.jpg" alt="Before - Skandinavisk stil" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=Before'" />
        <div className="absolute top-3 left-3 bg-black bg-opacity-70 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Före
        </div>
      </div>
      
      
      <div className="relative group">
        <img src="/images/gallery/scandi-after.jpg" alt="After - Skandinavisk stil" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=After'" />
        <div className="absolute top-3 right-3 bg-pink-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Efter
        </div>
      </div>
    </div>
    
    
    <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 bg-white bg-opacity-90 px-3 py-1 rounded-full text-sm font-medium text-gray-700">
      Wedding
    </div>
  </div>
  
  <div className="p-6">
    <h3 className="text-xl font-bold text-gray-900 mb-3">Skandinavisk stil</h3>
    <p className="text-gray-600 text-sm leading-relaxed">Ljust och luftigt med naturliga element och enkla linjer</p>
    
    <div className="flex justify-between items-center mt-4">
      <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
        Se fler bilder →
      </button>
      <button className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Inspireras
      </button>
    </div>
  </div>
</div>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <p>Vackert året runt</p>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
  <div className="relative">
    <div className="grid grid-cols-2 gap-0">
      
      <div className="relative group">
        <img src="/images/gallery/spring-before.jpg" alt="Before - Vårbröllop" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=Before'" />
        <div className="absolute top-3 left-3 bg-black bg-opacity-70 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Före
        </div>
      </div>
      
      
      <div className="relative group">
        <img src="/images/gallery/spring-after.jpg" alt="After - Vårbröllop" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=After'" />
        <div className="absolute top-3 right-3 bg-pink-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Efter
        </div>
      </div>
    </div>
    
    
    <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 bg-white bg-opacity-90 px-3 py-1 rounded-full text-sm font-medium text-gray-700">
      Wedding
    </div>
  </div>
  
  <div className="p-6">
    <h3 className="text-xl font-bold text-gray-900 mb-3">Vårbröllop</h3>
    <p className="text-gray-600 text-sm leading-relaxed">Färska blommor och pastellfärger för vårkänsla</p>
    
    <div className="flex justify-between items-center mt-4">
      <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
        Se fler bilder →
      </button>
      <button className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Inspireras
      </button>
    </div>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
  <div className="relative">
    <div className="grid grid-cols-2 gap-0">
      
      <div className="relative group">
        <img src="/images/gallery/summer-before.jpg" alt="Before - Sommarbröllop" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=Before'" />
        <div className="absolute top-3 left-3 bg-black bg-opacity-70 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Före
        </div>
      </div>
      
      
      <div className="relative group">
        <img src="/images/gallery/summer-after.jpg" alt="After - Sommarbröllop" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=After'" />
        <div className="absolute top-3 right-3 bg-pink-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Efter
        </div>
      </div>
    </div>
    
    
    <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 bg-white bg-opacity-90 px-3 py-1 rounded-full text-sm font-medium text-gray-700">
      Wedding
    </div>
  </div>
  
  <div className="p-6">
    <h3 className="text-xl font-bold text-gray-900 mb-3">Sommarbröllop</h3>
    <p className="text-gray-600 text-sm leading-relaxed">Utomhusfest med ljusa färger och naturlig skönhet</p>
    
    <div className="flex justify-between items-center mt-4">
      <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
        Se fler bilder →
      </button>
      <button className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Inspireras
      </button>
    </div>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
  <div className="relative">
    <div className="grid grid-cols-2 gap-0">
      
      <div className="relative group">
        <img src="/images/gallery/autumn-before.jpg" alt="Before - Höstbröllop" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=Before'" />
        <div className="absolute top-3 left-3 bg-black bg-opacity-70 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Före
        </div>
      </div>
      
      
      <div className="relative group">
        <img src="/images/gallery/autumn-after.jpg" alt="After - Höstbröllop" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=After'" />
        <div className="absolute top-3 right-3 bg-pink-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Efter
        </div>
      </div>
    </div>
    
    
    <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 bg-white bg-opacity-90 px-3 py-1 rounded-full text-sm font-medium text-gray-700">
      Wedding
    </div>
  </div>
  
  <div className="p-6">
    <h3 className="text-xl font-bold text-gray-900 mb-3">Höstbröllop</h3>
    <p className="text-gray-600 text-sm leading-relaxed">Varma toner och säsongens färgprakt</p>
    
    <div className="flex justify-between items-center mt-4">
      <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
        Se fler bilder →
      </button>
      <button className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Inspireras
      </button>
    </div>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
  <div className="relative">
    <div className="grid grid-cols-2 gap-0">
      
      <div className="relative group">
        <img src="/images/gallery/winter-before.jpg" alt="Before - Vinterbröllop" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=Before'" />
        <div className="absolute top-3 left-3 bg-black bg-opacity-70 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Före
        </div>
      </div>
      
      
      <div className="relative group">
        <img src="/images/gallery/winter-after.jpg" alt="After - Vinterbröllop" 
             className="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
             onError="this.src='https://via.placeholder.com/400x300?text=After'" />
        <div className="absolute top-3 right-3 bg-pink-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
          Efter
        </div>
      </div>
    </div>
    
    
    <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 bg-white bg-opacity-90 px-3 py-1 rounded-full text-sm font-medium text-gray-700">
      Wedding
    </div>
  </div>
  
  <div className="p-6">
    <h3 className="text-xl font-bold text-gray-900 mb-3">Vinterbröllop</h3>
    <p className="text-gray-600 text-sm leading-relaxed">Magisk vinteratmosphär med ljus och elegans</p>
    
    <div className="flex justify-between items-center mt-4">
      <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
        Se fler bilder →
      </button>
      <button className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Inspireras
      </button>
    </div>
  </div>
</div>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Blomsterarrangemang</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Handplockade blommor som speglar er personlighet och tema</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Bordsdukning</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Perfekt koordinerade detaljer från servetter till centerpieces</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Ljussättning</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Romantisk atmosfär med genomtänkt belysning</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Små överraskningar</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Personliga detaljer som gör ert bröllop unikt</p>
    </div>
  </div>
</section>
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
  <div className="max-w-4xl mx-auto px-4 text-center">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">Inspirerad av det ni ser?</h2>
    <p className="text-xl text-blue-100 mb-8">Låt oss skapa något lika vackert för ert bröllop - boka en konsultation idag</p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Diskutera idéer
      </Link>
    </div>
  </div>
</section>
    </>
  );
}
