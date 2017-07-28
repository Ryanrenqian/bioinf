if __name__=='__main__':
    mylist={}
    with open('geneID','r')as f:
        for line in f.readlines():
            line=line.strip()
            mylist[line]=1

    with open('lnc.log','r') as f:
        myflag=''
        mydict={}
        for line in f.readlines():
            if not mylist.get(line.split()[0])==None:
                gene=line.split()[0]
                if myflag=='':
                    myflag=gene
                    length=int(line.split()[3])-int(line.split()[2])
                    mydict[gene]=line
                elif myflag==gene:
                    print "one to duplication!"
                    leng2=int(line.split()[3])-int(line.split()[2])
                    if leng2>length:
                        mydict[gene]=line
                        length=leng2
                elif not myflag==gene:
                    mydict[gene]=line
                    length=int(line.split()[3])-int(line.split()[2])
        with open('result', 'w') as o:
            for key in mydict.keys():
                o.write(mydict[key])



