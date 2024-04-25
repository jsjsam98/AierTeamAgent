from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_most_similar(input_text: str, functions: List[str]):
    # Create a TfidfVectorizer
    vectorizer = TfidfVectorizer()

    # Combine the input text and the list of functions to form a corpus
    corpus = [input_text] + functions
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Calculate cosine similarity between the input text and each function
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Find the index of the highest similarity score
    most_similar_index = similarities.argmax()

    # Return the most similar function and the similarity score
    return functions[most_similar_index], similarities[most_similar_index]
