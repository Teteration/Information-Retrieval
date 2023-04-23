import xml.sax

class ReviewHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.docid = 0
        self.body = ""
        self.name = ""
        self.docs = []
        
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

if __name__ == "__main__":
    # create an instance of the handler class
    handler = ReviewHandler()

    # parse the XML file using the handler
    xml.sax.parse("./output2.xml", handler)

    # print the list of docs
    # print(handler.docs)
    # print(len(handler.docs))
    # print(type(handler.docs[5]))
    # print(handler.docs[20]["DocId"])
    # print(handler.docs[20]["Body"])

    # print(handler.docs[5])




    #Tokenization
    docs = handler.docs[20]["Body"]
    translation_table = str.maketrans('\+\-\@\$\#\%\^\&\*0987654321\!\?\)\(\,\;\\.\"\\\/', '                                              ')
    docs = docs.translate(translation_table)

    tokens = docs.lower().split(" ")
    # print(len(tokens),'start')
    tokens = list(set(tokens))
    # print(len(tokens),'after removing duplicate values and special chars')
    
    with open('stopwords.txt', 'r') as f:
        stopwords = [line.rstrip() for line in f.readlines()]
    tokens = [x for x in tokens if x not in stopwords]
    # print(len(tokens),'after removeing \'\' and stop words')
    

    # Lemmatization
    import nltk
    from nltk.stem import WordNetLemmatizer
    from nltk.corpus import wordnet 

    # nltk.download('wordnet')
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word, wordnet.VERB) for word in tokens]

    lemmatized_words = list(set(lemmatized_words))
    # print(lemmatized_words)
    # print(len(lemmatized_words),'after removing duplicate values due to words with the same stem like loving, loved => love ')
    



    ### start making Inverted Index

    # # docs=[{},{}]
    tokens= lemmatized_words
    index={}
    docs = handler.docs

    for m in range(len(tokens)):
        for n in range(len(docs)):
            PostingList={"df":0, "docs":[]}
            if tokens[m] in docs[n]["Body"]:
                PostingList = index[tokens[m]]
                tf = docs[n]["Body"].count(tokens[m])
                PostingList["df"] =+ 1
                PostingList["docs"].append([docs[n]["DocId"],tf])
                index[tokens[m]] = PostingList

