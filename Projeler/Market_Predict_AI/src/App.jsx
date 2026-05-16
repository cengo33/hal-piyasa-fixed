import React, { useState, useEffect } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area 
} from 'recharts';
import { 
  TrendingUp, TrendingDown, Activity, Zap, Info, ArrowUpRight, ArrowDownRight, RefreshCw, BarChart3, PieChart
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// Mock Data for Hal Market
const MARKET_DATA = [
  { name: '08:00', price: 12.5, prediction: 12.6 },
  { name: '10:00', price: 13.2, prediction: 13.1 },
  { name: '12:00', price: 14.8, prediction: 14.5 },
  { name: '14:00', price: 14.2, prediction: 14.9 },
  { name: '16:00', price: 15.5, prediction: 15.8 },
  { name: '18:00', price: 16.1, prediction: 16.5 },
  { name: '20:00', price: 15.8, prediction: 17.2 },
];

const PRODUCTS = [
  { id: 1, name: 'Domates (Salkım)', price: '₺16.50', trend: '+4.2%', status: 'up', confidence: '89%' },
  { id: 2, name: 'Salatalık', price: '₺12.20', trend: '-2.1%', status: 'down', confidence: '72%' },
  { id: 3, name: 'Biber (Sivri)', price: '₺24.00', trend: '+1.5%', status: 'up', confidence: '65%' },
  { id: 4, name: 'Patlıcan', price: '₺18.40', trend: '+8.7%', status: 'up', confidence: '94%' },
];

const App = () => {
  const [selectedProduct, setSelectedProduct] = useState(PRODUCTS[0]);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const refreshData = () => {
    setIsRefreshing(true);
    setTimeout(() => setIsRefreshing(false), 1500);
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header>
        <div className="logo">
          <Zap size={32} />
          <span>HAL PREDICT AI</span>
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
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
                <AreaChart data={MARKET_DATA}>
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
            {PRODUCTS.map((prod, index) => (
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
