import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

file_path = 'C:/Users/bruna/Downloads/azul-ml.xlsx'

# COLOQUE AQUI OS LINKS PARA TREINAR A ML 

# LINHA AZUL -> C:/Users/bruna/Downloads/azul-ml.xlsx
# LINHA VERMELHA -> C:/Users/bruna/Downloads/vermelha-ml.xlsx
# LINHA PRATA -> C:/Users/bruna/Downloads/prata-ml.xlsx
# LINHA VERDE -> C:/Users/bruna/Downloads/verde-ml.xlsx

try:
  df = pd.read_excel(file_path)

  print(df.head())

except FileNotFoundError:
  print(f"Erro: Arquivo '{file_path}' não encontrado.")
except Exception as e:
  print(f"Ocorreu um erro ao importar o arquivo: {e}")

x=df['MES']
y=df['PESSOAS']
print(x)
print(y)

x = df['MES'].values.reshape(-1, 1) 
y = df['PESSOAS'].values

X_train_track, X_test_track, y_train_track, y_test_track = train_test_split(x, y, test_size=0.8, random_state=42)

modelo_track = LinearRegression()
modelo_track.fit(X_train_track, y_train_track)

y_pred_track = modelo_track.predict(X_test_track)
r2_score_track = modelo_track.score(X_test_track, y_test_track)
print(f"R² for TRACK SECURE model: {r2_score_track}")

plt.scatter(x, y, color='blue')
plt.plot(x, modelo_track.predict(x), color='red')
plt.title('Regressão Linear Simples - Track Secure')
plt.xlabel('Mês')
plt.ylabel('Pessoas na Linha')
plt.show()
