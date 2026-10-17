import numpy as np


def loss_function(y_true, y_pred,loss_name, derivative=False):
    functions = {
        "MSE": (np.mean(np.power(y_true - y_pred, 2)), 2 * (y_pred - y_true) / y_true.size),
    }
    return functions[loss_name][int(derivative)]

#Definicija aktivacijskih funkcij
def activation_function(x, func_name, derivative=False):
    functions = {
        "tanh": (np.tanh(x), 1 - np.tanh(x)**2),
        "sigmoid": (1 / (1 + np.exp(-x)), (1 / (1 + np.exp(-x))) * (1 - (1 / (1 + np.exp(-x))))),
        "relu": (np.maximum(0, x), np.where(x > 0, 1, 0)),
        "linear": (x, np.ones_like(x)),
    }
    return functions[func_name][int(derivative)]

#Temelji razred Layer
class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    # computes the output Y of a layer for a given input X
    def forward_propagation(self, input):
        raise NotImplementedError

    # computes dE/dX for a given dE/dY (and update parameters if any)
    def backward_propagation(self, output_error, learning_rate):
        raise NotImplementedError

# Podeduje parametre iz razreda Layer
class ActivationLayer(Layer):
    def __init__(self, func_name):
        self.name="Activation"
        self.func_name=func_name
        self.activation = lambda x: activation_function(x, self.func_name, derivative=False)
        self.activation_prime = lambda x: activation_function(x, self.func_name, derivative=True)

    # returns the activated input
    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output

    # Returns input_error=dE/dX for a given output_error=dE/dY.
    # learning_rate is not used because there is no "learnable" parameters.
    def backward_propagation(self, output_error, learning_rate):
        return self.activation_prime(self.input) * output_error

# Podeduje parametre iz razreda Layer
class FCLayer(Layer):
    # input_size = number of input neurons
    # output_size = number of output neurons
    def __init__(self,input_size,output_size,name):
        self.name=name
        self.weights = np.random.rand(input_size, output_size) - 0.5
        self.bias = np.random.rand(1, output_size) - 0.5
        self.shape=self.weights.shape
        print(f"Layer {self.name} -> {self.shape}")
    
    # returns output for a given input
    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output
    
    # computes dE/dW, dE/dB for a given output_error=dE/dY. Returns input_error=dE/dX.
    def backward_propagation(self, output_error, learning_rate):
        input_error = np.dot(output_error, self.weights.T)
        
        weights_error = np.dot(self.input.T, output_error)
        # dBias = output_error

        # update parameters
        self.weights -= learning_rate * weights_error
        self.bias -= learning_rate * output_error
        return input_error


class Network:
    def __init__(self):
        self.layers = []
        self.loss = None #Metrika za natančnost celotne mreže
        self.loss_prime = None #Odvod metrike za natančnost celotne mreže

    # add layer to network
    def add(self, layer):
        self.layers.append(layer)

    # set loss to use
    def use(self, loss_name):
        self.loss = lambda y_true, y_pred: loss_function(y_true, y_pred, loss_name, derivative=False)
        self.loss_prime = lambda y_true, y_pred: loss_function(y_true, y_pred, loss_name, derivative=True)

    # predict output for given input
    def predict(self, input_data):
        # sample dimension first
        samples = len(input_data)
        result = []

        # run network over all samples
        for i in range(samples):
            # forward propagation
            output = input_data[i]
            for layer in self.layers:
                output = layer.forward_propagation(output)
            result.append(output)
        return result
    
    # train the network
    def fit(self, x_train, y_train, epochs, learning_rate, show=False):
        # sample dimension first
        samples = len(x_train)

        # training loop
        err = 0
        for i in range(epochs):
            err = 0
            for j in range(samples):
                # forward propagation
                output = x_train[j]
                for layer in self.layers:
                    output = layer.forward_propagation(output)

                # compute loss (for display purpose only)
                err += self.loss(y_train[j], output)

                # backward propagation
                error = self.loss_prime(y_train[j], output)
                for layer in reversed(self.layers):
                    error = layer.backward_propagation(error, learning_rate)

            # calculate average error on all samples
            err /= samples
            if show:
                print(f'\repoch {i+1}/{epochs}   error={err:.5f}',end="")
        #print(f'\repoch {epochs}   error={err:.5f}',end="")
        return err


def ustvari_nevronsko_mrezo(arh,func_name):
    """
    arh -> arhitektura mreže, npr. [1,2,4,2,1]
    arh[0] je vhodna plast (podatki, ni plast nevronov); za vsak par (arh[l], arh[l+1])
    ustvarimo polno povezano plast FCLayer in aktivacijsko plast.
    """
    net = Network()
    for l in range(len(arh) - 1):
        net.add(FCLayer(arh[l], arh[l + 1], l))
        net.add(ActivationLayer(func_name))
    return net
