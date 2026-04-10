from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np

# A very simple mock dataset for 3 roles: Data Scientist, ML Engineer, Web Developer
MOCK_DATA = [
    ("python sql machine learning deep learning statistics pandas numpy data science analytics", "Data Scientist"),
    ("python pytorch tensorflow modeling nlp computer vision llm machine learning deployment", "ML Engineer"),
    ("html css javascript react nodejs nextjs frontend backend api web architecture tailwind", "Web Developer"),
    ("python data visualization sql tableau powerbi statistics math modeling predicting", "Data Scientist"),
    ("machine learning deployment mlops docker kubernetes fastai transformer neural networks", "ML Engineer"),
    ("javascript typescript tailwindcss react ui ux web performance database queries frontend", "Web Developer")
]

tfidf = TfidfVectorizer()
clf = LogisticRegression()

# Train the simple model on startup
X, y = zip(*MOCK_DATA)
X_vec = tfidf.fit_transform(X)
clf.fit(X_vec, y)

def predict_roles(text):
    """
    Predicts the top 3 roles based on the input text probabilities.
    """
    vec = tfidf.transform([text.lower()])
    probs = clf.predict_proba(vec)[0]
    
    # Get indices of top probabilities in descending order
    top_indices = np.argsort(probs)[::-1][:3]
    
    roles = []
    for idx in top_indices:
        role_name = clf.classes_[idx]
        score = int(probs[idx] * 100)
        roles.append({"name": role_name, "score": score})
        
    return roles
