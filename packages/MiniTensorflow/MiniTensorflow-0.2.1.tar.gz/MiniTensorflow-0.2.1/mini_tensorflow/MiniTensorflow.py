import numpy as np
import pandas as pd
class Layer:
    def __init__(self,inputs:np.array,n,activation = 'sigmoid',weights=None,bias=None,random_state=123,name=None) -> None:
        """Initializes the Layer with the given parameters

        Args:
            name (str): Name of the layer, defaults to None
            inputs (np.array): The inputs to the layer
            n ([type]): Number of neurons in the layer
            activation (str, optional): The activation function to use ['sigmoid','tanh']. Defaults to 'sigmoid'.
            weights ([type], optional): The weights for the neural network, choses random weights if not passed. Defaults to None.
            bias ([type], optional): The bias for the neural network, choses random bias if not passed. Defaults to None.
        """    
        np.random.seed(random_state)    
        self.inputs = inputs
        self.weights = weights
        self.bias = bias
        self.name = name
        self.random_state = random_state
        if self.weights is None:
            self.weights = np.random.randn(n,inputs.shape[0])*0.01
        if self.bias is None:
            self.bias = np.zeros((n,1))
        if activation.strip().lower() not in ['sigmoid','tanh','relu','softmax']:
            raise ValueError('Activation should be among [sigmoid,tanh,relu,softmax]')
        else:
            self.activation = activation.strip().lower()
        self.activations = {'sigmoid':self.__sigmoid,'tanh':np.tanh,'relu':self.__relu, 'leaky relu':self.__leaky_relu, 'softmax':self.__softmax}
    def __sigmoid(self,x:np.array)->np.array:
        """Sigmoid activation function for the neural network
        Calculates sigmoid value by using the formula sigmoid(z) = 1/(1+e^(-z))

        Args:
            x (np.array): The array of values on which you want to apply sigmoid 

        Returns:
            np.array: The array of sigmoid values
        """        
        a =  1/(1+np.exp(-x))
        return a 
    def __relu(self,x:np.array)->np.array:
        """Returns the ReLU function applied on that array

        Args:
            x (np.array): The array on which you want to apply the ReLU function on

        Returns:
            np.array: The array with ReLU function applied 
        """              
        a = np.maximum(0,x)
        return a 
    def __leaky_relu(self,x:np.array,alpha=0.01,derivative=False)->np.array:
        """Implements the leaky relu activation function 

        Args:
            x (np.array): The inputs on which leaky relu activation function has to be implemented
            alpha (float, optional): The negative slope for leaky relu. Defaults to 0.01.
            derivative (bool, optional): Whether to return derivative or not. Defaults to False.

        Returns:
            np.array: The array containing the leaky relu activation function or its derivative
        """        
        a = np.maximum(alpha*x, x)
        if not derivative:
            return a
        else:
            return np.array([i if i>alpha*i else alpha for i in x.flatten()]).reshape(x.shape)

    def __softmax(self,x:np.array)->np.array:
        """Implements the softmax activation function

        Args:
            x (np.array): Input for which the softmax activation function has to be implemented

        Returns:
            np.array: The array containing the softmax activation function
        """        
        return np.exp(x)/np.sum(np.exp(x),axis=0)
    def derivative(self)->np.array:
        """Returns the differentiation of the activation function for a corresponding layer

        Returns:
            np.array: The array containing the derivative of the activation function
        """        
        a = self.fit()
        if self.activation == 'sigmoid':
            return a*(1-a)
        elif self.activation == 'tanh':
            return 1-(a**2)
        elif self.activation == 'relu':
            return np.int64(a>0)
        elif self.activation == 'leaky relu':
            return self.__leaky_relu(a,derivative=True)

    def fit(self)->np.array:
        """Fits the layer according to the formula a = activation_function(wx+b)

        Returns:
            np.array: The output of the activation function for that layer
        """        
        z = np.dot(self.weights, self.inputs) + self.bias
        a = self.activations[self.activation](z)
        return a
class Network:
    def __init__(self,layers:list,y:list,alpha=0.01) -> None:
        """Initializes the neural network with the given layers

        Args:
            layers (list): List of layers in the network

        Raises:
            TypeError: Raises a TypeError if any of the layers in the layers list is not a Layer instance
        """            
        self.layers = layers
        for layer in layers:
            if not isinstance(layer,Layer):
                raise TypeError('All the values in the layers list should by Layer instances')
        self.y = y
        self.m = self.y.size
        self.alpha = alpha
    def fit(self,get_history=False)->tuple:
        """Propagates through the network and returns the output and history of outputs if specified

        Args:
            get_history (bool, optional): Whether you want outputs of all layers or not. Defaults to False

        Returns:
            tuple: A tuple containing the output of the network and history if specified
        """                     
        memory = {}
        for layer in self.layers:
            output = layer.fit()
            memory[layer.name] = output
        if get_history:
            return output, memory
        else:
            return output
    @property
    def summary(self)->pd.DataFrame:
        """Returns the DataFrame containing the summary of the network passed to it

        Returns:
            pd.DataFrame: The DataFrame containing the summary of the network
        """        
        summary_df = pd.DataFrame()
        layer_name = []
        layer_weights = []
        layer_bias = []
        total_params = [] 
        for layer in self.layers:
            layer_name.append(layer.name)
            layer_weights.append(layer.weights.shape)
            layer_bias.append(layer.bias.shape)
            total_params.append(layer.weights.size+layer.bias.size)
        summary_df['Layer Name'] = layer_name
        summary_df['Weights'] = layer_weights
        summary_df['Bias'] = layer_bias
        summary_df['Total Parameters'] = total_params
        return summary_df
    @property
    def params(self)->list:
        """Gets the total number of parameters in each layer

        Returns:
            params_list: The list containing the total number of parameters in each layer
        """        
        params_list = []
        for layer in self.layers:
            params_list.append(layer.weights.size+layer.bias.size)
        return params_list
    def compute_cost(self,y:np.array,natural_log=True)->float:
        """Calculates the cost of the network compared to the target

        Args:
            y (np.array): Target values for the network 
            natural_log (bool, optional): Whether you want to use log10 or natural log. Defaults to True.

        Returns:
            float: The cost of that network
        """       
        if self.layers[-1].activation == 'sigmoid':        
            outputs = self.fit()
            if natural_log:
                cost = -np.mean((y*np.log(outputs))+((1-y)*np.log(1-outputs)))
            else:
                cost = -np.mean((y*np.log10(outputs))+((1-y)*np.log10(1-outputs)))
            return cost
    def __one_hot(self)->np.array:
        """Implements the one hot encoding 
        NOTE - For internal purposes only
        Used for the back propagation in case of softmax activation function

        Returns:
            np.array: The one hot encoded version of the vector 
        """        
        one_hot = np.zeros(shape=(self.y.size, self.y.max() + 1))
        one_hot[np.arange(self.y.size), self.y] = 1 
        return one_hot.T
    def __backward_propagation(self)->dict:
        """Implements the back propagation in the neural network 
        NOTE - For internal use only 
        Will be used for training the network 

        Returns:
            dict: The dictionary containing the derivatives of parameters at every layer
        """               
        grads = {}
        output = self.fit()
        
        if self.layers[-1].activation == 'softmax':
            one_hot_y = self.__one_hot(self.y)
            prod = output-one_hot_y
        elif self.layers[-1].activation == 'sigmoid':
            prod = output-self.y
        
        dw_output = np.dot(prod, self.layers[-1].inputs.T)/self.m
        db_output = np.sum(prod,axis=1,keepdims=True)/self.m
        grads[f'dw_{self.layers[-1].name}'] = dw_output
        grads[f'db_{self.layers[-1].name}'] = db_output
        self.layers[-1].weights = self.layers[-1].weights - (self.alpha*dw_output)
        self.layers[-1].bias = self.layers[-1].bias - (self.alpha*db_output)
        prod = np.dot(self.layers[-1].weights.T,prod)
        for i in reversed(range(len(self.layers[:-1]))):
            prod = prod * self.layers[i].derivative()
            dw_layer = np.dot(prod, self.layers[i].inputs.T)/self.m
            db_layer = np.sum(prod, axis=1,keepdims=True)/self.m
            grads[f'dw_{self.layers[i].name}'] = dw_layer
            grads[f'db_{self.layers[i].name}'] = db_layer
            self.layers[i].weights = self.layers[i].weights-(self.alpha*dw_layer)
            self.layers[i].bias = self.layers[i].bias-(self.alpha*db_layer)
            prod = np.dot(self.layers[i].weights.T, prod)
        return grads
    def train(self, epochs:int,history=False)->dict:
        """Trains the network for the specified number of iterations 

        Args:
            epochs (int): The number of iterations for which you want to train the network 
            history (bool, optional): If you want the history of gradients at each iterations. Defaults to False.

        Returns:
            dict: The dictionary containing the gradients of parameters at each iteration 
        """               
        history_dict = {}
        for i in range(epochs):
            grads = self.__backward_propagation()
            history_dict[f'epoch_{i}'] = grads
        if history:
            return history_dict
        else:
            return None
    def predict(self,values:np.array)->np.array:
        """Performs prediction for the given values 

        Args:
            values (np.array): The values on which you want to predict 
        Returns:
            np.array: The array of predictions 
        """        
        outputs = self.fit()
        if self.layers[-1].activation == 'sigmoid':
            return np.array([1 if i>0 else 0 for i in outputs]).reshape(outputs.shape)
        elif self.layers[-1].activation == 'softmax':
            return np.argmax(outputs, axis=0)
            