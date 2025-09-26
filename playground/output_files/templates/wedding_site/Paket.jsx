import React from 'react';
import { Link } from 'react-router-dom';

export default function Wedding_SitePaketPage() {
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
      <p>Välj det paket som passar er dröm och budget</p>
      <section className="relative bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 text-white min-h-screen flex items-center">
  <div className="absolute inset-0 bg-black opacity-20"></div>
  <div className="relative z-10 max-w-6xl mx-auto px-4 py-20 text-center">
    <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
      Från intima ceremonier till storslagna fester
    </h1>
    <h2 className="text-xl md:text-2xl font-light mb-8 text-blue-100 max-w-3xl mx-auto">
      Vi erbjuder flexibla paket som kan anpassas efter era önskemål och behov
    </h2>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-semibold px-8 py-4 rounded-lg text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Jämför paket
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
      <div className="relative bg-gradient-to-br from-pink-50 to-rose-50 rounded-2xl shadow-xl border-2 border-pink-300 p-8 transition-all duration-300 hover:shadow-2xl transform hover:-translate-y-2">
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
            <div className="bg-pink-600 text-white px-4 py-1 rounded-full text-sm font-semibold flex items-center">
                <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                </svg>
                Mest populär
            </div>
        </div>
  <div className="text-center mb-8">
    <h3 className="text-3xl font-bold text-gray-900 mb-3">Romantisk start</h3>
    <p className="text-gray-600 mb-6 leading-relaxed">Perfekt för intima bröllop med närmaste familj och vänner</p>
    
    <div className="mb-6">
      <span className="text-5xl font-bold text-pink-600">45 000</span>
      <span className="text-gray-600 text-lg"> kr</span>
    </div>
    
    <div className="grid grid-cols-2 gap-4 mb-6">
      <div className="bg-white bg-opacity-50 rounded-lg p-3">
        <div className="text-2xl font-bold text-gray-900">50</div>
        <div className="text-sm text-gray-600">gäster</div>
      </div>
      <div className="bg-white bg-opacity-50 rounded-lg p-3">
        <div className="text-lg font-bold text-gray-900">6 timmar</div>
        <div className="text-sm text-gray-600">varaktighet</div>
      </div>
    </div>
  </div>
  
  <div className="mb-8">
    <h4 className="text-lg font-semibold text-gray-800 mb-4">Ingår i paketet:</h4>
    <ul className="space-y-2">
                <li className="flex items-start text-gray-600 mb-3">
                    <svg className="w-5 h-5 text-pink-500 mr-3 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                    </svg>
                    [Grundläggande planering
                </li>
    </ul>
  </div>
  
  <button className="w-full bg-pink-600 hover:bg-pink-700 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg">
    Välj detta paket
  </button>
  
  <div className="text-center mt-4">
    <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
      Anpassa paketet →
    </button>
  </div>
</div>
      <div className="relative bg-gradient-to-br from-pink-50 to-rose-50 rounded-2xl shadow-xl border-2 border-pink-300 p-8 transition-all duration-300 hover:shadow-2xl transform hover:-translate-y-2">
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
            <div className="bg-pink-600 text-white px-4 py-1 rounded-full text-sm font-semibold flex items-center">
                <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                </svg>
                Mest populär
            </div>
        </div>
  <div className="text-center mb-8">
    <h3 className="text-3xl font-bold text-gray-900 mb-3">Drömbröllopet</h3>
    <p className="text-gray-600 mb-6 leading-relaxed">Vårt mest populära paket med allt för en perfekt bröllopdag</p>
    
    <div className="mb-6">
      <span className="text-5xl font-bold text-pink-600">85 000</span>
      <span className="text-gray-600 text-lg"> kr</span>
    </div>
    
    <div className="grid grid-cols-2 gap-4 mb-6">
      <div className="bg-white bg-opacity-50 rounded-lg p-3">
        <div className="text-2xl font-bold text-gray-900">100</div>
        <div className="text-sm text-gray-600">gäster</div>
      </div>
      <div className="bg-white bg-opacity-50 rounded-lg p-3">
        <div className="text-lg font-bold text-gray-900">8 timmar</div>
        <div className="text-sm text-gray-600">varaktighet</div>
      </div>
    </div>
  </div>
  
  <div className="mb-8">
    <h4 className="text-lg font-semibold text-gray-800 mb-4">Ingår i paketet:</h4>
    <ul className="space-y-2">
                <li className="flex items-start text-gray-600 mb-3">
                    <svg className="w-5 h-5 text-pink-500 mr-3 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                    </svg>
                    [Fullständig planering
                </li>
    </ul>
  </div>
  
  <button className="w-full bg-pink-600 hover:bg-pink-700 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg">
    Välj detta paket
  </button>
  
  <div className="text-center mt-4">
    <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
      Anpassa paketet →
    </button>
  </div>
</div>
      <div className="relative bg-gradient-to-br from-pink-50 to-rose-50 rounded-2xl shadow-xl border-2 border-pink-300 p-8 transition-all duration-300 hover:shadow-2xl transform hover:-translate-y-2">
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
            <div className="bg-pink-600 text-white px-4 py-1 rounded-full text-sm font-semibold flex items-center">
                <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                </svg>
                Mest populär
            </div>
        </div>
  <div className="text-center mb-8">
    <h3 className="text-3xl font-bold text-gray-900 mb-3">Lyxig celebration</h3>
    <p className="text-gray-600 mb-6 leading-relaxed">Ultimata lyxupplevelsen för er stora dag</p>
    
    <div className="mb-6">
      <span className="text-5xl font-bold text-pink-600">150 000</span>
      <span className="text-gray-600 text-lg"> kr</span>
    </div>
    
    <div className="grid grid-cols-2 gap-4 mb-6">
      <div className="bg-white bg-opacity-50 rounded-lg p-3">
        <div className="text-2xl font-bold text-gray-900">150</div>
        <div className="text-sm text-gray-600">gäster</div>
      </div>
      <div className="bg-white bg-opacity-50 rounded-lg p-3">
        <div className="text-lg font-bold text-gray-900">10 timmar</div>
        <div className="text-sm text-gray-600">varaktighet</div>
      </div>
    </div>
  </div>
  
  <div className="mb-8">
    <h4 className="text-lg font-semibold text-gray-800 mb-4">Ingår i paketet:</h4>
    <ul className="space-y-2">
                <li className="flex items-start text-gray-600 mb-3">
                    <svg className="w-5 h-5 text-pink-500 mr-3 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                    </svg>
                    [Premiumplanering
                </li>
    </ul>
  </div>
  
  <button className="w-full bg-pink-600 hover:bg-pink-700 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg">
    Välj detta paket
  </button>
  
  <div className="text-center mt-4">
    <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
      Anpassa paketet →
    </button>
  </div>
</div>
      <div className="relative bg-gradient-to-br from-pink-50 to-rose-50 rounded-2xl shadow-xl border-2 border-pink-300 p-8 transition-all duration-300 hover:shadow-2xl transform hover:-translate-y-2">
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
            <div className="bg-pink-600 text-white px-4 py-1 rounded-full text-sm font-semibold flex items-center">
                <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                </svg>
                Mest populär
            </div>
        </div>
  <div className="text-center mb-8">
    <h3 className="text-3xl font-bold text-gray-900 mb-3">Destination wedding</h3>
    <p className="text-gray-600 mb-6 leading-relaxed">Magiskt bröllop på er drömplats utomlands</p>
    
    <div className="mb-6">
      <span className="text-5xl font-bold text-pink-600">120 000</span>
      <span className="text-gray-600 text-lg"> kr</span>
    </div>
    
    <div className="grid grid-cols-2 gap-4 mb-6">
      <div className="bg-white bg-opacity-50 rounded-lg p-3">
        <div className="text-2xl font-bold text-gray-900">75</div>
        <div className="text-sm text-gray-600">gäster</div>
      </div>
      <div className="bg-white bg-opacity-50 rounded-lg p-3">
        <div className="text-lg font-bold text-gray-900">3 dagar</div>
        <div className="text-sm text-gray-600">varaktighet</div>
      </div>
    </div>
  </div>
  
  <div className="mb-8">
    <h4 className="text-lg font-semibold text-gray-800 mb-4">Ingår i paketet:</h4>
    <ul className="space-y-2">
                <li className="flex items-start text-gray-600 mb-3">
                    <svg className="w-5 h-5 text-pink-500 mr-3 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                    </svg>
                    [Resplanering och koordinering
                </li>
    </ul>
  </div>
  
  <button className="w-full bg-pink-600 hover:bg-pink-700 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg">
    Välj detta paket
  </button>
  
  <div className="text-center mt-4">
    <button className="text-pink-600 hover:text-pink-700 font-semibold text-sm transition-colors duration-300">
      Anpassa paketet →
    </button>
  </div>
</div>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <p>Gör ert bröllop ännu mer speciellt</p>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Extra fotografi</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Förlovningsfotografering, brudparsbilder dagen innan, eller extra timmar på bröllopsdagen</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Videografi</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Professionell bröllopsvideo som fångar alla känslor och ögonblick</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Livemusik</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Akustisk musik under ceremonin, pianist under cocktails, eller liveband på festen</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Specialdekoration</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Temaspecifika dekorationer, extra blommor, eller unika installationer</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Gästaktiviteter</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Photobooth, spel, underhållning eller aktiviteter för barn</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Spa & skönhet</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Bröllopsspa för brudparet, makeup artist, eller frisör</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Flexibla paket</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Alla våra paket kan anpassas efter era specifika önskemål och behov</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Säsongsrabatter</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Specialpriser för bröllop under lågsäsong (november-mars)"</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Familjerabatt</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Rabatt för återkommande kunder eller familjemedlemmar</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Betalningsplan</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Flexibla betalningsalternativ för att sprida kostnaderna över tid</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Personlig konsultation</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Detaljerad planering och rådgivning från början till slut</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Leverantörskoordinering</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Vi hanterar all kommunikation med leverantörer och partners</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Tidsplanering</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Detaljerad timeline för en smidig bröllopdag</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Krisberedskap</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Vi har alltid backup-planer för oväntade situationer</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Obegränsad support</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Ni kan kontakta oss när som helst under planeringsprocessen</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <p>Transparent prissättning utan dolda kostnader</p>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Grundpris</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Paketpriset inkluderar alla listade tjänster för angivet antal gäster</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Extra gäster</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Tillägg per person: 450-850 kr beroende på paket och tjänster</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Helger och högsäsong</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Tillägg 15-25% för bröllop under maj-september och helger</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Resekostnader</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">För bröllop utanför Stockholm tillkommer resekostnader enligt självkostnadspris</p>
    </div>
  </div>
</section>
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
  <div className="max-w-4xl mx-auto px-4 text-center">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">Redo att börja planera?</h2>
    <p className="text-xl text-blue-100 mb-8">Kontakta oss för en kostnadsfri konsultation där vi diskuterar era drömmar och skapar ett skräddarsytt förslag</p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Boka konsultation nu
      </Link>
    </div>
  </div>
</section>
    </>
  );
}
