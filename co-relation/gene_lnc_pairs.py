import os,threading

#This file is designed to get gene-lnc pairs.
def dict(file):
    mydict={}
    with open(file,'r') as f:
        for line in f.readlines():
            line=line.strip()
            gene=line.split()[0]
            lnc=line.split()[1]
            mydict[gene]=lnc
    return mydict
# deal with plenty of file, you only need to set the path as input

def openFileinDir(PATH,suffix='.count.txt'):
    filelist=[]
    if os.path.isdir(PATH):
        for parents,dirnames,filenames in os.walk(PATH):
            for filename in filenames:
                if filename.endswith(suffix):
                   filelist.append(os.path.join(parents,filename))
    elif os.path.isfile(PATH):
        filelist.append(PATH)
    return filelist

# input the file
def operation(file,dict):
    with open(file,'r') as f:
        filename= os.path.split(file)[1]
        with open('/mnt/cfs/project/test_freshman/renqian/yang/'+filename+'.sub','w') as o:
            for line in f.readlines():
                gene=line.split()[0]
                count=line.split()[1]
                if not dict.get(gene)==None:
                    print '%s\tsub:%s\t%s' % (filename, gene, dict[gene])
                    gene=dict[gene]
                    line=gene+'\t'+count+'\n'

                o.write(line)
        print "%s has beed finished!!"%filename

#this is threading part
def runoperation(filelist,diction):
    for i in filelist:
        operation(i,diction)

# this is threading part
if __name__=='__main__':
    path='/mnt/cfs/prj16a/T769000/analysis_3/result/expression/htseq_lncRNA'
    file2='/mnt/cfs/project/test_freshman/renqian/result'
    diction = dict(file2)
    filelist=openFileinDir(path)
    num=0
    for i in range(0, len(filelist), len(filelist)/8):
        num+=1
        threading.Thread(target=runoperation,args=(filelist[i:i+len(filelist)/8],diction,),name='No.%d'%num).run()
