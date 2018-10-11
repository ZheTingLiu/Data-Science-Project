# -*- coding: utf-8 -*- 
import sys
import re
import time
import jieba
import logging
import numpy as np
import crawl
import collections
from io import open
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM,CuDNNLSTM,Bidirectional
from keras.utils import np_utils
from gensim.models import word2vec
import keras.preprocessing.text as T
from sklearn.cross_validation import train_test_split
from sklearn.metrics import precision_score,recall_score,f1_score
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from keras.callbacks import ModelCheckpoint

#manage memory 
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.15
set_session(tf.Session(config=config))

def creat_model():
    model = Sequential()
    model.add(Dense(256, input_shape=(23,250)))
    model.add(Bidirectional(CuDNNLSTM(256)))
    model.add(Dense(2, activation='softmax'))

    return model

def train():
    f = open('train_comment.txt','r',encoding='utf-8')
    jieba.set_dictionary('jieba/extra_dict/dict.txt.big')
    stopword_set = set()
    with open('jieba/extra_dict/stop_words.txt','r', encoding='utf-8') as stopwords:
        for stopword in stopwords:
            stopword_set.add(stopword.strip('\n'))
    rule = re.compile(u"[^0-9\\u4e00-\\u9fa5]")
    output = open('train_segement.txt', 'w', encoding='utf-8')
    for texts_num, line in enumerate(f.readlines()):
        flag = 0
        line = line.strip('\n')
        line = rule.sub('',line)
        words = jieba.cut(line, cut_all=False)
        for word in words:
            if word not in stopword_set:
                if flag == 0:
                    output.write(str(texts_num)+":")
                    flag = 1
                output.write(word + ' ')
        output.write('\n')
    output.close()
    f.close()
    word_model = word2vec.Word2Vec.load("cbow.model")
    f = open('train_segement.txt','r')
    vocab = []
    m = 0
    for row in f.readlines():
        if(m<len(row.split())):
            m = len(row.split())
        for voc in row.split():
            if voc not in vocab:
                vocab.append(voc)
            else:
                pass
    f.close()
    max_features = len(vocab) # number of words
    maxlen = m  # cut texts after this number of words (among top max_features most common words)
    batch_size = 32
    num_class = 2
    x_train = []
    y_train = []
    f = open('train_segement.txt','r',encoding='utf-8')
    f1 = open('train_label.txt','r',encoding ='utf-8')
    for row,row1 in zip(f.readlines(),f1.readlines()):
        tmp = []
        if row != '\n' and row1.strip() != '-1':
            for v_ in row.split()[:-1]:
                try:
                    tmp.append(word_model.wv[v_])
                except:
                    pass
            if tmp != []:
                x_train.append(tmp)
                y_train.append(row1.strip())
        else:
            pass
    for i in range(len(x_train)):
        idx = 0
        while len(x_train[i]) != 23:
            x_train[i].append(x_train[i][idx])
            idx+=1
                
    x_train = np.asarray(x_train)
                       
    f.close()
    f1.close()
    
    y_train = np_utils.to_categorical(y_train, num_class)
   
    y_train = np.asarray(y_train)
    
    x_train, x_test, y_train, y_test = train_test_split(x_train , y_train, test_size=0.2, random_state=0)
    
    print('x_train shape:', x_train.shape)

    print('Build model...')

    model = creat_model()
    model.compile(loss='binary_crossentropy',
              optimizer='RMSProp',
              metrics=['accuracy'])
    print('Train...')
    checkpointer = ModelCheckpoint(filepath="./1_weights.hdf5", verbose=1, save_best_only=True)
    model.fit(x_train, y_train,epochs=10,batch_size = 32,callbacks=[checkpointer],validation_split=0.2)
    
    y_test = np.asarray(y_test)
    y_pred = model.predict(x_test)
    np.argmax(y_pred,axis=-1)
    np.argmax(y_test,axis=-1)
    precision = precision_score(np.argmax(y_test,axis=-1),np.argmax(y_pred,axis=-1),average='micro')
    recall = recall_score(np.argmax(y_test,axis=-1),np.argmax(y_pred,axis=-1),average='micro')
    print("Precision=",precision)
    print("recall=",recall)
    score, acc = model.evaluate(x_test, y_test)
    print(acc)
        

def segment(url):
    comment,_ = crawl.get_comment(url)
    jieba.set_dictionary('jieba/extra_dict/dict.txt.big')
    stopword_set = set()
    with open('jieba/extra_dict/stop_words.txt','r', encoding='utf-8') as stopwords:
        for stopword in stopwords:
            stopword_set.add(stopword.strip('\n'))
    rule = re.compile(u"[^0-9\\u4e00-\\u9fa5]")
    output = open('segment.txt', 'w', encoding='utf-8')
    for texts_num, line in enumerate(comment):
        flag = 0
        line = line.strip('\n')
        line = rule.sub('',line)
        words = jieba.cut(line, cut_all=False)
        for word in words:
            if word not in stopword_set:
                if flag == 0:
                    output.write(str(texts_num)+":")
                    flag = 1
                output.write(word + ' ')
        output.write('\n')
        
def demo():
    word_model = word2vec.Word2Vec.load("cbow.model")
    model = creat_model()
    model.load_weights('./weights.hdf5')
    testX = []
    index = []
    f = open('segment.txt','r',encoding='utf-8')
    for row in f.readlines():
#         print (row)
        tmp = []
        if row != []:
            for v_ in row.split(':')[-1].split():
                try:
                    tmp.append(word_model.wv[v_])
                except:
                    pass
            if tmp != []:
#                 print(row.split(':')[1].split())
                index.append(row.split(':')[0])
                testX.append(tmp)
        else:
            pass
    f.close()
    for i in range(len(testX)):
        idx = 0
        while len(testX[i]) != 23:
            testX[i].append(testX[i][idx])
            idx+=1
    testX = np.asarray(testX)
    y_pred =  model.predict(testX)
    y_pred = y_pred.argmax(axis=-1)
    print("Test:",y_pred)
    useless = []
    for i,j in zip(y_pred,index):
        if i == 0:
            useless.append(j)
    return useless
def appearance(useless_list,url):
    confidence = np.load('confidence.npy').item()
    
    garbage_flag=0
    comment,user=crawl.get_comment(url)
    replace_str_list=[]
    for item in useless_list:
        replace_str_list.append(comment[int(item)])
    if(len(useless_list)/len(comment)>0.3):
        garbage_flag=1
        print("garbage!!")
    file=open('demo.html', 'r')
    content=file.readlines()
    file.close()
    replace_str_list_idx=0
    content_idx=0
    replace_user_list_idx=0
    #confidence
    for content_idx in range(0,len(content)):
        find_str=user[replace_user_list_idx]
        if(content[content_idx].find(find_str)!=-1):
            if(confidence[find_str]!=-1):
                content[content_idx]=content[content_idx].replace(find_str,"("+str(round(confidence[find_str],2))+")"+find_str)
            replace_user_list_idx=replace_user_list_idx+1
            if(replace_user_list_idx==len(replace_str_list)):
                break
    for content_idx in range(0,len(content)):
        
        find_str=replace_str_list[replace_str_list_idx]+"</span>"
        if(garbage_flag==1):
            content[content_idx]=content[content_idx].replace("<span class=\"f2\">※ 發信站:","<img src=\"./garbage.jpg\" height=\"250\" width=\"250\">\n<span class=\"f2\">※ 發信站:")
        if(content[content_idx].find(find_str)!=-1):
            #print(content[content_idx])
            content[content_idx]=content[content_idx].replace(": "+find_str,"<font color=\"#111111\">"+": "+find_str+ "</font>")
            replace_str_list_idx=replace_str_list_idx+1
            if(replace_str_list_idx==len(replace_str_list)):
                break
    file=open('demo.html', 'w')
    file.writelines(content)
    file.close()
    
def confidence():
    idxrange = [0,500000,1000000,1500000,2000000,2500000,3000000,3500000,4000000,4500000,5000000,5500000,6000000,6500000,7000000,7500000,8000000,8500000,9000000,9500000,9883027]
    for i in range(len(idxrange)-1):
#         f = open('./test/ALL_comment.txt','r',encoding='utf-8')
#         jieba.set_dictionary('jieba/extra_dict/dict.txt.big')
#         stopword_set = set()
#         with open('jieba/extra_dict/stop_words.txt','r', encoding='utf-8') as stopwords:
#             for stopword in stopwords:
#                 stopword_set.add(stopword.strip('\n'))
#         rule = re.compile(u"[^0-9\\u4e00-\\u9fa5]")
#         output = open('segment_all.txt', 'w', encoding='utf-8')
#         for texts_num, line in enumerate(f.readlines()):
#             flag = 0
#             line = line.strip('\n')
#             line = rule.sub('',line)
#             words = jieba.cut(line, cut_all=False)
#             for word in words:
#                 if word not in stopword_set:
#                     if flag == 0:
#                         output.write(str(texts_num)+":")
#                         flag = 1
#                     output.write(word + ' ')
#             output.write('\n')
#         output.close()
#         f.close()
        word_model = word2vec.Word2Vec.load("cbow.model")
        model = creat_model()
        model.load_weights('./weights.hdf5')
        testX = []
        index = []
        f = open('./segment_all.txt','r',encoding='utf-8')
        aa=0
        for row in f.readlines()[idxrange[i]:idxrange[i+1]]:
            tmp = []
            if row != []:
                for v_ in row.split(':')[-1].split():
                    try:
                        tmp.append(word_model.wv[v_])
                    except:
                        pass
                if tmp != []:
                    index.append(row.split(':')[0])
                    if(len(tmp))>23:
                        testX.append(tmp[:23])
                    else:
                        testX.append(tmp)
            else:
                pass
            if(aa%10000)==0:
                print(aa)
            aa+=1
        f.close()
        aa=0
        for i in range(len(testX)):
            idx = 0
            while len(testX[i]) < 23:
                testX[i].append(testX[i][idx])
                idx+=1
            if(aa%10000==0):
                print(aa)
            aa+=1
        testX = np.asarray(testX)
        print("Strat test")
        y_pred =  model.predict(testX)
        y_pred = y_pred.argmax(axis=-1)
        print("Test:",y_pred)
        result = open('confidence.txt','a',encoding='utf-8')
        for i,j in zip(index,y_pred):
            result.write(str(i)+' '+str(j)+'\n')
        result.close()
def cal_confidence():
    confidence = collections.OrderedDict()
    f = open('./test/ALL_author.txt','r',encoding='utf-8')
    author = []
    for row in f.readlines():
        author.append(row.strip('\n'))
    f.close()
    for a in author:
        if a not in confidence.keys():
            confidence.update({a:[0,0]})
        else:
            continue
    f = open('./confidence.txt','r',encoding='utf-8')
    for row in f.readlines():
        au = int(row.split()[0])
        rat = row.split()[1]
        if rat == '0':
            confidence[author[au]][1]+=1
        elif rat == '1':
            confidence[author[au]][0]+=1
        else:
            pass
    f.close();
    f = open('confidence_dict.txt','w',encoding='utf-8')
    for key,value in confidence.items():
        f.write(key+':'+str(value[0])+' '+str(value[1])+'\n')
    f.close()

segment(sys.argv[1]) 
useless_list=demo()
appearance(useless_list,sys.argv[1])

# train()



