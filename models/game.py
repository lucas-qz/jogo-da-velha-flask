# Função para Criar um Novo Tabuleiro
def create_new_board():
    return [["" for _ in range(3)] for _ in range(3)] 

# Verificar Condições de Vitória
def check_winner(board):
    # Verificar linhas
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != "":
            return row[0]

    # Verificar colunas
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "":
            return board[0][col]

    # Verificar diagonais
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return board[0][2]

    return None

# Verificar Empate
def check_draw(board):
    for row in board:
        if "" in row:
            return False
    return True

# Verificar Jogadas Válidas
def is_valid_move(board, row, col):
    return 0 <= row < 3 and 0 <= col < 3 and board[row][col] == ""
