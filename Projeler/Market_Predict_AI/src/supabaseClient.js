import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

// If credentials are missing, we create a mock object that mimics Supabase client
// to prevent the app from crashing when trying to fetch from invalid URLs.
// Improved mock client that supports chaining and returns a Promise-like object
// Proxy-based mock client that handles any method call and remains chainable
// Proxy-based mock client that uses localStorage for demo persistence
const createMockClient = () => {
  const getData = (table) => JSON.parse(localStorage.getItem(`mock_${table}`) || '[]');
  const setData = (table, data) => localStorage.setItem(`mock_${table}`, JSON.stringify(data));

  const handler = {
    get: (target, prop) => {
      if (prop === 'then') {
        const table = target.table;
        const data = getData(table);
        return (onSuccess) => Promise.resolve({ data, error: null }).then(onSuccess);
      }
      
      if (prop === 'insert') {
        return (records) => {
          const table = target.table;
          const current = getData(table);
          setData(table, [...current, ...records]);
          return { then: (onSuccess) => Promise.resolve({ data: records, error: null }).then(onSuccess) };
        };
      }

      if (prop === 'select') return () => new Proxy(target, handler);
      if (prop === 'eq') return () => new Proxy(target, handler);
      if (prop === 'order') return () => new Proxy(target, handler);
      
      return () => new Proxy(target, handler);
    }
  };

  return {
    from: (table) => new Proxy({ table }, handler)
  };
};

if (!supabaseUrl || !supabaseAnonKey || supabaseUrl.includes('placeholder')) {
  console.warn("Supabase credentials missing! Running in DEMO MODE.");
}

export const supabase = (supabaseUrl && !supabaseUrl.includes('placeholder')) 
  ? createClient(supabaseUrl, supabaseAnonKey) 
  : createMockClient();
