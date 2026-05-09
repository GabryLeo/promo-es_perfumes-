# 💐 Bot de Promoções de Perfumes

Bot Python que monitora promoções de perfumes no Mercado Livre e envia alertas automaticamente via WhatsApp.

## ✨ Funcionalidades

- Pesquisa automatizada de +97 perfumes no Mercado Livre
- Detecção de promoções com desconto mínimo configurável
- Envio de alertas via WhatsApp com screenshot do produto
- Histórico de preços para comparação (últimas 30 entradas por produto)
- Deduplicação de resultados para evitar alertas repetidos
- Coleta otimizada com Playwright (1 browser para tudo)
- Suporte a múltiplos modos: debug, agendado e intervalo

## 🛒 Marcas Monitoradas

- **O Boticário** — Egeo, Malbec, Floratta, Lily, Coffee, Quasar e mais
- **Natura** — Essencial, Kaiak, Una, Luna, Kriska e mais
- **Eudora / Quem Disse Berenice** — Glamour, Soul, Vibe, Pulse e mais
- **Avon** — Far Away, Black Suede, Little Black Dress e mais
- **Importados** — Dior, Chanel, YSL, Armani, Versace, Paco Rabanne e mais

## 🚀 Como usar

### Instalar dependências

```bash
pip install requests beautifulsoup4 playwright
playwright install chromium
```

### Configurar

Edite as variáveis no topo do arquivo `bot_perfume.py`:

```python
CONTATO = "Nome do contato no WhatsApp"
MODO_EXECUCAO = "debug"   # "debug" | "agendado" | "intervalo"
DESCONTO_MINIMO = 10       # % mínimo de desconto para alertar
TOP_N_RESULTADOS = 5       # Quantos resultados por perfume analisar
```

### Executar

```bash
python bot_perfume.py
```

## ⚙️ Modos de execução

| Modo | Descrição |
|------|-----------|
| `debug` | Roda uma vez com duração e intervalo curtos (ideal para testes) |
| `agendado` | Executa em horários fixos do dia (ex: 06:00, 12:00, 18:00, 22:00) |
| `intervalo` | Repete automaticamente a cada X horas |

## 🛠️ Tecnologias

- **Python** — Linguagem principal
- **Playwright** — Automação do navegador (Mercado Livre + WhatsApp Web)
- **BeautifulSoup** — Parsing HTML
- **Requests** — Requisições HTTP
- **Threading** — Coleta paralela de resultados

## 📁 Estrutura

```
promo-es_perfumes-/
├── bot_perfume.py       # Script principal
├── data/
│   └── historico_precos.json  # Histórico de preços (gerado automaticamente)
└── screenshots/         # Prints dos produtos (gerado automaticamente)
```

## 📚 Sobre o projeto

Bot desenvolvido para monitorar o mercado de perfumes e encontrar automaticamente as melhores promoções, enviando alertas em tempo real pelo WhatsApp. Projeto de estudo de automação web com Python e Playwright.

Feito com 💙 por Gabryel Leonardo
