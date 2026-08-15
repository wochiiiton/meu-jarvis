import streamlit as st
import speech_recognition as sr
from google import genai
from google.genai import types

# ======== CONFIGURAÇÃO DA CHAVE E CLIENTE GOOGLE ========
MINHA_API_KEY = "AQ.Ab8RN6JqYlk1eyrKZ0LZPzZYWSaOFzzeA06x36tYRODEy_xk4Q"

try:
    client = genai.Client(api_key=MINHA_API_KEY)
except Exception as e:
    st.error(f"Erro na API: {e}")

# ======== INTERFACE VISUAL PERSONALIZADA ========
st.set_page_config(page_title="J.A.R.V.I.S. Mainframe", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #020914; color: #80E5FF; }
    .stButton>button { background-color: #0A2236 !important; color: #80E5FF !important; border: 2px solid #00A6FF !important; }
    .stTextInput>div>div>input { background-color: #051424 !important; color: #80E5FF !important; border: 1px solid #00A6FF !important; }
    h1 { color: #00BFFF !important; text-shadow: 0 0 15px #0066FF; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 J.A.R.V.I.S. — Sistema Online")
st.write("---")

# Personalidade única e fixa do Jarvis
PROMPT_SISTEMA = (
    "Você é o J.A.R.V.I.S., o assistente pessoal criado pelo Senhor. "
    "Você é altamente inteligente, prestativo e ligeiramente irônico. "
    "Responda sempre em português brasileiro de forma direta e chame o usuário de 'Senhor'."
)

# Memória do Chat
if "historico" not in st.session_state: st.session_state.historico = []
if "mensagens_api" not in st.session_state: st.session_state.mensagens_api = []

for msg in st.session_state.historico:
    with st.chat_message(msg["role"]): st.write(msg["content"])

# Função do Microfone
def ouvir_microfone():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as fonte:
        st.sidebar.info("🎙️ Jarvis ouvindo... Fale, Senhor.")
        reconhecedor.adjust_for_ambient_noise(fonte, duration=1)
        try:
            audio = reconhecedor.listen(fonte, timeout=5, phrase_time_limit=10)
            st.sidebar.success("🤖 Sinal limpo! Processando...")
            return reconhecedor.recognize_google(audio, language="pt-BR")
        except Exception:
            st.sidebar.error("⚠️ Sinal não compreendido.")
            return None

st.sidebar.title("🎙️ Controles de Voz")
if st.sidebar.button("🎙️ Falar com o Jarvis"):
    fala = ouvir_microfone()
    if fala: st.session_state["novo_comando"] = fala

# Execução dos Comandos
comando_final = st.chat_input("O que deseja pesquisar ou ordenar, Senhor?")
if "novo_comando" in st.session_state: comando_final = st.session_state.pop("novo_comando")

if comando_final:
    with st.chat_message("user"): st.write(comando_final)
    st.session_state.historico.append({"role": "user", "content": comando_final})
    st.session_state.mensagens_api.append(types.Content(role="user", parts=[types.Part.from_text(text=comando_final)]))

    with st.chat_message("assistant"):
        with st.spinner("Processando..."):
            try:
                # MODELO SEGURO E EM FUNCIONAMENTO TOTAL: gemini-3.6-flash
                resposta = client.models.generate_content(
                    model='gemini-3.6-flash', 
                    contents=st.session_state.mensagens_api,
                    config=types.GenerateContentConfig(system_instruction=PROMPT_SISTEMA)
                )
                st.write(resposta.text)
                st.session_state.historico.append({"role": "assistant", "content": resposta.text})
                st.session_state.mensagens_api.append(types.Content(role="model", parts=[types.Part.from_text(text=resposta.text)]))
            except Exception as e:
                st.error(f"Erro: {e}")
