import turtle
import random
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import time

turtle.register_shape("x3.gif")

tamanho_janela = 700
turtle.setup(tamanho_janela+100,tamanho_janela+100,0,0)

screen = turtle.Screen()
screen.colormode(255)

# Matriz adjacencia
A = np.array([[0,1,0,1,0,0],
              [0,0,1,0,0,0],
              [0,1,0,0,0,0],
              [1,0,0,0,0,0],
              [1,0,0,1,0,0],
              [0,0,1,0,0,0]])

# A = np.array([[0,1,0,0,0,0,0,1,0,0],
#               [1,0,0,0,1,1,0,1,0,0],
#               [0,0,0,0,0,0,1,0,1,1],
#               [0,0,0,0,1,1,0,1,0,0],
#               [0,1,0,1,0,1,0,1,0,0],
#               [0,1,0,1,1,0,0,1,0,0],
#               [0,0,1,0,0,0,0,0,1,0],
#               [1,1,0,1,1,1,0,0,0,0],
#               [0,0,1,0,0,0,1,0,0,1],
#               [0,0,1,0,0,0,0,0,1,0]])



# Tempo de simulação
t_sim = 100

# Passo de integração
h = 0.05

# Time series
t = np.array([])
aux = 0
for i in range(int(t_sim/h)):
    aux = aux+h
    t = np.append(t, aux)

# Número de iterações
n_steps = len(t)

# Número de nós (robos)
n = A.shape[0]

# Matriz que representa quais robos sabem a referência
B = np.array([0,0,1,0,0,0,0,0,0,0])

# Dimesão dos estados (coordenadas x e y)
m = 2

# Número de referências
N = 1

alcance_dos_robos = 200

# Informação inicial dos estados
x0 = np.random.randint(-alcance_dos_robos,alcance_dos_robos,(n,m))

# Indica se o raio de comunicação é levado em consideração
topologia_dinamica = True

# Vetor que contém o raio de comunicação dos robôs
raio = np.array([70, 90, 50, 50, 30, 30, 70, 90, 50, 50])
raio = raio*3

# Referência
r = np.random.randint(-alcance_dos_robos,alcance_dos_robos,(N,2))

# Algoritmo principal
x = np.zeros((n,m,n_steps))

# Tipo de movimentação que a referência irá fazer
desenho_referencia = "quadrado"

# Tamanho da aresta dos desenhos feitos pela referência
aresta = 80

# Atribui a posição inicial para os robôs
x[:, :, 0] = x0

# Variáveis auxiliares
movimenta_referencia = True

iteracoes_para_movimento = 2

cont_iteracoes = 0

velocidade_referencia = 2

robos = {}

for i in range(n):
    robos[i] = turtle.Turtle()
    robos[i].pen(pensize=3)
    robos[i].shape("circle")
    if B[i] == 1:
        robos[i].shape("square")
    robos[i].penup()
    robos[i].color( random.randint(0, 255), 
                    random.randint(0, 255), 
                    random.randint(0, 255))
    size = robos[i].turtlesize()
    increase = tuple([0.8* num for num in size])
    robos[i].turtlesize(*increase)

for i in range(n):
    robos[i].setpos(x0[i])
    robos[i].pendown()

referencia = {}
for l in range(N):
    referencia[l] = turtle.Turtle()
    referencia[l].shape("x3.gif")
    referencia[l].penup()
    referencia[l].setpos(r[l,:])

vertices = {}
v = {}
for l in range(N):
    v[l] = 0
    vertices[l] = {}
    if desenho_referencia == "quadrado":
        vertices[l][0] = r[l,:]
        vertices[l][1] = [r[l,0],r[l,1]+aresta]
        vertices[l][2] = [r[l,0]-aresta,r[l,1]+aresta]
        vertices[l][3] = [r[l,0]-aresta,r[l,1]]
    elif desenho_referencia == "triangulo":
        vertices[l][0] = r[l,:]
        vertices[l][1] = [r[l,0]-aresta/2,r[l,1]+aresta*math.sqrt(3)/2]
        vertices[l][2] = [r[l,0]-aresta,r[l,1]]
    elif desenho_referencia == "aleatorio":
        vertices[l][0] = r[l,:]
        for i in range(1, random.randint(1, 10)):
            vertices[l][i] = [r[l,0]+aresta*random.uniform(0, 1),r[l,1]+aresta*random.uniform(0, 1)]

tRadiumDrawer = turtle.Turtle()
tRadiumDrawer.speed(0)
tRadiumDrawer.shapesize(0.001,0.001)
tRadiumDrawer.penup()
for robo in range(n):
    radiun = raio[robo]
    tRadiumDrawer.setpos(robos[robo].pos()[0],robos[robo].pos()[1]+8)
    tRadiumDrawer.write("{}".format(robo),font=('Arial',10,'normal'))
    tRadiumDrawer.setpos(robos[robo].pos()[0],robos[robo].pos()[1]-radiun)
    tRadiumDrawer.pendown()

  #  tRadiumDrawer.pencolor(robos[robo].getcolor())
    tRadiumDrawer.circle(radiun)
    tRadiumDrawer.penup()

time.sleep(10)

tRadiumDrawer.clear()

for k in range(n_steps-1):
    for i in range(n):
        sum_i = 0

        for j in range(n):
            comunicacao = 1
            if topologia_dinamica:
                distancia = abs(complex((x[j, 0, k] - x[i, 0, k]), (x[j, 1, k] - x[i, 1, k])))
                if distancia >= raio[j]:
                    comunicacao = 0

            sum_i = sum_i + (x[j, :, k] - x[i, :, k])*A[i, j]*comunicacao

        for l in range(N):
            sum_i = sum_i + (referencia[l].position() - x[i, :, k])*B[i]

        x[i, :, k + 1] = x[i, :, k] + h*sum_i
        robos[i].setpos(x[i,:,k+1])

    cont_iteracoes += 1

    if cont_iteracoes == iteracoes_para_movimento and movimenta_referencia:
        cont_iteracoes = 0
        for l in range(N):
            if abs(referencia[l].position()[0] - vertices[l][v[l]][0]) < 0.5 and abs(referencia[l].position()[1] - vertices[l][v[l]][1]) < 0.5:
                if v[l] < len(vertices[l])-1:
                    v[l] += 1
                else:
                    v[l] = 0
                referencia[l].setheading(referencia[l].towards(vertices[l][v[l]][0], vertices[l][v[l]][1]))
            else:
                referencia[l].forward(velocidade_referencia)

screen.exitonclick()