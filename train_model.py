# Treinar um Modelo de Machine Learning
# --> Execute o script para treinar e salvar o modelo no arquivo jogo_da_velha_model.pkl
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

# Obter o diretório onde o script está localizado
base_dir = os.path.dirname(os.path.abspath(__file__))

# Caminho absoluto para o dataset
dataset_path = os.path.join(base_dir, 'jogo_da_velha_dataset.csv')


# Função para codificar o tabuleiro
def encode_board(board):
    encoding = {'X': 1, 'O': -1, '': 0}
    return [encoding[cell] for cell in board]

# Carregar o dataset
df = pd.read_csv(dataset_path)

# Processar os dados
X = pd.DataFrame(df['board'].apply(eval).apply(encode_board).tolist())  # Convertendo o tabuleiro
y = df['best_move']

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar o modelo
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Avaliar o modelo
y_pred = model.predict(X_test)
print("Acurácia do modelo:", accuracy_score(y_test, y_pred))

# Salvar o modelo treinado
# Caminho absoluto para salvar o modelo
model_path = os.path.join(base_dir, 'jogo_da_velha_model.pkl')
# Salvar o modelo treinado
joblib.dump(model, model_path)

print(f"Modelo salvo com sucesso em: {model_path}")
