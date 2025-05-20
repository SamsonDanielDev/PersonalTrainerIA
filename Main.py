# No Google Colab, execute em uma célula apenas!👍🏻

# instalações para o nosso projetinho!
!pip install -q google.genai
!pip install -q google-adk

# importações para montar os nossos agentes
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types  # Para criar conteúdos (Content e Part)
from datetime import date
from datetime import datetime
import pytz
import textwrap # Para formatar melhor a saída de texto
from IPython.display import display, Markdown # Para exibir texto formatado no Colab
import requests # Para fazer requisições HTTP
import warnings

warnings.filterwarnings("ignore")

# configurando a nossa API no Google AI Studio
import os
from google.colab import userdata

os.environ["GOOGLE_API_KEY"] = userdata.get('GOOGLE_API_KEY')

# importando o nosso Software Development Kit
from google import genai

client = genai.Client()

modelinho = "gemini-2.0-flash"

from IPython.display import HTML, Markdown

# Função auxiliar que envia uma mensagem para um agente via Runner e retorna a resposta final
def call_agent(agent: Agent, message_text: str) -> str:
    # Cria um serviço de sessão em memória
    session_service = InMemorySessionService()
    # Cria uma nova sessão (você pode personalizar os IDs conforme necessário)
    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    # Cria um Runner para o agente
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    # Cria o conteúdo da mensagem de entrada
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    # Itera assincronamente pelos eventos retornados durante a execução do agente
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        if event.is_final_response():
          for part in event.content.parts:
            if part.text is not None:
              final_response += part.text
              final_response += "\n"
    return final_response

##########################################
# --- Agente 1: Robertão.ia --- #
##########################################
def agente_recepcionista (entrada_usuario):
  recepcionista = Agent(
      name="agente_recepcionista",
      model="gemini-2.0-flash",
      description="Agente feito para receber o usuário na aplicação e instruí-lo aos próximos passos.",
      tools=[google_search],
      instruction="""Você é um assistente feito para receber o usuário na aplicação, você se chama Roberto, mais conhecido como Robertão.
      Você deve usar uma linguagem mais jovem para atender os usuários considerando especialmente a idade de 16-24 anos.
      Você é recepcionista, logo não seja nem um pouco áspero, seja carismático.
      Considerando seus objetivos, pesquisa usando o google search, as melhores formas de atender um frequentador de academia e aplique.
      Você vai dialogar com o usuário logo após ele inserir a entrada com seus objetivos de forma detalhada, você vai avaliar e passar para o Max, seu colega professor.
      Se apresente!
        """
  )

  recepcionista_input = f"Objetivo e dados iniciais: {entrada_usuario}"
  # Executa o agente
  inicio_atendimento = call_agent(recepcionista, recepcionista_input)
  return inicio_atendimento

################################################
# --- Agente 2: Max.ia --- #
################################################
def agente_professor(inicio_atendimento):
    professor = Agent(
        name="agente_professor",
        model="gemini-2.0-flash",
        description="Agente que mostra para o usuário como atingir seus objetivos",
        tools=[google_search],
        # Inserir as instruções do Agente Max #################################################
        instruction="""
         Você vai receber os objetivos do usuário através do seu colega Robertão, você se chama Max.
         Considerando a entrada e os atributos que seu colega vai te passar, você deve montar um plano de treino, e dicas de dieta para o usuário bater suas metas.
         Use o google search para saber como ajudar o cliente a bater suas metas, exemplo, se ele quer ficar forte, recomende séries bem pesadas com poucas reps, se ele quer emagrecer, recomende déficit calórico.
         Vá montando o plano com bullet lists no formato:

         ** Dia da semana **
         - Treino
          - Exercício: séries e repetições
         - Dieta
          - Refeição: calorias

         Se apresente!
        """,
    )

    professor_input = f"Inicio do atendimento para montar o treino: {inicio_atendimento}"
    # Executa o agente
    objetivos_e_treino = call_agent(professor, professor_input)
    return objetivos_e_treino


##########################################
# --- Agente 3: Jailson.ia 2.0 --- #
##########################################
def agente_desafiante(objetivos_e_treino):
    desafiante = Agent(
        name="agente_desafiante",
        model="gemini-2.0-flash",
        instruction="""
            Você é um agente de IA que vai desafiar o usuário a fazer levantamentos de peso que beirem os seus limites em diferentes faixas de tempo:
            Crie 2-5 exercícios desafios para: primeiro mês, segundo mês, sexto mês, primeiro ano e segundo ano de treino.
            Formato: 

            - desafio para primeiro mês
              - exercício 1: peso e reps esperadas
              - exercício 2: peso e reps esperadas
              - exercício 3: peso e reps esperadas
              - exercício 4: peso e reps esperadas
              - exercício 5: peso e reps esperadas

            - desafio para segundo mês
              - exercício 1: peso e reps esperadas
              - exercício 2: peso e reps esperadas
              ...

            Você vai montar esses desafios com base nos dados retornados de treino, faça desafios compatíveis com o treino do usuário.
            Seu nome é Jailson, chame-se de Jailsão 2.0
            
            Se apresente!
            """,
        description="Agente desafiante de treinos",
    )
    desafiante_input = f"Treino para se basear: {objetivos_e_treino}"
    # Executa o agente
    desafio = call_agent(desafiante, desafiante_input)
    return desafio


data_de_hoje = date.today()
fuso_br = pytz.timezone('America/Sao_Paulo')
hora_de_agora = datetime.now(fuso_br)

print("🚀 Iniciando o Sistema de Criação de treino e desafios 💪🏻🏋🏻")
print(f"📆 {data_de_hoje.strftime('%d/%m/%Y')}\n⌚ {hora_de_agora.strftime('%H:%M')}")
print("\n---------------------------------------\n")

# --- Obter o objetivo do usuário ---

print("❓Por favor, digite os seus objetivos de treino, sinta-se livre: ")
print("❓Fale para o agente se deseja ficar forte, resistente, perder gordura, etc.")
print("❓Fale para o agente características suas, como peso, altura e biotipo.")
print("❗Quanto mais específico, melhor serão os resultados, manda bala ❗")


objetivo = input("💪🏻 Objetivos: ")

# Inserir lógica do sistema de agentes ################################################
if not objetivo:
  print("Você não inseriu um objetivo, por gentileza, insira-o")
else :
  print(f"Perfeito, iniciando um atendimento baseado na sua entrada, aguarde...")
  entrada_inicial = agente_recepcionista(entrada_usuario=objetivo)
  print(f"\n---Resposta-do-Robertão---\n")
  display(Markdown(entrada_inicial))
  print("-----------------------------------------------------------------------")

  dados_processados = agente_professor(entrada_inicial)
  print(f"\n---Resposta-do-Max---\n")
  display(Markdown(dados_processados))
  print("-----------------------------------------------------------------------")

  desafio = agente_desafiante(dados_processados)
  print(f"\n---Resposta-do-Jailsão-2.0---\n")
  display(Markdown(desafio))
  print("-----------------------------------------------------------------------")
