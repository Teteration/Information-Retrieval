import os
import xml.sax
import json
from nltk.corpus import wordnet 
from nltk.stem import WordNetLemmatizer


class ReviewHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.docid = 0
        self.body = ""
        self.name = ""
        self.docs = []

    def startElement(self, name, attrs):
        if name == "DOCNO":
            self.name = ""
        elif name == "DOC":
            self.body = ""
        elif name == "TEXT" or name == "FAVORITE":
            self.body += ""
        
    def endElement(self, name):
        if name == "DOCNO":
            self.name = self.current_data.strip()

        elif name == "TEXT" or name == "FAVORITE":
            self.body = self.body.strip()+self.current_data.strip()
        elif name == "DOC":
            self.docid += 1
            doc = {"DocId": self.docid, "Body": self.body.strip(), "Name": self.name}
            self.docs.append(doc)

    def characters(self, content):
        self.current_data = content.strip()

handler = ReviewHandler()





def Fetch_Docs():
    # make a dictionary with following format => {"DocID": ,"Body": ,"Name": } from XML file.

    # Test
    xml.sax.parse('o.txt', handler)
    docs = handler.docs[3]["Body"]
    # Test



    # Main
    # root_directory = "./wellFormatedXML"
    # for dirpath, dirname,filenames in os.walk(root_directory):
    #     for filename in filenames:
    #         file_path = os.path.join(dirpath, filename)

    #         # parse the XML file using the handler
    #         xml.sax.parse(file_path, handler)

    # docs = ''
    # for i in range(len(handler.docs)):
    #     docs = docs + handler.docs[i]["Body"]
    #Main



    # print(handler.docs)
    # print(handler.docs[5])
    # print(len(handler.docs))
    # print(type(handler.docs[5]))
    # print(handler.docs[20]["DocId"])
    # print(handler.docs[20000]["Body"])



    docs= handler.docs
    # docs is a dictionary with following format => {"DocID": ,"Body": ,"Name": }
    return docs






def Dict2Str(dict):

    # get a dictionary with following format => {"DocID": ,"Body": ,"Name": } and return its "Body" key

    String =''
    for i in range(len(dict)):
        String = String + dict[i]["Body"]

    return String





def Cleaner(string):

    # input = string
    # output = token

    translation_table = str.maketrans('\+\-\=\_\@\$\#\%\^\&\*0987654321\!\?\)\(\,\;\\.\"\\\/',
                                       '                                                  ')
    string = string.translate(translation_table)
    tokens = string.lower().split(" ")
    # print(len(tokens),'start')
    tokens = list(set(tokens))
    # print(len(tokens),'after removing duplicate values and special chars')

    with open('./stopwords.txt', 'r') as f:
        stopwords = [line.rstrip() for line in f.readlines()]
    tokens = [x for x in tokens if x not in stopwords]
    # print(len(tokens),'after removeing \'\' and stop words')

    return tokens






def Lemmatizer(wordList):

    # nltk.download('wordnet')
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word, wordnet.VERB) for word in wordList]
    lemmatized_words = list(set(lemmatized_words))
    # print(lemmatized_words)
    # print(len(lemmatized_words),'after removing duplicate values due to words with the same stem like loving, loved => love ')
    return lemmatized_words






def Tokenizer(text):
    
    return Lemmatizer(Cleaner(text))




def invertedIndex(tokens, docs):

    # input: list and dictionary with following format:
    #    tokens: ['Word1','Word2','Word3', ...]
    #    docs  : {"DocID": ,"Body": ,"Name": }

    # output: dictionary as inverted index with following format:
    #          {
    #           "Word1":{"df": x ,"docs":[DocId ,tf]},
    #           "Word2":{"df": x ,"docs":[DocId ,tf]},
    #           "Word3":{"df": x ,"docs":[DocId ,tf]}
    #           }


    # df === Document Frecuency
    # tf === Term Frecuency

    index={}
    tokens = list(tokens)

    for m in range(len(tokens)):

        PostingList={"df":0, "docs":[]}
        for n in range(len(docs)):

            if tokens[m] in docs[n]["Body"]:

                tf = docs[n]["Body"].count(tokens[m])#مشخص کردن تعداد کلمه در داکیومتت 
                # if tf >= 20:
                    # print(tokens[m]," : ",tf)
                PostingList["docs"].append([docs[n]["DocId"],tf])# اضافه کردن عای دی و تعداد به اتریبیوت داکس هر  کلمه
                PostingList["df"] = PostingList["df"] + 1
                index[tokens[m]] = PostingList

                # index[tokens[m]] = json.dumps(PostingList)
                # final_index = json.dumps(index)

    return index





# To see the process step by step, Run the following lines one by one

# print(Fetch_Docs())
# print(Dict2Str(Fetch_Docs()))
# print(Tokenizer(Dict2Str(Fetch_Docs())))
print(invertedIndex(Tokenizer(Dict2Str(Fetch_Docs())),Fetch_Docs()))
print("\n\nuncomment lines 54-64 and comment lines 47-48 to make index with origin data.\n")
