# função para transformar o tabuleiro antes de enviar ao modelo
def encode_board(board):
    encoding = {'X': 1, 'O': -1, '': 0}
    return [encoding[cell] for row in board for cell in row]

# função check_victory
def check_victory(board, player):
    """
    Verifica se o jogador venceu o jogo.
    :param board: Tabuleiro do jogo como uma matriz 3x3.
    :param player: Jogador ('X' ou 'O').
    :return: True se o jogador venceu, False caso contrário.
    """
    # Verificar linhas
    for row in board:
        if all(cell == player for cell in row):
            return True

    # Verificar colunas
    for col in range(3):
        if all(row[col] == player for row in board):
            return True

    # Verificar diagonais
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False
