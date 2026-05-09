# ============================================================================
# 💐 BOT PERFUMES - VERSÃO TURBO (REQUESTS PARALELO)
# ============================================================================
#
# 🚀 SUPER OTIMIZAÇÃO:
#   ✅ Coleta com REQUESTS (sem browser) - 10x mais rápido!
#   ✅ 10 paralelos sem bug
#   ✅ Coleta 97 perfumes em ~30 segundos
#   ✅ Total: ~16 min (vs 45 min antes)
#
# Como instalar:
#   pip install requests beautifulsoup4 playwright
#   playwright install chromium
#
# ============================================================================

from __future__ import annotations
import os
import re
import sys
import time
import json
import base64
import random
import mimetypes
import datetime
import threading
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import (
    sync_playwright, Playwright, BrowserContext, Page, expect,
)


# ============================================================================
# 🔧 CONFIGURAÇÕES
# ============================================================================

CONTATO = "test perfume"

MODO_EXECUCAO = "debug"   # "debug" | "agendado" | "intervalo"

HORARIOS_AGENDADOS = ["06:00", "12:00", "18:00", "22:00"]
INTERVALO_HORAS = 6

# 🚀 TURBO: Coleta com REQUESTS (sem browser)
PESQUISAS_PARALELAS = 10   # Pode ir até 15 sem problema!

# ⏰ Modo DEBUG
DEBUG_DURACAO_MINUTOS = 14
DEBUG_INTERVALO_MINUTOS = 2

# Promoções
APENAS_PROMOCAO_REAL = True
DESCONTO_MINIMO = 10
TOP_N_RESULTADOS = 5

# Pastas
USER_PROFILE_PATH = os.path.expanduser('~')
USER_DATA_DIR = os.path.join(USER_PROFILE_PATH, ".perfil_perfume_bot")
SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
HISTORICO_FILE = os.path.join(DATA_DIR, "historico_precos.json")

WHATSAPP_URL = "https://web.whatsapp.com/"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

_print_lock = threading.Lock()


# ============================================================================
# 💐 PERFUMES
# ============================================================================

PERFUMES = [
    # ===== BOTICÁRIO =====
    {"nome": "Egeo Dolce 90ml", "marca": "O Boticário", "genero": "👩 Feminino", "emoji": "🌹", "ativo": True},
    {"nome": "Malbec Tradicional 100ml", "marca": "O Boticário", "genero": "👨 Masculino", "emoji": "🌹", "ativo": True},
    {"nome": "Lily Eau de Parfum 30ml", "marca": "O Boticário", "genero": "👩 Feminino", "emoji": "🌹", "ativo": True},
    {"nome": "Malbec Black 100ml", "marca": "O Boticário", "genero": "👨 Masculino", "emoji": "🌹", "ativo": True},
    {"nome": "Floratta Blue 75ml", "marca": "O Boticário", "genero": "👩 Feminino", "emoji": "🌹", "ativo": True},
    {"nome": "Malbec Gold 100ml", "marca": "O Boticário", "genero": "👨 Masculino", "emoji": "🌹", "ativo": True},
    {"nome": "Egeo Choc 90ml", "marca": "O Boticário", "genero": "👩 Feminino", "emoji": "🌹", "ativo": True},
    {"nome": "Malbec Noir 100ml", "marca": "O Boticário", "genero": "👨 Masculino", "emoji": "🌹", "ativo": True},
    {"nome": "Floratta Red 75ml", "marca": "O Boticário", "genero": "👩 Feminino", "emoji": "🌹", "ativo": True},
    {"nome": "Malbec Club 100ml", "marca": "O Boticário", "genero": "👨 Masculino", "emoji": "🌹", "ativo": True},
    {"nome": "Lily Lumiere 75ml", "marca": "O Boticário", "genero": "👩 Feminino", "emoji": "🌹", "ativo": True},
    {"nome": "Egeo Man 90ml", "marca": "O Boticário", "genero": "👨 Masculino", "emoji": "🌹", "ativo": True},
    {"nome": "Floratta Gold 75ml", "marca": "O Boticário", "genero": "👩 Feminino", "emoji": "🌹", "ativo": True},
    {"nome": "Coffee Man Seductive 100ml", "marca": "O Boticário", "genero": "👨 Masculino", "emoji": "🌹", "ativo": True},
    {"nome": "Coffee Woman Seduction 100ml", "marca": "O Boticário", "genero": "👩 Feminino", "emoji": "🌹", "ativo": True},
    {"nome": "Quasar Cyber 100ml", "marca": "O Boticário", "genero": "👨 Masculino", "emoji": "🌹", "ativo": True},
    {"nome": "Match Feminino 100ml", "marca": "O Boticário", "genero": "👩 Feminino", "emoji": "🌹", "ativo": True},
    {"nome": "Quasar Stellar 100ml", "marca": "O Boticário", "genero": "👨 Masculino", "emoji": "🌹", "ativo": True},
    {"nome": "Egeo Original Mini 30ml", "marca": "O Boticário", "genero": "👩 Feminino", "emoji": "🌹", "ativo": True},
    {"nome": "Match Masculino 100ml", "marca": "O Boticário", "genero": "👨 Masculino", "emoji": "🌹", "ativo": True},

    # ===== NATURA =====
    {"nome": "Essencial Exclusivo Feminino 100ml", "marca": "Natura", "genero": "👩 Feminino", "emoji": "🌿", "ativo": True},
    {"nome": "Essencial Exclusivo Masculino 100ml", "marca": "Natura", "genero": "👨 Masculino", "emoji": "🌿", "ativo": True},
    {"nome": "Una Senses 75ml", "marca": "Natura", "genero": "👩 Feminino", "emoji": "🌿", "ativo": True},
    {"nome": "Kaiak Aero Masculino 100ml", "marca": "Natura", "genero": "👨 Masculino", "emoji": "🌿", "ativo": True},
    {"nome": "Una Artisan 75ml", "marca": "Natura", "genero": "👩 Feminino", "emoji": "🌿", "ativo": True},
    {"nome": "Kaiak Tradicional 100ml", "marca": "Natura", "genero": "👨 Masculino", "emoji": "🌿", "ativo": True},
    {"nome": "Una Eclipse 75ml", "marca": "Natura", "genero": "👩 Feminino", "emoji": "🌿", "ativo": True},
    {"nome": "Kaiak Pulso 100ml", "marca": "Natura", "genero": "👨 Masculino", "emoji": "🌿", "ativo": True},
    {"nome": "Humor Você Feminino 75ml", "marca": "Natura", "genero": "👩 Feminino", "emoji": "🌿", "ativo": True},
    {"nome": "Kaiak Oceano 100ml", "marca": "Natura", "genero": "👨 Masculino", "emoji": "🌿", "ativo": True},
    {"nome": "Ilía Natura 50ml", "marca": "Natura", "genero": "👩 Feminino", "emoji": "🌿", "ativo": True},
    {"nome": "Biografia Masculino 100ml", "marca": "Natura", "genero": "👨 Masculino", "emoji": "🌿", "ativo": True},
    {"nome": "Luna Cristal 75ml", "marca": "Natura", "genero": "👩 Feminino", "emoji": "🌿", "ativo": True},
    {"nome": "Homem Sensação 100ml", "marca": "Natura", "genero": "👨 Masculino", "emoji": "🌿", "ativo": True},
    {"nome": "Luna Fascinada 75ml", "marca": "Natura", "genero": "👩 Feminino", "emoji": "🌿", "ativo": True},
    {"nome": "Homem Sintonia 100ml", "marca": "Natura", "genero": "👨 Masculino", "emoji": "🌿", "ativo": True},
    {"nome": "Kriska Natura 100ml", "marca": "Natura", "genero": "👩 Feminino", "emoji": "🌿", "ativo": True},
    {"nome": "Humor Você Masculino 75ml", "marca": "Natura", "genero": "👨 Masculino", "emoji": "🌿", "ativo": True},
    {"nome": "Essencial Suprem Feminino 100ml", "marca": "Natura", "genero": "👩 Feminino", "emoji": "🌿", "ativo": True},
    {"nome": "Essencial Original Masculino 100ml", "marca": "Natura", "genero": "👨 Masculino", "emoji": "🌿", "ativo": True},

    # ===== EUDORA + BERENICE =====
    {"nome": "Niina Secrets Eudora 100ml", "marca": "Eudora", "genero": "👩 Feminino", "emoji": "💄", "ativo": True},
    {"nome": "H Eudora Masculino 100ml", "marca": "Eudora", "genero": "👨 Masculino", "emoji": "💄", "ativo": True},
    {"nome": "Soul Eudora 100ml", "marca": "Eudora", "genero": "👩 Feminino", "emoji": "💄", "ativo": True},
    {"nome": "Magnetic Eudora Masculino 100ml", "marca": "Eudora", "genero": "👨 Masculino", "emoji": "💄", "ativo": True},
    {"nome": "Pulse Eudora 100ml", "marca": "Eudora", "genero": "👩 Feminino", "emoji": "💄", "ativo": True},
    {"nome": "Eudora Elements Masculino 100ml", "marca": "Eudora", "genero": "👨 Masculino", "emoji": "💄", "ativo": True},
    {"nome": "Vibe Eudora 100ml", "marca": "Eudora", "genero": "👩 Feminino", "emoji": "💄", "ativo": True},
    {"nome": "Eudora Sport Masculino 100ml", "marca": "Eudora", "genero": "👨 Masculino", "emoji": "💄", "ativo": True},
    {"nome": "Glamour Eudora 100ml", "marca": "Eudora", "genero": "👩 Feminino", "emoji": "💄", "ativo": True},
    {"nome": "Eudora Bold Masculino 100ml", "marca": "Eudora", "genero": "👨 Masculino", "emoji": "💄", "ativo": True},
    {"nome": "Glamour Diva Eudora 100ml", "marca": "Eudora", "genero": "👩 Feminino", "emoji": "💄", "ativo": True},
    {"nome": "Glam Power Quem Disse Berenice 100ml", "marca": "Berenice", "genero": "👩 Feminino", "emoji": "👛", "ativo": True},
    {"nome": "Glam Black Quem Disse Berenice 100ml", "marca": "Berenice", "genero": "👩 Feminino", "emoji": "👛", "ativo": True},
    {"nome": "Eudora Belle 100ml", "marca": "Eudora", "genero": "👩 Feminino", "emoji": "💄", "ativo": True},
    {"nome": "Glam Gold Quem Disse Berenice 100ml", "marca": "Berenice", "genero": "👩 Feminino", "emoji": "👛", "ativo": True},

    # ===== AVON =====
    {"nome": "Avon Far Away 50ml", "marca": "Avon", "genero": "👩 Feminino", "emoji": "🎀", "ativo": True},
    {"nome": "Avon Black Suede 100ml", "marca": "Avon", "genero": "👨 Masculino", "emoji": "🎀", "ativo": True},
    {"nome": "Avon Far Away Gold 50ml", "marca": "Avon", "genero": "👩 Feminino", "emoji": "🎀", "ativo": True},
    {"nome": "Avon Wild Country 100ml", "marca": "Avon", "genero": "👨 Masculino", "emoji": "🎀", "ativo": True},
    {"nome": "Avon Little Black Dress 50ml", "marca": "Avon", "genero": "👩 Feminino", "emoji": "🎀", "ativo": True},
    {"nome": "Avon Mesmerize 100ml", "marca": "Avon", "genero": "👨 Masculino", "emoji": "🎀", "ativo": True},
    {"nome": "Avon Encanto Pixie 50ml", "marca": "Avon", "genero": "👩 Feminino", "emoji": "🎀", "ativo": True},
    {"nome": "Avon X Masculino 100ml", "marca": "Avon", "genero": "👨 Masculino", "emoji": "🎀", "ativo": True},
    {"nome": "Avon Anew Power 50ml", "marca": "Avon", "genero": "👩 Feminino", "emoji": "🎀", "ativo": True},
    {"nome": "Avon Real Masculino 100ml", "marca": "Avon", "genero": "👨 Masculino", "emoji": "🎀", "ativo": True},
    {"nome": "Avon Eve Truth 50ml", "marca": "Avon", "genero": "👩 Feminino", "emoji": "🎀", "ativo": True},
    {"nome": "Avon Soft Musk 50ml", "marca": "Avon", "genero": "👩 Feminino", "emoji": "🎀", "ativo": True},
    {"nome": "Avon Tomorrow 50ml", "marca": "Avon", "genero": "👩 Feminino", "emoji": "🎀", "ativo": True},

    # ===== IMPORTADOS =====
    {"nome": "Lady Million Paco Rabanne 80ml", "marca": "Paco Rabanne", "genero": "👩 Feminino", "emoji": "✨", "ativo": True},
    {"nome": "1 Million Paco Rabanne 100ml", "marca": "Paco Rabanne", "genero": "👨 Masculino", "emoji": "✨", "ativo": True},
    {"nome": "Olympea Paco Rabanne 80ml", "marca": "Paco Rabanne", "genero": "👩 Feminino", "emoji": "✨", "ativo": True},
    {"nome": "1 Million Lucky Paco Rabanne 100ml", "marca": "Paco Rabanne", "genero": "👨 Masculino", "emoji": "✨", "ativo": True},
    {"nome": "212 VIP Carolina Herrera 80ml", "marca": "Carolina Herrera", "genero": "👩 Feminino", "emoji": "✨", "ativo": True},
    {"nome": "Invictus Paco Rabanne 100ml", "marca": "Paco Rabanne", "genero": "👨 Masculino", "emoji": "✨", "ativo": True},
    {"nome": "Good Girl Carolina Herrera 80ml", "marca": "Carolina Herrera", "genero": "👩 Feminino", "emoji": "✨", "ativo": True},
    {"nome": "Phantom Paco Rabanne 100ml", "marca": "Paco Rabanne", "genero": "👨 Masculino", "emoji": "✨", "ativo": True},
    {"nome": "La Vie Est Belle Lancôme 50ml", "marca": "Lancôme", "genero": "👩 Feminino", "emoji": "✨", "ativo": True},
    {"nome": "212 VIP Men Carolina Herrera 100ml", "marca": "Carolina Herrera", "genero": "👨 Masculino", "emoji": "✨", "ativo": True},
    {"nome": "Idôle Lancôme 50ml", "marca": "Lancôme", "genero": "👩 Feminino", "emoji": "✨", "ativo": True},
    {"nome": "Bad Boy Carolina Herrera 100ml", "marca": "Carolina Herrera", "genero": "👨 Masculino", "emoji": "✨", "ativo": True},
    {"nome": "J'adore Dior 50ml", "marca": "Dior", "genero": "👩 Feminino", "emoji": "✨", "ativo": True},
    {"nome": "CH Men Carolina Herrera 100ml", "marca": "Carolina Herrera", "genero": "👨 Masculino", "emoji": "✨", "ativo": True},
    {"nome": "Miss Dior 50ml", "marca": "Dior", "genero": "👩 Feminino", "emoji": "✨", "ativo": True},
    {"nome": "Sauvage Dior 100ml", "marca": "Dior", "genero": "👨 Masculino", "emoji": "✨", "ativo": True},
    {"nome": "Coco Mademoiselle Chanel 50ml", "marca": "Chanel", "genero": "👩 Feminino", "emoji": "✨", "ativo": True},
    {"nome": "Dior Homme Intense 100ml", "marca": "Dior", "genero": "👨 Masculino", "emoji": "✨", "ativo": True},
    {"nome": "Light Blue Dolce Gabbana 50ml", "marca": "D&G", "genero": "👩 Feminino", "emoji": "✨", "ativo": True},
    {"nome": "Acqua di Gio Giorgio Armani 100ml", "marca": "Armani", "genero": "👨 Masculino", "emoji": "✨", "ativo": True},
    {"nome": "Black Opium Yves Saint Laurent 50ml", "marca": "YSL", "genero": "👩 Feminino", "emoji": "✨", "ativo": True},
    {"nome": "Acqua di Gio Profumo 75ml", "marca": "Armani", "genero": "👨 Masculino", "emoji": "✨", "ativo": True},
    {"nome": "Mon Guerlain 50ml", "marca": "Guerlain", "genero": "👩 Feminino", "emoji": "✨", "ativo": True},
    {"nome": "Stronger With You Armani 100ml", "marca": "Armani", "genero": "👨 Masculino", "emoji": "✨", "ativo": True},
    {"nome": "Y Yves Saint Laurent 100ml", "marca": "YSL", "genero": "👨 Masculino", "emoji": "✨", "ativo": True},
    {"nome": "La Nuit de l'Homme YSL 100ml", "marca": "YSL", "genero": "👨 Masculino", "emoji": "✨", "ativo": True},
    {"nome": "Hugo Boss Bottled 100ml", "marca": "Hugo Boss", "genero": "👨 Masculino", "emoji": "✨", "ativo": True},
    {"nome": "Polo Blue Ralph Lauren 125ml", "marca": "Ralph Lauren", "genero": "👨 Masculino", "emoji": "✨", "ativo": True},
    {"nome": "Eros Versace 100ml", "marca": "Versace", "genero": "👨 Masculino", "emoji": "✨", "ativo": True},
]


# ============================================================================
# 🛠️ UTILS
# ============================================================================

def log(msg, tag=None):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    prefix = f"[{timestamp}]"
    if tag:
        prefix += f" [{tag}]"
    with _print_lock:
        print(f"{prefix} {msg}")


def banner(text, char="="):
    line = char * 70
    with _print_lock:
        print(f"\n{line}\n  {text}\n{line}\n")


def formatar_preco(valor):
    if valor is None:
        return "N/A"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def parse_preco(texto):
    if not texto:
        return None
    limpo = re.sub(r"[^\d,.]", "", str(texto))
    if not limpo:
        return None
    if "," in limpo and "." in limpo:
        limpo = limpo.replace(".", "").replace(",", ".")
    elif "," in limpo:
        limpo = limpo.replace(",", ".")
    try:
        valor = float(limpo)
        if 30 <= valor <= 5000:
            return valor
    except ValueError:
        pass
    return None


def normalizar_url(url):
    if not url:
        return ""
    return url.split("?")[0].split("#")[0].lower().strip()


def normalizar_titulo(titulo):
    if not titulo:
        return ""
    t = titulo.lower()
    t = re.sub(r'[^\w\s]', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t


# ============================================================================
# 💾 PERSISTÊNCIA
# ============================================================================

def carregar_historico():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(HISTORICO_FILE):
        return {}
    try:
        with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def salvar_historico(historico):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(HISTORICO_FILE, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)


def adicionar_ao_historico(historico, nome, preco_atual, preco_cheio=None, url=None):
    if nome not in historico:
        historico[nome] = []
    registro = {"data": datetime.datetime.now().isoformat(), "preco": preco_atual}
    if preco_cheio:
        registro["preco_cheio"] = preco_cheio
    if url:
        registro["url"] = url
    historico[nome].append(registro)
    historico[nome] = historico[nome][-30:]


def get_ultimo_preco(historico, nome):
    if nome not in historico or not historico[nome]:
        return None
    if len(historico[nome]) >= 2:
        return historico[nome][-2]["preco"]
    return None


def get_menor_preco(historico, nome):
    if nome not in historico or not historico[nome]:
        return None
    return min(h["preco"] for h in historico[nome])


# ============================================================================
# 🚀 PESQUISA NO ML COM PLAYWRIGHT OTIMIZADO
# ============================================================================

def pesquisar_ml_playwright(page, perfume):
    """🚀 Pesquisa rápida usando Playwright (page reutilizada)."""
    nome = perfume["nome"]
    busca_url = f"https://lista.mercadolivre.com.br/{urllib.parse.quote(nome)}"
    
    try:
        page.goto(busca_url, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(2500)  # 🚀 reduzido de 4s pra 2.5s
        
        resultados = page.evaluate(f"""
        () => {{
            const TOP_N = {TOP_N_RESULTADOS};
            const items = document.querySelectorAll('li.ui-search-layout__item, .ui-search-result__wrapper, .poly-card');
            const out = [];
            
            for (let i = 0; i < Math.min(items.length, TOP_N); i++) {{
                const item = items[i];
                let titulo = "";
                const tituloEl = item.querySelector('h2, .ui-search-item__title, .poly-component__title');
                if (tituloEl) titulo = tituloEl.innerText.trim();
                
                let url = null;
                const linkEls = item.querySelectorAll('a[href]');
                for (const l of linkEls) {{
                    if (l.href && (l.href.includes('mercadolivre.com.br') || l.href.includes('produto.mercado'))) {{
                        url = l.href;
                        break;
                    }}
                }}
                if (!url && linkEls.length > 0) url = linkEls[0].href;
                
                let precoAtual = null;
                let precoCheio = null;
                const todosPrecos = item.querySelectorAll('.andes-money-amount__fraction');
                
                for (const p of todosPrecos) {{
                    const inteiro = p.innerText.trim();
                    let centavos = "00";
                    const parent = p.parentElement;
                    if (parent) {{
                        const cents = parent.querySelector('.andes-money-amount__cents');
                        if (cents) centavos = cents.innerText.trim();
                    }}
                    
                    const isRiscado = (
                        p.closest('s') !== null ||
                        p.closest('.andes-money-amount--previous') !== null
                    );
                    
                    if (isRiscado) {{
                        if (!precoCheio) precoCheio = {{ inteiro, centavos }};
                    }} else {{
                        if (!precoAtual) precoAtual = {{ inteiro, centavos }};
                    }}
                }}
                
                if (precoAtual && url) {{
                    out.push({{
                        titulo, url,
                        atual_inteiro: precoAtual.inteiro,
                        atual_centavos: precoAtual.centavos,
                        cheio_inteiro: precoCheio ? precoCheio.inteiro : null,
                        cheio_centavos: precoCheio ? precoCheio.centavos : null,
                    }});
                }}
            }}
            return out;
        }}
        """)
        
        if not resultados:
            return None
        
        produtos = []
        for r in resultados:
            preco_atual = parse_preco(f"{r['atual_inteiro']},{r['atual_centavos']}")
            if not preco_atual:
                continue
            preco_cheio = None
            if r.get('cheio_inteiro'):
                preco_cheio = parse_preco(f"{r['cheio_inteiro']},{r['cheio_centavos']}")
            desconto_pct = 0
            if preco_cheio and preco_cheio > preco_atual:
                desconto_pct = ((preco_cheio - preco_atual) / preco_cheio) * 100
            url = r.get("url")
            if not url:
                continue
            produtos.append({
                "preco_atual": preco_atual,
                "preco_cheio": preco_cheio,
                "desconto_pct": desconto_pct,
                "url": url,
                "titulo": r.get("titulo", nome),
            })
        
        if not produtos:
            return None
        
        com_desconto = [p for p in produtos if p["desconto_pct"] > 0]
        if com_desconto:
            return max(com_desconto, key=lambda x: x["desconto_pct"])
        return min(produtos, key=lambda x: x["preco_atual"])
    
    except Exception as e:
        return None


# ============================================================================
# 🌐 PLAYWRIGHT (só pra screenshot e WhatsApp)
# ============================================================================

def create_context(p: Playwright, target_url: str, headless: bool = True, viewport=None) -> Page:
    launch_args = {
        "user_data_dir": USER_DATA_DIR,
        "headless": False,
        "args": [
            "--start-maximized",
            "--remote-debugging-port=3731",
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
        ],
        "user_agent": UA,
        "permissions": ["clipboard-read", "clipboard-write", "notifications"],
        "locale": "pt-BR",
        "timezone_id": "America/Sao_Paulo",
    }
    if viewport:
        launch_args["viewport"] = viewport
        launch_args["no_viewport"] = False
    else:
        launch_args["no_viewport"] = True

    context = p.chromium.launch_persistent_context(**launch_args)
    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
    """)
    page = context.pages[0] if context.pages else context.new_page()
    page.wait_for_timeout(500)
    page.goto(target_url, wait_until="domcontentloaded")
    if viewport:
        page.set_viewport_size(viewport)
    return page


def capturar_screenshot_busca(p: Playwright, perfume, url):
    if not url:
        return None
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    
    browser = None
    try:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(
            viewport={"width": 1366, "height": 900},
            user_agent=UA,
            locale="pt-BR",
        )
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        page.wait_for_timeout(4000)

        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arq = re.sub(r'[^\w]', '_', perfume["nome"])
        out = os.path.join(SCREENSHOT_DIR, f"{nome_arq}_{ts}.png")

        page.screenshot(path=out, clip={"x": 0, "y": 0, "width": 1366, "height": 800}, animations="disabled")
        return out
    except Exception as e:
        log(f"⚠️ Erro screenshot: {e}", "shot")
        return None
    finally:
        if browser:
            try:
                browser.close()
            except Exception:
                pass


def pesquisar_no_ml(p: Playwright, perfume):
    """Wrapper pra usar nos testes individuais."""
    nome = perfume["nome"]
    log(f"💐 Pesquisando: {nome}", "ml")
    
    browser = None
    try:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = browser.new_context(
            viewport={"width": 1366, "height": 900},
            user_agent=UA,
            locale="pt-BR",
        )
        page = ctx.new_page()
        page.route("**/*.{png,jpg,jpeg,gif,svg,webp,woff,woff2,ttf,otf,css}", lambda r: r.abort())
        
        dados = pesquisar_ml_playwright(page, perfume)
        if dados:
            desc = dados.get("desconto_pct", 0)
            if desc > 0:
                log(f"   ✅ {formatar_preco(dados['preco_atual'])} (era {formatar_preco(dados.get('preco_cheio'))}, -{desc:.0f}%)", "ml")
            else:
                log(f"   ✅ {formatar_preco(dados['preco_atual'])} (sem promoção)", "ml")
        else:
            log(f"   ❌ Nenhum resultado", "ml")
        return dados
    finally:
        if browser:
            try:
                browser.close()
            except Exception:
                pass
# ============================================================================
# 💬 MENSAGEM
# ============================================================================

def formatar_alerta(perfume, dados, preco_anterior, menor_historico):
    nome = perfume["nome"]
    marca = perfume["marca"]
    emoji = perfume.get("emoji", "💐")
    genero = perfume.get("genero", "")
    
    preco_atual = dados["preco_atual"]
    preco_cheio = dados.get("preco_cheio")
    desconto_pct = dados.get("desconto_pct", 0)
    url = dados.get("url", "")
    titulo = dados.get("titulo", nome)

    if desconto_pct >= DESCONTO_MINIMO:
        tipo_alerta = f"🔥 *PROMOÇÃO {desconto_pct:.0f}% OFF!*"
    elif preco_anterior and preco_atual < preco_anterior:
        tipo_alerta = "🎉 *PREÇO BAIXOU!*"
    else:
        tipo_alerta = "💐 *PERFUME EM DESTAQUE*"

    if preco_anterior:
        diferenca = preco_atual - preco_anterior
        if diferenca < 0:
            percentual = abs((diferenca / preco_anterior) * 100)
            variacao_hist = f"📉 BAIXOU {formatar_preco(abs(diferenca))} ({percentual:.1f}%) vs última"
        elif diferenca > 0:
            percentual = (diferenca / preco_anterior) * 100
            variacao_hist = f"📈 Subiu {formatar_preco(diferenca)} ({percentual:.1f}%) vs última"
        else:
            variacao_hist = "➡️ Mesmo preço da última verificação"
    else:
        variacao_hist = "🆕 Primeira verificação"

    if preco_cheio and preco_cheio > preco_atual:
        economia = preco_cheio - preco_atual
        precos_block = (
            f"❌ ~De: {formatar_preco(preco_cheio)}~\n"
            f"✅ *Por: {formatar_preco(preco_atual)}*\n"
            f"💸 Economia: {formatar_preco(economia)} ({desconto_pct:.0f}% OFF)"
        )
    else:
        precos_block = f"💰 *Preço: {formatar_preco(preco_atual)}*"

    menor_msg = ""
    if menor_historico and preco_atual <= menor_historico:
        menor_msg = "\n🏆 *MENOR PREÇO JÁ REGISTRADO!*"
    elif menor_historico:
        menor_msg = f"\n📊 Menor histórico: {formatar_preco(menor_historico)}"

    sep = "─" * 30
    return (
        f"{tipo_alerta}\n"
        f"{sep}\n"
        f"{emoji} *{nome}*\n"
        f"🏷️ {marca}\n"
        f"{genero}\n"
        f"{sep}\n"
        f"{precos_block}\n"
        f"{sep}\n"
        f"📊 *Histórico:*\n"
        f"{variacao_hist}"
        f"{menor_msg}\n"
        f"{sep}\n"
        f"📦 _{titulo[:80] if titulo else nome}_\n"
        f"🛒 Mercado Livre\n"
        f"🔗 {url}\n"
        f"{sep}\n"
        f"🤖 _Bot de Perfumes_"
    )


# ============================================================================
# 📱 WHATSAPP
# ============================================================================

def whatsapp_auth_check(p: Playwright, page: Page) -> Page:
    try:
        expect(page.locator("#side")).to_be_visible(timeout=15000)
        log("✅ WhatsApp autenticado")
    except Exception:
        try:
            expect(page.locator("#app progress")).to_be_visible(timeout=5000)
            expect(page.locator("#side")).to_be_visible(timeout=120000)
        except Exception:
            log("⚠️ Escaneie o QR Code...")
            page.context.close()
            page = create_context(p, WHATSAPP_URL, headless=False, viewport=None)
            expect(page.locator("#side")).to_be_visible(timeout=300000)

    try:
        progress = page.locator("#app progress")
        if progress.is_visible(timeout=2000):
            expect(progress).not_to_be_attached(timeout=120000)
    except Exception:
        pass

    page.wait_for_timeout(8000)
    return page


def prior_whatsapp_auth(p: Playwright):
    context: BrowserContext = None
    try:
        log("📱 Verificando WhatsApp...")
        page = create_context(p, WHATSAPP_URL, headless=False, viewport=None)
        context = page.context
        page = whatsapp_auth_check(p, page)
        context = page.context
        log("✅ WhatsApp OK")
    finally:
        if context:
            context.close()


def send_whatsapp(p: Playwright, contact_name: str, image_path, message_text: str) -> bool:
    if not contact_name:
        return False
    if image_path and not os.path.exists(image_path):
        image_path = None

    context: BrowserContext = None
    try:
        page = create_context(p, WHATSAPP_URL, headless=True, viewport=None)
        context = page.context
        page = whatsapp_auth_check(p, page)
        context = page.context

        expect(page.locator("#side")).to_be_visible(timeout=30000)

        search = None
        for selector in [
            "#side input[type='text']",
            "div[contenteditable='true'][data-tab='3']",
            "div[contenteditable='true'][data-tab='2']",
            "#side div[contenteditable='true']",
            "div[role='textbox'][data-tab='3']",
            "#side [role='searchbox']",
        ]:
            try:
                candidate = page.locator(selector).first
                if candidate.is_visible(timeout=2000):
                    search = candidate
                    break
            except Exception:
                continue

        if not search:
            log("❌ Busca não encontrada", "wpp")
            return False

        contact_list = page.locator("#pane-side > [data-tab='4'] [aria-rowcount]").first
        contact_list_aria_label = contact_list.get_attribute("aria-label")
        search.click()
        page.wait_for_timeout(500)
        search.fill(contact_name)
        expect(contact_list).not_to_have_attribute("aria-label", contact_list_aria_label)
        contact_results = contact_list.locator("[role='gridcell'][tabindex]")
        expect(contact_results).not_to_have_count(0)
        page.wait_for_timeout(2000)
        contact_results.first.click()

        try:
            expect(page.locator("#main header").first).to_be_visible(timeout=8000)
        except Exception:
            log("❌ Chat não abriu", "wpp")
            return False

        log(f"📱 Enviando para: {contact_name}", "wpp")
        page.wait_for_timeout(1500)

        if image_path:
            target = "div[data-tab='10'][contenteditable]:not([contenteditable='false'])"
            try:
                expect(page.locator(target)).to_be_enabled(timeout=15000)
            except Exception:
                target = "#main footer div[role='textbox'][contenteditable='true']"
                expect(page.locator(target)).to_be_enabled(timeout=15000)

            with open(image_path, "rb") as f:
                content = f.read()
            file_type = mimetypes.guess_type(image_path)[0] or "image/png"

            page.evaluate(
                """
                async (args) => {
                    const [selector, fileType, base64] = args;
                    const blob = await (await fetch('data:' + fileType + ';base64,' + base64)).blob();
                    const dt = new DataTransfer();
                    dt.items.add(new File([blob], "image.png", { type: fileType }));
                    const el = document.querySelector(selector);
                    el.dispatchEvent(new ClipboardEvent('paste', { bubbles: true, cancelable: true, clipboardData: dt }));
                }
                """,
                [target, file_type, base64.b64encode(content).decode("utf-8")]
            )

            log("📎 Imagem anexada", "wpp")
            page.wait_for_timeout(4000)

            caption = None
            caption_selectors = [
                "div[contenteditable='true'][data-tab='undefined']",
                "div[role='textbox'][contenteditable='true'][data-tab='undefined']",
                "div[aria-label='Digite uma legenda']",
                "div[aria-label='Type a caption']",
                "div[aria-label='Adicionar legenda']",
                "div[aria-label='Add a caption']",
            ]
            
            log("⏳ Procurando caixa de legenda...", "wpp")
            for tentativa in range(5):
                for sel in caption_selectors:
                    try:
                        loc = page.locator(sel).first
                        if loc.is_visible(timeout=2000):
                            caption = loc
                            log(f"✅ Caixa de legenda encontrada", "wpp")
                            break
                    except Exception:
                        continue
                if caption:
                    break
                page.wait_for_timeout(1500)

            if not caption:
                log("⚠️ Tentando footer...", "wpp")
                caption = page.locator("#main footer div[role='textbox'][contenteditable='true']").first
                try:
                    expect(caption).to_be_visible(timeout=8000)
                except Exception:
                    log("❌ Nenhuma caixa encontrada!", "wpp")
                    return False

            try:
                caption.click()
                page.wait_for_timeout(500)
                caption.fill(message_text)
                page.wait_for_timeout(1500)
                
                texto_digitado = caption.inner_text() or ""
                if not texto_digitado or len(texto_digitado) < 10:
                    log("⚠️ Tentando digitar de novo...", "wpp")
                    caption.click()
                    page.wait_for_timeout(500)
                    page.keyboard.type(message_text, delay=10)
                    page.wait_for_timeout(1500)
            except Exception as e:
                log(f"⚠️ Erro: {e}", "wpp")

            log(f"✅ Legenda digitada", "wpp")
            page.wait_for_timeout(1000)

            sent = False
            for sel_envio in [
                "[aria-label='Enviar']",
                "[aria-label='Send']",
                "span[data-icon='send']",
                "button[data-testid='compose-btn-send']",
            ]:
                try:
                    btn = page.locator(sel_envio).first
                    if btn.is_visible(timeout=3000):
                        btn.click()
                        sent = True
                        break
                except Exception:
                    continue

            if not sent:
                try:
                    caption.press("Enter")
                except Exception:
                    page.keyboard.press("Enter")
        else:
            target_box = None
            for ts in [
                "div[data-tab='10'][contenteditable]:not([contenteditable='false'])",
                "#main footer div[role='textbox'][contenteditable='true']",
            ]:
                try:
                    loc = page.locator(ts).first
                    if loc.is_visible(timeout=3000):
                        target_box = loc
                        break
                except Exception:
                    continue

            if not target_box:
                return False

            target_box.click()
            page.wait_for_timeout(300)
            target_box.fill(message_text)
            page.wait_for_timeout(500)
            target_box.press("Enter")

        page.wait_for_timeout(5000)
        log(f"✅ Enviado!", "wpp")
        page.wait_for_timeout(1500)
        return True

    except Exception as e:
        log(f"❌ Erro envio: {e}", "wpp")
        return False
    finally:
        if context:
            context.close()


# ============================================================================
# 🚀 COLETA OTIMIZADA (1 browser, sequencial mas rápida)
# ============================================================================

def coletar_promocoes():
    """🚀 Coleta otimizada: 1 browser, todas as buscas dentro dele."""
    perfumes_ativos = [pe for pe in PERFUMES if pe.get("ativo", True)]
    log(f"🚀 Coletando {len(perfumes_ativos)} perfumes (Playwright otimizado)...")
    
    if len(perfumes_ativos) == 0:
        return []
    
    todos_resultados = []
    encontrados = 0
    nao_encontrados = 0
    
    inicio = time.time()
    
    # 🚀 1 BROWSER PRA TUDO
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
            ],
        )
        ctx = browser.new_context(
            viewport={"width": 1366, "height": 900},
            user_agent=UA,
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
        )
        ctx.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """)
        page = ctx.new_page()
        
        # 🚀 Bloqueia recursos desnecessários (imagens, fontes) pra ficar MAIS RÁPIDO
        page.route("**/*.{png,jpg,jpeg,gif,svg,webp,woff,woff2,ttf,otf}", lambda r: r.abort())
        page.route("**/*.css", lambda r: r.abort())
        
        try:
            for i, perfume in enumerate(perfumes_ativos, 1):
                try:
                    dados = pesquisar_ml_playwright(page, perfume)
                    
                    if dados:
                        encontrados += 1
                        desc = dados.get("desconto_pct", 0)
                        if desc > 0:
                            log(f"[{i}/{len(perfumes_ativos)}] ✅ {perfume['emoji']} {perfume['nome']}: {formatar_preco(dados['preco_atual'])} (-{desc:.0f}%)")
                        else:
                            log(f"[{i}/{len(perfumes_ativos)}] ⚪ {perfume['emoji']} {perfume['nome']}: {formatar_preco(dados['preco_atual'])} (sem promoção)")
                        todos_resultados.append((perfume, dados))
                    else:
                        nao_encontrados += 1
                        log(f"[{i}/{len(perfumes_ativos)}] ❌ {perfume['emoji']} {perfume['nome']}: não encontrado")
                except Exception as e:
                    nao_encontrados += 1
                    log(f"[{i}/{len(perfumes_ativos)}] ❌ {perfume['emoji']} {perfume['nome']}: {str(e)[:40]}")
        finally:
            try:
                browser.close()
            except Exception:
                pass
    
    tempo_total = time.time() - inicio
    log(f"\n📊 Coleta: {encontrados} encontrados | {nao_encontrados} não | {tempo_total:.1f}s ({tempo_total/60:.1f} min)")
    
    # Filtra promoção real
    if APENAS_PROMOCAO_REAL:
        com_promo = [(p, d) for p, d in todos_resultados 
                     if d.get("desconto_pct", 0) >= DESCONTO_MINIMO]
        log(f"🔥 Com promoção (>={DESCONTO_MINIMO}%): {len(com_promo)}")
    else:
        com_promo = todos_resultados
    
    # Deduplicação
    log(f"🔍 Deduplicando...")
    vistos = {}
    for perfume, dados in com_promo:
        url_norm = normalizar_url(dados.get("url", ""))
        titulo_norm = normalizar_titulo(dados.get("titulo", ""))
        chave_url = url_norm[:100] if url_norm else None
        chave_tit = titulo_norm[:80] if titulo_norm else None
        
        chave_existente = None
        if chave_url and chave_url in vistos:
            chave_existente = chave_url
        elif chave_tit and chave_tit in vistos:
            chave_existente = chave_tit
        
        if chave_existente:
            _, dados_existente = vistos[chave_existente]
            if dados["preco_atual"] < dados_existente["preco_atual"]:
                vistos[chave_existente] = (perfume, dados)
        else:
            chave = chave_url or chave_tit or perfume["nome"]
            vistos[chave] = (perfume, dados)
    
    unicos = list(vistos.values())
    log(f"✅ {len(unicos)} produtos únicos após deduplicação")
    
    unicos.sort(key=lambda x: x[1].get("desconto_pct", 0), reverse=True)
    return unicos


def enviar_um_produto(p, perfume, dados, historico):
    nome = perfume["nome"]
    preco_atual = dados["preco_atual"]
    preco_cheio = dados.get("preco_cheio")
    url = dados.get("url")
    
    preco_anterior = get_ultimo_preco(historico, nome)
    menor_historico = get_menor_preco(historico, nome)

    adicionar_ao_historico(historico, nome, preco_atual, preco_cheio, url)
    salvar_historico(historico)

    log(f"📸 Capturando print...")
    img = capturar_screenshot_busca(p, perfume, url)
    
    log(f"📝 Montando mensagem...")
    msg = formatar_alerta(perfume, dados, preco_anterior, menor_historico)
    
    log(f"📤 Enviando WhatsApp...")
    return send_whatsapp(p, CONTATO, img, msg)

# ============================================================================
# 🎯 MODO DEBUG TURBO
# ============================================================================

def modo_debug():
    """🚀 Modo DEBUG TURBO: coleta com requests + envio escalonado."""
    banner("⚡ MODO DEBUG TURBO (REQUESTS PARALELO)")
    log(f"🚀 Pesquisas paralelas: {PESQUISAS_PARALELAS}x (com requests, sem browser!)")
    log(f"⏱️ Duração envios: {DEBUG_DURACAO_MINUTOS} min")
    log(f"⏰ Intervalo: {DEBUG_INTERVALO_MINUTOS} min entre envios")
    
    max_envios = max(1, DEBUG_DURACAO_MINUTOS // DEBUG_INTERVALO_MINUTOS)
    log(f"📨 Máx envios: {max_envios}")
    
    # ===== FASE 1: COLETA (sem playwright, super rápida!) =====
    banner("🚀 FASE 1/2: COLETA RÁPIDA (REQUESTS)", char="─")
    promocoes = coletar_promocoes()
    
    if not promocoes:
        log("❌ Nenhuma promoção encontrada!")
        return
    
    top_promocoes = promocoes[:max_envios]
    
    banner(f"🏆 TOP {len(top_promocoes)} PROMOÇÕES", char="─")
    for i, (perfume, dados) in enumerate(top_promocoes, 1):
        desc = dados.get("desconto_pct", 0)
        preco = dados["preco_atual"]
        log(f"   {i}. {perfume['emoji']} {perfume['nome']:40} | {formatar_preco(preco)} | -{desc:.0f}%")
    
    # ===== FASE 2: ENVIO (com playwright) =====
    with sync_playwright() as p:
        prior_whatsapp_auth(p)
        
        banner(f"📤 FASE 2/2: ENVIANDO ({DEBUG_INTERVALO_MINUTOS} min entre cada)", char="─")
        
        historico = carregar_historico()
        inicio = datetime.datetime.now()
        sucesso = 0
        falhas = 0
        
        for i, (perfume, dados) in enumerate(top_promocoes, 1):
            agora = datetime.datetime.now()
            decorrido = (agora - inicio).total_seconds() / 60
            
            log(f"\n{'='*60}")
            log(f"📤 ENVIO {i}/{len(top_promocoes)} | Decorrido: {decorrido:.1f} min")
            log(f"{'='*60}")
            log(f"💐 {perfume['emoji']} {perfume['nome']}")
            log(f"💰 {formatar_preco(dados['preco_atual'])} (-{dados.get('desconto_pct', 0):.0f}%)")
            
            if enviar_um_produto(p, perfume, dados, historico):
                sucesso += 1
                log(f"✅ Enviado com sucesso!")
            else:
                falhas += 1
                log(f"❌ Falha no envio")
            
            if i < len(top_promocoes):
                proximo = DEBUG_INTERVALO_MINUTOS * 60
                log(f"\n💤 Próximo envio em {DEBUG_INTERVALO_MINUTOS} min...")
                time.sleep(proximo)
        
        banner("✅ MODO DEBUG FINALIZADO", char="═")
        log(f"📊 Total enviados: {sucesso}/{len(top_promocoes)}")
        log(f"❌ Falhas: {falhas}")
        log(f"⏱️ Tempo total: {(datetime.datetime.now() - inicio).total_seconds() / 60:.1f} min")


# ============================================================================
# 🔄 OUTROS MODOS
# ============================================================================

def executar_um_ciclo(p):
    banner(f"🔍 CICLO INICIADO: {datetime.datetime.now():%d/%m/%Y %H:%M:%S}")
    
    promocoes = coletar_promocoes()
    if not promocoes:
        log("❌ Nenhuma promoção")
        return
    
    top = promocoes[:10]
    log(f"\n📤 Enviando {len(top)} promoções...")
    historico = carregar_historico()
    
    for i, (perfume, dados) in enumerate(top, 1):
        log(f"\n[{i}/{len(top)}] {perfume['emoji']} {perfume['nome']}")
        enviar_um_produto(p, perfume, dados, historico)
        time.sleep(random.randint(20, 30))
    
    banner(f"✅ CICLO FINALIZADO: {datetime.datetime.now():%H:%M:%S}")


def modo_intervalo():
    banner(f"🔄 MODO INTERVALO - A cada {INTERVALO_HORAS}h")
    with sync_playwright() as p:
        prior_whatsapp_auth(p)
        while True:
            try:
                executar_um_ciclo(p)
                proxima = datetime.datetime.now() + datetime.timedelta(hours=INTERVALO_HORAS)
                log(f"\n💤 Próxima: {proxima:%d/%m/%Y %H:%M}")
                time.sleep(INTERVALO_HORAS * 3600)
            except KeyboardInterrupt:
                break
            except Exception as e:
                log(f"❌ Erro: {e}")
                time.sleep(300)


def modo_agendado():
    banner("⏰ MODO AGENDADO")
    log(f"📅 Horários: {', '.join(HORARIOS_AGENDADOS)}")
    
    with sync_playwright() as p:
        prior_whatsapp_auth(p)
        ja_executados = set()
        
        while True:
            try:
                agora = datetime.datetime.now()
                hora_atual = agora.strftime("%H:%M")
                data_atual = agora.strftime("%Y-%m-%d")
                
                if hora_atual in HORARIOS_AGENDADOS:
                    chave = f"{data_atual}_{hora_atual}"
                    if chave not in ja_executados:
                        log(f"\n⏰ HORÁRIO: {hora_atual}")
                        executar_um_ciclo(p)
                        ja_executados.add(chave)
                        ja_executados = {x for x in ja_executados if x.startswith(data_atual)}
                
                time.sleep(30)
            except KeyboardInterrupt:
                break
            except Exception as e:
                log(f"❌ Erro: {e}")
                time.sleep(60)


def main_loop():
    modo = MODO_EXECUCAO.lower().strip()
    if modo == "debug":
        modo_debug()
    elif modo == "agendado":
        modo_agendado()
    elif modo == "intervalo":
        modo_intervalo()
    else:
        log(f"❌ Modo desconhecido: '{MODO_EXECUCAO}'")


# ============================================================================
# 🧪 TESTES
# ============================================================================

def teste_listar_perfumes():
    banner("📋 PERFUMES CADASTRADOS")
    if len(PERFUMES) == 0:
        print("📭 Lista vazia!")
        return
    for i, perf in enumerate(PERFUMES, 1):
        status = "✅" if perf.get("ativo", True) else "❌"
        print(f"  {i:3}. {status} {perf['emoji']} {perf['nome']:50} | {perf.get('genero', '')}")
    masc = sum(1 for p in PERFUMES if "Masculino" in p.get("genero", ""))
    fem = sum(1 for p in PERFUMES if "Feminino" in p.get("genero", ""))
    print(f"\n📊 Total: {len(PERFUMES)} | 👨 {masc} | 👩 {fem}")


def teste_buscar_um():
    """Busca UM perfume usando Playwright otimizado."""
    banner("🔎 TESTE: Buscar UM perfume")
    ativos = [pe for pe in PERFUMES if pe.get("ativo", True)]
    print("Digite parte do nome ou número:")
    busca = input("\n👉 Busca: ").strip()
    
    try:
        idx = int(busca) - 1
        perfume = ativos[idx] if 0 <= idx < len(ativos) else None
    except ValueError:
        matches = [p for p in ativos if busca.lower() in p["nome"].lower()]
        if not matches:
            print("❌ Não encontrado")
            return
        elif len(matches) > 1:
            print(f"\n{len(matches)} encontrados:")
            for i, p in enumerate(matches, 1):
                print(f"  [{i}] {p['emoji']} {p['nome']}")
            op = input("\n👉 Número: ").strip()
            try:
                perfume = matches[int(op) - 1]
            except (ValueError, IndexError):
                return
        else:
            perfume = matches[0]
    
    if not perfume:
        return
    
    print(f"\n🔎 Buscando: {perfume['nome']}\n")
    inicio = time.time()
    
    # 🚀 Usa Playwright otimizado
    with sync_playwright() as p:
        dados = pesquisar_no_ml(p, perfume)
    
    tempo = time.time() - inicio
    
    if dados:
        print(f"\n✅ ENCONTRADO em {tempo:.1f}s!")
        print(f"💰 Atual: {formatar_preco(dados['preco_atual'])}")
        if dados.get('preco_cheio'):
            print(f"❌ Cheio: {formatar_preco(dados['preco_cheio'])}")
            print(f"💸 Desconto: {dados['desconto_pct']:.0f}%")
        print(f"📦 {dados['titulo'][:80]}")
        print(f"🔗 {dados['url']}")
    else:
        print(f"\n❌ NÃO ENCONTRADO ({tempo:.1f}s)")


def teste_envio_completo():
    banner("📤 TESTE: Envio completo")
    ativos = [pe for pe in PERFUMES if pe.get("ativo", True)]
    print("Digite parte do nome ou número:")
    busca = input("\n👉 Busca: ").strip()
    
    try:
        idx = int(busca) - 1
        perfume = ativos[idx] if 0 <= idx < len(ativos) else None
    except ValueError:
        matches = [p for p in ativos if busca.lower() in p["nome"].lower()]
        if not matches:
            return
        perfume = matches[0]
    
    if not perfume:
        return
    
    print(f"\n🔎 Testando: {perfume['nome']}\n")
    
    # 🚀 Usa Playwright otimizado
    with sync_playwright() as pw:
        prior_whatsapp_auth(pw)
        dados = pesquisar_no_ml(pw, perfume)
        
        if not dados:
            print("❌ Não conseguiu pegar preço")
            return
        
        historico = carregar_historico()
        ok = enviar_um_produto(pw, perfume, dados, historico)
        print("✅ PASSOU!" if ok else "❌ FALHOU!")

def teste_envio_completo():
    banner("📤 TESTE: Envio completo")
    ativos = [pe for pe in PERFUMES if pe.get("ativo", True)]
    print("Digite parte do nome ou número:")
    busca = input("\n👉 Busca: ").strip()
    
    try:
        idx = int(busca) - 1
        perfume = ativos[idx] if 0 <= idx < len(ativos) else None
    except ValueError:
        matches = [p for p in ativos if busca.lower() in p["nome"].lower()]
        if not matches:
            return
        perfume = matches[0]
    
    if not perfume:
        return
    
    print(f"\n🔎 Testando: {perfume['nome']}\n")
    
    # 🚀 Coleta + Envio (tudo dentro de sync_playwright)
    with sync_playwright() as pw:
        prior_whatsapp_auth(pw)
        
        # Coleta com Playwright
        dados = pesquisar_no_ml(pw, perfume)
        
        if not dados:
            print("❌ Não conseguiu pegar preço")
            return
        
        # Envia
        historico = carregar_historico()
        ok = enviar_um_produto(pw, perfume, dados, historico)
        print("✅ PASSOU!" if ok else "❌ FALHOU!")

def teste_so_coletar():
    """🚀 Coleta com REQUESTS, mostra ranking, NÃO envia."""
    banner("🚀 TESTE: COLETA TURBO (sem enviar)")
    
    inicio = time.time()
    promocoes = coletar_promocoes()
    tempo = time.time() - inicio
    
    if not promocoes:
        print("\n❌ Nenhuma promoção encontrada")
        return
    
    print(f"\n⚡ Coleta finalizada em {tempo:.1f} segundos!")
    
    banner(f"🏆 RANKING DE PROMOÇÕES ({len(promocoes)})", char="─")
    for i, (perfume, dados) in enumerate(promocoes, 1):
        desc = dados.get("desconto_pct", 0)
        preco_atual = dados["preco_atual"]
        preco_cheio = dados.get("preco_cheio")
        cheio_str = f" (era {formatar_preco(preco_cheio)})" if preco_cheio else ""
        print(f"\n  {i}. {perfume['emoji']} {perfume['nome']}")
        print(f"      💰 {formatar_preco(preco_atual)}{cheio_str}")
        if desc > 0:
            print(f"      🔥 -{desc:.0f}% OFF")
        print(f"      📦 {dados['titulo'][:70]}")
        print(f"      🔗 {dados['url'][:80]}")


def teste_debug_completo():
    banner("⚡ TESTE: Modo DEBUG TURBO completo")
    print(f"🚀 {PESQUISAS_PARALELAS} pesquisas em paralelo (REQUESTS)")
    print(f"⚡ Coleta esperada: ~30 segundos")
    print(f"⏱️ Duração total: ~{DEBUG_DURACAO_MINUTOS + 1} min")
    print(f"📨 Vai enviar até {DEBUG_DURACAO_MINUTOS // DEBUG_INTERVALO_MINUTOS} promoções\n")
    
    confirma = input("Continuar? (s/n): ").strip().lower()
    if confirma != "s":
        return
    modo_debug()


def teste_proximos_horarios():
    banner("⏰ PRÓXIMOS HORÁRIOS")
    print(f"📅 Configurados: {', '.join(HORARIOS_AGENDADOS)}\n")
    agora = datetime.datetime.now()
    print(f"⏰ Agora: {agora:%d/%m/%Y %H:%M:%S}\n")
    print("Próximas 8 execuções:\n")
    encontradas = []
    dias = 0
    while len(encontradas) < 8 and dias < 7:
        dia = agora + datetime.timedelta(days=dias)
        for h in HORARIOS_AGENDADOS:
            h_dt = datetime.datetime.strptime(f"{dia:%Y-%m-%d} {h}", "%Y-%m-%d %H:%M")
            if h_dt > agora:
                encontradas.append(h_dt)
        dias += 1
    for i, h_dt in enumerate(encontradas[:8], 1):
        diff = h_dt - agora
        horas = int(diff.total_seconds() / 3600)
        print(f"  {i}. {h_dt:%d/%m %a %H:%M} (em {horas}h)")


def teste_historico():
    banner("📊 HISTÓRICO DE PREÇOS")
    historico = carregar_historico()
    if not historico:
        print("📭 Nenhum histórico ainda")
        return
    print(f"📊 {len(historico)} produtos\n")
    for nome, registros in sorted(historico.items()):
        print(f"\n💐 {nome}")
        print("─" * 60)
        for reg in registros[-5:]:
            data = datetime.datetime.fromisoformat(reg["data"])
            cheio = reg.get("preco_cheio")
            cheio_str = f" (cheio: {formatar_preco(cheio)})" if cheio else ""
            print(f"  {data:%d/%m/%Y %H:%M} | {formatar_preco(reg['preco'])}{cheio_str}")


def teste_estatisticas():
    banner("📊 ESTATÍSTICAS")
    total = len(PERFUMES)
    ativos = [p for p in PERFUMES if p.get("ativo", True)]
    masc = [p for p in ativos if "Masculino" in p.get("genero", "")]
    fem = [p for p in ativos if "Feminino" in p.get("genero", "")]
    
    print(f"📋 TOTAL: {total}")
    print(f"✅ ATIVOS: {len(ativos)}")
    print(f"👨 MASCULINOS: {len(masc)}")
    print(f"👩 FEMININOS: {len(fem)}\n")
    
    marcas = {}
    for p in ativos:
        m = p["marca"]
        marcas[m] = marcas.get(m, 0) + 1
    print("🏷️ POR MARCA:")
    for marca, qtd in sorted(marcas.items(), key=lambda x: -x[1]):
        print(f"   {marca}: {qtd}")
    
    historico = carregar_historico()
    print(f"\n💾 Histórico: {len(historico)} produtos")
    print(f"\n⚙️ CONFIGURAÇÕES:")
    print(f"   Modo: {MODO_EXECUCAO}")
    print(f"   🚀 Paralelas: {PESQUISAS_PARALELAS}")
    print(f"   Apenas promoção real: {APENAS_PROMOCAO_REAL}")
    print(f"   Desconto mínimo: {DESCONTO_MINIMO}%")
    print(f"   Debug: {DEBUG_DURACAO_MINUTOS}min, 1 a cada {DEBUG_INTERVALO_MINUTOS}min")


def teste_limpar_historico():
    banner("🗑️ LIMPAR HISTÓRICO")
    historico = carregar_historico()
    if not historico:
        print("📭 Nada pra limpar")
        return
    print(f"📊 {len(historico)} produtos no histórico")
    confirma = input("\n⚠️ Confirmar? (sim/não): ").strip().lower()
    if confirma in ["sim", "s", "y", "yes"]:
        if os.path.exists(HISTORICO_FILE):
            os.remove(HISTORICO_FILE)
        print("✅ Limpo!")
    else:
        print("❌ Cancelado")


def menu_teste():
    opcoes = {
        "1": ("Listar perfumes", teste_listar_perfumes),
        "2": ("📊 Estatísticas", teste_estatisticas),
        "3": ("🔎 Buscar UM perfume (RÁPIDO)", teste_buscar_um),
        "4": ("📤 Envio completo (1 perfume)", teste_envio_completo),
        "5": ("🚀 SÓ COLETAR TURBO (não envia)", teste_so_coletar),
        "6": ("⚡ MODO DEBUG TURBO completo", teste_debug_completo),
        "7": ("⏰ Próximos horários", teste_proximos_horarios),
        "8": ("📈 Histórico", teste_historico),
        "9": ("🗑️ Limpar histórico", teste_limpar_historico),
    }
    while True:
        banner(f"🧪 MODO DE TESTE - {MODO_EXECUCAO.upper()} (REQUESTS {PESQUISAS_PARALELAS}x)")
        for k, (desc, _) in opcoes.items():
            print(f"  [{k}] {desc}")
        print("  [0] Sair\n")
        op = input("👉 Escolha: ").strip()
        if op == "0":
            break
        if op in opcoes:
            try:
                opcoes[op][1]()
            except Exception as e:
                print(f"❌ {e}")
                import traceback
                traceback.print_exc()
            input("\n⏸️ ENTER...")


# ============================================================================
# 🚀 MAIN
# ============================================================================

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            arg = sys.argv[1].lower()
            if arg == "teste":
                menu_teste()
            elif arg == "debug":
                modo_debug()
            elif arg == "agendado":
                modo_agendado()
            elif arg == "intervalo":
                modo_intervalo()
            else:
                print(f"❌ Argumento inválido: {arg}")
                print("\n📋 Comandos:")
                print("   python bot_perfumes.py            ← Modo configurado")
                print("   python bot_perfumes.py teste      ← Menu de testes")
                print("   python bot_perfumes.py debug      ← TURBO escalonado")
                print("   python bot_perfumes.py agendado   ← Horários fixos")
                print("   python bot_perfumes.py intervalo  ← A cada X horas")
        else:
            main_loop()
    except KeyboardInterrupt:
        log("\n⛔ Encerrado")
        sys.exit(0)
