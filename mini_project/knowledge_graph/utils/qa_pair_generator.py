#-*- coding:utf8 -*-
#!/usr/bin/python2.7

from optparse import OptionParser

import os, sys
reload(sys)

sys.setdefaultencoding('utf-8')

# set parser
parser = OptionParser(usage="%prog [options]", version="%prog 0.1")
parser.add_option("--triad_path", action="store", dest="triad_path")
parser.add_option("--template", action="store", dest="template")



# 检查函数返回
def CheckRet(ret):
    if 0 == ret:
        return
    print "err return code %d" % ret
    exit(1)

# 检查程序的参数是否有效
def CheckOption(option, option_str):
    if option is None:
        print "Please specify %s with --%s option" % (option_str, option_str)
        parser.print_help()
        return 1
    return 0

# 根据传入的字典和模板来生成字符串
def Render(template, para_dict):
    # 先根据 \t 进行分隔
    print template
    print para_dict
    result = []
    tokens = template.split('\t')
    for token in tokens:
        # 从第 0 个开始搜索
        start = token.find('{{', 0)
        end = token.find('}}', 0)
        if start == -1 and end == -1: # 如果俩都没有，直接加入数组，然后跳过
            result.append(token)
            continue
        # TODO 这里需要用 while，来确保能够完全替换
        if start != -1 and end != -1: # 如果都能找到，则进行替换后加入数组
            # 先找到字典的 key
            key = token[start+2:end]
            print key
            continue
        # 到这里的话，说明
        


    return "lalala"


# python qa_pair_generator.py --triad_path=product_graph --template=qa_pair.template
# python qa_pair_generator.py --triad_path=test --template=qa_pair.template

if __name__ == "__main__":

    (options, args) = parser.parse_args()
    if len(args) != 0:
        parser.print_help()
        sys.exit()

    # if there is no triad path, ask the user to specify it
    CheckRet(CheckOption(options.template, "template"))
    CheckRet(CheckOption(options.triad_path, "triad_path"))


    print "Step 1 Load Sentence Template from %s" % options.template
    with open(options.template,'r') as f:
        template_list = [line.strip() for line in f.readlines()] 

    print "Step 2 Load Triad Data from %s" % options.triad_path

    file_list= [i for i in os.listdir(options.triad_path)]
    for filename in file_list:
        path = options.triad_path + "/" + filename
        print "loading " + path
        for line in open(options.triad_path + "/" + filename):
            tokens = line.split("\t")
            arr = tokens[0].split(' ')
            if len(arr) != 2: # 如果名称里不包含股票代码，跳过
                continue
            para_dict = {}
            para_dict['subject_entity'] = arr[0]
            para_dict['relationship'] = tokens[4][:-1] # 去掉最后的回车
            para_dict['object_entity'] = tokens[3]
            # 根据模板进行句子生成
            for template in template_list:
                print Render(template, para_dict)


    
