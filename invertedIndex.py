import os
import json
import math
import xml.sax
import logging
from nltk.corpus import wordnet 
from nltk.stem import WordNetLemmatizer

class ReviewHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.docid = 0
        self.body = ""
        self.name = ""
        # self.docs = []
        self.docs = {}

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
            # doc = {"DocId": self.docid, "Body": self.body.strip(), "Name": self.name}
            doc = {"Body": self.body.strip(), "Name": self.name }
            # self.docs.append(doc)
            self.docs[self.docid]= doc

    def characters(self, content):
        self.current_data = content.strip()

handler = ReviewHandler()





def Fetch_Docs():
    # make a dictionary with following format => {"DocId": {"Body": ,"Name": }} from XML file.

    # Test
    # xml.sax.parse('o.txt', handler)
    # docs = handler.docs
    # Test



    # Main
    root_directory = "./wellFormatedXML"
    for dirpath, dirname,filenames in os.walk(root_directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # parse the XML file using the handler
            xml.sax.parse(file_path, handler)

    # docs = ''
    # for i in range(len(handler.docs)):
    #     docs = docs + handler.docs[i]["Body"]
    docs = handler.docs
    # #Main



    # print(handler.docs)
    # print(handler.docs[5])
    # print(len(handler.docs))
    # print(type(handler.docs[5]))
    # print(handler.docs[20]["DocId"])
    # print(handler.docs[20000]["Body"])



    # docs is a dictionary with following format => {"DocId": {"Body": ,"Name": }}
    return docs






def Dict2Str(dict):

    # get a dictionary with following format => {"DocId": {"Body": ,"Name": }} and return its "Body" key

    String =''
    for i in dict.keys():
        String = String + dict[i]["Body"]

    return String





def Cleaner(string):

    # input = string
    # output = token

    translation_table = str.maketrans('\:\{\}\[\]\+\-\=\_\@\$\#\%\^\&\*0987654321\!\?\)\(\,\;\\.\"\'\\\/',
                                       '                                                             ')
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

    with open('./stopwords.txt', 'r') as f:
        stopwords = [line.rstrip() for line in f.readlines()]
    lemmatized_words = [x for x in lemmatized_words if x not in stopwords]
    # print(lemmatized_words)
    # print(len(lemmatized_words),'after removing duplicate values due to words with the same stem like loving, loved => love ')
    return lemmatized_words






def Tokenizer(text):
    
    return Lemmatizer(Cleaner(text))




def invertedIndex(tokens, docs):


    # input: list and dictionary with following format:
    #                   tokens: ['Word1','Word2','Word3', ...]
    #                   docs  : {"DocID": {"Body": ,"Name": }}

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

        PostingList={"iDF":0, "docs":[]}
        for n in docs.keys():

            if tokens[m] in docs[n]["Body"].lower():
                # w(t,d) instead tf
                tf = docs[n]["Body"].count(tokens[m])
                if tf > 0:
                    wtd = round((1 + math.log(tf)),2)
                else:
                    tf = 0

                PostingList["docs"].append([n,wtd])
                PostingList["iDF"] = PostingList["iDF"] + 1


        Nd = len(docs.keys())
        # Nd ==== number of total documents

        df = PostingList["iDF"]
        # iDF instead DF
        if df != 0:
            PostingList["iDF"] = round(math.log(Nd/df),2)



        index[tokens[m]] = PostingList



                # index[tokens[m]] = json.dumps(PostingList)
                # final_index = json.dumps(index)
    # print(docs.keys())
    return index







def prompt(entry,invertedIndex):
    # output: list of ordered pair with following format
    #         [[DocId,tf], [DocId,tf], [DocId,tf], ...]

    return invertedIndex[entry]["docs"]





def DocId2Text(DocId,docs):

    return docs[DocId]["Body"]





def Score(entry1,Index):
    # input : Query , Index
    # output: sorted list of scores of each document





    entry = Tokenizer(entry1)
    # print('this is entry : ', entry)

    score = {}
    for query_term in entry:    
        try:
        # print('\n',Index[query_term],'\n')

            PostingList = prompt(query_term,Index)
            # print('\nPosting list: ',PostingList,'\n')
            # print(len(PostingList))


            DocId=[]
            for x in PostingList:
                DocId.append(x[0])
            # print('DocId',DocId,'\n')


            tf_idf = []
            for x in PostingList:
                tf = x[1]
                iDF = Index[query_term]["iDF"]
                tf_idf.append(round((tf*iDF),2))
            # print('tf_idf: ',tf_idf,'\n\n')



            # make score with DocId and tf_idf => {'DocId': tf_idf, 'DocId': tf_idf} => e.g. {'1': 3.5 ,'7': 13.9}
            for key in DocId:
                for value in tf_idf:
                    if str(key) in score.keys():
                        score[str(key)] += value
                        score[str(key)] = round(score[str(key)],2)
                    else:
                        score[str(key)] = value
                        score[str(key)] = round(score[str(key)],2)
                    tf_idf.remove(value)
                    break
            # print('\n',score)





    #for each term in docs:
    #   score = calc tf_idf for each docs: ( relevency of doc / query )
    #sort docs based on score
    #return top k



    #for each query_term in doc:
    #   score = calc tf_idf of each query_term for each docs: ( relevency of doc / query )
    #   score_d = sum of tf_idf for each query_term in d
    #   امتیاز سند = مجموع بردار وزن دار کلمات مشترک با کوئری
    #   یعنی با این روش یک سری سند هست که شامل بیشترین تعداد کويری ترم هست هچنین سند های دیگری با این شرایط کم هست تا اسنادی که امتیازشون صفره
    #   یعنی هیچ کلمه مشترکی ندارن

    #   حالا لول بعدی اینکه که سمنتیک هم لحاظ کنیم

        except BaseException:
            # logging.exception("*Error goes here*")
            print("Not Exist!\n")

    print('\n',score,'\n\n')

    # Sort Ascending
    sorted_score = {k: v for k, v in sorted(score.items(), key=lambda item: item[1],reverse=True)}
    # sorted_score = {k: v for k, v in sorted(score.items(), key=lambda item: item[1])}
    # print(sorted_score,'\n\n')




    return sorted_score








def Top_K_doc(k,doc_scores):
    # input : k and document score with following format ====> SCORE = {'DocId1': score1, 'DocId2': score2, ...}
    # output: top K element of SCORE based on value
    return {n: doc_scores[n] for n in list(doc_scores)[:k]}






def Evaluation(top_K_docid,docs,entry1):



    ############## Pseudo Code ###############
    # System Evaluation : Average Percision and Mean Average Percision
    # for each query return R@k/P@k than Average Percision and finally for all query return MAP
    #
    # 1- Document Score : {'DocId': score , ... } => {'43':3.6, '982':7.21, ... }
    # 2- Evaluation Set : {'Query': [DocId1,DocId2 , ... } => {'fileName': [DocIds in file], ... }
    # 3- for doc in top-K:
    #       calc R@k/P@k:{        
    #       }
    #      
    # check if Docid in dict['filename']




    # print final doc and result( R@k/P@k => AP => MAP)
    #    docs  : {"DocID": {"Body": ,"Name": }}

    Precision = 0
    relevency=[]
    # it is binery representaion of relevency => 0 : Not relevent,
    #                                            1 : relevent

    for Docid in top_K_docid:
        print(DocId2Text(int(Docid),docs),'\n')

        # [5:] => convert 2007_carName to carName
        fileName = docs[int(Docid)]["Name"][5:]
        
        if fileName == entry1:
            relevency.append(1)
        else:
            relevency.append(0)
            print(entry1 ,'!=',fileName)
        
        print('Precision:',Precision_K(relevency))
        Precision += Precision_K(relevency)

        try:
            print('Recall: ',Recall_K(relevency,VSet,entry1),'\n\n\n')
        except:
            print('Please Enter A Valid Query(file name)')


    try:
        total_doc = len(top_K_docid)
        Average_Precision = Precision / total_doc
        print('Average Precision: ', Average_Precision)
    except:
        print('No Match!')
    # print('relevency: ',relevency)
    # print('validation set : ',ValidationSet(docs))
    # print('Recall: ',Recall_K(relevency,VSet,entry1))

    Recall = Recall_K(relevency,VSet,entry1)


    return [Average_Precision, Recall]




###################### System Evaluation Functions #####################


# it shoud read docs from file or DB
def ValidationSet(docs):
    # input  =>  {"DocID": {"Body": ,"Name": }}
    # output =>  {'fileName1': [DocId1, DocId2, DocId3], 'fileName2': [DocId4, DocId5, DocId6]}

    ValidationSet = {}
    for DocId in docs.keys():
        fileName = docs[DocId]["Name"][5:]

        if fileName in ValidationSet.keys():
            ValidationSet[fileName].append(DocId)
        else:
            ValidationSet[fileName] = [DocId]


    return ValidationSet







def Recall_K(relevency_list, validation_set,entry):
    # tp : True Positive
    relevent = relevency_list.count(1)
    # تعداد کل داکیومنت هایی که نام فایلشان با کوعری برابر است
    total_relevent = len(validation_set[entry])
    Recall = relevent / total_relevent

    return Recall






def Precision_K(relevency_list):
    # tp : True Positive
    tp = relevency_list.count(1)
    total = len(relevency_list)
    precision = tp / total

    return precision










# To see the process step by step, Run the following lines one by one

docs=Fetch_Docs()
# print(docs)
# print(Dict2Str(Fetch_Docs()))
# print(Tokenizer(Dict2Str(docs)))
# print(invertedIndex(Tokenizer(Dict2Str(docs)),docs))

# print("\n\nuncomment lines 58-68 and comment lines 51-52 to make index with origin data.\n")







Index = invertedIndex(Tokenizer(Dict2Str(docs)),docs)
VSet = ValidationSet(docs)
# print(Index.keys())


# while True:
#     entry1 = input("Entry : ")

#     sorted_score = Score(entry1, Index)

#     # return top 5
#     first5pairs = Top_K_doc(5,sorted_score)
#     top_K_docid = list(first5pairs.keys())
#     Evaluation(top_K_docid, docs)






# print(list(VSet.keys()))








Mean_Average_precision = 0
Recall = 0
for filename in list(VSet.keys()):

    sorted_score = Score(filename, Index)

    # return top 5
    first5pairs = Top_K_doc(5,sorted_score)
    top_K_docid = list(first5pairs.keys())
    Mean_Average_precision += Evaluation(top_K_docid, docs,filename)[0]
    Recall += Evaluation(top_K_docid, docs,filename)[1]
    # print('aadsf is :',Mean_Average_precision)



total_query = len(list(VSet.keys()))
print(total_query)
print('Mean_Average_precision: ', Mean_Average_precision / total_query )
print('Average_Recall: ', Recall / total_query )