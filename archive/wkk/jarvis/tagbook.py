import os, sys, codecs, json, re
import jieba
import jieba.analyse

bookbase = './data/doubanbooks/bookinfolite.txt'
# this two sentence can solve Chinese Problem
reload(sys)
sys.setdefaultencoding('utf-8')

def bookproc():
    bookinfos = open(bookbase,'r')
    booklist = []
    for book in bookinfos:
        target = json.JSONDecoder().decode(book)
        tags = jieba.analyse.extract_tags(target['context'], topK=10, withWeight=True)
        output = target['name']
        print target['name'],

        for t in target['tags']:
            print ' ' + t[0],
            output = output + u'*' + t[0]

        for t in tags:
            print ' ' + t[0],
            output = output + u'*' + t[0]

        print ''
        booklist.append(output + '\n')

    fh = codecs.open('./seg/books.txt', 'w', 'utf-8')
    for b in booklist:
        fh.write(b)

    print 'done'

if __name__ == '__main__':
    bookproc()
