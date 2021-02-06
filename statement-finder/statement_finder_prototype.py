
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

# Dependencies:
# pip install: nltk, pandas, sklearn
# nltk.download('wordnet')
# nltk.download('punkt')
# nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english') #Read in stopwords for easy access later
wn = nltk.WordNetLemmatizer() #Instantiate lemmatizer

def clean_text(text): #Method for cleaning text in preparation for vectorizing
    text = "".join([word.lower() for word in text if word not in string.punctuation])
    tokens = re.findall('\w+', text)
    text = [wn.lemmatize(word) for word in tokens if word not in stopwords] #lemmatize and remove stopwords
    # text = [wn.lemmatize(word) for word in tokens] #lemmatize
    # text = [word for word in tokens if word not in stopwords] #remove stopwords
    # text = [word for word in tokens] #no lemmatize and no removing stopwords
    return text

def find_statements(in_text):
    #Process input_text from webpage parser
    input_text = pd.DataFrame(nltk.sent_tokenize(in_text))
    input_text.columns = ['body_text']
    input_text['label'] = ['undecided' for i in range(input_text.size)]
    test_size = input_text.size // 2

    #Read in training data from dataset file
    # data = pd.read_csv('dataset.txt', sep='|')
    data = pd.read_csv('dataset-binary.txt', sep='|')
    data.columns = ['label', 'body_text']
    train_size = data.size // 2
    data = data.append(input_text, ignore_index=True) #Add the input text to the training data

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

    return returned_statements

# print("Calling function:")
# print(find_statements(sampleText))


#---------------------------------------------------------------------------#
# Testing Block
#---------------------------------------------------------------------------#
# Test 1: Test expected normal input
test1_in = "I like going to the zoo. Cheetahs are my favorite animal there! They can run up to 80 miles per hour! What is your favorite animal? Mr. Smith was our guide last time."
test1_out = find_statements(test1_in)
test1_expected_out = ["They can run up to 80 miles per hour!", "Mr. Smith was our guide last time."]
if test1_out == test1_expected_out:
    print("Test 1: Pass")
else:
    print("Test 1: Fail")
    print(test1_out)
    print(test1_expected_out)
# Test 2: Test opinions
test2_in = "I like ice cream. My favorite pizza topping is pepperoni!"
test2_out = find_statements(test2_in)
test2_expected_out = []
if test2_out == test2_expected_out:
    print("Test 2: Pass")
else:
    print("Test 2: Fail")
    print(test2_out)
    print(test2_expected_out)
# Test 3: Test questions
test3_in = "Who are you? Why can cheetahs run so fast? Is Columbus the capital of Ohio?"
test3_out = find_statements(test3_in)
test3_expected_out = []
if test3_out == test3_expected_out:
    print("Test 3: Pass")
else:
    print("Test 3: Fail")
    print(test3_out)
    print(test3_expected_out)
# Test 4: Test commands
test4_in = "Drive! Shine your shoes. Tell me what time it is."
test4_out = find_statements(test4_in)
test4_expected_out = []
if test4_out == test4_expected_out:
    print("Test 4: Pass")
else:
    print("Test 4: Fail")
    print(test4_out)
    print(test4_expected_out)
# Test 5: Test salutations
test5_in = "Good morning! See you later. Goodbye."
test5_out = find_statements(test5_in)
test5_expected_out = []
if test5_out == test5_expected_out:
    print("Test 5: Pass")
else:
    print("Test 5: Fail")
    print(test5_out)
    print(test5_expected_out)

#---------------------------------------------------------------------------#
# Model Comparison and Grid Search for finding optimal parameters
#---------------------------------------------------------------------------#

# import nltk
# import pandas as pd
# import re
# from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
# import string
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import GridSearchCV

# stopwords = nltk.corpus.stopwords.words('english')
# ps = nltk.PorterStemmer()

# # data = pd.read_csv("SMSSpamCollection.tsv", sep='\t')
# data = pd.read_csv('dataset-binary.txt', sep='|')
# data.columns = ['label', 'body_text']

# def count_punct(text):
#     count = sum([1 for char in text if char in string.punctuation])
#     return round(count/(len(text) - text.count(" ")), 3)*100

# data['body_len'] = data['body_text'].apply(lambda x: len(x) - x.count(" "))
# data['punct%'] = data['body_text'].apply(lambda x: count_punct(x))

# def clean_text(text):
#     text = "".join([word.lower() for word in text if word not in string.punctuation])
#     tokens = re.split('\W+', text)
#     text = [ps.stem(word) for word in tokens if word not in stopwords]
#     return text

# # TF-IDF
# tfidf_vect = TfidfVectorizer(analyzer=clean_text)
# X_tfidf = tfidf_vect.fit_transform(data['body_text'])
# X_tfidf_feat = pd.concat([data['body_len'], data['punct%'], pd.DataFrame(X_tfidf.toarray())], axis=1)

# # CountVectorizer
# count_vect = CountVectorizer(analyzer=clean_text)
# X_count = count_vect.fit_transform(data['body_text'])
# X_count_feat = pd.concat([data['body_len'], data['punct%'], pd.DataFrame(X_count.toarray())], axis=1)

# X_count_feat.head()

# #Tfidf grid search
# rf = RandomForestClassifier()
# param = {'n_estimators': [10, 150, 300], 'max_depth': [30, 60, 90, None]}

# gs = GridSearchCV(rf, param, cv=5, n_jobs=-1)
# gs_fit = gs.fit(X_tfidf_feat, data['label'])
# print(pd.DataFrame(gs_fit.cv_results_).sort_values('mean_test_score', ascending=False)[0:5])

# #Count grid search
# rf = RandomForestClassifier()
# param = {'n_estimators': [10, 150, 300], 'max_depth': [30, 60, 90, None]}

# gs = GridSearchCV(rf, param, cv=5, n_jobs=-1)
# gs_fit = gs.fit(X_count_feat, data['label'])
# print(pd.DataFrame(gs_fit.cv_results_).sort_values('mean_test_score', ascending=False)[0:5])








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


