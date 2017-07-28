from numpy import *
import os,sys
#import matplotlib.pyplot as plt

def get_lenth(newline):
    line=newline.split()
    return int(line[4])-int(line[3])



def len_distribution(file):
    Tranlen=[]
    with open(file,"r") as f:
        while True:
            a=f.readline()
            if a=='':
                break
            if not (a.startswith('#') or ('exon' in a)):
                length=str(get_lenth(a))
                Tranlen.append(length)
    return Tranlen

def walkdir(PATH,file):
    with open(file,'w+') as O:
        for parent,dirnames,filenames in os.walk(PATH):
            for filename in filenames:
                if filename.endswith('.gtf'):
#                if filename.endswith('.gtf') & filename.startswith('LUAD'):
                    print filename
                    print parent
                    filepath=os.path.join(parent,filename)
                    print filepath
                    O.write(filename+"\n")
                    O.write(" ".join(len_distribution(filepath))+'\n')



if __name__=='__main__':
    path=sys.argv[1]
    file=sys.argv[2]
    print path
    walkdir(path,file)
