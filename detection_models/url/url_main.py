import sys
import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

def sanitization(web):
    web = web.lower()
    token = []
    dot_token_slash = []
    raw_slash = str(web).split('/')
    for i in raw_slash:
        raw1 = str(i).split('-')
        slash_token = []
        for j in range(0, len(raw1)):
            raw2 = str(raw1[j]).split('.')
            slash_token = slash_token + raw2
        dot_token_slash = dot_token_slash + raw1 + slash_token
    token = list(set(dot_token_slash)) 
    if 'com' in token:
        token.remove('com')
    return token

def predict_url(url):
    whitelist = ['hackthebox.eu', 'root-me.org', 'gmail.com']
    s_url = [url] if url not in whitelist else []

    # Loading the model and vectorizer
    model_path = "detection_models/url/Classifier/pickel_model.pkl"
    vectorizer_path = "detection_models/url/Classifier/pickel_vector.pkl"

    with open(model_path, 'rb') as model_file, open(vectorizer_path, 'rb') as vectorizer_file:
        lgr = pickle.load(model_file)
        vectorizer = pickle.load(vectorizer_file)

    # Predicting
    x = vectorizer.transform(s_url)
    y_predict = lgr.predict(x)

    for site in whitelist:
        s_url.append(site)

    predict = list(y_predict)
    for j in range(len(whitelist)):
        predict.append('good')

    return predict[0]

if __name__ == "__main__":
    # Check if a URL argument is provided
    if len(sys.argv) < 2:
        print("Usage: python url_main.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    prediction = predict_url(url)
    print("\nThe entered domain is:", prediction)
    print("\nIf you feel that this prediction is wrong, or if you are not sure about this output, "
          "you can contact us at ayushkumarmishra000@gmail.com. We'll check the URL and update the machine accordingly. "
          "Thank you.")
