# -*- coding: utf-8 -*-
from sklearn.cross_validation import train_test_split
from gensim.models.word2vec import Word2Vec
import numpy as np
import pandas as pd
import jieba
from sklearn.externals import joblib
from sklearn.svm import SVC
import datetime
import sys, os
reload(sys)  
sys.setdefaultencoding('utf8')

datadir = ''
modeldir = ''

# 加载文件，导入数据,分词
def loadfile():
    neg=pd.read_excel(datadir + '/neg.xls',header=None,index=None)
    pos=pd.read_excel(datadir + '/pos.xls',header=None,index=None)

    cw = lambda x: list(jieba.cut(x))
    pos['words'] = pos[0].apply(cw)
    neg['words'] = neg[0].apply(cw)

    #print pos['words']
    #use 1 for positive sentiment, 0 for negative
    y = np.concatenate((np.ones(len(pos)), np.zeros(len(neg))))

    x_train, x_test, y_train, y_test = train_test_split(np.concatenate((pos['words'], neg['words'])), y, test_size=0.2)
    
    np.save(modeldir + '/y_train.npy',y_train)
    np.save(modeldir + '/y_test.npy',y_test)
    return x_train,x_test
 


#对每个句子的所有词向量取均值
def buildWordVector(text, size,imdb_w2v):
    vec = np.zeros(size).reshape((1, size))
    count = 0.
    for word in text:
        try:
            vec += imdb_w2v[word].reshape((1, size))
            count += 1.
        except KeyError:
            continue
    if count != 0:
        vec /= count
    return vec
    
#计算词向量
def get_train_vecs(x_train,x_test):
    n_dim = 300
    #Initialize model and build vocab
    imdb_w2v = Word2Vec(size=n_dim, min_count=10)
    imdb_w2v.build_vocab(x_train)
    
    #Train the model over train_reviews (this may take several minutes)
    imdb_w2v.train(x_train)
    
    train_vecs = np.concatenate([buildWordVector(z, n_dim,imdb_w2v) for z in x_train])
    #train_vecs = scale(train_vecs)
    
    np.save(modeldir + '/train_vecs.npy',train_vecs)
    print train_vecs.shape
    #Train word2vec on test tweets
    imdb_w2v.train(x_test)
    if not os.path.exists(modeldir + '/w2v_model'):
        os.mkdir(modeldir + '/w2v_model')
    imdb_w2v.save(modeldir + '/w2v_model/w2v_model.pkl')
    #Build test tweet vectors then scale
    test_vecs = np.concatenate([buildWordVector(z, n_dim,imdb_w2v) for z in x_test])
    #test_vecs = scale(test_vecs)
    np.save(modeldir + '/test_vecs.npy',test_vecs)
    print test_vecs.shape



def get_data():
    train_vecs=np.load(modeldir + '/train_vecs.npy')
    y_train=np.load(modeldir + '/y_train.npy')
    test_vecs=np.load(modeldir + '/test_vecs.npy')
    y_test=np.load(modeldir + '/y_test.npy') 
    return train_vecs,y_train,test_vecs,y_test
    

##训练svm模型
def svm_train(train_vecs,y_train,test_vecs,y_test):
    clf=SVC(kernel='rbf',verbose=True)
    clf.fit(train_vecs,y_train)
    if not os.path.exists(modeldir + '/svm_model'):
        os.mkdir(modeldir + '/svm_model')
    joblib.dump(clf, modeldir + '/svm_model/model.pkl')
    print clf.score(test_vecs,y_test)
    
    
##得到待预测单个句子的词向量    
def get_predict_vecs(words):
    n_dim = 300
    imdb_w2v = Word2Vec.load(modeldir + '/w2v_model/w2v_model.pkl')
    #imdb_w2v.train(words)
    train_vecs = buildWordVector(words, n_dim,imdb_w2v)
    #print train_vecs.shape
    return train_vecs

def batchtest(filepath):
    clf=joblib.load(modeldir + '/svm_model/model.pkl')

    test_count = 0
    correct_count = 0
    if os.path.exists(filepath):
        f = open(filepath, 'r')
        try:
            lines = f.readlines()
            for line in lines:
                if len(line) <= 0:
                    continue
                else:
                    arr = line.split(',')
                    label = arr[0]
                    test_count += 1
                    text = ",".join(arr[1:])
                    words=jieba.lcut(text)
                    words_vecs=get_predict_vecs(words)
                    result=clf.predict(words_vecs)

                    if result[0] > 0.5 and label == '1' or result[0] <= 0.5 and label == '0':
                        correct_count += 1
                        print '['+ str(test_count) + ']:',label, result[0], text,
                    else:
                        print '['+ str(test_count) + ']:[x]',label, result[0], text,
        finally:
            f.close() # 确保关闭
    return correct_count, test_count

####对单个句子进行情感判断    
def predict(string):
    words=jieba.lcut(string)
    words_vecs=get_predict_vecs(words)
    clf=joblib.load(modeldir + '/svm_model/model.pkl')
     
    result=clf.predict(words_vecs)
    
    if int(result[0])==1:
        print 'positive', string
    else:
        print 'negative', string

def train():
    ##导入文件，处理保存为向量
    x_train,x_test=loadfile() #得到句子分词后的结果，并把类别标签保存为y_train。npy,y_test.npy
    get_train_vecs(x_train,x_test) #计算词向量并保存为train_vecs.npy,test_vecs.npy
    train_vecs,y_train,test_vecs,y_test=get_data()#导入训练数据和测试数据
    svm_train(train_vecs,y_train,test_vecs,y_test)#训练svm并保存模型


if __name__=='__main__':
    argvs_length = len(sys.argv)
    if argvs_length >= 4:
        argvs = sys.argv
        action = argvs[1]
        if action == 'train': # 训练
            datadir = argvs[2]
            modeldir = argvs[3]
            begin = datetime.datetime.now()
            train()
            end = datetime.datetime.now()
            # 统计训练时间、模型大小，写入到 result.txt 中
            with open(modeldir + '/result.txt', "w") as f:
                f.write('训练时长: ' + str(end-begin))
        elif action == 'predict':
            modeldir = argvs[2]
            sentence = " ".join(argvs[3:])
            predict(sentence)
        elif action == 'test':
            datadir = argvs[2]
            modeldir = argvs[3]
            testdir = argvs[4]
            begin = datetime.datetime.now()
            result = batchtest(datadir+'/test.txt')
            end = datetime.datetime.now()
            # 统计训练时间、模型大小，写入到 result.txt 中
            with open(testdir + '/result.txt', "w") as f:
                f.write('测试时长: ' + str(end-begin) + '\n')
                f.write('正确率: ' + str(float(result[0])/float(result[1])) + ' (' + str(result[0]) + '/' + str(result[1]) + ')\n')