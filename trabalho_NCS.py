import turtle
import random
import numpy as np
import matplotlib.pyplot as plt
import random
import time

turtle.register_shape("x3.gif")

tamanho_janela = 800
turtle.setup(tamanho_janela+100,tamanho_janela+100,0,0)

screen = turtle.Screen()
screen.colormode(255)

#Matriz adjacencia
A = np.array([[0,1,0,1,0,0],
              [0,0,1,0,0,0],
              [0,1,0,0,0,0],
              [1,0,0,0,0,0],
              [1,0,0,1,0,0],
              [0,0,1,0,0,0]])

#Tempo de simulação
t_sim = 200

#Passo de integração
h = 0.5

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
    robos[i].color( random.randint(0, 255), 
                    random.randint(0, 255), 
                    random.randint(0, 255))
    size = robos[i].turtlesize()
    increase = tuple([0.8* num for num in size])
    robos[i].turtlesize(*increase)

#dimesão dos estados (coordenadas x e y)
m = 2

#número de referências
N = 1

#informação inicial dos estados
x0 = np.random.randint(-200,200,(n,m))

for i in range(n):
    robos[i].setpos(x0[i])
    robos[i].pendown()


#referência
r = np.random.randint(-200,200,(1,2))
referencia = turtle.Turtle()
referencia.shape("x3.gif")
referencia.penup()
referencia.setpos(r[0])

#matriz que representa quais robos sabem a referência
B = np.array([0,0,1,0,0,0])

#Algoritmo principal
x = np.zeros((n,m,n_steps))

x[:, :, 0] = x0


for k in range(n_steps-1):
    #print("{}%".format(k/(n_steps-1)*100))
    for i in range(n):

        sum_i = 0

        for j in range(n):
            sum_i = sum_i + (x[j, :, k] - x[i, :, k])*A[i, j]

        for l in range(N):
            sum_i = sum_i + (r[l,:] - x[i, :, k])*B[i]

        x[i, :, k + 1] = x[i, :, k] + h*sum_i
        robos[i].setpos(x[i,:,k+1])
        time.sleep(0.1)

    
        
# plt.figure(1).suptitle("Robôs", fontsize=10)
# plt.plot(x[0,:,:])
# plt.show()

