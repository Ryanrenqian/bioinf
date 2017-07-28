import os,sys
def openFileinDir(PATH):
    filelist=[]
    for parents,dirnames,filenames in os.walk(PATH):
        for filename in filenames:
            if filename.endswith('.gtf'):
               filelist.append(os.path.join(parents,filename))
    return filelist

if __name__=='__main__':
    gffpath=openFileinDir(sys.argv[1])
    fpkmpath=sys.argv[2]
    outfile=sys.argv[3]
    for i in gffpath:
        filename=i.split('/')[-2]
 #       print filename
        gffdict={}
        fpkmdict={}
        with open(i,'r') as gff:
            while True:
                a=gff.readline()
                if a=='':
                    break
                if '\ttranscript\t' in a:
                    b=a.split('"')
                #    print a.split('"')[-8]
                #    print a.split('"')[-4]
                #    if b[-4]=='=' or b[-4]=='c':
                #        gffdict[b[-8]]=b[-4]
                    for i in range(len(b)):
                        if b[i]=="; oId ":
                            id=b[i+1]
                        if b[i]=="; class_code ":
                            gf=b[i+1]
                    gffdict[id]=gf
        for parents,dirnames,filenames in os.walk(fpkmpath):
            if filename+'.gtf' in filenames:
                with open(os.path.join(parents,filename+'.gtf'),'r') as fpkm:
                    while True:
                        c=fpkm.readline()
                        if c=='':
                            break
                        if '\ttranscript\t' in c:
                            d=c.split('"')
                            for i in range(len(d)):
                                if d[i]=='; transcript_id ':
                                    id=d[i+1]
                                if d[i]=='; FPKM ':
                                    fp=d[i+1]
                            fpkmdict[id]=fp
        with open(outfile,'a') as f:
            line1=[filename+'_fpkm\t']
            line2=[filename+'_class_code\t']
        #    print filename
            for key in gffdict.keys():
                print key
            #    if gffdict[key]=='='or gffdict[key]=='c':
                line1.append(fpkmdict[key])
                line2.append(gffdict[key])
            f.write('\t'.join(line1)+'\n')
            f.write('\t'.join(line2)+'\n')