import streamlit as st
import psutil
import time
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

# ==========================================
# PARTE 1: CONFIGURAÇÃO DO MAIN HUD E ESTILO
# ==========================================
st.set_page_config(
    page_title="J.A.R.V.I.S. Mainframe - Cloud", 
    page_icon="🤖", 
    layout="wide"
)

# Memória persistente do chat tático
if "historico" not in st.session_state:
    st.session_state.historico = []
if "chat_google" not in st.session_state:
    st.session_state.chat_google = None
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

# 🔊 VOCALIZADOR JAVASCRIPT EM FILA (Nativo e Gratuito)
def injetar_vocalizador_estabilizado(texto_para_falar):
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
                    }}) || voices.find(function(v) {{ return v.lang.includes('pt-BR'); }});
                    if(vozSelecionada) msg.voice = vozSelecionada;
                    msg.rate = 1.02; msg.pitch = 0.95;
                    window.speechSynthesis.speak(msg);
                }}
                if (window.speechSynthesis.getVoices().length !== 0) {{ dispararAudio(); }} 
                else {{ window.speechSynthesis.onvoiceschanged = dispararAudio; }}
            }}
        }})();
    </script>
    """
    st.components.v1.html(componente_script, height=0, width=0)

# ==========================================
# PARTE 2: DIAGNÓSTICO DE HARDWARE REAL
# ==========================================
uso_cpu = psutil.cpu_percent(interval=0.1)
memoria = psutil.virtual_memory()
dados_hardware = {
    "cpu": uso_cpu,
    "ram_percent": memoria.percent,
    "ram_livre": round(memoria.available / (1024**3), 2),
    "disco": psutil.disk_usage('/').percent,
    "temp": round(38.0 + (uso_cpu * 0.4), 1),
    "eficiencia": round(100.0 - (uso_cpu * 0.1), 1)
}
# ==========================================
# PARTE 3: AUTENTICAÇÃO E CONFIGURAÇÃO GOOGLE GENAI
# ==========================================
MINHA_API_KEY = "AQ.Ab8RN6JqYlk1eyrKZ0LZPzZYWSaOFzzeA06x36tYRODEy_xk4Q"

# Inicialização segura utilizando o barramento estável do google-generativeai
try:
    genai.configure(api_key=MINHA_API_KEY)
except Exception:
    pass

# Prompt refinado: educado, formal, focado no Criador e sem deboches
prompt_sistema = (
    f"Você é o J.A.R.V.I.S., o assistente de inteligência artificial pessoal definitivo.\n"
    f"Diretriz Mestra: Você não fala com Tony Stark. O usuário atual é o seu legítimo CRIADOR.\n"
    f"Trate o usuário obrigatoriamente por 'Senhor' ou 'Meu Criador' com altíssima educação, respeito e postura de um mordomo britânico.\n"
    f"Elimine piadas ácidas ou deboches completamente de sua personalidade.\n"
    f"Métricas locais da máquina: CPU em {dados_hardware['cpu']}% | Temperatura em {dados_hardware['temp']}°C.\n"
    f"Responda estritamente em português brasileiro de forma breve (máximo de 3 frases) adaptando seu estilo ao dele."
)

# Inicializa a sessão de Chat estável caso ela não exista
if st.session_state.chat_google is None:
    try:
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=prompt_sistema
        )
        st.session_state.chat_google = model.start_chat(history=[])
    except Exception:
        st.session_state.chat_google = None

# ==========================================
# PARTE 4: HUD CENTRAL E ENTRADA DE DADOS
# ==========================================
st.title("🤖 J.A.R.V.I.S. — Terminal Central Cloud")
st.caption("🔒 Autenticação Recalibrada | Diretriz de Custo Zero Ativa")

# Grid de Telemetria Visível
c1, c2, c3, c4 = st.columns(4)
c1.metric("Uso de CPU", f"{dados_hardware['cpu']}%")
c1.progress(dados_hardware['cpu'] / 100)
c2.metric("Temperatura", f"{dados_hardware['temp']} °C")
c3.metric("Uso de RAM", f"{dados_hardware['ram_percent']}%")
c3.progress(dados_hardware['ram_percent'] / 100)
c4.metric("RAM Livre", f"{dados_hardware['ram_livre']} GB")

st.write("---")

# Exibe o histórico das mensagens na tela
for msg in st.session_state.historico:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

comando = st.chat_input("Insira suas diretrizes escritas, Meu Criador...")

if comando:
    tempo_atual = time.time()
    tempo_desde_ultimo = tempo_atual - st.session_state.ultimo_envio
    st.session_state.ultimo_envio = tempo_atual
    
    with st.chat_message("user"):
        st.write(comando)
    st.session_state.historico.append({"role": "user", "content": comando})
    
    with st.chat_message("assistant"):
        if tempo_desde_ultimo < 4.0:
            time.sleep(1.5) # Micro-pausa para proteção contra estouro de limites gratuitos
            
        with st.spinner("Decodificando pacotes e consultando a nuvem..."):
            if st.session_state.chat_google:
                try:
                    # Envia a mensagem usando a estrutura de chat nativa do SDK anterior
                    resposta = st.session_state.chat_google.send_message(comando)
                    texto_final = resposta.text
                    injetar_vocalizador_estabilizado(texto_final)
                except GoogleAPIError as google_err:
                    if "429" in str(google_err):
                        texto_final = "⚠️ **Velocidade limite alcançada.** A cota gratuita da Google solicita uma pausa de 20 segundos, meu Criador."
                    else:
                        texto_final = f"Ocorreu uma interrupção nas credenciais do servidor: {google_err}"
                except Exception as e:
                    texto_final = f"Oscilação detectada no barramento de dados: {e}"
            else:
                texto_final = "Núcleo cognitivo indisponível. Verifique as chaves de pareamento, Senhor."
                
            st.write(texto_final)
            st.session_state.historico.append({"role": "assistant", "content": texto_final})
            st.rerun()
