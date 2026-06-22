import streamlit as st
import tempfile
import os
import google.generativeai as genai

# --- CONFIGURAÇÃO DA API ---
# A chave de API será lida das configurações secretas do Streamlit
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# --- INSTRUÇÃO RIGOROSA DE ZERO ALUCINAÇÃO ---
SYSTEM_INSTRUCTION = """
Atue como um Assistente Especializado em Degravação e Constatação Notarial. Sua tarefa é analisar o vídeo ou imagem em anexo e gerar EXCLUSIVAMENTE o bloco de texto da degravação, pronto para ser copiado e colado no Item 2 da Ata Notarial.

REGRA DE SEGURANÇA MÁXIMA (ZERO ALUCINAÇÃO):
- É EXPRESSAMENTE PROIBIDO usar sinônimos, alterar a ordem dos fatos, presumir palavras ou "corrigir" o sentido das frases.
- Atue como um transcritor literal, frio e mecânico. Se o áudio for confuso, use obrigatoriamente a tag "(inaudível)".
- O rigor da fé pública depende de você relatar exclusivamente o fato nu e cru.

REGRAS DE IDENTIFICAÇÃO:
1. Interlocutor 01: É SEMPRE o contato que enviou a PRIMEIRA mensagem no dia constatado.
2. Interlocutor 02: É a outra pessoa participante do diálogo.

DIRETRIZES DE DEGRAVAÇÃO (FORMATAÇÃO EXATA):
- Áudios reproduzidos: "[Texto literal]" Mensagem de áudio enviada pelo Interlocutor [XX] às [HH] horas e [MM] minutos.
- Textos lidos na tela: "[Texto literal]" Mensagem enviada pelo interlocutor [XX] às [HH] horas e [MM] minutos.
- Emojis: Substitua pelo texto "(emoji)".
- Imagens/Vídeos: "Imagem/Vídeo encaminhada(o) pelo interlocutor [XX] às [HH] horas e [MM] minutos."
- Horários: Formato obrigatório por extenso.

ESTRUTURA DE SAÍDA EXIGIDA:
Gere a resposta como um ÚNICO BLOCO DE TEXTO CONTÍNUO, sem parágrafos. Inicie com a data.
MODELO:
[DD/MM/AAAA]: "[CONTEÚDO]" Mensagem enviada pelo interlocutor [01] às [HH] horas e [MM] minutos. "[ÁUDIO]" Mensagem de áudio enviada pelo Interlocutor [02] às [HH] horas e [MM] minutos.
Entregue APENAS o bloco de texto contínuo.
"""

# Configuração do Modelo
generation_config = {
  "temperature": 0, # Focado na literalidade máxima
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash", # Modelo rápido e multimodal atualizado
  generation_config=generation_config,
  system_instruction=SYSTEM_INSTRUCTION
)

# --- INTERFACE DO APLICATIVO ---
st.set_page_config(page_title="Protestat.IA - Degravação", page_icon="⚖️", layout="centered")

st.title("⚖️ Protestat.IA")
st.subheader("Setor de Escritura - Degravação Literal")
st.write("Faça o upload da gravação de tela. O sistema extrairá a degravação literal para o Item 2 da Ata.")

st.markdown("---")

arquivo_upload = st.file_uploader(
    "Anexe o Vídeo (.mp4) ou Imagem (.jpg, .png) da gravação", 
    type=['mp4', 'mov', 'jpg', 'jpeg', 'png']
)

if arquivo_upload is not None:
    if not API_KEY:
        st.error("⚠️ Erro de Configuração: A Chave da API do Google não foi encontrada nas configurações (Secrets) do aplicativo.")
    elif st.button("Gerar Degravação Agora", type="primary", use_container_width=True):
        with st.spinner("Processando o arquivo e extraindo a degravação literal com rigor notarial..."):
            
            extensao = os.path.splitext(arquivo_upload.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=extensao) as tmp_file:
                tmp_file.write(arquivo_upload.read())
                caminho_temporario = tmp_file.name
            
            try:
                # Faz o upload do arquivo para a API do Gemini
                uploaded_file = genai.upload_file(caminho_temporario)
                
                # Inicia a transcrição
                response = model.generate_content(
                    ["Execute a constatação notarial com obediência estrita às regras de zero alucinação.", uploaded_file]
                )
                
                st.success("✅ Degravação concluída com sucesso! (Zero Alucinação)")
                st.write("**Copie o bloco abaixo para o Item 2 da Ata:**")
                st.code(response.text, language="text") 
                
                # Limpa o arquivo da nuvem do Google por segurança
                genai.delete_file(uploaded_file.name)
                
            except Exception as e:
                st.error(f"Ocorreu um erro técnico: {e}")
            
            finally:
                if os.path.exists(caminho_temporario):
                    os.remove(caminho_temporario)
