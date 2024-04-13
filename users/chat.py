import random
import json
import torch

from .model1 import NeuralNet
from .nltk_utils import bag_of_words, tokenize, stem



# Define the device (CPU or CUDA if available)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the intents data from a JSON file
with open('./intents.json', 'r', encoding="utf8") as json_data:
    intents = json.load(json_data)

# Load the chatbot model and its configuration
MODEL_FILE = "data.pth"
model_data = torch.load(MODEL_FILE)

input_size = model_data["input_size"]
hidden_sizes = model_data["hidden_sizes"]
output_size = model_data["output_size"]
all_words = model_data['all_words']
tags = model_data['tags']
model_state = model_data["model_state"]

# Initialize the model and set it to evaluation mode
model = NeuralNet(input_size, hidden_sizes, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "SmartCare"

def get_response(msg):
    # Tokenize the user's message
    sentence = tokenize(msg)
    # Convert the message to a bag of words
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    # Get the model's output
    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.2555:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])

    return "أعطني معلومات أوضح من فضلك"


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(f"{bot_name}: {resp}")
def chatbot_response(user_message):
    response = get_response(user_message)
    return response