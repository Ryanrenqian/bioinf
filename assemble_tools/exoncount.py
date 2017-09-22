import os,sys,re
def exoncount(file):
    with open(file,'r') as f:
        exon=[]
        flag=-1
    #    print flag
        while True:
            a=f.readline()
            if a=='':
                break
            elif '\ttranscript\t' in a:
    #            print a
                flag+=1
                exon.append(0)
            elif '\texon\t' in a:
    #            print flag
    #            print exon[flag]
                exon[flag]+=1
    exon=[str(i) for i in exon]
    return exon


if __name__=='__main__':
    path = sys.argv[1]
    file = sys.argv[2]
    with open(file,'w') as w:
        for parent,dirname,filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith('gtf'):
                    filepath=os.path.join(parent,filename)
                    w.write(filename+'\t')
                    w.write(' '.join((exoncount(filepath)))+'\n')
