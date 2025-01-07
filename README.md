# #️⃣ Jogo da Velha com Flask e IA
Este projeto implementa um Jogo da Velha utilizando Flask para o backend e Machine Learning (IA) para melhorar o desempenho do jogo. A IA é treinada com um conjunto de dados histórico de jogadas anteriores para fazer escolhas inteligentes durante o jogo.
<br/><br/>


## 🚦 Pré-requisitos:
Antes de rodar o projeto, é necessário ter as seguintes ferramentas instaladas:
- Python 3.x
- pip (gerenciador de pacotes do Python)
<br/><br/>


## 🔧 Instalação
Siga os passos abaixo para configurar o ambiente e executar o projeto:

1. Clone este repositório em seu computador:
```bash
git clone https://github.com/lucas-qz/jogo-da-velha-flask.git
cd jogo-da-velha-flask
```
2. Crie um ambiente virtual para isolar as dependências do projeto:
```bash
python -m venv venv
```
<br/><br/>


3. Ative o ambiente virtual:
- No Windows:
```bash
venv\Scripts\activate
```
- No macOS/Linux:
```bash
source venv/bin/activate
```
<br/><br/>


4. Instale as dependências do projeto:
```bash
pip install -r requirements.txt
```
<br/><br/>


## ⚓ Estrutura do Projeto
- app.py: Arquivo principal que executa o servidor Flask.
- generate_dataset.py: Arquivo para criar um Dataset de histórico de jogadas.
- train_model.py: Arquivo para treinar o modelo de Machine Learning
- game_history.csv: Histórico com os resultados dos jogos para melhorias futuras no modelo.
- jogo_da_velha_model.pkl: Modelo treinado de IA para o Jogo da Velha.
- jogo_da_velha_dataset.csv: Conjunto de dados histórico (dataset) utilizado para treinar a IA.
- requirements.txt: Arquivo com as dependências do projeto.
<br/><br/>


## 💻 Executando o Servidor Flask
Para iniciar o servidor Flask, execute o seguinte comando:
```bash
flask run
```
O servidor estará disponível em http://127.0.0.1:5000
<br/><br/>


## ☑️ Interagindo com a API
## 1. Registrar Jogador
Para registrar um novo jogador, envie uma requisição POST para o endpoint /api/register com o nome do jogador. Exemplo:
Request:
```bash
POST http://127.0.0.1:5000/api/register
Content-Type: application/json

{
  "name": "Jogador 1"
}
```

Response:
```json
{
  "player_id": 1
}
```
<br/><br/>


## 2. Iniciar Jogo
Para iniciar um novo jogo, envie uma requisição POST para o endpoint /api/start com o ID do jogador. Exemplo:

Request:
```bash
POST http://127.0.0.1:5000/api/start
Content-Type: application/json

{
  "player_id": 1
}
```
Response:
```json
{
  "board": [["", "", ""], ["", "", ""], ["", "", ""]],
  "game_id": 1,
  "player_id": 1
}
```
<br/><br/>


## 3. Realizar Jogada
Para realizar uma jogada, envie uma requisição POST para o endpoint /api/move com o ID do jogo, a linha (row) e a coluna (col) da jogada. Exemplo:

Request:
```bash
POST http://127.0.0.1:5000/api/move
Content-Type: application/json

{
  "game_id": 1,
  "row": 2,
  "col": 1
}
```
Response:
```json
{
  "board": [["O", "", ""], ["", "", ""], ["", "X", ""]],
  "result": "Game ongoing"
}
```
<br/><br/>


## 4. Sugestão de Jogada pela IA
Para obter a sugestão de jogada da IA, envie uma requisição GET para o endpoint /api/ai-move com o ID do jogo. Exemplo:

Request:
```bash
GET http://127.0.0.1:5000/api/ai-move?game_id=1
```
Response:
```json
{
  "suggested_move": {
    "row": 1,
    "col": 2
  }
}
```
<br/><br/>


## 5. Estatísticas do Jogador
Para obter as estatísticas de um jogador, envie uma requisição GET para o endpoint /api/player-stats/{player_id}. Exemplo:

Request:
```bash
GET http://127.0.0.1:5000/api/player-stats/1
```
Response:
```json
{
  "draws": 0,
  "losses": 0,
  "name": "Jogador 1",
  "player_id": 1,
  "total_games": 1,
  "wins": 1
}
```
<br/><br/>


## 6. Feedback do Jogador
Para obter feedback sobre o desempenho de um jogador, envie uma requisição GET para o endpoint /api/feedback/{player_id}. Exemplo:
Request:
```bash
GET http://127.0.0.1:5000/api/feedback/1
```
Response:
```json
{
  "feedback": [
    "Ótimo trabalho! Sua estratégia está funcionando bem. Continue assim.",
    "Jogue mais partidas para melhorar sua estratégia e ganhar experiência."
  ],
  "name": "Jogador 1",
  "player_id": 1
}
```
<br/><br/>


## 🏋🏻‍♂️ Treinando o Modelo de IA
A IA utiliza um modelo de Machine Learning treinado com um conjunto de dados histórico de jogadas de Jogo da Velha. Para treinar o modelo, siga os passos abaixo:
1. Certifique-se de que o arquivo `jogo_da_velha_dataset.csv` está presente no projeto. Este arquivo contém as jogadas anteriores que serão usadas para treinar o modelo.
2. Execute o script de treinamento para gerar o modelo `jogo_da_velha_model.pkl`:
```bash
python train_model.py
```
3. O modelo será salvo em `jogo_da_velha_model.pkl` e estará pronto para ser carregado na aplicação Flask para tomar decisões durante o jogo.
<br/><br/>


## 👨🏻‍🏫 Como o Conjunto de Dados Histórico Melhora o Desempenho da IA
O conjunto de dados histórico contém informações sobre jogadas anteriores, que permitem que o modelo aprenda a identificar padrões e estratégias vencedoras. Quanto mais dados históricos a IA tiver, melhor ela será em prever a próxima jogada e aumentar suas chances de ganhar. O processo de treinamento usa esses dados para "ensinar" o modelo como reagir em diferentes situações, aprimorando sua habilidade ao longo do tempo.
<br/><br/>


## 🎓 Conclusão
Agora, você pode executar o servidor Flask, registrar jogadores, iniciar jogos, realizar jogadas e até treinar a IA com o histórico de dados. O modelo de IA aprende com os dados históricos e pode melhorar o desempenho do jogo, proporcionando uma experiência mais desafiadora.
<br/><br/>


## 👨🏼 Autor - Lucas Queiróz
<div align="left"> 
<a  href="https://github.com/lucas-qz" target="_blank"><img align="left" alt="GitHub" height="30" width="30" src="https://cdn.worldvectorlogo.com/logos/github-icon-2.svg"> GitHub - Lucas Queiróz </a><br/><br/>
<a  href="https://www.linkedin.com/in/lucas-qz/" target="_blank"><img align="left" alt="Linkedin" height="30" width="30" src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png"> Linkedin - Lucas Queiróz </a><br/><br/>
<a  href="http://lucasqz.com.br" target="_blank"><img align="left" alt="Portfólio" height="30" width="30" src="https://cdn-icons-png.flaticon.com/512/5602/5602732.png"> Portfólio - Lucas Queiróz </a><br/><br/>
</div>
<br/><br/>









