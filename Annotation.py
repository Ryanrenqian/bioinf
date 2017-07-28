import os,re,sys

#should be tracking file
def GetReflection(infile,codon):
    IDdict={}
    Altdict={}
    with open(infile,'r') as f:
        while True:
            line=f.readline()
            if line=='':
                break
            colunm=line.split()
#TCONS_00000001  XLOC_000001     DDX11L1|ENST00000450305.2       j       q1:MSTRG.1|MSTRG.1.1|100|0.000000|0.000000|0.000000|0.000000|-
            if colunm !='-':
                newGeneID=colunm[2].split('|')[0]
                newTransID=colunm[2].split("|")[1]
            oldGeneID=colunm[0]
            oldTransID=colunm[1]
            if codon=='gencode':
                if colunm[3] !='u' and colunm[3] !='j' and colunm[3] !='x' and colunm[3] !='s':
                    IDdict[oldGeneID]=newGeneID
                    IDdict[oldTransID]=newTransID
                else:
                    Altdict[oldGeneID] = newGeneID
                    Altdict[oldGeneID] = newGeneID
            elif codon=='noncode':
                if colunm[3]!='u' and colunm[3] !='j':
                    IDdict[oldGeneID] = newGeneID
                    IDdict[oldTransID] = newTransID
                else:
                    Altdict[oldGeneID] = newGeneID
                    Altdict[oldGeneID] = newGeneID
    return IDdict,Altdict

def run(gencodefile,noncodefile,mergefile):
    gedict=GetReflection(gencodefile,'gencode')
    nondict=GetReflection(noncodefile,'noncode')
    with open(mergefile,'r') as f:
        with open('filterout','w') as o1:
            with open(mergefile.rstrip('.gtf')+'.Annotation.gtf','w') as o2:
                while True:
                    a=f.readline()
                    if a=='':
                        break
#chr1    StringTie       transcript      11869   192397  1000    +       .       gene_id "MSTRG.1"; transcript_id "MSTRG.1.1";
                    oldGeneID=re.search(r'gene_id "(\w+.?\d+)";').group(1)
                    oldTransID=re.search(r'transcipt_id "(\w+.?\d+)";')
                    if gedict.get(oldGeneID,None)==None and nondict.get(oldTransID,None)==None:
                        o1.write(a)
                    else:
                        o2.write(a)
    return 'All finished!'

if __name__=='__main__':
    gencodefile=sys.argv[1]
    noncodefile=sys.argv[2]
    mergefile=sys.argv[3]
    run(gencodefile, noncodefile, mergefile)