import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';

export default function Wedding_SiteKontaktPage() {
  const navigate = useNavigate();

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
      <p>Vi ser fram emot att höra om era drömmar</p>
      <section className="relative bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 text-white min-h-screen flex items-center">
  <div className="absolute inset-0 bg-black opacity-20"></div>
  <div className="relative z-10 max-w-6xl mx-auto px-4 py-20 text-center">
    <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
      Låt oss skapa magin tillsammans
    </h1>
    <h2 className="text-xl md:text-2xl font-light mb-8 text-blue-100 max-w-3xl mx-auto">
      Boka en kostnadsfri konsultation och låt oss diskutera hur vi kan göra ert bröllop perfekt
    </h2>
    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
      
      <Link to="/blog" className="bg-white text-blue-600 hover:bg-blue-50 font-semibold px-8 py-4 rounded-lg text-lg transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
        Boka nu
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
      <section className="py-12 bg-gray-50">
  <div className="max-w-2xl mx-auto px-4">
    <div className="text-center mb-8">
      <h2 className="text-3xl font-bold text-gray-900 mb-4">Berätta om ert drömbröllopet</h2>
      <p className="text-gray-600">We'd love to hear from you. Send us a message and we'll respond as soon as possible.</p>
    </div>
    
    <form className="bg-white rounded-lg shadow-md p-8">
      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
          <input 
            id="cf-name"
            name="name"
            type="text" 
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter your full name" 
            required 
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
          <input 
            id="cf-email"
            name="email"
            type="email" 
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter your email address" 
            required 
          />
        </div>
      </div>
      
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">Subject</label>
        <input 
          id="cf-subject"
          name="subject"
          type="text" 
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="What is this about?" 
          required 
        />
      </div>
      
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">Message</label>
        <textarea 
          id="cf-message"
          name="message"
          rows="5" 
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-vertical"
          placeholder="Tell us more about your inquiry..." 
          required
        ></textarea>
      </div>
      
      <button 
        type="button" 
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-md transition-colors duration-200"
         onClick={(event) => {const formData = {name: document.getElementById('cf-name').value, email: document.getElementById('cf-email').value, subject: document.getElementById('cf-subject').value, message: document.getElementById('cf-message').value}; const btn = event.target; btn.disabled = true; btn.textContent = 'Sending...';fetch('http://localhost:8000/api/contact', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(formData)}).then(response => response.json()).then(result => {console.log('Contact form response:', result); if (result.msg || result.message) {alert(result.msg || result.message); setTimeout(() => { navigate('/'); }, 2000);} btn.disabled = false; btn.textContent = 'Send Message';}).catch(error => {console.error('Contact form error:', error); alert('Error: Could not send message. Please try again.'); btn.disabled = false; btn.textContent = 'Send Message';});}}
      >
        Send Message
      </button>
    </form>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <p>Storgatan 15, 111 51 Stockholm, Sverige</p>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Besöksadress</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Centralt beläget i Stockholms hjärta med närhet till kollektivtrafik</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Öppettider</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Måndag-Fredag 09:00-17:00, Lördag efter överenskommelse</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Parkering</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Betalparkering på gatan och närliggande parkeringshus</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Telefon</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">+46 8 123 456 78 - Ring för akuta frågor eller snabb konsultation</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">E-post</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">info@drombröllopet.se - Skicka oss era frågor när som helst</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Nödkontakt</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">+46 70 123 456 78 - 24/7 support för våra kunder på bröllopsdagen</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Kostnadsfri första konsultation</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">60 minuters möte där vi diskuterar era drömmar och behov</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Hembesök</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Vi kommer gärna hem till er för en mer personlig konsultation</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Videokonsultation</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Perfekt för par som bor långt bort eller har tidsbrist</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Platsbesök</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Vi besöker gärna er tänkta vigselplats tillsammans med er</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Emma Andersson</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Huvudplanerare och grundare - Specialist på romantiska bröllop och destination weddings</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Sofia Lindberg</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Senior bröllopskoordinator - Expert på design och dekoration</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Marcus Holmberg</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Eventkoordinator - Ansvarig för logistik och leverantörsrelationer</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Instagram</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">@drombröllopet - Dagliga inspirationsbilder och bakom kulisserna</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Facebook</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Drömbröllopet Wedding Planning - Nyheter, tips och kundberättelser</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Pinterest</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Drömbröllopet Inspiration - Tusentals idéer för ert perfekta bröllop</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Svenska</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Vårt modersmål - vi erbjuder fullservice på svenska</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Engelska</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Flyt engelska för internationella par och destination weddings</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Franska</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Grundläggande franska för bröllop i Frankrike</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Stockholm</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Vårt huvudområde med full service och inga extra resekostnader</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Göteborg & Malmö</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Regelbundna uppdrag med lokala partnerskap</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Övriga Sverige</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Vi tar gärna uppdrag i hela Sverige med tillägg för resa</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Internationellt</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Specialister på destination weddings i Europa och tropiska områden</p>
    </div>
  </div>
</section>
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 text-left">Header</h1>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Hur långt i förväg bör vi boka?</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Vi rekommenderar 12-18 månader för stora bröllop, men kan ofta hjälpa till även med kortare varsel</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Vad kostar era tjänster?</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Våra paket börjar på 45 000 kr. Kontakta oss för en skräddarsydd offert</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Kan ni hjälpa med destination weddings?</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Ja, vi har stor erfarenhet av bröllop utomlands och samarbetar med lokala koordinatorer</p>
    </div>
  </div>
</section>
      <section className="py-16 bg-gray-50">
  <div className="max-w-7xl mx-auto px-4">
    <div className="text-center mb-12">
      <h2 className="text-4xl font-bold text-gray-900 mb-4">Vad händer om det regnar?</h2>
      <p className="text-xl text-gray-600 max-w-3xl mx-auto">Vi har alltid backup-planer och kan snabbt ställa om för väderomslag</p>
    </div>
  </div>
</section>
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
  <div className="max-w-4xl mx-auto px-4 text-center">
    <h2 className="text-4xl md:text-5xl font-bold mb-6">Redo att börja planera ert drömbröllopet?</h2>
    <p className="text-xl text-blue-100 mb-8">Kontakta oss idag för en kostnadsfri konsultation och låt oss skapa magin tillsammans</p>
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
