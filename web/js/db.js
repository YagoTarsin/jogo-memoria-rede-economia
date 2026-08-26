const DB = (() => {
  const DB_NAME = 'supermercado_memoria';
  const DB_VERSION = 1;
  let dbPromise = null;

  function open() {
    if (dbPromise) return dbPromise;
    dbPromise = new Promise((resolve, reject) => {
      const req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains('cards')) {
          db.createObjectStore('cards', { keyPath: 'id', autoIncrement: true });
        }
        if (!db.objectStoreNames.contains('settings')) {
          db.createObjectStore('settings', { keyPath: 'key' });
        }
      };
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
    });
    return dbPromise;
  }

  async function addCard(card) {
    const db = await open();
    return new Promise((resolve, reject) => {
      const store = db.transaction('cards', 'readwrite').objectStore('cards');
      const req = store.add(card);
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
    });
  }

  async function updateCard(card) {
    const db = await open();
    return new Promise((resolve, reject) => {
      const store = db.transaction('cards', 'readwrite').objectStore('cards');
      const req = store.put(card);
      req.onsuccess = () => resolve();
      req.onerror = () => reject(req.error);
    });
  }

  async function deleteCard(id) {
    const db = await open();
    return new Promise((resolve, reject) => {
      const store = db.transaction('cards', 'readwrite').objectStore('cards');
      const req = store.delete(id);
      req.onsuccess = () => resolve();
      req.onerror = () => reject(req.error);
    });
  }

  async function getAllCards() {
    const db = await open();
    return new Promise((resolve, reject) => {
      const store = db.transaction('cards', 'readonly').objectStore('cards');
      const req = store.getAll();
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
    });
  }

  async function getSetting(key, defaultValue) {
    const db = await open();
    return new Promise((resolve, reject) => {
      const store = db.transaction('settings', 'readonly').objectStore('settings');
      const req = store.get(key);
      req.onsuccess = () => resolve(req.result ? req.result.value : defaultValue);
      req.onerror = () => reject(req.error);
    });
  }

  async function setSetting(key, value) {
    const db = await open();
    return new Promise((resolve, reject) => {
      const store = db.transaction('settings', 'readwrite').objectStore('settings');
      const req = store.put({ key, value });
      req.onsuccess = () => resolve();
      req.onerror = () => reject(req.error);
    });
  }

  return { addCard, updateCard, deleteCard, getAllCards, getSetting, setSetting };
})();
