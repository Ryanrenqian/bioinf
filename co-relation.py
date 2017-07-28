
import sys,math,threading
import numpy as np
import scipy.stats


def Correlate2(data1,data2):
    return scipy.stats.pearsonr(data1,data2)

def Correlate1(data1, data2):
    return scipy.stats.spearmanr(data1,data2)

def getdata(file,lst):
    mydata={}
    with open(file,'r') as f:
        for i,line in enumerate(f.readlines()):
            if i==0:
                continue
            a=line.split()[0]
            if a in lst:
                data=np.array(line.split()[1:],dtype=float)
                mydata[a]=data
    return mydata

def mimRNA((ffile, tfile, list), cor=0.5, pva=0.01):
    milist = []
    mrlist = []
    mim = {}
    with open(list, 'r') as f:
        for line in f.readlines():
            mi = line.split()[0]
            mr = line.split()[1]
            milist.append(mi)
            mrlist.append(mr)
            mim[(mi,mr)]=0
    fdata = getdata(ffile,mrlist)
    tdata = getdata(tfile,milist)
    threading.Thread(target=write,args=('spearman.xls', Correlate1, (fdata, tdata), (cor, pva), mim,),
                                    name='spearman').run()
    threading.Thread(target=write, args=('pearson.xls', Correlate2, (fdata, tdata), (cor, pva), mim,),
                                     name='pearson').run()

def write(name,func,(fdata,tdata),(cor,pva),mim):
    with open(name,'w') as f:
        for key in mim.keys():
            if key[1] not in fdata:
                continue
            if key[0] not in tdata:
                continue
            fpkm = fdata[key[1]]
            tpm = tdata[key[0]]
            if len(fpkm) == len(tpm):
                try :
                    Cor,Pval=func(fpkm, tpm)
                    if math.sqrt(Cor)>cor and Pval<pva:
                        f.write("%s\t%s\t%s\t%s\n"%(key[0],key[1],Cor,Pval))
                except:
                    print "something wrong!!"
                    print key
            else:
                print "length is not equal!"
                print key

def lncmRNA((mfile,mlist),(lfile,llist),cor=0.5,pva=0.01):
    lnclist = []
    mrlist = []
    mim={}
    with open(llist, 'r') as f:
        for line in f.readlines():
            lnc = line.split()[0]
            lnclist.append(lnc)
    with open(mlist, 'r') as f:
        for line in f.readlines():
            mr = line.split()[0]
            mrlist.append(mr)
    mrdata=getdata(mfile,mrlist)
    lncdata=getdata(lfile,lnclist)
    for i in lnclist:
        for j in mrlist:
            mim[i,j]=0
    threading.Thread(target=write,args=('spearman.xls', Correlate1, (mrdata, lncdata), (cor, pva), mim,),
                     name='spearman').run()
    threading.Thread(target=write, args=('pearson.xls', Correlate2, (mrdata, lncdata), (cor, pva), mim,),
                     name='pearson').run()


if __name__=='__main__':
    if len(sys.argv)==4:
        ffile=sys.argv[1]
        tfile=sys.argv[2]
        list=sys.argv[3]
        mimRNA((ffile,tfile,list))
        print "finished!"
    else:
        ffile=sys.argv[1]
        tfile=sys.argv[2]
        flist=sys.argv[3]
        tlist = sys.argv[4]
        lncmRNA((ffile, flist), (tfile, tlist))
        print "finished"


