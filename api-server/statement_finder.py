### Statement Finder Tool
## Description: This tool takes text as input, replcaes pronouns with their antecedents, and returns statements that meet dependency relationship criteria.


import nltk, string, spacy, neuralcoref, re
import pandas as pd #Not necessary for final version

#---------------------------------------------------------------------------#
# Pronoun Replacement Tool
#---------------------------------------------------------------------------#

#Daniel's Code
#nlp = spacy.load('en_core_web_sm')

#Changed import structure to work on Andrew's machine
import en_core_web_sm
nlp = en_core_web_sm.load()

neuralcoref.add_to_pipe(nlp, greedyness=0.48)

#input: a body of text potentially spanning multiple sentences
#output: the input body with pronouns replaced by their antecedents
def replace_pronouns(text):
    doc = nlp(text)
    return doc._.coref_resolved

#---------------------------------------------------------------------------#
# Atomic Statement Finder
#---------------------------------------------------------------------------#

#input: sentence with (potentially) punctuation and and capital letters
#output: sentence with punctuation removed and all letters converted to lowercase
def remove_punct(text):
    text = "".join([word.lower() for word in text if word not in string.punctuation])
    return text

#input: uncleaned sentence
#output: list of cleaned sentence/sentences split on conjunctions
def split_clauses(text):
    nlp = spacy.load("en_core_web_sm")
    text = remove_punct(text)
    doc = nlp(text)
    clauses = []
    clause = []
    for token in doc:
        if token.pos_ != "CCONJ":
            clause.append(token.text)
        else:
            clauses.append(" ".join(clause))
            clause = []
    clauses.append(" ".join(clause))
    return clauses

#input: token and document to check for dependencies on the token
#output: list of tokens from doc that depend on the input token
def get_dependencies(token, doc):
    deps = []
    for tok in doc:
        if tok.head == token:
            deps.append(tok)
    return deps

#input: non-root token and doc
#output: chunk containing all tokens recursively dependent on the input token
def get_chunk(token, doc):
    chunk = [token]
    i = 0
    dep = get_dependencies(chunk[i], doc)
    while(len(dep) > 0):
        for word in dep:
            chunk.append(word)
        i = i + 1
        dep = get_dependencies(chunk[i], doc)
    return chunk
        
#input: unordered chunk and doc with ordered sentence
#output: ordered chunk
def order_chunk(chunk, doc):
    new_chunk = []
    for token in doc:
        for word in chunk:
            if token == word:
                new_chunk.append(token)
    return new_chunk

#input: uncleaned text of one or more sentences
#output: list of atomic statements from input sentences
def atomic_find_statements(text):
    nlp = spacy.load("en_core_web_sm")
    statements = []
    resolved_text = replace_pronouns(text)
    sentences = nltk.sent_tokenize(resolved_text)
    clauses = []
    for sent in sentences: #split sentences into clauses
        if sent[-1] != "?": #filter out sentences ending with a ?
            for clause in split_clauses(sent):
                clauses.append(clause)
    for sentence in clauses: #search for statements within each clause
        chunks = []
        root = ""
        tags = ""
        doc = nlp(sentence)
        for token in doc: #find and store the root word in the clause
            # print("Word: {}, Word tag: {}, Dependency: {}, Depends on: {}".format(token.text, token.pos_, token.dep_, token.head.text))
            if token.dep_ == "ROOT":
                root = token
        # print("First word: {}, Tag: {}, Dependency: {}, Depends on: {}".format(doc[0].text, doc[0].pos_, doc[0].dep_, doc[0].head.text))
        # # print("First word: {}, Tag: {}, Dependency: {}, Depends on: {}".format(doc[1].text, doc[1].pos_, doc[1].dep_, doc[1].head.text))
        # print("Last word: {}, Tag: {}, Dependency: {}, Depends on: {}".format(doc[-1].text, doc[-1].pos_, doc[-1].dep_, doc[-1].head.text))
        # print("Root word: {}, Tag: {}, Dependency: {}, Depends on: {}".format(root.text, root.pos_, root.dep_, root.head.text))
        chunks = get_dependencies(root, doc) #get words that depend on the root word (includes root)
        ordered_chunks = []
        for word in chunks: #get chunks from clauses
            tags = tags + " " + word.dep_
            if word.dep_ == "ROOT":
                chunk = [word]
                ordered_chunks.append(chunk)
            else:
                chunk = get_chunk(word, doc)
                ordered_chunks.append(order_chunk(chunk, doc))
            # print("Word: {} || Dependency: {} || Chunk: {}".format(word, word.dep_, chunk))
            # print("Ordered chunk: {}".format(order_chunk(chunk, doc)))
        statement = ""
        for chunk in ordered_chunks:
            for word in chunk:
                statement = statement + " " + word.text
        statement = statement[1:]
        
        # print("Sentence: {}".format(sentence))
        # print("Tags: {}".format(tags))
        r1 = re.compile(".*nsubj\s(\w+\s)*ROOT\s(\w+\s)*(dobj)*(advmod)*(acomp)*(attr)*(prep)*(ccomp)*")
        r2 = re.compile(".*npadvmod\s(\w+\s)*ROOT\s(\w+\s)*(dobj)*(advmod)*(acomp)*(attr)*(prep)*(ccomp)*")
        r3 = re.compile(".*nsubjpass\s(\w+\s)*ROOT\s(\w+\s)*(dobj)*(advmod)*(acomp)*(attr)*(prep)*(ccomp)*")
        r4 = re.compile(".*expl\s(\w+\s)*ROOT\s(\w+\s)*(dobj)*(advmod)*(acomp)*(attr)*(prep)*(ccomp)*")

        #Return statements if they meet the structure of a statement
        if chunks[0].dep_ != "aux" and chunks[0].dep_ != "advmod":
            if "like" not in statement and "favorite" not in statement: #poor attempt at removing opinions, will also remove statements that contain those words
                if len(list(filter(r1.match, [tags]))) > 0:
                    statements.append(statement)
                elif len(list(filter(r2.match, [tags]))) > 0:
                    statements.append(statement)
                elif len(list(filter(r3.match, [tags]))) > 0:
                    statements.append(statement)
                elif len(list(filter(r4.match, [tags]))) > 0:
                    statements.append(statement)
    return statements

#---------------------------------------------------------------------------#
# Testing Block for Atomic Statement Finder
#---------------------------------------------------------------------------#

#input: none
#output: results of running the tests on the data
def run_tests():
    # Test 1: [noun] is [adjective]
    test1 = "Granny Smith apples are green. Do you like Granny Smith apples?"
    output1 = ["granny smith apples are green"]
    if atomic_find_statements(test1) == output1:
        print("Test 1 successful")
    else:
        print("Test 1 failed")

    # Test 2: Questions, commands, and exclamations
    test2 = "Good morning! Who might you be? Sit up straight!"
    output2 = []
    if atomic_find_statements(test2) == output2:
        print("Test 2 successful")
    else:
        print("Test 2 failed")

    # Test 3: [noun] has [object]
    test3 = "Timmy owns 3 different cars. His Honda Civic has good gas mileage."
    output3 = ["timmy owns 3 different cars", "timmy honda civic has good gas mileage"]
    if atomic_find_statements(test3) == output3:
        print("Test 3 successful")
    else:
        print("Test 3 failed")

    # Test 4: [subject] does [action] | [subject] causes [action]
    test4 = "Cheetahs run very fast. They run fast because of evolution."
    output4 = ["cheetahs run very fast", "cheetahs run fast because of evolution"]
    if atomic_find_statements(test4) == output4:
        print("Test 4 successful")
    else:
        print("Test 4 failed")

    # Test 5: Opinions
    test5 = "I like pizza. Pepperoni is my favorite pizza topping."
    output5 = []
    if atomic_find_statements(test5) == output5:
        print("Test 5 successful")
    else:
        print("Test 5 failed")
    return

run_tests()



