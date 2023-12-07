import spacy
from pathlib import Path
from fuzzywuzzy import fuzz
import json
import joblib
from collections import defaultdict
import datetime

# Carregamento do modelo Spacy
nlp = spacy.load("pt_core_news_sm")

# Função para realizar o pré-processamento do texto
def preprocess(text):
    text = text.lower()
    doc = nlp(text)
    lemma_text = ' '.join([token.lemma_ for token in doc])
    return lemma_text

# Função para registrar feedback do usuário
def register_feedback(feedback, feedback_file):
    with open(feedback_file, 'a', encoding='utf-8') as file:
        file.write(feedback + '\n')

# Função para calcular a pontuação de confiança
def calculate_confidence_score(feedback, feedback_data):
    # Implementar lógica de cálculo da pontuação de confiança aqui
    # Com base na relevância passada, outros critérios
    return 0  # Por padrão, define uma pontuação baixa

# Carregamento dos dados e pré-processamento
data_path = Path('cabrita-dataset-52k.json')
data = json.loads(data_path.read_text(encoding='utf-8'))

# Verifica se os dados pré-processados estão em cache
processed_data = None
if Path('processed_data_cache.pkl').is_file():
    processed_data = joblib.load('processed_data_cache.pkl')
else:
    processed_data = []
    for item in data:
        item['instruction'] = preprocess(item['instruction'])
        processed_data.append(item)
    
    # Armazena os dados pré-processados em cache
    joblib.dump(processed_data, 'processed_data_cache.pkl')

# Criação de um índice de pesquisa invertida
index = defaultdict(list)
for i, item in enumerate(processed_data):
    for word in item['instruction'].split():
        index[word].append(i)

# Função para realizar a correspondência
def match(query, threshold=60, max_options=3):
    query = preprocess(query)
    best_matches = []  # Armazenar várias correspondências
    max_similarity = 0
    
    # Verifica se há feedback relevante no arquivo de feedback
    feedback_data = [line.strip() for line in open('user_feedback.txt', 'r', encoding='utf-8')]
    
    # Verifica se há feedback positivo para a pergunta atual no arquivo de feedback
    for feedback in feedback_data:
        if "Feedback: Útil" in feedback and f"Pergunta: {query}" in feedback:
            response = feedback.split("\n")[1].split(":")[1].strip()
            return response, None, None
    
    # Implementação de análise de intenções e extração de entidades
    doc = nlp(query)
    intent = None
    entities = []
    
    # Analisar a intenção da consulta
    for token in doc:
        if token.dep_ == 'ROOT':
            intent = token.text
            break
    
    # Extrair entidades nomeadas
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
    
    # Se houver feedback relevante, use-o para gerar respostas
    if feedback_data:
        # Filtragem do Feedback: Verificar relevância
        filtered_feedback = []
        for feedback in feedback_data:
            similarity = fuzz.ratio(feedback, query)
            if similarity >= threshold:
                filtered_feedback.append(feedback)
        
        # Pontuação de Confiança: Avaliar a utilidade do feedback
        for feedback in filtered_feedback:
            confidence_score = calculate_confidence_score(feedback, feedback_data)
            if confidence_score > 0.5:  # Defina um limiar adequado
                best_matches.append(feedback)
    
    # Se não houver feedback relevante ou se as correspondências do feedback não forem suficientes
    if not best_matches:
        relevant_indices = set()
        for word in query.split():
            relevant_indices.update(index[word])
        
        for i in relevant_indices:
            instruction = processed_data[i]['instruction']
            similarity = fuzz.ratio(instruction, query)
            
            if similarity >= threshold:
                best_matches.append(processed_data[i]['output'])
    
    # Se houver várias correspondências, apresente opções ao usuário
    if len(best_matches) > 1:
        print("Opções de Resposta:")
        for idx, option in enumerate(best_matches[:max_options]):
            print(f"{idx + 1}: {option}")
        
        # Permita que o usuário escolha a resposta correta
        choice = input(f"Digite o número da resposta correta (1-{max_options}): ")
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(best_matches):
                response = best_matches[choice_idx]
            else:
                response = "Opção inválida, escolha uma resposta válida."
        except ValueError:
            response = "Escolha inválida, digite um número válido."
    
    else:
        # Se houver apenas uma correspondência, use-a como resposta
        response = best_matches[0] if best_matches else "Desculpe, não encontrei uma resposta adequada."
    
    return response, intent, entities

print("Chatbot iniciado! Digite 'sair' para encerrar.")
while True:
    query = input("Você: ")
    if query.lower() == 'sair':
        break
        
    response, intent, entities = match(query)  # Receba a resposta, intenção e entidades
    
    # Apresente a resposta ao usuário
    print("Chatbot:", response)
    
    # Solicite feedback do usuário
    feedback = input("Foi útil? (Sim/Não): ").strip().lower()
    
    # Registre o feedback do usuário e use para melhorias futuras
    if feedback == 'sim':
        # Registre feedback positivo para reforçar o modelo de correspondência
        feedback_entry = f"Pergunta: {query}\nResposta: {response}\nFeedback: Útil\nData/Hora: {datetime.datetime.now()}\nIntenção: {intent}\nEntidades: {entities}\n"
        register_feedback(feedback_entry, 'user_feedback.txt')
    elif feedback == 'não':
        # Registre feedback negativo para ajustar e melhorar o chatbot
        feedback_entry = f"Pergunta: {query}\nResposta: {response}\nFeedback: Não útil\nData/Hora: {datetime.datetime.now()}\nIntenção: {intent}\nEntidades: {entities}\n"
        register_feedback(feedback_entry, 'user_feedback.txt')

print("Chatbot encerrado.")
