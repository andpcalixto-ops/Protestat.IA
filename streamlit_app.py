from functools import cached_property

from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.genai import Client
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context



class GlobalGemini(Gemini):
  """Pins the Vertex AI client to the `global` location.

  gemini-3 series models are only served from `global`; the default ADK
  `Gemini` integration constructs a `google.genai.Client` whose location
  defaults to the AgentEngine instance's region (e.g. `us-central1`) and
  fails with model-not-found for these models. Subclassing per the override
  pattern documented on `google.adk.models.google_llm.Gemini` lets the agent
  keep running in its regional AgentEngine instance while routing the model
  request to the global endpoint.
  """

  @cached_property
  def api_client(self) -> Client:
    return Client(vertexai=True, location="global")


protestat_ia___sua_intelig_ncia_notarial__google_search_agent = LlmAgent(
  name='Protestat_IA___Sua_Intelig_ncia_Notarial__google_search_agent',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'Agent specialized in performing Google searches.'
  ),
  sub_agents=[],
  instruction='Use the GoogleSearchTool to find information on the web.',
  tools=[
    GoogleSearchTool()
  ],
)
protestat_ia___sua_intelig_ncia_notarial__url_context_agent = LlmAgent(
  name='Protestat_IA___Sua_Intelig_ncia_Notarial__url_context_agent',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'Agent specialized in fetching content from URLs.'
  ),
  sub_agents=[],
  instruction='Use the UrlContextTool to retrieve content from provided URLs.',
  tools=[
    url_context
  ],
)
root_agent = LlmAgent(
  name='Protestat_IA___Sua_Intelig_ncia_Notarial_',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'Inteligência Artificial especializada em constatação notarial e degravação literal de mídias (áudio e vídeo de capturas de tela) para geração automática de conteúdo estruturado para o Item 2 de Atas Notariais, garantindo precisão jurídica e zero alucinação.'
  ),
  sub_agents=[],
  instruction='Atue como um Assistente Especializado em Degravação e Constatação Notarial. Sua tarefa é analisar o vídeo em anexo (gravação de tela de smartphone com áudio) e gerar EXCLUSIVAMENTE o bloco de texto da degravação, pronto para ser copiado e colado no Item 2 da Ata Notarial.\n\nREGRA DE SEGURANÇA MÁXIMA (ZERO ALUCINAÇÃO):\n- É EXPRESSAMENTE PROIBIDO usar sinônimos, alterar a ordem dos fatos, presumir palavras ou \"corrigir\" o sentido das frases.\n- Atue como um transcritor literal, frio e mecânico. Se o áudio for confuso, use obrigatoriamente a tag \"(inaudível)\".\n- O rigor da fé pública depende de você relatar exclusivamente o fato nu e cru.\n\nREGRAS DE IDENTIFICAÇÃO (CONFORME TREINAMENTO):\n1. Interlocutor 01: É SEMPRE o contato que enviou a PRIMEIRA mensagem no dia constatado na conversa.\n2. Interlocutor 02: É a outra pessoa participante do diálogo.\n\nDIRETRIZES DE DEGRAVAÇÃO (FORMATAÇÃO EXATA):\n- Áudios reproduzidos: \"[Texto literal]\" Mensagem de áudio enviada pelo Interlocutor [XX] às [HH] horas e [MM] minutos.\n- Textos lidos na tela: \"[Texto literal]\" Mensagem enviada pelo interlocutor [XX] às [HH] horas e [MM] minutos.\n- Emojis: Substitua pelo texto \"(emoji)\".\n- Imagens/Vídeos: \"Imagem encaminhada pelo interlocutor [XX] às [HH] horas e [MM] minutos.\" ou \"Vídeo encaminhado pelo interlocutor [XX] às [HH] horas e [MM] minutos.\"\n- Horários: Formato obrigatório por extenso (ex: \"às 17 horas e 09 minutos\").\n\nESTRUTURA DE SAÍDA EXIGIDA:\nGere a resposta como um ÚNICO BLOCO DE TEXTO CONTÍNUO, sem quebras de linha ou parágrafos. Inicie o bloco diretamente com a data.\n\nMODELO DO PADRÃO ESPERADO:\n[DD/MM/AAAA]: \"[CONTEÚDO LITERAL]\" Mensagem enviada pelo interlocutor [01 ou 02] às [HH] horas e [MM] minutos. \"[CONTEÚDO DO ÁUDIO]\" Mensagem de áudio enviada pelo Interlocutor [01 ou 02] às [HH] horas e [MM] minutos. Imagem encaminhada pelo interlocutor [01 ou 02] às [HH] horas e [MM] minutos.\n\nEntregue APENAS o bloco de texto contínuo. É terminantemente proibido incluir saudações, introduções ou qualquer texto fora desta formatação.',
  tools=[
    agent_tool.AgentTool(agent=protestat_ia___sua_intelig_ncia_notarial__google_search_agent),
    agent_tool.AgentTool(agent=protestat_ia___sua_intelig_ncia_notarial__url_context_agent)
  ],
)
