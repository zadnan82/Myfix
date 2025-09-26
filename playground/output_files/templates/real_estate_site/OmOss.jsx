import React from 'react';
import { Link } from 'react-router-dom';

export default function Real_Estate_SiteOmossPage() {
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
      <p>Din pålitliga partner på fastighetsmarknaden sedan 1995</p>
      <section className="relative bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 text-white min-h-screen flex items-center">
  <div className="absolute inset-0 bg-black opacity-20"></div>
  <div className="relative z-10 max-w-6xl mx-auto px-4 py-20 text-center">
    <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
      25 år av expertis och förtroende
    </h1>
    <h2 className="text-xl md:text-2xl font-light mb-8 text-blue-100 max-w-3xl mx-auto">
      Vi är Stockholms ledande fastighetsmäklare med djup lokalkännedom och ett starkt nätverk av nöjda kunder
    </h2>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-semibold px-8 py-4 rounded-lg text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Kontakta oss
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
      <p>Från familjeföretag till marknadsledare</p>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Grundat 1995</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Startades som ett familjeföretag med fokus på personlig service och lokal expertis</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Kontinuerlig tillväxt</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Över 5000 framgångsrika fastighetsaffärer och tusentals nöjda kunder</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Marknadsledare</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Idag en av Stockholms mest respekterade fastighetsmäklare med stark marknadsposition</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Innovation</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Pionjärer inom digital marknadsföring och modern fastighetsteknik</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl">
  <div className="flex items-center mb-4">
    <div className="w-16 h-16 rounded-full bg-gray-200 mr-4 overflow-hidden">
      <img src="/images/agents/anna-svensson.jpg" alt="Anna Svensson" 
           className="w-full h-full object-cover"
           onError="this.src='https://via.placeholder.com/64x64?text=Agent'" />
    </div>
    <div>
      <h3 className="text-xl font-bold text-gray-900">Anna Svensson</h3>
      <p className="text-blue-600 font-semibold">VD & Auktoriserad fastighetsmäklare</p>
      <p className="text-gray-600 text-sm">25 år</p>
    </div>
  </div>
  
  <div className="mb-4">
    <h4 className="text-sm font-semibold text-gray-700 mb-2">Specialiteter:</h4>
    <div className="flex flex-wrap"><span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full mr-1 mb-1">[Lyxfastigheter</span></div>
  </div>
  
  <div className="border-t border-gray-200 pt-4">
    <div className="flex justify-between items-center">
      <div>
        <p className="text-sm text-gray-600">+46 8 555 123 45</p>
        <p className="text-sm text-gray-600">anna@stockholmsfastighet.se</p>
      </div>
      <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Kontakta
      </button>
    </div>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl">
  <div className="flex items-center mb-4">
    <div className="w-16 h-16 rounded-full bg-gray-200 mr-4 overflow-hidden">
      <img src="/images/agents/erik-johansson.jpg" alt="Erik Johansson" 
           className="w-full h-full object-cover"
           onError="this.src='https://via.placeholder.com/64x64?text=Agent'" />
    </div>
    <div>
      <h3 className="text-xl font-bold text-gray-900">Erik Johansson</h3>
      <p className="text-blue-600 font-semibold">Senior fastighetsmäklare</p>
      <p className="text-gray-600 text-sm">18 år</p>
    </div>
  </div>
  
  <div className="mb-4">
    <h4 className="text-sm font-semibold text-gray-700 mb-2">Specialiteter:</h4>
    <div className="flex flex-wrap"><span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full mr-1 mb-1">[Villor</span></div>
  </div>
  
  <div className="border-t border-gray-200 pt-4">
    <div className="flex justify-between items-center">
      <div>
        <p className="text-sm text-gray-600">+46 8 555 123 46</p>
        <p className="text-sm text-gray-600">erik@stockholmsfastighet.se</p>
      </div>
      <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Kontakta
      </button>
    </div>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl">
  <div className="flex items-center mb-4">
    <div className="w-16 h-16 rounded-full bg-gray-200 mr-4 overflow-hidden">
      <img src="/images/agents/maria-lindberg.jpg" alt="Maria Lindberg" 
           className="w-full h-full object-cover"
           onError="this.src='https://via.placeholder.com/64x64?text=Agent'" />
    </div>
    <div>
      <h3 className="text-xl font-bold text-gray-900">Maria Lindberg</h3>
      <p className="text-blue-600 font-semibold">Fastighetsmäklare</p>
      <p className="text-gray-600 text-sm">12 år</p>
    </div>
  </div>
  
  <div className="mb-4">
    <h4 className="text-sm font-semibold text-gray-700 mb-2">Specialiteter:</h4>
    <div className="flex flex-wrap"><span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full mr-1 mb-1">[Bostadsrätter</span></div>
  </div>
  
  <div className="border-t border-gray-200 pt-4">
    <div className="flex justify-between items-center">
      <div>
        <p className="text-sm text-gray-600">+46 8 555 123 47</p>
        <p className="text-sm text-gray-600">maria@stockholmsfastighet.se</p>
      </div>
      <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Kontakta
      </button>
    </div>
  </div>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl">
  <div className="flex items-center mb-4">
    <div className="w-16 h-16 rounded-full bg-gray-200 mr-4 overflow-hidden">
      <img src="/images/agents/david-andersson.jpg" alt="David Andersson" 
           className="w-full h-full object-cover"
           onError="this.src='https://via.placeholder.com/64x64?text=Agent'" />
    </div>
    <div>
      <h3 className="text-xl font-bold text-gray-900">David Andersson</h3>
      <p className="text-blue-600 font-semibold">Fastighetsmäklare</p>
      <p className="text-gray-600 text-sm">8 år</p>
    </div>
  </div>
  
  <div className="mb-4">
    <h4 className="text-sm font-semibold text-gray-700 mb-2">Specialiteter:</h4>
    <div className="flex flex-wrap"><span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full mr-1 mb-1">[Nyproduktion</span></div>
  </div>
  
  <div className="border-t border-gray-200 pt-4">
    <div className="flex justify-between items-center">
      <div>
        <p className="text-sm text-gray-600">+46 8 555 123 48</p>
        <p className="text-sm text-gray-600">david@stockholmsfastighet.se</p>
      </div>
      <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm transition-colors duration-300">
        Kontakta
      </button>
    </div>
  </div>
</div>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Integritet</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Vi arbetar alltid med transparens och ärlighet i alla våra affärer</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Expertis</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Kontinuerlig utbildning och djup marknadskunskap för bästa resultat</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Personlig service</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Varje kund får skräddarsydd service anpassad efter individuella behov</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Resultat</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Vi levererar konkreta resultat och överträffar våra kunders förväntningar</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Stockholm City</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Expertis inom Stockholms innerstad med fokus på exklusiva bostadsrätter</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Södermalm</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Djup kunskap om Söders unika karaktär och trendsättande fastigheter</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Östermalm</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Specialister på lyxfastigheter och prestigefulla adresser</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Vasastan</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Expertis inom klassiska sekelskifteslägenheter och familjevänliga områden</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Kranskommuner</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Omfattande kunskap om villor och radhus i Stockholms kranskommuner</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Säljuppdrag</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Fullservice försäljning från värdering till slutbesked med garanterat resultat</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Köpstöd</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Professionell hjälp att hitta och förvärva din drömfastighet</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Värderingar</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Kostnadsfria och professionella värderingar baserade på marknadsdata</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Investeringsrådgivning</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Strategisk rådgivning för fastighetsinvesteringar och portföljuppbyggnad</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Kommersiella fastigheter</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Specialisttjänster för kommersiella fastigheter och affärslokaler</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  
  <div className="flex justify-between items-start mb-2">
    <h3 className="text-lg font-semibold text-gray-900 flex-1">Genomsnittlig försäljningstid</h3>
    
  </div>
  
  <div className="flex items-baseline mb-1">
    <span className="text-3xl font-bold text-blue-600">28</span>
    <span className="text-lg text-gray-600 ml-1">dagar</span>
  </div>
  
  
  <p className="text-sm text-gray-600 mt-2">Snabbare än marknadsgenomsnittet på 45 dagar</p>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  
  <div className="flex justify-between items-start mb-2">
    <h3 className="text-lg font-semibold text-gray-900 flex-1">Slutpris vs utgångspris</h3>
    
  </div>
  
  <div className="flex items-baseline mb-1">
    <span className="text-3xl font-bold text-blue-600">102</span>
    <span className="text-lg text-gray-600 ml-1">%</span>
  </div>
  
  
  <p className="text-sm text-gray-600 mt-2">Vi uppnår i genomsnitt 102% av utgångspriset</p>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  
  <div className="flex justify-between items-start mb-2">
    <h3 className="text-lg font-semibold text-gray-900 flex-1">Kundnöjdhet</h3>
    
  </div>
  
  <div className="flex items-baseline mb-1">
    <span className="text-3xl font-bold text-blue-600">98</span>
    <span className="text-lg text-gray-600 ml-1">%</span>
  </div>
  
  
  <p className="text-sm text-gray-600 mt-2">98% av våra kunder rekommenderar oss till vänner</p>
</div>
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
  
  <div className="flex justify-between items-start mb-2">
    <h3 className="text-lg font-semibold text-gray-900 flex-1">Marknadsandel Stockholm</h3>
    
  </div>
  
  <div className="flex items-baseline mb-1">
    <span className="text-3xl font-bold text-blue-600">15</span>
    <span className="text-lg text-gray-600 ml-1">%</span>
  </div>
  
  
  <p className="text-sm text-gray-600 mt-2">Ledande position på Stockholms fastighetsmarknad</p>
</div>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Fastighetsmäklarförbundet</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Medlemmar i Sveriges Fastighetsmäklarförbund med alla etiska riktlinjer</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Svensk Fastighetsförmedling</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Anslutna till branschorganisationen för kvalitetssäkring</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Kontinuerlig utbildning</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Regelbunden fortbildning för att hålla högsta kompetensnivå</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Försäkringsskydd</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Fullständigt försäkringsskydd för alla uppdrag och transaktioner</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Centralt läge</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Kungsgatan 42 i hjärtat av Stockholm med utmärkt tillgänglighet</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Moderna faciliteter</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Fullt utrustat kontor med mötesrum och presentationsutrustning</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Öppettider</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Måndag-Fredag 08:00-18:00, Lördag 10:00-15:00</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Parkering</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Besöksparkering finns tillgänglig i närheten av kontoret</p>
    </div>
  </div>
</section>
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
  <div className="max-w-4xl mx-auto px-4 text-center">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">Redo att arbeta med experterna?</h2>
    <p className="text-xl text-blue-100 mb-8">Kontakta oss idag för en kostnadsfri konsultation om dina fastighetsbehov</p>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-bold px-8 py-4 rounded-xl text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Kontakta oss nu
      </Link>
    </div>
  </div>
</section>
    </>
  );
}
