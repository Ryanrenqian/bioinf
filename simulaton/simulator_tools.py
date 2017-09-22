'''
this is my first time to do research about the alignment of reads. In spite of the fact that only half \
number of reads was mapped into genome. I still try to count junction and count sensitivity and precision \
of different alignment software. i hope it will work good!!
'''
import sys

def unique(lst):
    return list(set(lst))

def fromresult(file):
    ls=[]
    with open(file,'r')as f:
        while True:
            line=f.readline()
            if line=='':
                break
            ls.append(line.split()[0])
    return unique(ls)

if __name__=='__main__':
    file1=sys.argv[1]
    file2=sys.argv[2]
    ls=fromresult(file2)
    share=0
    re=len(ls)
    count=0
    a=[]
    with open(file1,'r') as f:
        while True:
            line=f.readline()
            if line=='':
                break
            a.append(line.split()[0])
            if line.split()[0] in ls:
                ls.remove(line.split()[0])
                share+=1
    count=len(unique(a))
    print('right:\t%d'%share)
    print('found:\t%d'%re)
    print('real:\t%d'%count)
    print('not_consider:\t%d'%(count-share))
    print('wrong:\t%d'%(re-share))
    print('precision:\t%f'%(float(share)/re))
    print('sensitivity:\t%f'%(float(share)/count))