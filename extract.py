import os
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

if __name__=='__main__':
    path = '/mnt/cfs/prj16a/T769000/analysis_3/result/expression/htseq_lncRNA'
    filelist=openFileinDir(path)
    num=0
    for i in range(0, len(filelist), len(filelist)/8):
        print filelist[i]
        num+1
    print num
