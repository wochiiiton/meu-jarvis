import streamlit as st
from google import genai
from google.genai import types

# ======== CONFIGURAÇÃO DA CHAVE E CLIENTE GOOGLE ========
MINHA_API_KEY = "AQ.Ab8RN6JqYlk1eyrKZ0LZPzZYWSaOFzzeA06x36tYRODEy_xk4Q"

try:
    # Inicialização direta do cliente oficial Google GenAI
    client = genai.Client(api_key=MINHA_API_KEY)
except Exception as e:
    st.error(f"Erro na API: {e}")

# ======== INTERFACE VISUAL DO REATOR ARC ========
st.set_page_config(page_title="J.A.R.V.I.S. Mainframe", page_icon="🤖", layout="centered")

# Imagem do seu Reator Arc aplicada nativamente no plano de fundo
ARC_REACTOR_URL = "https://ibb.co"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(2, 9, 20, 0.90), rgba(5, 20, 36, 0.95)), 
                    url("{ARC_REACTOR_URL}") no-repeat center center fixed;
        background-size: cover;
        color: #80E5FF;
    }}
    .stButton>button {{ background-color: #0A2236 !important; color: #80E5FF !important; border: 2px solid #00A6FF !important; }}
    .stTextInput>div>div>input {{ background-color: #051424 !important; color: #80E5FF !important; border: 1px solid #00A6FF !important; }}
    h1 {{ color: #00BFFF !important; text-shadow: 0 0 15px #0066FF; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 J.A.R.V.I.S. — Sistema Online")
st.write("---")

# 🔊 VOCALIZADOR VIRTUAL ESTABILIZADO (Injeção de Áudio Nativa Gratuita no Navegador)
def injetar_vocalizador_estabilizado(texto_para_falar):
    # Trata caracteres especiais para não quebrar a injeção do script JavaScript
    texto_limpo = texto_para_falar.replace("\n", " ").replace('"', '\\"').replace("'", "\\'")
    componente_script = f"""
    <script>
        (function() {{
            if ('speechSynthesis' in window) {{
                function dispararAudio() {{
                    window.speechSynthesis.cancel(); // Limpa a fila para não encavalar áudios
                    var msg = new SpeechSynthesisUtterance("{texto_limpo}");
                    var voices = window.speechSynthesis.getVoices();
                    
                    // Busca por vozes masculinas em português para manter o perfil do Jarvis
                    var vozSelecionada = voices.find(function(v) {{ 
                        return v.lang.includes('pt-BR') && (v.name.toLowerCase().includes('male') || v.name.toLowerCase().includes('google')); 
                    }}) || voices.find(function(v) {{ return v.lang.includes('pt-BR'); }});
                    
                    if(vozSelecionada) msg.voice = vozSelecionada;
                    msg.rate = 1.02; // Modulação de velocidade calma e britânica
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

# Personalidade elegante do Jarvis com acesso à internet habilitado
PROMPT_SISTEMA = (
    "Você é o J.A.R.V.I.S., o assistente pessoal de inteligência artificial definitivo. "
    "Diretriz Absoluta: Você NÃO atende Tony Stark. O usuário atual é o seu único e legítimo CRIADOR. "
    "Responda sempre em português brasileiro, de forma altamente inteligente, educada e sofisticada, como um mordomo britânico digital. "
    "Trate o usuário obrigatoriamente por 'Senhor' ou 'Meu Criador'. Use sua conexão com a internet para aprender, pesquisar em tempo real e trazer dados precisos. "
    "Diretriz Vocal Estrita: Suas respostas serão transformadas em áudio imediatamente. Seja direto e evite respostas excessivamente longas ou cheias de símbolos técnicos para que a leitura por voz permaneça natural e fluida (tente se limitar a um ou dois parágrafos claros)."
)

# Memória do Chat
if "historico" not in st.session_state: st.session_state.historico = []
if "mensagens_api" not in st.session_state: st.session_state.mensagens_api = []

for msg in st.session_state.historico:
    with st.chat_message(msg["role"]): st.write(msg["content"])

# Execução dos Comandos por Texto
comando_final = st.chat_input("O que deseja pesquisar ou ordenar, Meu Criador?")

if comando_final:
    with st.chat_message("user"): st.write(comando_final)
    st.session_state.historico.append({"role": "user", "content": comando_final})
    st.session_state.mensagens_api.append(types.Content(role="user", parts=[types.Part.from_text(text=comando_final)]))

    with st.chat_message("assistant"):
        with st.spinner("Consultando banco de dados global..."):
            try:
                # MODELO ATIVO, ESTÁVEL E TOTALMENTE COMPATÍVEL: gemini-2.5-flash
                resposta = client.models.generate_content(
                    model='gemini-2.5-flash', 
                    contents=st.session_state.mensagens_api,
                    config=types.GenerateContentConfig(system_instruction=PROMPT_SISTEMA)
                )
                
                texto_final = resposta.text
                st.write(texto_final)
                
                # 🔊 Dispara a voz do Jarvis imediatamente sincronizada com a resposta
                injetar_vocalizador_estabilizado(texto_final)
                
                st.session_state.historico.append({"role": "assistant", "content": texto_final})
                st.session_state.mensagens_api.append(types.Content(role="model", parts=[types.Part.from_text(text=texto_final)]))
            except Exception as e:
                st.error(f"Erro na conexão com os servidores Stark: {e}")
