# Personal Trainers de IA

<p> Este projeto foi desenvolvido por Daniel Assis, ele apresenta um sistema de Personal Trainers de IA inovador, utilizando a arquitetura de múltiplos agentes para oferecer uma experiência personalizada de treino e acompanhamento. O sistema é composto por três agentes especializados: Robertão.ia, Max.ia e Jailson.ia 2.0, que trabalham em conjunto para guiar o usuário em sua jornada de fitness.
</p>

## Estrutura do Projeto 

<p> O projeto foi construído em Python e utiliza as bibliotecas google.genai (para interação com modelos Gemini) e google-adk (para orquestração de agentes).
Agentes Envolvidos: </p>


    Robertão.ia (Recepcionista)
        Função: Receber o usuário de forma carismática e jovem, coletando seus objetivos de treino detalhados (ex: ficar forte, perder gordura, biotipo, peso, altura).
        Modelo: gemini-2.0-flash
        Ferramentas: Google Search (para buscar as melhores práticas de atendimento em academias).
        Linguagem: Jovem e acessível, focada em usuários de 16-24 anos.
    Max.ia (Professor)
        Função: Com base nos objetivos coletados pelo Robertão.ia, o Max.ia elabora um plano de treino e dicas de dieta personalizados.
        Modelo: gemini-2.0-flash
        Ferramentas: Google Search (para pesquisar métodos de treino e dietas específicas para cada objetivo).
        Saída: Plano de treino formatado com bullet points, incluindo exercícios, séries, repetições e sugestões de dieta com calorias.
    Jailson.ia 2.0 (Desafiador)
        Função: Criar desafios de levantamento de peso progressivos, compatíveis com o plano de treino do usuário, para diferentes marcos de tempo (1º mês, 2º mês, 6º mês, 1º ano, 2º ano).
        Modelo: gemini-2.0-flash
        Saída: Lista de desafios com exercícios, pesos e repetições esperadas para cada período.
        

Como Usar:

    !pip install -q google.genai
    !pip install -q google-adk
    

Configuração da API Key: O projeto requer uma chave de API do Google AI Studio. Armazene-a no Google Colab como uma variável de ambiente GOOGLE_API_KEY usando 
      
    userdata.get('GOOGLE_API_KEY').

    import os
    from google.colab import userdata

    os.environ["GOOGLE_API_KEY"] = userdata.get('GOOGLE_API_KEY')

Execução:

    Execute as células de instalação e importação.
    Execute as definições das funções dos agentes (agente_recepcionista, agente_professor, agente_desafiante).
    A última parte do código iniciará o fluxo do sistema, solicitando seus objetivos de treino. Quanto mais detalhes você fornecer, mais personalizado será o plano gerado.

<!-- end list -->

# ... (código dos agentes e imports) ...

    print("🚀 Iniciando o Sistema de Criação de treino e desafios 💪🏻🏋🏻")
    print(f"📆 {data_de_hoje.strftime('%d/%m/%Y')}\n⌚ {hora_de_agora.strftime('%H:%M')}")
    print("\n---------------------------------------\n")

    print("❓ Por favor, digite os seus objetivos de treino, sinta-se livre: ")
    print("❓Fale para o agente se deseja ficar forte, resistente, perder gordura, etc.")
    print("❓Fale para o agente características suas, como peso, altura e biotipo.")
    print("❗Quanto mais específico, melhor serão os resultados, manda bala ❗")

    objetivo = input("💪🏻 Objetivos: ")

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
      print("-----------------------------------------------------------------
