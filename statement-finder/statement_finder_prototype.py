
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

def remove_punct(text):
    text = "".join([word.lower() for word in text if word not in string.punctuation])
    return text

def tokenize(text):
    tokens = re.findall('\w+', text)
    return tokens

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

#---------------------------------------------------------------------------#
# Pronoun Replacement Tool
#---------------------------------------------------------------------------#

import spacy
import neuralcoref

nlp = spacy.load('en_core_web_sm')
neuralcoref.add_to_pipe(nlp, greedyness=0.48)

def replace_pronouns(text):
    doc = nlp(text)
    return doc._.coref_resolved

#---------------------------------------------------------------------------#
# Atomic Statement Finder
#---------------------------------------------------------------------------#
# Input: Text with pronouns replaced
# Output: List of atomic statements
# Process: 
#   -Split into sentences (or perform upon individual sentences in a loop)
#       -Find POS tags for words
#       -Determine statement parts from within sentence
#       -Arrange statement(s)
#           -If needed, retrieve quantifiers
#       -Add statement(s) to return array
#           -If needed, an index of the statements' original sentences could be added here
#   -Return array of statements

# import spacy #import added above for pronoun replacement
import textacy #pip install required
# import nltk
# import pandas as pd
from spacy import displacy

def atomic_find_statements(text):
    nlp = spacy.load("en_core_web_sm")
    statements = []
    resolved_text = replace_pronouns(text)
    sentences = pd.DataFrame(nltk.sent_tokenize(text))
    sentences.columns = ['input_sentence']
    sentences['semi_clean_sentence'] = [remove_punct(text) for text in sentences['input_sentence']]
    sentences['resolved_sentence'] = pd.DataFrame(nltk.sent_tokenize(resolved_text))
    sentences['clean_resolved_sentence'] = [remove_punct(text) for text in sentences['resolved_sentence']]
    
    # sentences['tokens'] = [tokenize(remove_punct(text)) for text in sentences['input_sentence']]
    # sentences['cleaned_tokens'] = [clean_text(text) for text in sentences['input_sentence']]
    # sentences['cleaned_sentence'] = [" ".join(word) for word in sentences['cleaned_tokens']]
    # print(sentences.head())
    
    # #Block for visualizing dependencies for datasets
    # data = pd.read_csv('dataset-nonstatements.txt', sep='|')
    # data.columns = ['label', 'body_text']
    # for sentence in data['body_text']:
    #     doc = nlp(sentence)
    #     displacy.serve(doc, style='dep')


    for sentence in sentences['clean_resolved_sentence']:
    # for sentence in sentences['semi_clean_sentence']:
        doc = nlp(sentence)
        aux_words, adj_words, nouns, verbs = [], [], [], []

        #Store noun chunks
        for chunk in doc.noun_chunks:
            nouns.append(chunk.text)
        #Store verb phrases
        verb_pattern = [{"POS": "VERB", "OP": "*"},{"POS": "ADV", "OP": "*"},{"POS": "VERB", "OP": "+"},{"POS": "PART", "OP": "*"}]
        sentenceDoc = textacy.make_spacy_doc(sentence, lang='en_core_web_sm')
        verb_phrases = textacy.extract.matches(sentenceDoc, verb_pattern)
        for chunk in verb_phrases:
            verbs.append(chunk.text)
        #Store auxiliary words and adjectives
        for word in doc:
            print("Word: {}, Word tag: {}, Dependency: {}".format(word, word.tag_, word.dep_))
            if word.tag_ == "VBP":
                aux_words.append(word.text)
            elif word.tag_ == "JJ" or word.tag_ == "RB":
                adj_words.append(word.text)
            elif (word.tag_ == "VBZ" or word.tag_ == "VBP") and len(verbs) == 0:
                verbs.append(word.text)
        
        #Print things, delete after development complete
        # print("-"*75)
        # print(sentence)
        # print("Noun Chunks: ", len(nouns), "; ", nouns)
        # print("Auxilary words: ", len(aux_words), "; ", aux_words)
        # print("Adjective words: ", len(adj_words), "; ", adj_words)
        # print("Verb Phrases: ", len(verbs), "; ", verbs)
        # print("-"*75)

        # displacy.serve(doc, style='dep')

        if doc[0].dep_ != "ROOT" and doc[-1].dep_ != "ROOT":
            if len(nouns) == 2 and len(verbs) > 0:
                # if len(verbs) > 0:
                    # statements.append(nouns[0] + " " + aux_words[0] + " " + verbs[0] + " " + nouns[1])
                statements.append(nouns[0] + " " + verbs[0] + " " + nouns[1])
                # else:
                #     statements.append(nouns[0] + " " + aux_words[0] + " " + nouns[1])
            if len(nouns) == 1 and len(adj_words) > 0 and len(aux_words) > 0:
                statement = nouns[0] + " " + aux_words[0] + " " + adj_words[0]
                statements.append(statement)
    
    # print("#"*100)
    
    print(statements)
    return statements

# # Block for testing tool on dataset sentences
# data = pd.read_csv('dataset-nonstatements.txt', sep='|')
# data.columns = ['label', 'body_text']
# for sentence in data['body_text'][0:10]:
#     print("Original sentence: {}".format(sentence))
#     print("Statements: {}".format(atomic_find_statements(sentence)))
#     print("#"*100)

# print(spacy.explain("MD"))
print(spacy.explain("RB"))

#---------------------------------------------------------------------------#
# Testing Block for Atomic Statement Finder
#---------------------------------------------------------------------------#

# # Test 1: [noun] is [adjective]
# test1 = "Granny Smith apples are green. Do you like Granny Smith apples?"
# output1 = ["granny smith apples are green"]
# if atomic_find_statements(test1) == output1:
#     print("Test 1 successful")
# else:
#     print("Test 1 failed")

# # Test 2: Questions, commands, and exclamations
# test2 = "Good morning! Who might you be? Sit up straight!"
# output2 = []
# if atomic_find_statements(test2) == output2:
#     print("Test 2 successful")
# else:
#     print("Test 2 failed")

# # Test 3: [noun] has [object]
# test3 = "Timmy owns 3 different cars. His Honda Civic has good gas mileage."
# output3 = ["timmy owns 3 different cars", "timmy honda civic has good gas mileage"]
# if atomic_find_statements(test3) == output3:
#     print("Test 3 successful")
# else:
#     print("Test 3 failed")

# Test 4: [subject] does [action] | [subject] causes [action]
test4 = "Cheetahs run very fast. They run fast because of evolution."
output4 = ["cheetahs run very fast", "Cheetahs run fast because of evolution"]
if atomic_find_statements(test4) == output4:
    print("Test 4 successful")
else:
    print("Test 4 failed")

# # Test 5: Opinions
# test5 = "I like pizza. Pepperoni is my favorite pizza topping."
# output5 = []
# if atomic_find_statements(test5) == output5:
#     print("Test 5 successful")
# else:
#     print("Test 5 failed")

#---------------------------------------------------------------------------#
# Testing Block
#---------------------------------------------------------------------------#
# # Test 1: Test expected normal input
# test1_in = "I like going to the zoo. Cheetahs are my favorite animal there! They can run up to 80 miles per hour! What is your favorite animal? Mr. Smith was our guide last time."
# test1_out = find_statements(test1_in)
# test1_expected_out = ["They can run up to 80 miles per hour!", "Mr. Smith was our guide last time."]
# if test1_out == test1_expected_out:
#     print("Test 1: Pass")
# else:
#     print("Test 1: Fail")
#     print(test1_out)
#     print(test1_expected_out)
# # Test 2: Test opinions
# test2_in = "I like ice cream. My favorite pizza topping is pepperoni!"
# test2_out = find_statements(test2_in)
# test2_expected_out = []
# if test2_out == test2_expected_out:
#     print("Test 2: Pass")
# else:
#     print("Test 2: Fail")
#     print(test2_out)
#     print(test2_expected_out)
# # Test 3: Test questions
# test3_in = "Who are you? Why can cheetahs run so fast? Is Columbus the capital of Ohio?"
# test3_out = find_statements(test3_in)
# test3_expected_out = []
# if test3_out == test3_expected_out:
#     print("Test 3: Pass")
# else:
#     print("Test 3: Fail")
#     print(test3_out)
#     print(test3_expected_out)
# # Test 4: Test commands
# test4_in = "Drive! Shine your shoes. Tell me what time it is."
# test4_out = find_statements(test4_in)
# test4_expected_out = []
# if test4_out == test4_expected_out:
#     print("Test 4: Pass")
# else:
#     print("Test 4: Fail")
#     print(test4_out)
#     print(test4_expected_out)
# # Test 5: Test salutations
# test5_in = "Good morning! See you later. Goodbye."
# test5_out = find_statements(test5_in)
# test5_expected_out = []
# if test5_out == test5_expected_out:
#     print("Test 5: Pass")
# else:
#     print("Test 5: Fail")
#     print(test5_out)
#     print(test5_expected_out)

