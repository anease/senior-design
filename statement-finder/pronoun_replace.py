# Pronoun Replacement Tool
# Goal: replace all pronouns in a string with their antecedent
# Sample input and output:
# sampleString = "I drive a red Ferrari. It can go very fast."
sampleExpectedOutput = "I drive a red Ferrari. [red Ferrari] can go very fast."

sampleString = "I like going to the zoo. Cheetahs are my favorite animal there! They can run up to 80 miles per hour! What is your favorite animal? Mr. Smith was our guide last time."
sampleString3 = 'Because he lives nearby, I drove John home.'
sampleString4 = 'We completed the job quickly because Ted is our boss and he wanted it done today.'

# Steps:
# 1) preprocess text? (remove punctuation, tokenize)
# 2) search for pronouns (find library of pronouns first)
# 3) Identify dependencies
# 4) Use dependencies to replace pronouns
#
# X) Look into applying methods to atomic clause statement construction

# Dependencies: pip install neuralcoref

import spacy
import neuralcoref

nlp = spacy.load('en_core_web_sm')
# neuralcoref.add_to_pipe(nlp, greedyness=0.5)
# neuralcoref.add_to_pipe(nlp, greedyness=0.6)
neuralcoref.add_to_pipe(nlp, greedyness=0.75)
# neuralcoref.add_to_pipe(nlp, greedyness=1.0)

doc1 = nlp('My sister has a dog. She loves him.')
print(doc1._.coref_clusters)

doc2 = nlp('Angela lives in Boston. She is quite happy in that city.')
for ent in doc2.ents:
    print(ent._.coref_cluster)

print("-"*50)
# print(doc2.ents)

doc3 = nlp(sampleString)
print(doc3)
# print(doc3._.coref_clusters)
print(doc3._.coref_resolved)

for ent in doc3.ents:
    print(ent._.coref_cluster)
