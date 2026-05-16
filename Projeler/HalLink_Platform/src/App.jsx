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
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

const App = () => {
  const [view, setView] = useState('landing'); // landing, register, dashboard, admin
  const [userRole, setUserRole] = useState(null); // komisyoncu, tuccar
  const [isAdminAuthenticated, setIsAdminAuthenticated] = useState(false);
  const [adminPassword, setAdminPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    address: '',
    products: ''
  });
  const [listings, setListings] = useState([]);

  // Fetch listings from Supabase
  useEffect(() => {
    fetchListings();
  }, []);

  const fetchListings = async () => {
    setLoading(true);
    const { data, error } = await supabase
      .from('listings')
      .select('*')
      .order('created_at', { ascending: false });
    
    if (data) setListings(data);
    setLoading(false);
  };

  const handleAdminLogin = (e) => {
    e.preventDefault();
    if (adminPassword === '8888') {
      setIsAdminAuthenticated(true);
      setError('');
    } else {
      setError('Hatalı Şifre!');
      setAdminPassword('');
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    const newListing = {
      role: userRole,
      name: formData.name,
      phone: formData.phone,
      address: formData.address,
      products: formData.products,
      date: new Date().toISOString().split('T')[0]
    };

    const { data, error } = await supabase
      .from('listings')
      .insert([newListing])
      .select();

    if (error) {
      alert('Veritabanı hatası: ' + error.message);
    } else {
      setListings([data[0], ...listings]);
      setView('dashboard');
    }
  };

  const deleteListing = async (id) => {
    const { error } = await supabase
      .from('listings')
      .delete()
      .eq('id', id);

    if (error) {
      alert('Silme hatası: ' + error.message);
    } else {
      setListings(listings.filter(item => item.id !== id));
    }
  };

  const AdminDashboard = () => {
    const stats = {
      total: listings.length,
      brokers: listings.filter(i => i.role === 'komisyoncu').length,
      traders: listings.filter(i => i.role === 'tuccar').length
    };

    if (!isAdminAuthenticated) {
      return (
        <div className="container" style={{ maxWidth: '400px', padding: '6rem 0' }}>
          <div className="glass-card animate-fade-in" style={{ textAlign: 'center' }}>
            <div style={{ background: 'rgba(255,255,255,0.05)', width: '60px', height: '60px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.5rem' }}>
              <Users size={30} color="var(--primary)" />
            </div>
            <h2 style={{ marginBottom: '1.5rem' }}>Yönetim Girişi</h2>
            <form onSubmit={handleAdminLogin} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <input 
                type="password" 
                placeholder="Admin Şifresi" 
                value={adminPassword}
                onChange={e => setAdminPassword(e.target.value)}
                style={{ textAlign: 'center', fontSize: '1.2rem', letterSpacing: '0.5rem' }}
                autoFocus
              />
              {error && <div style={{ color: '#ff4757', fontSize: '0.8rem' }}>{error}</div>}
              <button type="submit" className="btn btn-primary" style={{ justifyContent: 'center' }}>
                Giriş Yap
              </button>
              <button type="button" className="btn btn-secondary" onClick={() => setView('landing')} style={{ justifyContent: 'center' }}>
                İptal
              </button>
            </form>
          </div>
        </div>
      );
    }

    return (
      <div className="container animate-fade-in" style={{ padding: '2rem 0' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem' }}>
          <div>
            <h2 className="gradient-text" style={{ fontSize: '2rem' }}>Yönetim Paneli</h2>
            <p style={{ color: 'var(--text-muted)' }}>Sistem genel durumu ve üye yönetimi.</p>
          </div>
          <div style={{ display: 'flex', gap: '1rem' }}>
            <button className="btn btn-secondary" onClick={() => { setIsAdminAuthenticated(false); setView('landing'); }}>
              Çıkış Yap
            </button>
            <button className="btn btn-primary" onClick={() => setView('dashboard')}>
              Pazaryerine Dön
            </button>
          </div>
        </div>

        {/* Stats Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem', marginBottom: '3rem' }}>
          {[
            { label: 'Toplam Üye', value: stats.total, icon: <Users />, color: 'var(--text)' },
            { label: 'Komisyoncu', value: stats.brokers, icon: <Users />, color: 'var(--primary)' },
            { label: 'Tüccar', value: stats.traders, icon: <Store />, color: 'var(--secondary)' },
          ].map((stat, idx) => (
            <div key={idx} className="glass-card" style={{ textAlign: 'center', padding: '1.5rem' }}>
              <div style={{ color: stat.color, marginBottom: '0.5rem', display: 'flex', justifyContent: 'center' }}>{stat.icon}</div>
              <div style={{ fontSize: '2rem', fontWeight: 800, color: stat.color }}>{stat.value}</div>
              <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Table */}
        <div className="glass-card" style={{ padding: '0', overflow: 'hidden' }}>
          <div style={{ padding: '1.5rem', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between' }}>
            <h4 style={{ margin: 0 }}>Üye Listesi</h4>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Son Güncelleme: {new Date().toLocaleTimeString()}</div>
          </div>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
              <thead>
                <tr style={{ background: 'rgba(255,255,255,0.02)', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                  <th style={{ padding: '1rem 1.5rem' }}>Üye / Ünvan</th>
                  <th style={{ padding: '1rem' }}>Sıfat</th>
                  <th style={{ padding: '1rem' }}>Ürünler</th>
                  <th style={{ padding: '1rem' }}>Tarih</th>
                  <th style={{ padding: '1rem', textAlign: 'right' }}>İşlem</th>
                </tr>
              </thead>
              <tbody>
                {listings.map(item => (
                  <tr key={item.id} style={{ borderBottom: '1px solid var(--border)' }}>
                    <td style={{ padding: '1rem 1.5rem' }}>
                      <div style={{ fontWeight: 600 }}>{item.name}</div>
                      <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{item.phone}</div>
                    </td>
                    <td style={{ padding: '1rem' }}>
                      <span style={{ fontSize: '0.7rem', padding: '2px 8px', borderRadius: '4px', background: item.role === 'komisyoncu' ? 'rgba(46, 204, 113, 0.1)' : 'rgba(230, 126, 34, 0.1)', color: item.role === 'komisyoncu' ? 'var(--primary)' : 'var(--secondary)' }}>
                        {item.role.toUpperCase()}
                      </span>
                    </td>
                    <td style={{ padding: '1rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>{item.products}</td>
                    <td style={{ padding: '1rem', fontSize: '0.9rem' }}>{item.date}</td>
                    <td style={{ padding: '1rem', textAlign: 'right' }}>
                      <button 
                        onClick={() => deleteListing(item.id)}
                        style={{ background: 'none', border: 'none', color: '#ff4757', cursor: 'pointer', fontSize: '0.8rem' }}
                      >
                        Sil
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  };

  const LandingPage = () => (
    <div className="container animate-fade-in" style={{ padding: '4rem 0' }}>
      {/* Unity Banner */}
      <motion.div 
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="glass-card"
        style={{ 
          marginBottom: '4rem', 
          padding: '0', 
          overflow: 'hidden', 
          display: 'flex', 
          flexDirection: 'row',
          background: 'linear-gradient(135deg, rgba(46, 204, 113, 0.1), rgba(230, 126, 34, 0.1))',
          minHeight: '400px'
        }}
      >
        <div style={{ flex: 1, padding: '3rem', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <h2 className="gradient-text" style={{ fontSize: '3rem', marginBottom: '1rem', lineHeight: 1.1 }}>
            Piyasanın Kalbi <br/>Burada Atıyor
          </h2>
          <p style={{ fontSize: '1.1rem', color: 'var(--text-muted)', lineHeight: '1.6', maxWidth: '500px' }}>
            Çiftçimiz üretiyor, komisyoncumuz dengeliyor, tüccarımız değer katıyor. 
            Güven ve şeffaflık üzerine kurulu geleceğin hal piyasasını birlikte inşa ediyoruz.
          </p>
          <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
            <div style={{ background: 'rgba(46, 204, 113, 0.1)', color: 'var(--primary)', padding: '0.5rem 1rem', borderRadius: '8px', fontSize: '0.8rem', fontWeight: 600, border: '1px solid rgba(46, 204, 113, 0.2)' }}>Şeffaf Ticaret</div>
            <div style={{ background: 'rgba(230, 126, 34, 0.1)', color: 'var(--secondary)', padding: '0.5rem 1rem', borderRadius: '8px', fontSize: '0.8rem', fontWeight: 600, border: '1px solid rgba(230, 126, 34, 0.2)' }}>Güçlü İş Birliği</div>
          </div>
        </div>
        <div style={{ flex: 2, position: 'relative' }}>
          <img 
            src="/assets/trust.png" 
            alt="Piyasa Birliği" 
            style={{ 
              width: '100%', 
              height: '100%', 
              objectFit: 'cover',
              maskImage: 'linear-gradient(to left, black 80%, transparent 100%)',
              WebkitMaskImage: 'linear-gradient(to left, black 80%, transparent 100%)'
            }} 
          />
        </div>
      </motion.div>

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
      
      <div style={{ textAlign: 'center', marginTop: '4rem' }}>
        <span 
          style={{ fontSize: '0.8rem', color: 'var(--border)', cursor: 'pointer' }}
          onDoubleClick={() => setView('admin')}
        >
          Sistem Yönetimi
        </span>
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
          <button className="btn btn-secondary" onClick={() => setView('admin')} style={{ fontSize: '0.8rem', padding: '0.5rem 1rem' }}>
            Yönetim
          </button>
          <div className="glass-card" style={{ padding: '0.5rem 1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: 'var(--primary)' }}></div>
            <span style={{ fontSize: '0.9rem' }}>Aktif</span>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '1.5rem' }}>
        {loading ? (
          <div style={{ gridColumn: '1/-1', textAlign: 'center', padding: '4rem' }}>
            <div className="loader" style={{ margin: '0 auto 1rem' }}></div>
            <p style={{ color: 'var(--text-muted)' }}>İlanlar yükleniyor...</p>
          </div>
        ) : listings.length === 0 ? (
          <div style={{ gridColumn: '1/-1', textAlign: 'center', padding: '4rem' }}>
            <p style={{ color: 'var(--text-muted)' }}>Henüz ilan bulunmuyor.</p>
          </div>
        ) : (
          listings.map(item => (
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
          ))
        )}
      </div>
    </div>
  );

  return (
    <div style={{ minHeight: '100vh' }}>
      <nav style={{ padding: '1.5rem 2rem', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 800, cursor: 'pointer' }} onClick={() => setView('landing')}>HalLink</h2>
        <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
          <span style={{ color: 'var(--text-muted)', fontSize: '0.9rem', cursor: 'pointer' }} onClick={() => setView('landing')}>Anasayfa</span>
          <span style={{ color: 'var(--text-muted)', fontSize: '0.9rem', cursor: 'pointer' }}>Yardım</span>
          {view !== 'landing' && (
            <div 
              style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'var(--card-bg)', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer' }}
              onClick={() => setView('admin')}
            >
              <User size={20} />
            </div>
          )}
        </div>
      </nav>

      <AnimatePresence mode="wait">
        {view === 'landing' && <LandingPage key="landing" />}
        {view === 'register' && <RegisterPage key="register" />}
        {view === 'dashboard' && <DashboardPage key="dashboard" />}
        {view === 'admin' && <AdminDashboard key="admin" />}
      </AnimatePresence>

      <footer style={{ marginTop: '4rem', padding: '4rem 0', borderTop: '1px solid var(--border)', textAlign: 'center' }}>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>© 2026 HalLink Platformu. Tüm hakları saklıdır.</p>
      </footer>
    </div>
  );
};


export default App;
