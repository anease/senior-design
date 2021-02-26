# Pronoun Replacement Tool
# Goal: replace all pronouns in a string with their antecedent
# Sample input and output:
# sampleString = "I drive a red Ferrari. It can go very fast."
# sampleExpectedOutput = "I drive a red Ferrari. [red Ferrari] can go very fast."

# Steps:
# 1) preprocess text? (remove punctuation, tokenize)
# 2) search for pronouns (find library of pronouns first)
# 3) Identify dependencies
# 4) Use dependencies to replace pronouns
#
# X) Look into applying methods to atomic clause statement construction

# Dependencies: pip install neuralcoref

#########################################################################
# Pronoun Replacement Function                                          #
#########################################################################
import spacy
import neuralcoref

nlp = spacy.load('en_core_web_sm')
neuralcoref.add_to_pipe(nlp, greedyness=0.48)

def replace_pronouns(text):
    doc = nlp(text)
    return doc._.coref_resolved

#########################################################################
# Testing Module                                                        #
#########################################################################
# Test 1: Intersentence and Intrasentence Coreferences
testString1 = "Sarah is my sister. She likes cats. Jon is my brother. He has two dogs named Spot and Charlie. Charlie is a pitbull and he is brown. Spot is a terrier and he barks loudly."
print(testString1)
print(replace_pronouns(testString1))

# Test 2: Chained Intersentence Coreferences
testString2 = "I like going to the zoo. Cheetahs are my favorite animal there! They can run up to 80 miles per hour! What is your favorite animal? Mr. Smith was our guide last time."
print(testString2)
print(replace_pronouns(testString2))

# Test 3: Cataphor Coreference
testString3 = "Because he lives nearby, I drove John home."
print(testString3)
print(replace_pronouns(testString3))

# Test 4: Anataphor Coreference
testString4 = "I drove John home because he lives nearby."
print(testString4)
print(replace_pronouns(testString4))

# Test 5: Multiple Independent Coreferences
testString5 = "We completed the job quickly because Ted is our boss and he wanted it done today."
print(testString5)
print(replace_pronouns(testString5))

# Test 6: Unclear Coreference
testString6 = "Jack and Jill raced down a hill. He fell down so she won."
print(testString6)
print(replace_pronouns(testString6))

# Test 7: Unclear Coreference Modified
testString7 = "Jack and Jill raced down a hill. She fell down so he won."
print(testString7)
print(replace_pronouns(testString7))

#########################################################################
# Notes and Experimentation Section                                     #
#########################################################################

# Neuralcoref module: uncomment next 31 lines to work with this again
# import spacy
# import neuralcoref

# nlp = spacy.load('en_core_web_sm')
# # neuralcoref.add_to_pipe(nlp, greedyness=0.25)
# neuralcoref.add_to_pipe(nlp, greedyness=0.5)
# # neuralcoref.add_to_pipe(nlp, greedyness=0.6)
# # neuralcoref.add_to_pipe(nlp, greedyness=0.75)
# # neuralcoref.add_to_pipe(nlp, greedyness=1.0)

# doc1 = nlp('My sister has a dog. She loves him.')
# print(doc1._.coref_clusters)

# doc2 = nlp('Angela lives in Boston. She is quite happy in that city.')
# for ent in doc2.ents:
#     print(ent._.coref_cluster)

# print("-"*50)
# # print(doc2.ents)

# doc3 = nlp(sampleString2)
# print(doc3) #Shows input string
# print("doc3.ents: ", doc3.ents)
# print(doc3._.coref_clusters)
# # print(doc3._.coref_clusters.mentions) #Fails
# print(doc3._.coref_resolved)

# # for ent in doc3.ents: #Runs through twice for some reason
# #     print(ent)
# #     print(ent._.coref_cluster)
#     # print(ent._.coref_resolved)
#     # print(ent._.coref_cluster.mentions)


##########################################################################
# Potential solution: look into setting the converstion dictionary
#   Issue: How to set conversion dictionary for an unknown dataset?
#   -Look into existing conversion dictionaries
##########################################################################

#Spacy module: uncomment next 20 lines to use
# import nltk, spacy
# from nltk.corpus import treebank
# from spacy import displacy

# # tree = treebank.parsed_sents(sampleString)[0]
# # tree.draw()

# nlp = spacy.load('en_core_web_sm')

# print(sampleString)

# sampleDoc = nlp(sampleString)

# #Find pronouns from text
# pronouns = [token.text for token in sampleDoc if token.tag_ == "PRP"]
# print(pronouns)

# for token in sampleDoc:
#     print(token.text, token.tag_, token.head.text, token.dep_)

# # displacy.serve(sampleDoc, style='dep')
