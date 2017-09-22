import re,sys
def position(file):
    gedict={}
    with open(file,'r') as f:
        for i in f.readlines():
            if 'start_codon' in i:
                r=re.search("gene_id \"(.+?)\";",i)
                id=r.groups()
                line=i.split()
                if gedict.get(id)==None:
                    start=int(line[3])
                elif int(line[3])<gedict[id][0]:
                    start=int(line[3])
            elif 'stop_codon' in i:
                line=i.split()
                if gedict.get(id)==None:
                    end=int(line[4])
                elif int(line[4])>gedict[id][1]:
                    end=int(line[4])
                gedict[id]=(start,end)
    return gedict


def real(file,gedict):
    redict={}
    with open(file,'r') as f:
        for i in f.readlines():
            line=i.split()
            pos=tuple(line[0].split('-'))
            count=line[1]
            length=len(gedict)
            num=0
            if not count=='0':
                for key in gedict.keys():
                    num+=1
                    if abs(int(pos[1]) - gedict[key][1])<50 and abs(int(pos[0]) - gedict[key][0])<50:
                        if not redict.get(key)==None:
                            if redict[key]<count:
                                redict[key]=count
                                print "warning:\t%s\t%s\t%s"% (key,gedict,line[0])
                        else:
                            redict[key] = count
                            genelength=gedict[1]-gedict[0]
                    elif num==length:
                        print("can not find compatible geneid!")
    return redict


def test(file, redict):
    with open(file, 'r') as f:
        with open("count.compare.txt", 'w') as o:
            o.write("gene\tcount\treal\n")
            for line in f.readlines():
                i = line.split()
                id = i[0]
                count = i[1]
                real = redict.get(id,0)
                newline = "%s\t%s\t%s\n"%(id,count,real)
                o.write(newline)

if __name__=="__main__":
    gedict=position('/mnt/cfs/project/test_freshman/renqian/expression/ref/rq.refgene.20150619.fixed.gtf')
    redict=real(sys.argv[1], gedict)
    test(sys.argv[2], redict)
