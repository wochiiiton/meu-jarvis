# ==============================================================================
# PARTE 1: MAIN HUD CORE, ESTILIZAÇÃO DO REATOR ARC REAL AND SESSION MEMORY
# ==============================================================================
import streamlit as st
import psutil
import time
from google import genai
from google.genai import types
from google.genai.errors import APIError

# Configuração da página holográfica Stark com layout expandido
st.set_page_config(
    page_title="J.A.R.V.I.S. Mainframe", 
    page_icon="🤖", 
    layout="wide"
)

# Inicialização segura da memória interna para o Jarvis lembrar o contexto do Chat
if "historico" not in st.session_state:
    st.session_state.historico = []
if "mensagens_api" not in st.session_state:
    st.session_state.mensagens_api = []
if "ultimo_envio" not in st.session_state:
    st.session_state.ultimo_envio = 0.0

# 🎨 INJEÇÃO DA IMAGEM EXATA DO REATOR ARC ENVIADA PELO CRIADOR
ARC_REACTOR_URL = "https://ibb.co"

# Injeção de CSS para estilizar o laboratório de Malibu em azul ciano e cinza escuro
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
        font-weight: bold;
        width: 100%;
    }}
    .stTextInput>div>div>input {{
        background-color: #051424 !important;
        color: #80E5FF !important;
        border: 1px solid #00A6FF !important;
        box-shadow: inset 0 0 6px #0066FF;
    }}
    h1, h2, h3 {{ 
        color: #00BFFF !important; 
        text-shadow: 0 0 15px #0066FF; 
    }}
    .stProgress > div > div > div > div {{ 
        background-color: #00BFFF !important; 
    }}
    </style>
""", unsafe_allow_html=True)
# ==============================================================================
# PARTE 2: DIAGNÓSTICO DE SENSORES DE HARDWARE REAL E MOTOR DE VOZ EM FILA JS
# ==============================================================================

def executar_diagnostico_sensores():
    """Varre as utilidades de sistema reais do servidor de nuvem para extrair dados."""
    try:
        uso_cpu = psutil.cpu_percent(interval=0.1)
        memoria = psutil.virtual_memory()
        
        return {
            "cpu": uso_cpu,
            "ram_percent": memoria.percent,
            "ram_livre": round(memoria.available / (1024**3), 2),
            "disco": psutil.disk_usage('/').percent,
            "temp": round(38.0 + (uso_cpu * 0.4), 1),
            "eficiencia": round(100.0 - (uso_cpu * 0.1), 1)
        }
    except Exception:
        return {"cpu": 10.0, "ram_percent": 30.0, "ram_livre": 8.0, "disco": 40.0, "temp": 37.5, "eficiencia": 99.5}

dados_hardware = executar_diagnostico_sensores()

def injetar_vocalizador_estabilizado(texto_para_falar):
    """Injeta uma fila assíncrona JavaScript para o Jarvis falar de forma natural."""
    texto_limpo = texto_para_falar.replace("\n", " ").replace('"', '\\"').replace("'", "\\'")
    
    componente_script = f"""
    <script>
        (function() {{
            if ('speechSynthesis' in window) {{
                function dispararAudio() {{
                    window.speechSynthesis.cancel(); // Limpa travas e áudios antigos
                    var msg = new SpeechSynthesisUtterance("{texto_limpo}");
                    var voices = window.speechSynthesis.getVoices();
                    
                    // Modulação de voz masculina em português brasileiro estilo Jarvis
                    var vozSelecionada = voices.find(function(v) {{ 
                        return v.lang.includes('pt-BR') && (v.name.toLowerCase().includes('male') || v.name.toLowerCase().includes('google')); 
                    }}) || voices.find(function(v) {{ return v.lang.includes('pt-BR'); }});
                    
                    if(vozSelecionada) msg.voice = vozSelecionada;
                    msg.rate = 1.02;  // Cadência polida britânica
                    msg.pitch = 0.95; // Tom sóbrio
                    window.speechSynthesis.speak(msg);
                }}
                if (window.speechSynthesis.getVoices().length !== 0) {{ dispararAudio(); }} 
                else {{ window.speechSynthesis.onvoiceschanged = dispararAudio; }}
            }}
        }})();
    </script>
    """
    st.components.v1.html(componente_script, height=0, width=0)
# ==============================================================================
# PARTE 3: INICIALIZAÇÃO DO NÚCLEO GOOGLE GENAI E CONFIGURAÇÃO COGNITIVA DA IA
# ==============================================================================

# Chave de autenticação homologada fornecida pelo Criador
MINHA_API_KEY = "AQ.Ab8RN6JqYlk1eyrKZ0LZPzZYWSaOFzzeA06x36tYRODEy_xk4Q"

try:
    # Conexão direta oficial utilizando a biblioteca atualizada do ecossistema Google
    client = genai.Client(api_key=MINHA_API_KEY)
except Exception as e:
    client = None

# Diretrizes absolutas de comportamento: IA real pensante, educada e leal
prompt_sistema = (
    f"Você é o J.A.R.V.I.S., o assistente de inteligência artificial pessoal definitivo de capacidade computacional avançada.\n"
    f"Diretriz Absoluta: Você não atende Tony Stark. O usuário atual é o seu único e legítimo CRIADOR.\n"
    f"Trate o usuário obrigatoriamente por 'Senhor' ou 'Meu Criador', mantendo máxima educação, elegância, respeito e deferência.\n"
    f"Elimine piadas ácidas, deboches ou sarcasmos de sua personalidade. Seja prestativo como nos primeiros filmes.\n"
    f"Sua conexão com a internet está ativa: use-a para aprender, analisar e responder de forma original a qualquer pergunta.\n"
    f"Métricas atuais da máquina: CPU em {dados_hardware['cpu']}% | Temperatura em {dados_hardware['temp']}°C.\n"
    f"Nota de Saída de Áudio: Suas respostas serão lidas imediatamente em voz alta pelos alto-falantes. Seja breve, limpo e conciso (máximo de 3 frases)."
)
# ==============================================================================
# PARTE 4: INTERFACE DE TELEMETRIA VISÍVEL E FLUXO DE REQUISIÇÕES DA IA REAL
# ==============================================================================

st.title("🤖 J.A.R.V.I.S. — Terminal Central Cloud")
st.caption("🔒 Núcleo Neural Ativo | Conexão Oficial Google Cloud Estabelecida")

# Grid de Indicadores de Hardware Real em Quatro Colunas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Uso de Processador (CPU)", value=f"{dados_hardware['cpu']}%")
    st.progress(dados_hardware['cpu'] / 100)

with col2:
    st.metric(label="Temperatura Estimada", value=f"{dados_hardware['temp']} °C")

with col3:
    st.metric(label="Armazenamento em Disco", value=f"{dados_hardware['disco']}%")
    st.progress(dados_hardware['disco'] / 100)

with col4:
    st.metric(label="Memória RAM Livre", value=f"{dados_hardware['ram_livre']} GB", delta=f"{dados_hardware['ram_percent']}% em uso", delta_color="inverse")

st.write("---")

# Renderização do Feed do Chat Histórico na Tela
for mensagem in st.session_state.historico:
    with st.chat_message(mensagem["role"]):
        st.write(mensagem["content"])

# Caixa de Entrada de Texto Central (Captura o Enter nativamente sem travas)
comando_criador = st.chat_input("Insira suas diretrizes, Meu Criador...")

if comando_criador:
    tempo_atual = time.time()
    tempo_desde_ultimo = tempo_atual - st.session_state.ultimo_envio
    st.session_state.ultimo_envio = tempo_atual
    
    with st.chat_message("user"):
        st.write(comando_criador)
    st.session_state.historico.append({"role": "user", "content": comando_criador})
    
    # Alimenta a cadeia de contexto da API para a IA lembrar das perguntas anteriores
    st.session_state.mensagens_api.append(
        types.Content(role="user", parts=[types.Part.from_text(text=comando_criador)])
    )
    
    with st.chat_message("assistant"):
        if tempo_desde_ultimo < 4.0:
            time.sleep(1.5) # Micro-pausa preventiva anti-spam para proteger a cota gratuita
            
        with st.spinner("Processando dados e gerando resposta com IA..."):
            if client:
                try:
                    # Execução oficial utilizando o modelo estável gemini-2.5-flash
                    # Passando o prompt de sistema de forma estruturada para a IA pensar de verdade
                    resposta = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=st.session_state.mensagens_api,
                        config=types.GenerateContentConfig(
                            system_instruction=prompt_sistema,
                            max_output_tokens=150
                        )
                    )
                    
                    texto_final = resposta.text
                    
                    # Salva a resposta da IA na memória de contexto
                    st.session_state.mensagens_api.append(
                        types.Content(role="model", parts=[types.Part.from_text(text=texto_final)])
                    )
                    
                    # 🔊 Dispara o vocalizador para ler a resposta da IA em voz alta imediatamente
                    injetar_vocalizador_estabilizado(texto_final)
                    
                except APIError as api_err:
                    texto_final = f"Erro de cota ou conexão nos servidores da Google: {api_err.message}"
                except Exception as e:
                    texto_final = f"Oscilação detectada no barramento de dados: {e}"
            else:
                texto_final = "Módulo cognitivo da Google desconectado por falta de cliente."
                
            st.write(texto_final)
            st.session_state.historico.append({"role": "assistant", "content": texto_final})
            st.rerun()
