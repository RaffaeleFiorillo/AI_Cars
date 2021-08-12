import random
import pygame
import Auxiliar as Aux


class mind:
    def __init__(self, name):
        self.name = name
        self.weights = [[], [], [], []]
        self.bias = [[], [], [], []]
        self.mutation_chance = Aux.MUTATION_POSSIBILITY
        self.fitness = 0
        self.energy = 1000
        self.distance_traveled = 0
        self.time_alive = 0

    def fitness_level(self):
        power = (1000-self.energy)*self.time_alive
        speed = self.distance_traveled/self.time_alive
        self.fitness = power*0.5 + speed*0.5

    def save_existence(self):
        file = open("parameters/current_generation.txt", "a")
        file.write(f"F:{self.fitness};W:{self.weights};B:{self.bias}\n")
        file.close()

    def get_wb(self, w, b):
        self.weights = w
        self.bias = b

    @staticmethod
    def create_mind_structure():
        # weights/biases number for layer 1: [2, 2, 5, 2, 2]
        layer_1 = [(Aux.random(), Aux.random()) for _ in range(5)]
        layer_1[2] += (Aux.random(), Aux.random())

        # weights/biases number for layer 2: [1, 1, 2, 2, 1, 1]
        layer_2 = [Aux.random() for _ in range(6)]
        layer_2[2] = (layer_2[2], Aux.random())
        layer_2[3] = (layer_2[3], Aux.random())

        # weights/biases number for layer 3: [1, 2, 2, 1]
        layer_3 = [Aux.random() for _ in range(4)]
        layer_3[1] = (layer_3[1], Aux.random())
        layer_3[2] = (layer_3[2], Aux.random())

        # weights/biases number for layer 4: [1, 2, 2, 1]
        layer_4 = [Aux.random() for _ in range(3)]
        return [layer_1, layer_2, layer_3, layer_4]

    def create_mind(self):
        self.weights = self.create_mind_structure()
        self.bias = self.create_mind_structure()

    def cross_over(self, individuo2):
        """cromossoms = [i for i in range(self.inputs)]
        cromossoms_individuo_1 = []
        for i in range(random.randint(1, len(cromossoms) // 2)):
            cromossoms_individuo_1.append(random.choice(cromossoms))
            cromossoms.remove(cromossoms_individuo_1[-1])
        cromossoms_individuo_2 = cromossoms
        weights_new_individuo = [self.weights[i] for i in cromossoms_individuo_1] + [individuo2.weights[y] for y in cromossoms_individuo_2]
        bias_new_individuo = [self.bias[i] for i in cromossoms_individuo_1] + [individuo2.bias[y] for y in cromossoms_individuo_2]
        return [weights_new_individuo, bias_new_individuo]"""

    def activation_function(self, variables):
        pass

    def mutation(self):
        new_w = []
        new_b = []
        for w, b in zip(self.weights, self.bias):
            if random.random() <= self.mutation_chance:
                new_w.append(w + (random.random() / 10) * random.choice([1, -1]))
            else:
                new_w.append(w)
            if random.random() <= self.mutation_chance:
                new_b.append(b + (random.random() / 10) * random.choice([1, -1]))
            else:
                new_b.append(b)
        self.weights = new_w
        self.bias = new_b

    def breed(self, individuo_2, i_name):
        """novo_individuo = _individuo(self.inputs, i_name, self.mutation_chance)
        novo_individuo.weights, novo_individuo.bias = self.cross_over(individuo_2)
        novo_individuo.mutation()
        return novo_individuo"""


class Population:
    def __init__(self, inputs, maxi, mc):
        self.lista = []
        self.generacao = 1
        self.best_indiv = None
        self.second_best = None
        self.numero_input = inputs
        self.max_indiv = maxi
        self.mutation_chance = mc
        self.criar_individuos_novos()

    def criar_individuos_novos(self):
        """for i in range(self.max_indiv):
            self.lista.append(_individuo(self.numero_input, i, self.mutation_chance))
            self.lista[-1].criar_individuo()
            #print(f"name: {self.lista[ -1].name},weights:{self.lista[ -1].weights}, bias: {self.lista[ -1].bias}")"""

    def mostrar_atributos_individuos(self):
        for ind in self.lista:
            print(f"name: {ind.name},weights:{ind.weights}, bias: {ind.bias}")

    def gravar_atributos_individuo(self):
        ficheiro = open("parameters/best_individuos.txt", "a")
        ficheiro.write(f"Geraçao: {self.generacao}\n")
        ficheiro.write(f"F:{self.best_indiv.fitness};W:{self.best_indiv.weights};B{self.best_indiv.bias}\n")
        ficheiro.write(f"F:{self.second_best.fitness};W:{self.second_best.weights};B{self.second_best.bias}\n\n")
        ficheiro.close()

    def ler_atributos_individuos(self):
        ficheiro = open("parameters/geracao_atual.txt", "r")
        lines = ficheiro.readlines()
        index = 0
        for line in lines[1:]:
            list_line = line.split(";")
            fit = float(list_line[0][2:])
            wei = list_line[1][3:-1].split(",")
            bia = list_line[2][3:-1].split(",")
            self.lista[index].weights = [float(w) for w in wei]
            self.lista[index].bias = [float(b) for b in bia[:-1]]
            self.lista[index].bias.append(float(bia[-1][:-1]))
            self.lista[index].fitness = fit
            index += 1

        ficheiro.close()
        ficheiro = open("parameters/geracao_atual.txt", "w")
        ficheiro.write(f"Geracao: {self.generacao+1}\n")
        ficheiro.close()

    def select_best(self):
        fit = -1
        for indv in self.lista:
            if indv.fitness >= fit:
                self.second_best = self.best_indiv
                self.best_indiv = indv
                fit = self.best_indiv.fitness

    def criar_familia(self):
        self.generacao += 1
        self.best_indiv.nome = 0
        self.second_best.nome = 1
        self.lista = []
        self.lista.append(self.best_indiv)
        self.lista.append(self.second_best)
        for i in range((self.max_indiv-2)//2):
            self.lista.append(self.best_indiv.breed(self.second_best, i+2))
            self.lista.append(self.second_best.breed(self.best_indiv, i+3))

