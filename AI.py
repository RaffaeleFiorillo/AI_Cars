import Auxiliar as Aux


class Mind:
    def __init__(self, name, new_born=True):
        self.name = str(name)
        self.weights = [[], [], []]
        self.bias = []
        self.directions_taken = {"left": 0, "center": 0, "right": 0}
        self.mutation_chance = Aux.MUTATION_POSSIBILITY
        self.fitness = 0
        self.energy = 4000
        self.monotony_should_be_1 = False
        self.distance_traveled = 0
        self.time_alive = 0
        if new_born:
            self.create_mind()

    def __copy__(self):
        copy_number = 1
        index = len(self.name)
        if "_" in self.name:
            copy_number = str(int(self.name[-1])+1)
            index = self.name.index('_')
        new_mind = Mind(f"{self.name[index:]}_{copy_number}", False)
        new_mind.weights = self.bias
        new_mind.bias = self.bias
        return new_mind

    def fitness_level(self):
        power = Aux.normal_minus1_1((1000-self.energy), 0, 1000)*-1

        if self.monotony_should_be_1:
            monotony = 1
        else:
            left_monotony = Aux.normal_minus1_1(Aux.module(self.directions_taken["left"]))
            right_monotony = Aux.normal_minus1_1(Aux.module(self.directions_taken["right"]))
            monotony = Aux.vectorized(left_monotony, right_monotony)
            monotony = Aux.module(1-Aux.normal_minus1_1(monotony, 0, 1000))

        self.fitness = (power * 0.5 + self.distance_traveled * 0.5) * monotony
        print(f"Name: {self.name} | Fitness: {self.fitness} Monotony: {monotony} Power: {power}"
              f" | Distance: {self.distance_traveled}")
        if self.fitness >= 70000:
            self.save_existence(override=True)
            exit()

    def save_existence(self, override=False):
        file = open(Aux.FILE_NAME, "a")
        if override:
            file.close()
            file = open(Aux.FILE_NAME, "w")
        file.write(f"F:{self.fitness};W:{self.weights};B:{self.bias}\n")
        file.close()

    def get_wb(self, w, b):
        self.weights = w
        self.bias = b

    def create_mind_structure(self):
        # weights/biases number for layer 1: [2, 2, 5, 2, 2]
        layer_1 = [(self.mutate_value(Aux.random()), self.mutate_value(Aux.random())) for _ in range(5)]
        layer_1[2]+=(self.mutate_value(Aux.random()), self.mutate_value(Aux.random()), self.mutate_value(Aux.random()))

        # weights/biases number for layer 2: [1, 2, 1, 1, 2, 1]
        layer_2 = [self.mutate_value(Aux.random()) for _ in range(6)]
        layer_2[1] = (layer_2[2], self.mutate_value(Aux.random()))
        layer_2[4] = (layer_2[3], self.mutate_value(Aux.random()))

        # weights/biases number for layer 3: [1, 2, 2, 1]
        layer_3 = [self.mutate_value(Aux.random()) for _ in range(4)]
        layer_3[1] = (layer_3[1], self.mutate_value(Aux.random()))
        layer_3[2] = (layer_3[2], self.mutate_value(Aux.random()))

        # weights/biases number for layer 4: [1, 2, 2, 1]
        layer_4 = [self.mutate_value(Aux.random()) for _ in range(3)]
        return [layer_1, layer_2, layer_3, layer_4]

    @staticmethod
    def mutate_value(value):
        if Aux.random() > 0.4:  # invert value's signal
            value *= Aux.random_choice([-1, 1])
        if Aux.random() > 0.4:   # increase or decrease value
            value += Aux.random_choice([-1, 1]) * (Aux.random()/Aux.random_choice([1000, 100, 10]))
        return value

    def mutate(self, values):
        if type(values) is tuple:
            new_tuple = (self.mutate_value(value) if Aux.random()>=self.mutation_chance else value for value in values)
            return tuple(new_tuple)
        return self.mutate_value(values) if Aux.random() >= self.mutation_chance else values

    def cross_over(self, layers1, layers2):
        # cross over for layer 1
        layer_1 = [self.mutate(value1) if Aux.random() > 0.5 else self.mutate(value2) for value1, value2
                   in zip(layers1[0], layers2[0])]

        # cross over for layer 2
        layer_2 = [self.mutate(value1) if Aux.random() > 0.5 else self.mutate(value2) for value1, value2
                   in zip(layers1[1], layers2[1])]

        # cross over for layer 3
        layer_3 = [self.mutate(value1) if Aux.random() > 0.5 else self.mutate(value2) for value1, value2
                   in zip(layers1[2], layers2[2])]

        # cross over for layer 4
        layer_4 = [self.mutate(value1) if Aux.random() > 0.5 else self.mutate(value2) for value1, value2
                   in zip(layers1[3], layers2[3])]

        return [layer_1, layer_2, layer_3, layer_4]

    def create_mind(self):
        self.weights = self.create_mind_structure()
        self.bias = self.create_mind_structure()

    def breed(self, mind2):
        new_mind = self.__copy__()
        new_mind.weights = new_mind.cross_over(self.weights, mind2.weights)
        new_mind.bias = new_mind.cross_over(self.bias, mind2.bias)
        return new_mind

    def create_layer_2(self, values):
        neuron_1 = tuple(w*values[0]+b for w, b in zip(self.weights[0][0], self.bias[0][0]))
        neuron_2 = tuple(w*values[1]+b for w, b in zip(self.weights[0][1], self.bias[0][1]))
        neuron_3 = tuple(w*values[2]+b for w, b in zip(self.weights[0][2], self.bias[0][2]))
        neuron_4 = tuple(w*values[3]+b for w, b in zip(self.weights[0][3], self.bias[0][3]))
        neuron_5 = tuple(w*values[4]+b for w, b in zip(self.weights[0][4], self.bias[0][4]))

        value_1 = Aux.normal_minus1_1(neuron_1[0] + neuron_2[0])
        value_2 = Aux.normal_minus1_1(neuron_1[1] + neuron_3[0])
        value_3 = Aux.normal_minus1_1(neuron_2[1] + neuron_3[1])
        value_4 = Aux.normal_minus1_1(neuron_3[2] + neuron_4[0])
        value_5 = Aux.normal_minus1_1(neuron_3[3] + neuron_5[0])
        value_6 = Aux.normal_minus1_1(neuron_4[1] + neuron_5[1])

        return value_1, value_2, value_3, value_4, value_5, value_6

    def create_layer_3(self, values):
        neuron_1 = self.weights[1][0]*values[0] + self.bias[1][0]
        neuron_2 = tuple(w * values[1] + b for w, b in zip(self.weights[1][1], self.bias[1][1]))
        neuron_3 = self.weights[1][2]*values[2] + self.bias[1][2]
        neuron_4 = self.weights[1][3]*values[3] + self.bias[1][3]
        neuron_5 = tuple(w * values[4] + b for w, b in zip(self.weights[1][4], self.bias[1][4]))
        neuron_6 = self.weights[1][5] * values[5] + self.bias[1][5]

        value_1 = Aux.normal_minus1_1(neuron_1 + neuron_2[0])
        value_2 = Aux.normal_minus1_1(neuron_2[1] + neuron_3)
        value_3 = Aux.normal_minus1_1(neuron_4 + neuron_5[0])
        value_4 = Aux.normal_minus1_1(neuron_5[1] + neuron_6)

        return value_1, value_2, value_3, value_4

    def create_layer_4(self, values):
        neuron_1 = self.weights[2][0] * values[0] + self.bias[2][0]
        neuron_2 = tuple(w * values[1] + b for w, b in zip(self.weights[2][1], self.bias[2][1]))
        neuron_3 = tuple(w * values[2] + b for w, b in zip(self.weights[2][2], self.bias[2][2]))
        neuron_4 = self.weights[2][3] * values[3] + self.bias[2][3]

        value_1 = Aux.normal_minus1_1(neuron_1 + neuron_2[0])
        value_2 = Aux.normal_minus1_1(neuron_2[1] + neuron_3[0])
        value_3 = Aux.normal_minus1_1(neuron_3[1] + neuron_4)

        return value_1, value_2, value_3

    def get_final_value(self, values):
        neuron_1 = self.weights[3][0] * values[0] + self.bias[3][0]
        neuron_2 = self.weights[3][1] * values[1] + self.bias[3][1]
        neuron_3 = self.weights[3][2] * values[2] + self.bias[3][2]

        return Aux.normal_minus1_1(neuron_1 + neuron_2 + neuron_3)

    def activation_function(self, inputs):
        input_layer = [Aux.normalize(inp) for inp in inputs]
        layer_2 = self.create_layer_2(input_layer)
        layer_3 = self.create_layer_3(layer_2)
        layer_4 = self.create_layer_4(layer_3)
        return self.get_final_value(layer_4)
