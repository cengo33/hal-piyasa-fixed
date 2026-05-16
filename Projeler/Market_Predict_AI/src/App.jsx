import React, { useState, useEffect } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area 
} from 'recharts';
import { 
  TrendingUp, TrendingDown, Activity, Zap, Info, ArrowUpRight, ArrowDownRight, RefreshCw, 
  BarChart3, PieChart, Lock, User, LayoutDashboard, Settings, LogOut, PlusCircle, Trash2
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// Mock Data for Hal Market
const INITIAL_MARKET_DATA = [
  { name: '08:00', price: 12.5, prediction: 12.6 },
  { name: '10:00', price: 13.2, prediction: 13.1 },
  { name: '12:00', price: 14.8, prediction: 14.5 },
  { name: '14:00', price: 14.2, prediction: 14.9 },
  { name: '16:00', price: 15.5, prediction: 15.8 },
  { name: '18:00', price: 16.1, prediction: 16.5 },
  { name: '20:00', price: 15.8, prediction: 17.2 },
];

const INITIAL_PRODUCTS = [
  { id: 1, name: 'Domates (Salkım)', price: '₺16.50', trend: '+4.2%', status: 'up', confidence: '89%' },
  { id: 2, name: 'Salatalık', price: '₺12.20', trend: '-2.1%', status: 'down', confidence: '72%' },
  { id: 3, name: 'Biber (Sivri)', price: '₺24.00', trend: '+1.5%', status: 'up', confidence: '65%' },
  { id: 4, name: 'Patlıcan', price: '₺18.40', trend: '+8.7%', status: 'up', confidence: '94%' },
];

const Login = ({ onLogin }) => {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (password === '8888') {
      onLogin();
    } else {
      setError('Hatalı şifre! Lütfen tekrar deneyin.');
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass-card" 
      style={{ maxWidth: '400px', margin: '100px auto', textAlign: 'center' }}
    >
      <div style={{ background: 'rgba(0, 210, 255, 0.1)', width: '64px', height: '64px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifySelf: 'center', marginBottom: '1.5rem' }}>
        <Lock size={32} color="var(--accent-primary)" style={{ margin: '0 auto' }} />
      </div>
      <h2 style={{ marginBottom: '0.5rem' }}>Admin Girişi</h2>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>Yönetim paneline erişmek için şifrenizi girin.</p>
      
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '1rem', textAlign: 'left' }}>
          <label style={{ display: 'block', fontSize: '0.8rem', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>ŞİFRE</label>
          <input 
            type="password" 
            placeholder="****" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoFocus
          />
        </div>
        {error && <p style={{ color: 'var(--danger)', fontSize: '0.8rem', marginBottom: '1rem' }}>{error}</p>}
        <button type="submit" className="btn-primary" style={{ width: '100%' }}>Giriş Yap</button>
      </form>
    </motion.div>
  );
};

const AdminDashboard = ({ products, setProducts, onLogout }) => {
  const [activeTab, setActiveTab] = useState('products');
  const [newProduct, setNewProduct] = useState({ name: '', price: '', trend: '', status: 'up', confidence: '' });

  const addProduct = () => {
    if (!newProduct.name || !newProduct.price) return;
    setProducts([...products, { ...newProduct, id: Date.now() }]);
    setNewProduct({ name: '', price: '', trend: '', status: 'up', confidence: '' });
  };

  const deleteProduct = (id) => {
    setProducts(products.filter(p => p.id !== id));
  };

  return (
    <div className="animate-fade">
      <header>
        <div className="logo">
          <LayoutDashboard size={32} />
          <span>ADMİN PANELİ</span>
        </div>
        <button onClick={onLogout} className="btn-secondary" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.5rem 1rem' }}>
          <LogOut size={18} /> Çıkış Yap
        </button>
      </header>

      <div className="admin-nav">
        <div 
          className={`admin-nav-item ${activeTab === 'products' ? 'active' : ''}`}
          onClick={() => setActiveTab('products')}
        >
          Ürün Yönetimi
        </div>
        <div 
          className={`admin-nav-item ${activeTab === 'stats' ? 'active' : ''}`}
          onClick={() => setActiveTab('stats')}
        >
          İstatistikler
        </div>
        <div 
          className={`admin-nav-item ${activeTab === 'settings' ? 'active' : ''}`}
          onClick={() => setActiveTab('settings')}
        >
          Sistem Ayarları
        </div>
      </div>

      <div className="glass-card">
        {activeTab === 'products' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
              <h3>Kayıtlı Ürünler</h3>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <input 
                  placeholder="Ürün Adı" 
                  value={newProduct.name}
                  onChange={(e) => setNewProduct({...newProduct, name: e.target.value})}
                  style={{ padding: '0.5rem' }}
                />
                <input 
                  placeholder="Fiyat (₺)" 
                  value={newProduct.price}
                  onChange={(e) => setNewProduct({...newProduct, price: e.target.value})}
                  style={{ padding: '0.5rem' }}
                />
                <button onClick={addProduct} className="btn-primary" style={{ padding: '0.5rem 1.5rem' }}>
                  <PlusCircle size={20} />
                </button>
              </div>
            </div>

            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--glass-border)', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                  <th style={{ padding: '1rem' }}>ÜRÜN</th>
                  <th style={{ padding: '1rem' }}>FİYAT</th>
                  <th style={{ padding: '1rem' }}>TREND</th>
                  <th style={{ padding: '1rem' }}>GÜVEN</th>
                  <th style={{ padding: '1rem' }}>İŞLEM</th>
                </tr>
              </thead>
              <tbody>
                {products.map(prod => (
                  <tr key={prod.id} style={{ borderBottom: '1px solid var(--glass-border)' }}>
                    <td style={{ padding: '1rem' }}>{prod.name}</td>
                    <td style={{ padding: '1rem' }}>{prod.price}</td>
                    <td style={{ padding: '1rem' }}>
                      <span className={`badge ${prod.status === 'up' ? 'badge-up' : 'badge-down'}`}>{prod.trend}</span>
                    </td>
                    <td style={{ padding: '1rem' }}>{prod.confidence}</td>
                    <td style={{ padding: '1rem' }}>
                      <button onClick={() => deleteProduct(prod.id)} style={{ background: 'none', border: 'none', color: 'var(--danger)', cursor: 'pointer' }}>
                        <Trash2 size={18} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === 'stats' && (
          <div style={{ textAlign: 'center', padding: '3rem' }}>
            <Activity size={48} color="var(--accent-primary)" style={{ marginBottom: '1rem' }} />
            <h3>Piyasa Verileri Yükleniyor...</h3>
            <p style={{ color: 'var(--text-secondary)' }}>Bu modül bir sonraki güncelleme ile aktif olacaktır.</p>
          </div>
        )}

        {activeTab === 'settings' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            <h3>Genel Ayarlar</h3>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', background: 'rgba(255,255,255,0.02)', borderRadius: '12px' }}>
              <div>
                <h4>Otomatik Güncelleme</h4>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Fiyatları her 15 dakikada bir otomatik yenile.</p>
              </div>
              <div style={{ width: '40px', height: '20px', background: 'var(--success)', borderRadius: '10px' }}></div>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', background: 'rgba(255,255,255,0.02)', borderRadius: '12px' }}>
              <div>
                <h4>Yapay Zeka Modeli</h4>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Kullanılan model: GPT-4 Market Predictor V3</p>
              </div>
              <button className="btn-secondary" style={{ padding: '0.5rem' }}>Değiştir</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

const MainApp = ({ products, onAdminClick }) => {
  const [selectedProduct, setSelectedProduct] = useState(products[0] || {});
  const [isRefreshing, setIsRefreshing] = useState(false);

  useEffect(() => {
    if (products.length > 0 && !selectedProduct.id) {
      setSelectedProduct(products[0]);
    }
  }, [products]);

  const refreshData = () => {
    setIsRefreshing(true);
    setTimeout(() => setIsRefreshing(false), 1500);
  };

  return (
    <div className="animate-fade">
      {/* Header */}
      <header>
        <div className="logo">
          <Zap size={32} />
          <span>HAL PREDICT AI</span>
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <button 
            onClick={onAdminClick}
            style={{ background: 'none', border: '1px solid var(--glass-border)', color: 'white', padding: '0.5rem 1rem', borderRadius: '8px', cursor: 'pointer', fontSize: '0.8rem' }}
          >
            Admin Paneli
          </button>
          <div className="glass-card" style={{ padding: '0.5rem 1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Activity size={16} className="text-gradient" />
            <span style={{ fontSize: '0.8rem', fontWeight: '600' }}>Canlı Veri Aktif</span>
          </div>
          <button 
            onClick={refreshData}
            style={{ 
              background: 'none', border: 'none', color: 'white', cursor: 'pointer',
              animation: isRefreshing ? 'spin 1s linear infinite' : 'none'
            }}
          >
            <RefreshCw size={24} />
          </button>
        </div>
      </header>

      <div className="dashboard-grid">
        {/* Main Prediction Chart */}
        <div className="col-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card"
            style={{ height: '500px', display: 'flex', flexDirection: 'column' }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem' }}>
              <div>
                <h3 style={{ fontSize: '1.5rem' }}>{selectedProduct.name} Analizi</h3>
                <p style={{ color: 'var(--text-secondary)' }}>Son 24 Saatlik Trend ve Gelecek Tahmini</p>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '1.5rem', fontWeight: '700' }}>{selectedProduct.price}</div>
                <div className={`badge ${selectedProduct.status === 'up' ? 'badge-up' : 'badge-down'}`}>
                  {selectedProduct.trend}
                </div>
              </div>
            </div>

            <div style={{ flex: 1, width: '100%' }}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={INITIAL_MARKET_DATA}>
                  <defs>
                    <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="var(--accent-primary)" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="var(--accent-primary)" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                  <XAxis dataKey="name" stroke="#666" />
                  <YAxis stroke="#666" />
                  <Tooltip 
                    contentStyle={{ background: '#141820', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px' }}
                    itemStyle={{ color: '#fff' }}
                  />
                  <Area type="monotone" dataKey="price" stroke="var(--accent-primary)" fillOpacity={1} fill="url(#colorPrice)" strokeWidth={3} />
                  <Line type="monotone" dataKey="prediction" stroke="var(--success)" strokeDasharray="5 5" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </motion.div>
        </div>

        {/* AI Insight Panel */}
        <div className="col-4">
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="glass-card"
            style={{ height: '500px', overflowY: 'auto' }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
              <Zap size={24} color="var(--warning)" />
              <h3 style={{ fontSize: '1.2rem' }}>AI İçgörüleri</h3>
            </div>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div className="glass-card" style={{ padding: '1rem', background: 'rgba(255,255,255,0.02)' }}>
                <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Tahmin Güveni</p>
                <div style={{ fontSize: '1.5rem', fontWeight: '700', color: 'var(--success)' }}>{selectedProduct.confidence}</div>
                <div style={{ width: '100%', height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: '2px', marginTop: '0.5rem' }}>
                  <div style={{ width: selectedProduct.confidence, height: '100%', background: 'var(--success)', borderRadius: '2px' }}></div>
                </div>
              </div>

              <div style={{ padding: '0.5rem' }}>
                <h4 style={{ fontSize: '0.9rem', marginBottom: '1rem' }}>Neden Yükseliyor?</h4>
                <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                  <li style={{ display: 'flex', gap: '0.5rem', fontSize: '0.85rem' }}>
                    <Info size={16} color="var(--accent-primary)" />
                    Mersin bölgesi yağışlı hava uyarısı (Arz daralması)
                  </li>
                  <li style={{ display: 'flex', gap: '0.5rem', fontSize: '0.85rem' }}>
                    <Info size={16} color="var(--accent-primary)" />
                    Artan ihracat talebi (Rusya sevkiyatı)
                  </li>
                  <li style={{ display: 'flex', gap: '0.5rem', fontSize: '0.85rem' }}>
                    <Info size={16} color="var(--accent-primary)" />
                    Hafta sonu lojistik kısıtlamaları
                  </li>
                </ul>
              </div>

              <button className="glass-card" style={{ 
                marginTop: '1rem', width: '100%', border: '1px solid var(--accent-primary)',
                background: 'rgba(0, 210, 255, 0.1)', cursor: 'pointer', fontWeight: '600'
              }}>
                Detaylı Raporu İndir
              </button>
            </div>
          </motion.div>
        </div>

        {/* Product Grid */}
        <div className="col-12">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem', marginTop: '1rem' }}>
            {products.map((prod, index) => (
              <motion.div
                key={prod.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 * index }}
                className="glass-card"
                onClick={() => setSelectedProduct(prod)}
                style={{ 
                  cursor: 'pointer',
                  border: selectedProduct.id === prod.id ? '1px solid var(--accent-primary)' : '1px solid var(--glass-border)'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontWeight: '600' }}>{prod.name}</span>
                  {prod.status === 'up' ? <ArrowUpRight color="var(--success)" /> : <ArrowDownRight color="var(--danger)" />}
                </div>
                <div style={{ fontSize: '1.25rem', fontWeight: '700', marginTop: '0.5rem' }}>{prod.price}</div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '1rem', alignItems: 'center' }}>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Trend</span>
                  <span className={`badge ${prod.status === 'up' ? 'badge-up' : 'badge-down'}`}>{prod.trend}</span>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

const App = () => {
  const [view, setView] = useState('landing'); // landing, login, dashboard
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [products, setProducts] = useState(INITIAL_PRODUCTS);

  const handleAdminAccess = () => {
    if (isAuthenticated) {
      setView('dashboard');
    } else {
      setView('login');
    }
  };

  return (
    <div className="app-container">
      <AnimatePresence mode="wait">
        {view === 'landing' && (
          <MainApp 
            key="main" 
            products={products} 
            onAdminClick={handleAdminAccess} 
          />
        )}
        
        {view === 'login' && (
          <Login 
            key="login" 
            onLogin={() => {
              setIsAuthenticated(true);
              setView('dashboard');
            }} 
          />
        )}

        {view === 'dashboard' && (
          <AdminDashboard 
            key="dashboard" 
            products={products} 
            setProducts={setProducts}
            onLogout={() => {
              setIsAuthenticated(false);
              setView('landing');
            }} 
          />
        )}
      </AnimatePresence>

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default App;
