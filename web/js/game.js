const Game = (() => {
  let firstCard = null;
  let secondCard = null;
  let lockBoard = false;
  let matchedCount = 0;
  let totalPairs = 0;
  let moves = 0;
  let foundCards = [];

  function boardEl() {
    return document.getElementById('game-board');
  }

  function statusEl() {
    return document.getElementById('game-status');
  }

  function init() {
    document.getElementById('game-back').addEventListener('click', () => {
      hideVictory();
      App.showScreen('menu');
    });
    document.getElementById('game-restart').addEventListener('click', startNewGame);
    document.getElementById('victory-again').addEventListener('click', () => {
      hideVictory();
      startNewGame();
    });
    document.getElementById('victory-menu').addEventListener('click', () => {
      hideVictory();
      App.showScreen('menu');
    });
  }

  async function startNewGame() {
    const allCards = await DB.getAllCards();
    const pairsSetting = Number(await DB.getSetting('pairsCount', 8)) || 8;
    const pairs = Math.min(pairsSetting, allCards.length);

    if (pairs < 2) {
      alert('Cadastre pelo menos 2 cartas nas Configurações para poder jogar.');
      App.showScreen('config');
      return false;
    }

    const chosen = shuffle(allCards).slice(0, pairs);
    const deck = shuffle([...chosen, ...chosen]).map((card, index) => ({ ...card, uid: index }));

    totalPairs = pairs;
    matchedCount = 0;
    moves = 0;
    foundCards = [];
    firstCard = null;
    secondCard = null;
    lockBoard = false;

    renderBoard(deck);
    updateStatus();
    return true;
  }

  function renderBoard(deck) {
    const board = boardEl();
    board.innerHTML = '';
    const cols = Math.max(2, Math.min(Math.ceil(Math.sqrt(deck.length * 1.6)), 8));
    board.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;

    deck.forEach((card) => {
      const el = document.createElement('div');
      el.className = 'card';
      el.innerHTML = `
        <div class="card-inner">
          <div class="card-face card-back">🛒</div>
          <div class="card-face card-front">
            <div class="card-image-wrap"><img src="${card.imageData}" alt=""></div>
            <div class="card-name">${escapeHtml(card.name)}</div>
            <div class="card-price"></div>
            <div class="treasure-overlay">
              <span class="treasure-icon">🎁</span>
              <span>Promoção encontrada!</span>
            </div>
          </div>
        </div>
      `;
      el.addEventListener('click', () => onCardClick(el, card));
      board.appendChild(el);
    });
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  function onCardClick(el, card) {
    if (lockBoard || el.classList.contains('flipped') || el.classList.contains('matched')) return;

    el.classList.add('flipped');

    if (!firstCard) {
      firstCard = { el, card };
      return;
    }

    secondCard = { el, card };
    lockBoard = true;
    moves += 1;
    updateStatus();

    setTimeout(resolveSelection, 700);
  }

  function resolveSelection() {
    if (firstCard.card.id === secondCard.card.id) {
      firstCard.el.classList.add('treasure');
      secondCard.el.classList.add('treasure');
      setTimeout(() => revealMatch(firstCard, secondCard), 550);
    } else {
      firstCard.el.classList.remove('flipped');
      secondCard.el.classList.remove('flipped');
      firstCard = null;
      secondCard = null;
      lockBoard = false;
    }
  }

  function revealMatch(first, second) {
    [first, second].forEach(({ el, card }) => {
      el.classList.remove('treasure');
      el.classList.add('matched');
      el.querySelector('.card-price').textContent =
        `De ${formatCurrency(card.realPrice)}\npor ${formatCurrency(card.promoPrice)}`;
    });

    foundCards.push(first.card);
    matchedCount += 1;
    firstCard = null;
    secondCard = null;
    lockBoard = false;
    updateStatus();

    if (matchedCount === totalPairs) {
      setTimeout(showVictory, 500);
    }
  }

  function updateStatus() {
    statusEl().textContent = `Pares encontrados: ${matchedCount}/${totalPairs}    ·    Jogadas: ${moves}`;
  }

  function showVictory() {
    const totalSavings = foundCards.reduce((sum, c) => sum + (c.realPrice - c.promoPrice), 0);
    document.getElementById('victory-moves').textContent = `Total de jogadas: ${moves}`;
    document.getElementById('victory-savings').textContent =
      `Economia total nas promoções: ${formatCurrency(totalSavings)}`;
    document.getElementById('victory-modal').classList.add('active');
  }

  function hideVictory() {
    document.getElementById('victory-modal').classList.remove('active');
  }

  return { init, startNewGame };
})();
