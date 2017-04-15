import random
import time
import math
import pickle

class Neuron:
    def __init__(self, numInput, layer, bias):
        self.layer = layer
        self.weights = [random.uniform(-1, 1) for i in range(numInput)] + [bias]
        self.numInput = numInput + 1
        self.netInput = 0
        self.output = 0

    def calculate_pd_error_wrt_total_net_input(self, target_output):
        return self.calculate_pd_error_wrt_output(target_output) * self.calculate_pd_total_net_input_wrt_input();

    def calculate_pd_error_wrt_output(self, target_output):
        return -(target_output - self.output)

    def calculate_pd_total_net_input_wrt_input(self):
        return self.output * (1 - self.output)

    def calculate_pd_total_net_input_wrt_weight(self, index):
        return self.layer.inputs[index]

    def calculate_error(self, target_output):
        return 0.5 * (target_output - self.output) ** 2

class NeuronLayer:
    def __init__(self, numNeuron, numInputPerNeuron, bias):
        self.numNeuron = numNeuron
        self.neuron = [Neuron(numInputPerNeuron, self, bias) for i in range(numNeuron)]
        self.inputs = []
        self.outputs = []

    def __iter__(self):
        return iter(self.neuron)

class NeuralNet:
    LEARNING_RATE = 0.5

    def __init__(self, numInput, numOutput, numHiddenLayer, neuronPerLayer):
        self.numInput = numInput
        self.numOutput = numOutput
        self.numHiddenLayer = numHiddenLayer
        self.neuronPerLayer = neuronPerLayer
        self.neuronLayers = []

        self.createNet()

    def createNet(self):
        #first hidden layer
        self.neuronLayers = [NeuronLayer(self.neuronPerLayer, self.numInput, 0.35)]
        #other hidden layer
        self.neuronLayers += [NeuronLayer(self.neuronPerLayer,self.neuronPerLayer) for i in range(self.numHiddenLayer - 1)]
        # output layer
        self.neuronLayers += [NeuronLayer(self.numOutput, self.neuronPerLayer, 0.6)]

    def getWeights(self):
        weights = []
        for layer in self.neuronLayers:
            for neuron in layer:
                weights += neuron.weights
        return weights

    def putWeights(self, weights):
        cWeights = 0
        for layer in self.neuronLayers:
            for neuron in layer:
                neuron.weights = weights[cWeights:(cWeights + neuron.numInput)]
                cWeights += neuron.numInput

    def Step(self, activation):
        if activation > 0.0 :
            return 1.0
        return 0.0

    def Sigmoid(self, activation, response = 1):
        try:
            return 1 / (1 + math.exp(-activation / response))
        except OverflowError:
            print("math range error: " + str(activation))
            exit()

    def translate(self, board):
        sum = 0
        trns_board = []
        for raw in board:
            for x in raw:
                if x == 0: break
                sum += x
            trns_board.append(sum/100)
            sum = 0
        return trns_board
        # new_board = []
        # for raw in board:
        #     raw += [0]*(8 - (len(raw) % 2))
        #     count = 7
        #     result = 0
        #     for element in raw:
        #         result += element*(2**count)
        #         if (count == 0):
        #             new_board.append(result)
        #             result = 0
        #             count = 8
        #         count -= 1
        # return new_board

    def move(self, board, sig):  #Update
        output = []
        i = 0

        for layer in self.neuronLayers:
            if (i > 0):
                layer.inputs = output
            else:
                layer.inputs = self.translate(board)
            output = []

            for neuron in layer:
                neuron.netInput = 0
                try:
                    for j in range(neuron.numInput - 1):
                        neuron.netInput += layer.inputs[j] * neuron.weights[j]
                except IndexError:
                    print("layer num " + str(self.neuronLayers.index(layer)))
                    print("neuron num " + str(layer.neuron.index(neuron)))
                    exit()
                neuron.netInput += neuron.weights[-1]
                if sig == True:
                    neuron.output = self.Sigmoid(neuron.netInput, response = 1)
                    output.append(neuron.output)
                else:
                    neuron.output = self.Step(neuron.netInput)
                    output.append(neuron.output)
            layer.outputs = output
            i+=1
        # output = [int(element * 100) for element in output]
        return output

    def train(self, trainig_inputs, training_outputs):
        "https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/"
        self.move(trainig_inputs, sig = True)

        # 1. Output neuron deltas
        pd_errors_wrt_output_neuron_total_net_input = [0] * len(self.neuronLayers[-1].neuron)
        for o in range(len(self.neuronLayers[-1].neuron)):
            # ∂E/∂zⱼ
            pd_errors_wrt_output_neuron_total_net_input[o] = self.neuronLayers[-1].neuron[
                o].calculate_pd_error_wrt_total_net_input(training_outputs[o])

        # 2. Hidden neuron deltas
        pd_errors_wrt_hidden_neuron_total_net_input = [0] * len(self.neuronLayers[-2].neuron)
        for h in range(len(self.neuronLayers[-2].neuron)):

            # We need to calculate the derivative of the error with respect to the output of each hidden layer neuron
            # dE/dyⱼ = Σ ∂E/∂zⱼ * ∂z/∂yⱼ = Σ ∂E/∂zⱼ * wᵢⱼ
            d_error_wrt_hidden_neuron_output = 0
            for o in range(len(self.neuronLayers[-1].neuron)):
                d_error_wrt_hidden_neuron_output += pd_errors_wrt_output_neuron_total_net_input[o] * \
                                                    self.neuronLayers[-1].neuron[o].weights[h]

            # ∂E/∂zⱼ = dE/dyⱼ * ∂zⱼ/∂
            pd_errors_wrt_hidden_neuron_total_net_input[h] = d_error_wrt_hidden_neuron_output * \
                                                             self.neuronLayers[-2].neuron[
                                                                 h].calculate_pd_total_net_input_wrt_input()

        # 3. Update output neuron weights
        for o in range(len(self.neuronLayers[-1].neuron)):
            for w_ho in range(len(self.neuronLayers[-1].neuron[o].weights) - 1):
                # ∂Eⱼ/∂wᵢⱼ = ∂E/∂zⱼ * ∂zⱼ/∂wᵢⱼ
                pd_error_wrt_weight = pd_errors_wrt_output_neuron_total_net_input[o] * self.neuronLayers[-1].neuron[
                    o].calculate_pd_total_net_input_wrt_weight(w_ho)

                # Δw = α * ∂Eⱼ/∂wᵢ
                self.neuronLayers[-1].neuron[o].weights[w_ho] -= NeuralNet.LEARNING_RATE * pd_error_wrt_weight


        # 4. Update hidden neuron weights
        for h in range(len(self.neuronLayers[-2].neuron)):
            for w_ih in range(len(self.neuronLayers[-2].neuron[h].weights) -1 ):
                # ∂Eⱼ/∂wᵢ = ∂E/∂zⱼ * ∂zⱼ/∂wᵢ
                pd_error_wrt_weight = pd_errors_wrt_hidden_neuron_total_net_input[h] * self.neuronLayers[-2].neuron[
                    h].calculate_pd_total_net_input_wrt_weight(w_ih)

                # Δw = α * ∂Eⱼ/∂wᵢ
                self.neuronLayers[-2].neuron[h].weights[w_ih] -= NeuralNet.LEARNING_RATE * pd_error_wrt_weight




# numInput, numOutput, numHiddenLayer, neuronPerLayer = 10000, 2, 2, 50
# net = NeuralNet(numInput, numOutput, numHiddenLayer, neuronPerLayer)
# print(len(net.getWeights()))