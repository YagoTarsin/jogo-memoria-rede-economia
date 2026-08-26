const App = (() => {
  const screens = {
    menu: document.getElementById('screen-menu'),
    game: document.getElementById('screen-game'),
    config: document.getElementById('screen-config'),
  };

  const IDLE_LIMIT_MS = 60000;
  let idleTimer = null;

  function currentScreenName() {
    return Object.entries(screens).find(([, el]) => el.classList.contains('active'))?.[0];
  }

  function showScreen(name) {
    Object.entries(screens).forEach(([key, el]) => {
      el.classList.toggle('active', key === name);
    });
    if (name === 'menu') Menu.refresh();
    if (name === 'config') Config.onEnter();
    resetIdleTimer();
  }

  function resetIdleTimer() {
    clearTimeout(idleTimer);
    const current = currentScreenName();
    if (current && current !== 'menu') {
      idleTimer = setTimeout(() => showScreen('menu'), IDLE_LIMIT_MS);
    }
  }

  function init() {
    ['click', 'touchstart', 'keydown'].forEach((evt) =>
      document.addEventListener(evt, resetIdleTimer, { passive: true })
    );
    document.addEventListener('contextmenu', (e) => e.preventDefault());

    Menu.init();
    Game.init();
    Config.init();

    showScreen('menu');
  }

  return { showScreen, init };
})();

document.addEventListener('DOMContentLoaded', App.init);
