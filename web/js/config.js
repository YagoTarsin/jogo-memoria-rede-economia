const Config = (() => {
  const DEFAULT_PIN = '1234';
  let editingId = null;
  let selectedImageData = null;
  let existingImageData = null;

  function applyMoneyMask(input) {
    input.addEventListener('input', () => {
      const digits = input.value.replace(/\D/g, '');
      const cents = parseInt(digits || '0', 10);
      const formatted = (cents / 100).toFixed(2).replace('.', ',');
      input.value = formatted;
    });
  }

  function parseMoneyInput(input) {
    return parseFloat(input.value.replace(',', '.')) || 0;
  }

  function init() {
    document.getElementById('config-back').addEventListener('click', () => App.showScreen('menu'));
    document.getElementById('pin-submit').addEventListener('click', submitPin);
    document.getElementById('pin-input').addEventListener('keydown', (e) => {
      if (e.key === 'Enter') submitPin();
    });
    applyMoneyMask(document.getElementById('card-real-price'));
    applyMoneyMask(document.getElementById('card-promo-price'));
    document.getElementById('card-image').addEventListener('change', onImageSelected);
    document.getElementById('card-form').addEventListener('submit', onSaveCard);
    document.getElementById('card-cancel').addEventListener('click', resetForm);
    document.getElementById('pairs-save').addEventListener('click', savePairs);
    document.getElementById('pin-save').addEventListener('click', savePin);
  }

  function onEnter() {
    document.getElementById('pin-gate').classList.remove('hidden');
    document.getElementById('config-body').classList.add('hidden');
    document.getElementById('pin-input').value = '';
    document.getElementById('pin-error').textContent = '';
    document.getElementById('pin-input').focus();
  }

  async function submitPin() {
    const entered = document.getElementById('pin-input').value.trim();
    const savedPin = (await DB.getSetting('adminPin', DEFAULT_PIN)) || DEFAULT_PIN;
    if (entered === savedPin) {
      document.getElementById('pin-gate').classList.add('hidden');
      document.getElementById('config-body').classList.remove('hidden');
      await refresh();
    } else {
      document.getElementById('pin-error').textContent = 'PIN incorreto.';
    }
  }

  async function refresh() {
    const cards = await DB.getAllCards();
    renderCardList(cards);

    const pairsInput = document.getElementById('pairs-input');
    pairsInput.max = Math.max(2, cards.length);
    const current = Number(await DB.getSetting('pairsCount', 8)) || 8;
    pairsInput.value = Math.min(Math.max(current, 2), Number(pairsInput.max));
  }

  function renderCardList(cards) {
    const list = document.getElementById('card-list');
    list.innerHTML = '';
    if (cards.length === 0) {
      list.innerHTML = '<p class="empty-hint">Nenhuma carta cadastrada ainda.</p>';
      return;
    }
    cards.forEach((card) => {
      const row = document.createElement('div');
      row.className = 'card-row';

      const thumb = document.createElement('img');
      thumb.className = 'card-row-thumb';
      thumb.src = card.imageData;

      const info = document.createElement('div');
      info.className = 'card-row-info';
      const name = document.createElement('strong');
      name.textContent = card.name;
      const price = document.createElement('span');
      const oldPrice = document.createElement('s');
      oldPrice.textContent = formatCurrency(card.realPrice);
      price.appendChild(oldPrice);
      price.appendChild(document.createTextNode(' '));
      const newPrice = document.createElement('b');
      newPrice.textContent = formatCurrency(card.promoPrice);
      price.appendChild(newPrice);
      info.appendChild(name);
      info.appendChild(price);

      const actions = document.createElement('div');
      actions.className = 'card-row-actions';
      const editButton = document.createElement('button');
      editButton.className = 'icon-btn icon-btn-edit';
      editButton.textContent = '✏️';
      editButton.setAttribute('aria-label', 'Editar');
      editButton.addEventListener('click', () => startEdit(card));
      const deleteButton = document.createElement('button');
      deleteButton.className = 'icon-btn icon-btn-delete';
      deleteButton.textContent = '🗑️';
      deleteButton.setAttribute('aria-label', 'Excluir');
      deleteButton.addEventListener('click', () => deleteCard(card));
      actions.appendChild(editButton);
      actions.appendChild(deleteButton);

      row.appendChild(thumb);
      row.appendChild(info);
      row.appendChild(actions);
      list.appendChild(row);
    });
  }

  function onImageSelected(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      selectedImageData = reader.result;
      const preview = document.getElementById('card-image-preview');
      preview.src = selectedImageData;
      preview.classList.remove('hidden');
    };
    reader.readAsDataURL(file);
  }

  function startEdit(card) {
    editingId = card.id;
    existingImageData = card.imageData;
    selectedImageData = null;
    document.getElementById('card-name').value = card.name;
    document.getElementById('card-real-price').value = Number(card.realPrice).toFixed(2).replace('.', ',');
    document.getElementById('card-promo-price').value = Number(card.promoPrice).toFixed(2).replace('.', ',');

    const preview = document.getElementById('card-image-preview');
    preview.src = card.imageData;
    preview.classList.remove('hidden');

    document.getElementById('form-title').textContent = 'Editar carta';
    document.getElementById('card-save').textContent = 'Salvar alterações';
    document.getElementById('card-cancel').classList.remove('hidden');
  }

  async function deleteCard(card) {
    if (!confirm(`Tem certeza que deseja excluir "${card.name}"?`)) return;
    await DB.deleteCard(card.id);
    if (editingId === card.id) resetForm();
    await refresh();
  }

  async function onSaveCard(event) {
    event.preventDefault();
    const name = document.getElementById('card-name').value.trim();
    const realPrice = parseMoneyInput(document.getElementById('card-real-price'));
    const promoPrice = parseMoneyInput(document.getElementById('card-promo-price'));

    if (!name) {
      alert('Informe o nome do produto.');
      return;
    }
    if (!(promoPrice < realPrice)) {
      alert('O preço da promoção deve ser menor que o preço normal.');
      return;
    }

    const imageData = selectedImageData || existingImageData;
    if (!imageData) {
      alert('Escolha uma imagem para o produto.');
      return;
    }

    const card = { name, realPrice, promoPrice, imageData };
    if (editingId) {
      card.id = editingId;
      await DB.updateCard(card);
    } else {
      await DB.addCard(card);
    }

    resetForm();
    await refresh();
  }

  function resetForm() {
    editingId = null;
    selectedImageData = null;
    existingImageData = null;
    document.getElementById('card-form').reset();
    const preview = document.getElementById('card-image-preview');
    preview.classList.add('hidden');
    preview.src = '';
    document.getElementById('form-title').textContent = 'Cadastrar carta';
    document.getElementById('card-save').textContent = 'Salvar carta';
    document.getElementById('card-cancel').classList.add('hidden');
  }

  async function savePairs() {
    const value = Number(document.getElementById('pairs-input').value);
    await DB.setSetting('pairsCount', value);
    alert('Quantidade de pares atualizada.');
  }

  async function savePin() {
    const newPin = document.getElementById('pin-new').value.trim();
    if (!/^\d{4,6}$/.test(newPin)) {
      alert('O PIN deve ter entre 4 e 6 dígitos numéricos.');
      return;
    }
    await DB.setSetting('adminPin', newPin);
    document.getElementById('pin-new').value = '';
    alert('PIN atualizado.');
  }

  return { init, onEnter };
})();
