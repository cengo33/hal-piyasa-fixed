import React, { useState, useEffect } from 'react';
import { 
  Users, 
  Store, 
  Phone, 
  MapPin, 
  ChevronRight, 
  CheckCircle, 
  ArrowRight, 
  Search,
  MessageSquare,
  Package,
  User,
  Plus
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const App = () => {
  const [view, setView] = useState('landing'); // landing, register, dashboard
  const [userRole, setUserRole] = useState(null); // komisyoncu, tuccar
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    address: '',
    products: ''
  });
  const [listings, setListings] = useState([
    { id: 1, role: 'komisyoncu', name: 'Mersin Tarım Ticaret', products: 'Domates, Biber, Salatalık', phone: '05330000000', address: 'Mersin Hal Kompleksi No: 12' },
    { id: 2, role: 'tuccar', name: 'Ankara Gıda Ltd', products: 'Limon, Mandalina', phone: '05440000000', address: 'Ankara Toptancı Hali' },
    { id: 3, role: 'komisyoncu', name: 'Kurtuluş Sebze', products: 'Patlıcan, Kabak', phone: '05550000000', address: 'Mersin Hal No: 45' },
  ]);

  const handleRegister = (e) => {
    e.preventDefault();
    const newUser = {
      id: Date.now(),
      role: userRole,
      ...formData
    };
    setListings([newUser, ...listings]);
    setView('dashboard');
  };

  const LandingPage = () => (
    <div className="container animate-fade-in" style={{ padding: '4rem 0' }}>
      <div style={{ textAlign: 'center', marginBottom: '4rem' }}>
        <h1 className="gradient-text" style={{ fontSize: '4rem', fontWeight: 800, lineHeight: 1.1 }}>
          HalLink
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.2rem', marginTop: '1rem', maxWidth: '600px', margin: '1rem auto' }}>
          Mersin Hal'inin dijital köprüsü. Komisyoncular ve tüccarlar için en hızlı ve güvenilir buluşma noktası.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div style={{ background: 'rgba(46, 204, 113, 0.1)', width: '60px', height: '60px', borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Users color="var(--primary)" size={32} />
          </div>
          <h3>Komisyoncuyum</h3>
          <p style={{ color: 'var(--text-muted)' }}>Ürünlerimi sergilemek ve güvenilir tüccarlarla tanışmak istiyorum.</p>
          <button className="btn btn-primary" onClick={() => { setUserRole('komisyoncu'); setView('register'); }}>
            Giriş Yap <ArrowRight size={18} />
          </button>
        </div>

        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div style={{ background: 'rgba(230, 126, 34, 0.1)', width: '60px', height: '60px', borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Store color="var(--secondary)" size={32} />
          </div>
          <h3>Tüccarım</h3>
          <p style={{ color: 'var(--text-muted)' }}>İhtiyacım olan ürünleri en iyi komisyonculardan bulmak istiyorum.</p>
          <button className="btn btn-secondary" onClick={() => { setUserRole('tuccar'); setView('register'); }}>
            İlanları Gör <ArrowRight size={18} />
          </button>
        </div>
      </div>
    </div>
  );

  const RegisterPage = () => (
    <div className="container" style={{ maxWidth: '500px', padding: '4rem 0' }}>
      <div className="glass-card animate-fade-in">
        <h2 style={{ marginBottom: '2rem' }}>Profilini Oluştur</h2>
        <form onSubmit={handleRegister} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>Ticari Ünvan</label>
            <input 
              required 
              placeholder="Örn: Akdeniz Tarım Ltd" 
              value={formData.name}
              onChange={e => setFormData({...formData, name: e.target.value})}
            />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>Telefon Numarası</label>
            <input 
              required 
              type="tel" 
              placeholder="05XX XXX XX XX" 
              value={formData.phone}
              onChange={e => setFormData({...formData, phone: e.target.value})}
            />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>Adres / Hal No</label>
            <input 
              required 
              placeholder="Örn: Mersin Hal Kompleksi No: 120" 
              value={formData.address}
              onChange={e => setFormData({...formData, address: e.target.value})}
            />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
              {userRole === 'komisyoncu' ? 'Sattığınız Ürünler' : 'İlgilendiğiniz Ürünler'}
            </label>
            <textarea 
              rows="3" 
              placeholder="Örn: Domates, Biber, Patlıcan..." 
              value={formData.products}
              onChange={e => setFormData({...formData, products: e.target.value})}
              style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border)', borderRadius: '12px', padding: '1rem', color: 'white', width: '100%' }}
            />
          </div>
          <button type="submit" className="btn btn-primary" style={{ justifyContent: 'center' }}>
            Kaydol ve Başla
          </button>
        </form>
      </div>
    </div>
  );

  const DashboardPage = () => (
    <div className="container" style={{ padding: '2rem 0' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem' }}>
        <div>
          <h2 className="gradient-text">Ticaret Pazarı</h2>
          <p style={{ color: 'var(--text-muted)' }}>Size uygun {userRole === 'komisyoncu' ? 'tüccarları' : 'komisyoncuları'} bulun.</p>
        </div>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <div className="glass-card" style={{ padding: '0.5rem 1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: 'var(--primary)' }}></div>
            <span style={{ fontSize: '0.9rem' }}>Aktif</span>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '1.5rem' }}>
        {listings.map(item => (
          <motion.div 
            layout
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            key={item.id} 
            className="glass-card" 
            style={{ borderLeft: `4px solid ${item.role === 'komisyoncu' ? 'var(--primary)' : 'var(--secondary)'}` }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
              <span style={{ fontSize: '0.75rem', padding: '4px 12px', borderRadius: '20px', background: item.role === 'komisyoncu' ? 'rgba(46, 204, 113, 0.1)' : 'rgba(230, 126, 34, 0.1)', color: item.role === 'komisyoncu' ? 'var(--primary)' : 'var(--secondary)', fontWeight: 600 }}>
                {item.role.toUpperCase()}
              </span>
              <Phone size={16} color="var(--text-muted)" />
            </div>
            <h4 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>{item.name}</h4>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1rem' }}>
              <MapPin size={14} />
              {item.address}
            </div>
            <div style={{ background: 'rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '12px', marginBottom: '1.5rem' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.4rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <Package size={14} /> Ürünler:
              </div>
              <div style={{ fontWeight: 500 }}>{item.products}</div>
            </div>
            <div style={{ display: 'flex', gap: '0.8rem' }}>
              <a href={`https://wa.me/${item.phone}`} target="_blank" className="btn btn-primary" style={{ flex: 1, justifyContent: 'center', fontSize: '0.9rem' }}>
                <MessageSquare size={18} /> WhatsApp
              </a>
              <a href={`tel:${item.phone}`} className="btn btn-secondary" style={{ padding: '0.8rem' }}>
                <Phone size={18} />
              </a>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );

  return (
    <div style={{ minHeight: '100vh' }}>
      <nav style={{ padding: '1.5rem 2rem', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 800, cursor: 'pointer' }} onClick={() => setView('landing')}>HalLink</h2>
        <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
          <span style={{ color: 'var(--text-muted)', fontSize: '0.9rem', cursor: 'pointer' }}>Hakkımızda</span>
          <span style={{ color: 'var(--text-muted)', fontSize: '0.9rem', cursor: 'pointer' }}>Yardım</span>
          {view === 'dashboard' && (
            <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'var(--card-bg)', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <User size={20} />
            </div>
          )}
        </div>
      </nav>

      <AnimatePresence mode="wait">
        {view === 'landing' && <LandingPage key="landing" />}
        {view === 'register' && <RegisterPage key="register" />}
        {view === 'dashboard' && <DashboardPage key="dashboard" />}
      </AnimatePresence>

      <footer style={{ marginTop: '4rem', padding: '4rem 0', borderTop: '1px solid var(--border)', textAlign: 'center' }}>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>© 2026 HalLink Platformu. Tüm hakları saklıdır.</p>
      </footer>
    </div>
  );
};

export default App;
