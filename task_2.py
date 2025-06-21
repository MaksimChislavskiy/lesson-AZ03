import numpy as np
import matplotlib.pyplot as plt

# Генерируем два набора случайных данных по 50 элементов каждый
x = np.random.rand(50)
y = np.random.rand(50)

# Построение диаграммы рассеяния
plt.scatter(x, y, alpha=0.7, edgecolors='b')
plt.title('Диаграмма рассеяния двух наборов случайных данных')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()