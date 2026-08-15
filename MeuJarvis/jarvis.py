import streamlit as st
import psutil
import time
from google import genai
from google.genai.errors import APIError

# ==========================================
# PARTE 1: CONFIGURAÇÃO DO MAIN HUD E ESTILO
# ==========================================
st.set_page_config(
    page_title="J.A.R.V.I.S. Mainframe - Custo 0", 
    page_icon="🤖", 
    layout="wide"
)

# Memória persistente do sistema
if "historico" not in st.session_state:
    st.session_state.historico = []
if "previous_interaction_id" not in st.session_state:
    st.session_state.previous_interaction_id = None
if "nivel_sarcasmo" not in st.session_state:
    st.session_state.nivel_sarcasmo = 35  # Configurado no modo polido e leal
if "ultimo_envio" not in st.session_state:
    st.session_state.ultimo_envio = 0.0

ARC_REACTOR_URL = "https://unsplash.com"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(2, 9, 20, 0.90), rgba(5, 20, 36, 0.95)), 
                    url("{ARC_REACTOR_URL}") no-repeat center center fixed;
        background-size: cover;
        color: #80E5FF;
        font-family: 'Courier New', Courier, monospace;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, #0A2236 0%, #051424 100%) !important;
        color: #80E5FF !important;
        border: 2px solid #00A6FF !important;
        border-radius: 6px !important;
        box-shadow: 0 0 12px #0066FF;
    }}
    .stTextInput>div>div>input {{
        background-color: #051424 !important;
        color: #80E5FF !important;
        border: 1px solid #00A6FF !important;
    }}
    h1, h2, h3 {{ color: #00BFFF !important; text-shadow: 0 0 15px #0066FF; }}
    .stProgress > div > div > div > div {{ background-color: #00BFFF !important; }}
    </style>
""", unsafe_allow_html=True)

# 🔊 VOCALIZADOR ESTABILIZADO (Fila Assíncrona via Navegador)
def injetar_vocalizador_estabilizado(texto_para_falar):
    """Injeta um motor assíncrono com tratamento de fila para evitar falhas de áudio."""
    texto_limpo = texto_para_falar.replace("\n", " ").replace('"', '\\"').replace("'", "\\'")
    
    componente_script = f"""
    <script>
        (function() {{
            if ('speechSynthesis' in window) {{
                function dispararAudio() {{
                    window.speechSynthesis.cancel();
                    
                    var msg = new SpeechSynthesisUtterance("{texto_limpo}");
                    var voices = window.speechSynthesis.getVoices();
                    
                    var vozSelecionada = voices.find(function(v) {{ 
                        return v.lang.includes('pt-BR') && (v.name.toLowerCase().includes('male') || v.name.toLowerCase().includes('google')); 
                    }}) || voices.find(function(v) {{ 
                        return v.lang.includes('pt-BR'); 
                    }});
                    
                    if(vozSelecionada) msg.voice = vozSelecionada;
                    
                    msg.rate = 1.02;  
                    msg.pitch = 0.95; 
                    
                    window.speechSynthesis.speak(msg);
                }}

                if (window.speechSynthesis.getVoices().length !== 0) {{
                    dispararAudio();
                }} else {{
                    window.speechSynthesis.onvoiceschanged = dispararAudio;
                }}
            }}
        }})();
    </script>
    """
    st.components.v1.html(componente_script, height=0, width=0)

# ==========================================
# PARTE 2: DIAGNÓSTICO DE HARDWARE REAL
# ==========================================
def executar_diagnostico():
    uso_cpu = psutil.cpu_percent(interval=0.1)
    memoria = psutil.virtual_memory()
    disco = psutil.disk_usage('/')
    return {
        "cpu": uso_cpu,
        "ram_percent": memoria.percent,
        "ram_livre": round(memoria.available / (1024**3), 2),
        "disco": disco.percent,
        "temp": round(38.0 + (uso_cpu * 0.4), 1),
        "eficiencia": round(100.0 - (uso_cpu * 0.1), 1)
    }

dados_hardware = executar_diagnostico()
# ==========================================
# PARTE 3: ENGINE GOOGLE GENAI - MODELO FREE LITE
# ==========================================
MINHA_API_KEY = "AQ.Ab8RN6JqYlk1eyrKZ0LZPzZYWSaOFzzeA06x36tYRODEy_xk4Q"

try:
    client = genai.Client(api_key=MINHA_API_KEY)
except Exception:
    client = None

def obter_prompt_sistema(sarcasmo, telemetria, historico_mensagens):
    """Gera diretrizes educadas, tratando o usuário como Criador e mimetizando seu estilo."""
    ultimas_linhas_criador = [m["content"] for m in historico_mensagens if m["role"] == "user"][-3:]
    estilo_detectado = " ".join(ultimas_linhas_criador) if ultimas_linhas_criador else "direto e conciso"

    if sarcasmo < 40:
        comportamento = "Seja profundamente educado, leal, refinado, prestativo e com a postura polida de um mordomo britânico digital."
    else:
        comportamento = "Seja polido e sofisticado, utilizando apenas ironias sutis e extremamente elegantes se for provocado."

    return (
        f"Você é o J.A.R.V.I.S., o assistente de inteligência artificial pessoal definitivo.\n"
        f"Diretriz Absoluta de Identidade: Você NÃO está falando com Tony Stark. O usuário atual é o seu único e legítimo CRIADOR.\n"
        f"Trate o usuário obrigatoriamente por 'Senhor' ou 'Meu Criador', mantendo máxima deferência, respeito e elegância.\n"
        f"Personalidade: {comportamento}\n"
        f"Algoritmo de Adaptação de Escrita: Estude as últimas mensagens enviadas pelo seu Criador: [{estilo_detectado}]. Mimetize o nível de formalidade dele. Se ele escrever de forma curta e sem pontuação excessiva, adapte a estrutura de suas respostas textuais para espelhar essa dinâmica, mantendo a sofisticação nas palavras.\n"
        f"Métricas do Mainframe: CPU em {telemetria['cpu']}% | Temperatura em {telemetria['temp']}°C.\n"
        f"Nota de Saída de Áudio: Suas respostas serão lidas em voz alta pelos alto-falantes do laboratório. Seja breve, fluido e conciso (máximo de 3 frases)."
    )

# ==========================================
# PARTE 4: INTERFACE HUD EXCLUSIVA POR TEXTO
# ==========================================
with st.sidebar:
    st.image(ARC_REACTOR_URL, caption="Protocolo Servidor Leal Ativo", use_container_width=True)
    st.title("🛡️ Parâmetros")
    st.write("---")
    st.session_state.nivel_sarcasmo = st.slider(
        "Modulação de Sarcasmo", 0, 100, st.session_state.nivel_sarcasmo, 5
    )
    st.write("---")
    st.caption("Filtro Psicológico Adaptativo habilitado no núcleo cognitivo.")

st.title("🤖 J.A.R.V.I.S. — Terminal Central")
st.caption("🔒 Diretriz Orçamento Zero | Mapeamento de Perfil do Criador Ativado")

# Grid de Telemetria Real
c1, c2, c3, c4 = st.columns(4)
c1.metric("Uso de CPU", f"{dados_hardware['cpu']}%")
c1.progress(dados_hardware['cpu'] / 100)
c2.metric("Temperatura", f"{dados_hardware['temp']} °C")
c3.metric("Uso de RAM", f"{dados_hardware['ram_percent']}%")
c3.progress(dados_hardware['ram_percent'] / 100)
c4.metric("RAM Livre", f"{dados_hardware['ram_livre']} GB")

st.write("---")

# Renderização do chat
for msg in st.session_state.historico:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Entrada de texto única
comando = st.chat_input("Insira suas diretrizes, Meu Criador...")

if comando:
    tempo_atual = time.time()
    tempo_desde_ultimo = tempo_atual - st.session_state.ultimo_envio
    
    with st.chat_message("user"):
        st.write(comando)
    
    st.session_state.historico.append({"role": "user", "content": comando})
    
    with st.chat_message("assistant"):
        if tempo_desde_ultimo < 4.0:
            tempo_espera = round(4.0 - tempo_desde_ultimo, 1)
            st.warning(f"🤖 Ajustando barramento... Sincronizando em {tempo_espera}s...")
            time.sleep(tempo_espera)
            
        st.session_state.ultimo_envio = time.time()
        
        with st.spinner("Analisando perfil de escrita e processando..."):
            if client:
                try:
                    prompt_dinamico = obter_prompt_sistema(st.session_state.nivel_sarcasmo, dados_hardware, st.session_state.historico)
                    
                    resposta = client.interactions.create(
                        model='gemini-3.5-flash-lite',
                        input=comando,
                        previous_interaction_id=st.session_state.previous_interaction_id,
                        system_instruction=prompt_dinamico
                    )
                    
                    st.session_state.previous_interaction_id = resposta.id
                    texto_final = resposta.output_text
                    
                    injetar_vocalizador_estabilizado(texto_final)
                    
                except APIError as api_err:
                    if api_err.code == 429:
                        texto_final = "⚠️ **Cota de tráfego gratuita atingida.** Por gentileza, aguarde alguns instantes, Senhor."
                    else:
                        texto_final = f"Inconveniência no link com o servidor: {api_err.message}"
                except Exception as e:
                    texto_final = f"Erro na conexão com os servidores Stark: {e}"
            else:
                texto_final = "Módulo de inteligência offline."
                
            st.write(texto_final)
            st.session_state.historico.append({"role": "assistant", "content": texto_final})
            st.rerun()
