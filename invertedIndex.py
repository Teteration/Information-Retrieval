import xml.sax
import os

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

if __name__ == "__main__":
    # create an instance of the handler class
    handler = ReviewHandler()

    # parse the XML file using the handler

    root_directory = "./wellFormatedXML"
    # fileList=[]
    # Loop through all directories and subdirectories
    for dirpath, dirnames, filenames in os.walk(root_directory):
        # Loop through all files in the current directory
        for filename in filenames:
            # Do something with the file
            file_path = os.path.join(dirpath, filename)
            # fileList.append(file_path)

            # print(filenames)
            # print(file_path)
    # print(fileList)
            xml.sax.parse(file_path, handler)
            # final = handler.docs


    # print the list of docs
    # print(handler.docs)
    print(len(handler.docs))
    # print(type(handler.docs[5]))
    # print(handler.docs[20]["DocId"])
    # print(handler.docs[20000]["Body"])
    # print(handler.docs[5])




    #Tokenization
    docs = handler.docs[20]["Body"]
    for i in range(len(handler.docs)):
        docs = docs + handler.docs[i]["Body"]


    print(len(docs))
    translation_table = str.maketrans('\+\-\@\$\#\%\^\&\*0987654321\!\?\)\(\,\;\\.\"\\\/', '                                              ')
    docs = docs.translate(translation_table)
    tokens = docs.lower().split(" ")
    # print(len(tokens),'start')
    tokens = list(set(tokens))
    # print(len(tokens),'after removing duplicate values and special chars')
    
    with open('./stopwords.txt', 'r') as f:
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

    tokens= lemmatized_words
    # print(tokens)
    # tokens= ['strong', 'edmunds', 'price']
    # tokens=['price','car','money']

    index={}
    docs = handler.docs
    # print(docs)

    # with open('./tes.txt', 'w') as f:
    #     f.write(str(docs))

    # print(str(docs).count("price"))
    # print(len(docs))

    # print(len(tokens))
    # print(tokens[1])

    # df === Document Frecuency
    # tf === Term Frecuency


    for m in range(len(tokens)):
        PostingList={"df":0, "docs":[]}
        for n in range(len(docs)):

            if tokens[m] in docs[n]["Body"]:

                tf = docs[n]["Body"].count(tokens[m])#مشخص کردن تعداد کلمه در داکیومتت 
                PostingList["docs"].append([docs[n]["DocId"],tf])# اضافه کردن عای دی و تعداد به اتریبیوت داکس هر  کلمه
                PostingList["df"] = PostingList["df"] + 1
                index[tokens[m]] = PostingList
                # print(PostingList)


    
    # print(index)
    print(len(index))

