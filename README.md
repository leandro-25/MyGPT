# MyGPT

**Chatbot de Suporte com Feedback**

Este projeto consiste em um chatbot de suporte desenvolvido em Python, utilizando a biblioteca Spacy para processamento de linguagem natural e a FuzzyWuzzy para correspondência de texto. O chatbot é capaz de responder a perguntas do usuário, analisar intenções e extrair entidades nomeadas.

### Funcionalidades Principais:

1. **Pré-processamento de Texto:**
   - O texto de entrada é pré-processado, convertido para minúsculas e lematizado para melhorar a correspondência.

2. **Feedback do Usuário:**
   - Os usuários têm a opção de fornecer feedback sobre a utilidade das respostas do chatbot.

3. **Correspondência de Perguntas:**
   - O chatbot usa um índice de pesquisa invertida para encontrar correspondências relevantes com base nas instruções pré-processadas.

4. **Opções de Resposta Múltipla:**
   - Quando há várias correspondências, o chatbot apresenta opções ao usuário, permitindo a escolha da resposta desejada.

5. **Melhoria Contínua com Feedback:**
   - O chatbot registra o feedback do usuário para ajustar e melhorar seu desempenho ao longo do tempo.

### Uso do Chatbot:

1. **Iniciar o Chatbot:**
   - Execute o script Python e inicie uma conversa digitando suas perguntas.

2. **Feedback do Usuário:**
   - Após receber uma resposta, o usuário pode fornecer feedback indicando se a resposta foi útil ou não.


### Estrutura do Projeto:

- **`MyCHAT.py`:** Contém o código-fonte do chatbot.
- **`cabrita-dataset-52k.json`:** Dataset de perguntas e respostas usado para treinamento e correspondência.
- **`processed_data_cache.pkl`:** Cache dos dados pré-processados para acelerar o carregamento.
- **`user_feedback.txt`:** Arquivo para armazenar o feedback do usuário.

### Dependências:

- `spacy`
- `fuzzywuzzy`
- `joblib`

### Melhorias e ideias:

1. criar uum menu para acessar determinados diretorios para maior desempenho 
2. gerer um pré-processmento apra cada diretorio
3. melhorar a forma que é gerado os dados pré-processados
4. encontrr uma forma de gerar sua propria base de dados com base nos arquivos
5. ler todos tipos de arquivos para gerar sua base de dados sem tratamento humano 

