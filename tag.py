import os,sys
def tag(tag,path):
    paths=[]
    for root,dirname,filenames in os.walk(path):
        for i in filenames:
            if tag in i:
                paths.append(os.path.join(root,i))
    with open(tag,'w')as f:
        flag=0
        for i in paths:
            NT=i.split('/')[-3]
            tag=i.split('/')[-1].split('.')[0]
            with open(i,'r') as r:
                for i,line in enumerate(r.readlines()):
                    if i==0 and flag==0:
                        f.write('N-Vs-T\ttype\t%s'%line)
                    elif i>0:
                        flag+=1
                        f.write('%s\t%s\t%s'%(NT,tag,line))

if __name__=='__main__':
    stag=sys.argv[1]
    path=sys.argv[2]
    tag(stag,path)
