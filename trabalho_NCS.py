import turtle
import random
import numpy as np
import matplotlib.pyplot as plt

turtle.setup(1920,1080,50,0)


#Matriz adjacencia
A = np.array([[0,1,0,1,0,0],
              [0,0,1,0,0,0],
              [0,1,0,0,0,0],
              [1,0,0,0,0,0],
              [1,0,0,1,0,0],
              [0,0,1,0,0,0]])

#Tempo de simulação
t_sim = 10

#Passo de integração
h = 1

#time series
t = np.array([])
aux = 0
for i in range(int(t_sim/h)):
    aux = aux+h
    t = np.append(t, aux)


#número de iterações
n_steps = len(t)

#número de nós (robos)
n = 6

robos = {}

for i in range(n):
    robos[i] = turtle.Turtle()
    robos[i].shape("circle")
    robos[i].penup()
    robos[i].color(1,1,1)
    #robos[i].color((np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255)))


#dimesão dos estados (coordenadas x e y)
m = 2

#número de referências
N = 1

tamanho_janela = 800
#informação inicial dos estados
x0 = np.random.randint(-tamanho_janela,tamanho_janela,(n,m))

for i in range(n):
    robos[i].setpos(x0[i])
    robos[i].pendown()


#referência
r = np.array([0,10])

#matriz que representa quais robos sabem a referência
B = np.array([0,0,1,0,0,0])


#Algoritmo principal

x = np.zeros((n,m,n_steps))

x[:, :, 0] = x0


for k in range(n_steps-1):
    print("{}%".format(k/(n_steps-1)*100))
    for i in range(n):

        sum_i = 0

        for j in range(n):
            sum_i = sum_i + (x[j, :, k] - x[i, :, k])*A[i, j]

        for l in range(N):
            sum_i = sum_i + (r[:] - x[i, :, k])*B[i]

        robos[i].setpos(x[i,:,k+1])

    x[i, :, k + 1] = x[i, :, k] + h*sum_i
    
        
# plt.figure(1).suptitle("Robôs", fontsize=10)
# plt.plot(x[0,:,:])
# plt.show()

