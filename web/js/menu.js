const Menu = (() => {
  function init() {
    document.getElementById('btn-play').addEventListener('click', async () => {
      const started = await Game.startNewGame();
      if (started) App.showScreen('game');
    });
    document.getElementById('btn-config').addEventListener('click', () => {
      App.showScreen('config');
    });
  }

  async function refresh() {
    const cards = await DB.getAllCards();
    const pairs = await DB.getSetting('pairsCount', 8);
    document.getElementById('menu-info').textContent =
      `${cards.length} carta(s) cadastrada(s)  ·  partida configurada para ${pairs} pares`;
  }

  return { init, refresh };
})();
