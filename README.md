# Jogo da Memória - Rede Economia

Jogo da memória para totens de supermercado: entretém o cliente enquanto
divulga as promoções da loja. Ao encontrar um par de cartas iguais, um "baú
de tesouro" se abre revelando a imagem do produto, o nome e o preço
promocional.

Existem duas versões no repositório:

- **`web/`** — app web (HTML/CSS/JS), pensado para rodar em **tablet Android**
  dentro de um navegador em modo quiosque (ex.: Fully Kiosk Browser). É a
  versão principal usada no totem.
- **`app/` + `main.py`** — versão desktop em Python (PySide6), para rodar em
  PC/mini-PC com monitor touch.

Ambas têm as mesmas 3 telas (Jogar, Jogo, Configurações) e a mesma lógica de
jogo.

## Versão Web (`web/`)

App 100% client-side: nenhum backend é necessário. Os dados (cartas, preços,
imagens, PIN de admin, quantidade de pares) ficam salvos no navegador via
IndexedDB, no próprio tablet/dispositivo.

### Telas

- **Jogar** — logo, título e botão para começar a partida.
- **Jogo** — tabuleiro de cartas embaralhadas; ao formar um par, mostra a
  animação de baú e o preço promocional. Ao final, exibe um resumo com total
  de jogadas e economia total.
- **Configurações** — protegida por PIN (padrão `1234`, alterável). Permite
  cadastrar/editar/excluir cartas (nome, imagem, preço normal e promocional)
  e definir quantos pares entram em cada partida.

### Rodar localmente

Como é só HTML/CSS/JS estático, qualquer servidor HTTP simples serve:

```bash
cd web
python -m http.server 8765
```

Depois acesse `http://localhost:8765/index.html` no navegador.

### Colocar no tablet do totem

1. Hospede a pasta `web/` em algum lugar acessível pelo tablet (rede local,
   GitHub Pages, ou qualquer hospedagem estática).
2. No tablet Android, instale um navegador de quiosque (ex.: **Fully Kiosk
   Browser**, gratuito).
3. Configure o app para abrir em tela cheia, sem barra de navegação, direto
   na URL do jogo.

### Estrutura

```
web/
  index.html            marcação das 3 telas
  css/styles.css         tema visual (fundo branco, botões vermelhos, texto verde)
  js/
    db.js                 acesso ao IndexedDB (cartas e configurações)
    utils.js               helpers (shuffle, formatação de preço)
    app.js                  navegação entre telas e timeout de inatividade
    menu.js                 tela "Jogar"
    game.js                 tela "Jogo"
    config.js               tela "Configurações" (PIN, CRUD de cartas, pares)
  assets/logo.png         logo exibido na tela inicial
```

## Versão Desktop (`app/`, Python + PySide6)

### Requisitos

- Python 3.10+
- PySide6

### Instalação

```bash
pip install -r requirements.txt
```

### Executar

```bash
python main.py
```

O app abre em tela cheia (modo totem). Pressione **Esc** para fechar ou
**F11** para alternar entre tela cheia e janela normal.

### Dados

- As cartas e a configuração de pares ficam em `app/data/database.db`
  (SQLite, criado automaticamente na primeira execução).
- As imagens cadastradas são copiadas para `app/assets/cards/`.

### Estrutura

```
main.py                    ponto de entrada
app/
  database.py               acesso ao SQLite (cartas e configurações)
  models.py                 dataclass Card
  paths.py                  caminhos de dados e imagens
  styles.py                 tema visual (QSS)
  ui/
    main_window.py          janela principal e navegação entre telas
    menu_screen.py           tela "Jogar"
    game_screen.py           tela "Jogo"
    config_screen.py         tela "Configurações"
    card_widget.py           widget de carta (verso, frente, baú, par encontrado)
```
