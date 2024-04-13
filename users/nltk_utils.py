import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
import nltk
from nltk.tokenize import word_tokenize

# Initialize the Porter Stemmer
stemmer = PorterStemmer()

def tokenize(sentence):
    """
    Tokenize a sentence into words.

    Args:
        sentence (str): The input sentence.

    Returns:
        list: A list of tokens (words).
    """
    return nltk.word_tokenize(sentence)

def stem(word):
    """
    Perform stemming on a word.

    Args:
        word (str): The word to be stemmed.

    Returns:
        str: The stemmed word in lowercase.
    """
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, words):
    """
    Create a bag of words representation for a tokenized sentence.

    Args:
        tokenized_sentence (list): List of tokens in a sentence.
        words (list): List of known words in the vocabulary.

    Returns:
        numpy.ndarray: A binary array representing the presence of words in the sentence.
    """
    # Stem each word in the sentence
    sentence_words = [stem(word) for word in tokenized_sentence]

    # Initialize a bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)

    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1

    return bag
