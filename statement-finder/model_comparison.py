# #Grid Search model tests


import nltk, string, re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

stopwords = nltk.corpus.stopwords.words('english')
ps = nltk.PorterStemmer()

data = pd.read_csv('dataset-binary.txt', sep='|')
data.columns = ['label', 'body_text']

def clean_text(text):
    text = "".join([word.lower() for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = [ps.stem(word) for word in tokens if word not in stopwords] #stemming and removing stopwords
    # text = [ps.stem(word) for word in tokens] #no removing stopwords
    # text = [word for word in tokens if word not in stopwords] #no stemming
    # text = [word for word in tokens] #no stemming or removing stopwords
    return text

#Vectorize the dataset that includes training and testing data
tfidf_vect = TfidfVectorizer(analyzer=clean_text)
x_tfidf = tfidf_vect.fit_transform(data['body_text'])
x_tfidf_feat = pd.DataFrame(x_tfidf.toarray())

#Random Forest Grid Search
rf = RandomForestClassifier()
param_rf = {'n_estimators': [400, 500, 600], 'max_depth': [20, 25, 30]}
gs = GridSearchCV(rf, param_rf, cv=5, n_jobs=-1)
gs_fit = gs.fit(x_tfidf_feat, data['label'])
print(pd.DataFrame(gs_fit.cv_results_).sort_values('mean_test_score', ascending=False)[0:5])

#Gradient Boosting Grid Search
gb = GradientBoostingClassifier()
param_gb = {'n_estimators': [10, 150, 300], 'max_depth': [20, 25, 30], 'learning_rate': [0.05, 0.1, 0.15]}
gs_gb = GridSearchCV(gb, param_gb, cv=5, n_jobs=-1)
cv_fit = gs_gb.fit(x_tfidf_feat, data['label'])
print(pd.DataFrame(cv_fit.cv_results_).sort_values('mean_test_score', ascending=False)[0:5])