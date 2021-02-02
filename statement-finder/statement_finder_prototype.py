
### statement_finder_prototype.py
# Working file for the statement finder tool
# The goal for this tool is to take a webpage as input, parse the text, and return a list of all the statements made on the webpage
# The statements will then be passed to a separate tool that can check their factual integrity



### Part 1: Webpage Parser
# This portion of the tool will take in a webpage as input, parse its text, and return strings with text from the webpage
# Note: I will work on this after developing a working prototype of the below statement finder tool
# Initial Thoughts: possibly look at paragraph and heading tags in html, filter out as much unnecessary text as possible
# Terms: Web scraping

# Sample text to be used below for the statement finder tool
# Tests: opinion, exclamation, statement, question, name with '.' abbreviation
# Expected output from the statement finder tool:
#   ["I like going to the zoo.", 
#    "They can run up to 80 miles per hour",
#    "Mr. Smith was our guide last time."]
# Note: "They" in the second statement refers to Cheetahs
sampleText = "I like going to the zoo. Cheetahs are my favorite animal there! They can run up to 80 miles per hour! What is your favorite animal? Mr. Smith was our guide last time."
sampleCompSentence = "Cheetahs can run up to 80 miles per hour and grow to be 160 pounds."


### Part 2: Statement Finder
# This portion of the tool will take strings/arrays of text as input, apply natural language processing to them, and output a list of statements
# Subtasks: Split text into sentences, use dataset to train model, use trained model to predict each sentence as a statement/nonstatement

import nltk, string, re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

nltk.download('wordnet')

#Process input_text from webpage parser
input_text = pd.DataFrame(nltk.sent_tokenize(sampleText))
input_text.columns = ['body_text']
input_text['label'] = ['undecided' for i in range(input_text.size)]
test_size = input_text.size // 2

stopwords = nltk.corpus.stopwords.words('english') #Read in stopwords for easy access later
wn = nltk.WordNetLemmatizer() #Instantiate lemmatizer

#Read in training data from dataset file
# data = pd.read_csv('dataset.txt', sep='|')
data = pd.read_csv('dataset-binary.txt', sep='|')
data.columns = ['label', 'body_text']
train_size = data.size // 2
data = data.append(input_text, ignore_index=True) #Add the input text to the training data

def clean_text(text): #Method for cleaning text in preparation for vectorizing
    text = "".join([word.lower() for word in text if word not in string.punctuation])
    tokens = re.findall('\w+', text)
    text = [wn.lemmatize(word) for word in tokens if word not in stopwords]
    return text

input_text['clean_text'] = [clean_text(text) for text in input_text['body_text']] #Debug line

#Vectorize the dataset that includes training and testing data
tfidf_vect = TfidfVectorizer(analyzer=clean_text)
x_tfidf = tfidf_vect.fit_transform(data['body_text'])
x_tfidf_feat = pd.DataFrame(x_tfidf.toarray())

#Split the data into x/y train/test sets, randomize the order of the training set
x_train, x_test, y_train, y_test = train_test_split(x_tfidf_feat[0:train_size], data['label'][0:train_size], train_size=train_size-1)
x_test = x_tfidf_feat[-test_size:]
y_test = data['label'][-test_size:]

#Training the Model
rf = RandomForestClassifier(n_estimators=450, max_depth=25, n_jobs=-1)
rf_model = rf.fit(x_train, y_train)

#Predictions
y_pred = rf_model.predict(x_test)
returned_statements = []
for i in range(test_size):
    input_text['label'][i] = y_pred[i]
    if y_pred[i] == "statement":
        returned_statements.append(input_text['body_text'][i])

#Results
print("-"*100)
print("Results:")
print(input_text)
print("Returned statements: ", returned_statements)


#---------------------------------------------------------------------------#
# Model Comparison and Grid Search for finding parameters
#---------------------------------------------------------------------------#

# #Preparing the vector for the training/testing
# tfidf_vect = TfidfVectorizer(analyzer=clean_text)
# tfidf_vect_fit = tfidf_vect.fit(x_train['body_text'])
# tfidf_train = tfidf_vect_fit.transform(x_train['body_text'])
# tfidf_test = tfidf_vect_fit.transform(x_test['body_text'])

# #For comparing count vector to tfidf vector
# count_vect = CountVectorizer(analyzer=clean_text)
# x_count = count_vect.fit_transform(data['body_text'])
# x_count_feat = pd.DataFrame(x_count.toarray())


# #Random Forest Classifier
# #Seems to have slightly higher accuracy than GBClassifier
# print("RandomForestClassifier:")
# rf = RandomForestClassifier(n_estimators=450, max_depth=25, n_jobs=-1)
# rf_model = rf.fit(x_train, y_train)
# #Predict for the test set
# y_pred = rf_model.predict(x_test)
# precision, recall, fscore, support = score(y_test, y_pred, pos_label='statement', average='binary')

# #Gradient Boosting Classifier
# print("GradientBoostingClassifier:")
# gb = GradientBoostingClassifier(n_estimators=50, max_depth=25, learning_rate=0.1)
# gb_model = gb.fit(x_train, y_train)
# y_pred = gb_model.predict(x_test)
# precision, recall, fscore, support = score(y_test, y_pred, pos_label='statement', average='binary')

# print('Precision: {} / Recall: {} / Accuracy: {}'.format(round(precision, 3), round(recall, 3), round((y_pred==y_test).sum() / len(y_pred), 3)))


# #Grid Search model tests

# #Random Forest Grid Search
# rf = RandomForestClassifier()
# param_rf = {'n_estimators': [400, 500, 600], 'max_depth': [25]}
# gs = GridSearchCV(rf, param_rf, cv=5, n_jobs=-1)
# gs_fit = gs.fit(x_tfidf_feat, data['label'])
# print(pd.DataFrame(gs_fit.cv_results_).sort_values('mean_test_score', ascending=False)[0:5])

# #Gradient Boosting Grid Search
# gb = GradientBoostingClassifier()
# param_gb = {'n_estimators': [10, 150, 300], 'max_depth': [25], 'learning_rate': [0.05, 0.1, 0.15]}
# gs_gb = GridSearchCV(gb, param_gb, cv=5, n_jobs=-1)
# cv_fit = gs_gb.fit(x_tfidf_feat, data['label'])
# print(pd.DataFrame(cv_fit.cv_results_).sort_values('mean_test_score', ascending=False)[0:5])

