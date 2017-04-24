# -*- coding: utf-8 -*-
import jieba
import jieba.analyse
from entity import *
import sys
import commands
import os
import os.path
import shutil
from sys import argv
sys.path.append('../code')
import cPickle as pickle
import datetime



from sentiment_lstm import predict_arr

# hadoop fs -get hdfs://zykjoffline1:9000/yibot/general/raw/log/day=20170417 test

if __name__=='__main__':

    # 载入文件
    if len(argv) != 3:
        print "参数个数错误，用法 python sentiment.py yyyymmdd outpath"
        sys.exit()

    starttime = datetime.datetime.now()
    # 从 hdfs 中获取
    command = "hadoop fs -get hdfs://zykjoffline1:9000/yibot/general/raw/log/day=" + argv[1] + " ."
    (status, output) = commands.getstatusoutput(command)

    if status != 0:
        print "获取 HDFS 文件错误"
        sys.exit()

    print output
    
    # 此时应该已经下载完成，且在文件夹 day=argv[1] 中
    # 遍历文件夹中文件
    files = os.listdir("day=" + argv[1]) #列出文件夹下所有的目录与文件
    count = 0
    for i in range(0,len(files)):
        path = os.path.join("day=" + argv[1],files[i])
        if os.path.isfile(path):
            # 读取每个日志文件并处理
            print "[DEBUG] processing " + path
            querylist = []
            infolist = []
            f = open(path)
            for line in f:
                if len(line) <= 2:
                    continue
                
                arr = line.split('|')
                try: 
                    # 记录 pid, bid, session id, time
                    info = "%s || %s || %s || %s" % (arr[1][5:-1], arr[2][5:-1],arr[-8][9:-1] , arr[0][1:-2])
                except Exception, e:
                    print Exception,":",e
                    print line
                # 如果处理没有问题
                infolist.append(info)  
                # 增加处理行数
                count = count + 1
                if count % 10000 == 0:
                    print "[DEBUG] processing line", count
                # 用户查询
                querylist.append(arr[-1][7:-2])
                    
            f.close()
            probas = predict_arr(querylist)
            length = len(probas)
            mode = "a+"
            if i == 0:
                mode = "w+"
            f = open(argv[2] + "/emotion" + argv[1], mode)
            current = 0
            for i in range(length):
                # 写入到文件中（用追加模式）
                line = "%f || %s || %s\n" % (probas[i], infolist[i], querylist[i]) 
                if current % 10000 == 0:
                    print "[DEBUG] writing line", current, "/", count
                current = current + 1
                f.write(line)
                # print line,
            f.close()
    # 处理完删除日志文件
    shutil.rmtree("day=" + argv[1])
    endtime = datetime.datetime.now()
    print "[DEBUG] processing time:", (endtime - starttime).seconds, "seconds"
    print "[DEBUG] total record count:", count

