import matplotlib.pyplot as plt
import numpy as np

sampling_period = 5.067567567567568

# Pontos de entrada
points = [(0,-0.5),(20,0.0),(35,3.4),(40,3.4),(60,1.0),(100,-0.6)]
points_intersect = [(sampling_period, -0.375), (sampling_period*2, -0.248), (sampling_period*3, -0.118), (sampling_period*4, 0.061), (sampling_period*5, 1.211), (sampling_period*6, 2.36), (sampling_period*7, 3.4), 
                    (sampling_period*8, 3.33), (sampling_period*9, 2.7), (sampling_period*10, 2.11), (sampling_period*11, 1.5), (sampling_period*12, 0.967)
                    , (sampling_period*13, 0.76), (sampling_period*14, 0.56), (sampling_period*15, 0.35), (sampling_period*16, 0.15), (sampling_period*17, -0.04)
                    , (sampling_period*18, -0.25)
                    , (sampling_period*19, -0.45)]
# Separe as coordenadas x e y
x_values, y_values = zip(*points)
x_inersect, y_intersect = zip(*points_intersect)
# Calcule os valores discretos de x com um período de amostragem de 100

x_discrete = np.arange(0, 106, sampling_period)

# Interpole os valores de y correspondentes aos valores discretos de x
y_discrete = np.interp(x_discrete, x_values, y_values)

# Crie as retas em azul escuro
plt.plot(x_values, y_values, marker='o', linestyle='-', label='Alteração da espessura da célula')
plt.step(x_discrete, y_discrete, where='post', color='mediumseagreen', label='Espessura pós-amostragem')  # Use 'post' para etapas pós-interpolação

# Defina os rótulos dos eixos
plt.xlabel('Altura (%)')
plt.ylabel('Alteração da espessura da célula (mm)')

# Título do gráfico
#plt.title('Gráfico de Retas com Função de Etapas')

# Plote os pontos em vermelho
plt.scatter(x_values, y_values, color='red', zorder=5, label='Entrada do usuário')  # Definindo zorder para sobrepor os pontos à linha

plt.scatter(x_inersect, y_intersect, color='green', zorder=5, label='Amostras discretas')  # Definindo zorder para sobrepor os pontos à linha

# Define o limite mínimo do eixo x para 0
plt.xlim(0)


# Adicione um traçado de grade
plt.grid(True, linestyle='--', alpha=0.7)

# Adicione uma linha vertical escura em x=0
plt.axhline(y=0, color='black', linewidth=1)

# Legenda
plt.legend()

plt.show()
