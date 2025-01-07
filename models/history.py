import os
import csv

# Implementar a Função de Salvamento - salvar o histórico do jogo no arquivo CSV
def save_game_history(game_id, board, result):
    """
    Salva o histórico do jogo no arquivo CSV.
    """
    history_file = 'game_history.csv'
    header = ['game_id', 'board', 'result']

    # Converte o tabuleiro 2D para uma lista linear
    flat_board = [cell if cell else '' for row in board for cell in row]

    # Verifica se o arquivo já existe
    file_exists = os.path.isfile(history_file)

    # Abre o arquivo em modo de adição
    with open(history_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Escreve o cabeçalho apenas se o arquivo for novo
        if not file_exists:
            writer.writerow(header)
        
        # Escreve os dados do jogo
        writer.writerow([game_id, flat_board, result])
