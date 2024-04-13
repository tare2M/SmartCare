import torch
import torch.nn as nn

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()

        # Create a list to hold the hidden layers
        self.hidden_layers = nn.ModuleList()

        # Add input layer
        self.hidden_layers.append(nn.Linear(input_size, hidden_size[0]))

        # Add hidden layers
        for i in range(len(hidden_size) - 1):
            self.hidden_layers.append(nn.Linear(hidden_size[i], hidden_size[i + 1]))

        # Add output layer
        self.output_layer = nn.Linear(hidden_size[-1], num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        # Forward pass through the network
        for layer in self.hidden_layers:
            x = self.relu(layer(x))
        out = self.output_layer(x)

        return out

# Example usage of the NeuralNet class
if __name__ == "__main__":
    # Define input size, hidden layer sizes, and output size
    input_size = 10
    hidden_sizes = [20, 30, 40, 30, 20]  # Modify this list to set the sizes of each hidden layer
    num_classes = 5

    # Create an instance of the neural network
    model = NeuralNet(input_size, hidden_sizes, num_classes)

    # Print the model architecture
    print(model)
