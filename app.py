from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os

from models.game import create_new_board, check_winner, check_draw, is_valid_move
from models.history import save_game_history
from models.ai import encode_board, check_victory

# Carregar o modelo treinado
model_path = os.path.join(os.path.dirname(__file__), 'jogo_da_velha_model.pkl')
model = joblib.load(model_path)

# criar app flask
app = Flask(__name__)

# Estrutura para armazenar jogadores
players = {}
player_id_counter = 1

# Dicionário de Jogos
games = {}
game_id_counter = 1

# ROTAS DA API
# Rota para Registro de Jogadores
@app.route('/api/register', methods=['POST'])
def register_player():
    global player_id_counter
    
    data = request.get_json()
    if 'name' not in data:
        return jsonify({"error": "Nome é obrigatório"}), 400

    name = data['name']
    player_id = player_id_counter
    players[player_id] = {
        "name": name,
        "wins": 0,
        "losses": 0,
        "draws": 0
    }
    player_id_counter += 1
    return jsonify({"player_id": player_id}), 201

# Rota para iniciar novo jogo
@app.route('/api/start', methods=['POST'])
def start_game():
    global game_id_counter

    data = request.get_json()
    if 'player_id' not in data:
        return jsonify({"error": "O ID do jogador é obrigatório"}), 400

    player_id = data['player_id']
    if player_id not in players:
        return jsonify({"error": "Jogador inexistente"}), 404

    # Criar um novo jogo
    game_id = game_id_counter
    games[game_id] = {
        "board": create_new_board(),
        "player_id": player_id,
        "status": "ongoing"  # Indica que o jogo está em andamento
    }
    game_id_counter += 1

    return jsonify({
        "game_id": game_id,
        "board": games[game_id]["board"],
        "player_id": player_id
    }), 201

# Rota para realizar uma jogada
@app.route('/api/move', methods=['POST'])
def make_move():
    data = request.get_json()
    if 'game_id' not in data or 'row' not in data or 'col' not in data:
        return jsonify({"error": "ID do jogo, linha e coluna são obrigatórios"}), 400

    game_id = data['game_id']
    row = data['row']
    col = data['col']

    if game_id not in games:
        return jsonify({"error": "Jogo inexistente"}), 404

    game = games[game_id]
    if game["status"] != "ongoing":
        return jsonify({"error": "Esse jogo terminou"}), 400

    if not is_valid_move(game["board"], row, col):
        return jsonify({"error": "Movimento invalido"}), 400

    game["board"][row][col] = "X"

    if check_winner(game["board"]) == "X":
        game["status"] = "finished"
        players[game["player_id"]]["wins"] += 1
        save_game_history(game_id, game["board"], "Jogador vence!")
        return jsonify({"board": game["board"], "result": "Jogador vence!"}), 200

    if check_draw(game["board"]):
        game["status"] = "finished"
        players[game["player_id"]]["draws"] += 1
        save_game_history(game_id, game["board"], "Draw")
        return jsonify({"board": game["board"], "result": "Draw"}), 200

    # IA faz a jogada
    for i in range(3):
        for j in range(3):
            if game["board"][i][j] == "":
                game["board"][i][j] = "O"
                break
        else:
            continue
        break

    if check_winner(game["board"]) == "O":
        game["status"] = "finished"
        players[game["player_id"]]["losses"] += 1
        save_game_history(game_id, game["board"], "A IA vence!")
        return jsonify({"board": game["board"], "result": "A IA vence!"}), 200

    if check_draw(game["board"]):
        game["status"] = "finished"
        players[game["player_id"]]["draws"] += 1
        save_game_history(game_id, game["board"], "Draw")
        return jsonify({"board": game["board"], "result": "Draw"}), 200

    return jsonify({"board": game["board"], "result": "Jogo em andamento"}), 200

# Rota para solicitar uma sugestão de jogada
@app.route('/api/ai-move', methods=['GET'])
def get_ai_suggestion():
    game_id = request.args.get('game_id')

    # Verificar se o game_id é válido
    if not game_id or int(game_id) not in games:
        return jsonify({"error": "O ID do jogo é obrigatório ou inválido"}), 400

    game = games[int(game_id)]
    board = game['board']

    # Converter o tabuleiro para o formato numérico esperado pelo modelo
    encoding = {'X': 1, 'O': -1, '': 0}
    try:
        flat_board = [encoding[cell] for row in board for cell in row]
        flat_board = pd.DataFrame([flat_board])  # Converter para DataFrame
    except Exception as e:
        return jsonify({"error": f"Erro na codificação do tabuleiro: {str(e)}"}), 500

    # Prever a próxima jogada usando o modelo
    try:
        predicted_move = model.predict(flat_board)[0]
        row, col = divmod(int(predicted_move), 3)  # Converter para int para evitar erros de serialização
        return jsonify({"suggested_move": {"row": int(row), "col": int(col)}})  # Garantir tipos nativos
    except Exception as e:
        return jsonify({"error": f"Erro ao prever movimento: {str(e)}"}), 500

# Rota para retornar as estatísticas de jogo do jogador, incluindo o número de vitórias, derrotas e empates
@app.route('/api/player-stats/<int:player_id>', methods=['GET'])
def get_player_stats(player_id):
    """
    Retorna as estatísticas do jogador com base no player_id.
    """
    if player_id not in players:
        return jsonify({"error": "Jogador inexistente"}), 404

    player = players[player_id]
    stats = {
        "1-player_id": player_id,
        "2-nome": player["name"],
        "4-vitorias": player["wins"],
        "6-perdas": player["losses"],
        "5-empates": player["draws"],
        "3-total_jogos": player["wins"] + player["losses"] + player["draws"]
    }
    return jsonify(stats), 200

# Rota para retornar sugestões personalizadas de feedback
@app.route('/api/feedback/<int:player_id>', methods=['GET'])
def get_feedback(player_id):
    """
    Retorna feedback baseado no desempenho do jogador.
    """
    if player_id not in players:
        return jsonify({"error": "Jogador inexistente"}), 404

    player = players[player_id]
    wins = player["wins"]
    losses = player["losses"]
    draws = player["draws"]
    total_jogos = wins + losses + draws

    feedback = []

    # Cenário: Muitas derrotas
    if losses > wins and losses > draws:
        feedback.append("Concentre-se mais na defesa e tente antecipar as jogadas do adversário.")

    # Cenário: Muitos empates
    if draws > wins and draws > losses:
        feedback.append("Experimente ser mais agressivo no início para sair do empate.")

    # Cenário: Bom desempenho
    if wins > losses:
        feedback.append("Ótimo trabalho! Sua estratégia está funcionando bem. Continue assim.")

    # Cenário: Número baixo de jogos
    if total_jogos < 5:
        feedback.append("Jogue mais partidas para melhorar sua estratégia e ganhar experiência.")

    # Cenário: Nenhum cenário específico
    if not feedback:
        feedback.append("Continue jogando e ajustando sua estratégia para melhorar.")

    return jsonify({
        "player_id": player_id,
        "nome": player["name"],
        "feedback": feedback
    }), 200
