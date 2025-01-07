# Criar um Dataset de Histórico de Jogadas
# Execute esse script para gerar o arquivo jogo_da_velha_dataset.csv.
import random
import pandas as pd
import os

# Função para gerar um tabuleiro aleatório
def generate_random_board():
    board = ['' for _ in range(9)]
    moves = random.randint(1, 8)  # Número de jogadas no tabuleiro
    for _ in range(moves):
        idx = random.choice([i for i, v in enumerate(board) if v == ''])
        board[idx] = random.choice(['X', 'O'])
    return board

# Função para gerar jogadas mais inteligentes no dataset.
def strategic_move(board, player='X'):
    # Tenta bloquear o oponente
    opponent = 'O' if player == 'X' else 'X'
    for i in range(9):
        if board[i] == '':
            board_copy = board[:]
            board_copy[i] = opponent
            if check_win(board_copy, opponent):
                return i
    
    # Prioriza o centro
    if board[4] == '':
        return 4
    
    # Prefere cantos
    corners = [0, 2, 6, 8]
    available_corners = [i for i in corners if board[i] == '']
    if available_corners:
        return random.choice(available_corners)
    
    # Caso contrário, retorna qualquer jogada válida
    return random.choice([i for i, v in enumerate(board) if v == ''])

# Função para verificar se o jogador venceu
def check_win(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
        [0, 4, 8], [2, 4, 6]              # Diagonal
    ]
    for condition in win_conditions:
        if all(board[pos] == player for pos in condition):
            return True
    return False

# Função para adicionar diversidade
def generate_diverse_dataset(num_samples=1000):
    data = []
    for _ in range(num_samples):
        board = generate_random_board()
        valid_moves = [i for i, v in enumerate(board) if v == '']
        
        # Para cada jogada válida, adiciona um exemplo ao dataset
        for move in valid_moves:
            board_copy = board[:]
            board_copy[move] = 'X'
            data.append({'board': board, 'best_move': move})
    
    return data

# Gerar e salvar o dataset diversificado
# Garantir que o arquivo seja gerado no mesmo diretório que o script
base_dir = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório onde o script está localizado
# Gerar e salvar o dataset diversificado
data = generate_diverse_dataset(1000)  # Gerar 1000 exemplos iniciais
df = pd.DataFrame(data)
# Caminho absoluto para salvar o arquivo CSV no mesmo diretório do script
csv_path = os.path.join(base_dir, 'jogo_da_velha_dataset.csv')
# Salvar o dataset no caminho especificado
df.to_csv(csv_path, index=False)
print(f"Dataset diversificado gerado com sucesso em: {csv_path}")
