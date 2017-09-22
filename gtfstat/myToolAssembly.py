import os,sys,re,time

#get the aimed file
def openFileinDir(PATH,suffix='.gtf'):
    filelist=[]
    if os.path.isdir(PATH):
        for parents,dirnames,filenames in os.walk(PATH):
            for filename in filenames:
                if filename.endswith(suffix):
                   filelist.append(os.path.join(parents,filename))
    elif os.path.isfile(PATH):
        filelist.append(PATH)
    return filelist


#count the exon
def GetExon(filepath):
    with open(filepath,'r') as f:
        exon=[]
        flag=-1
    #    print flag
        while True:
            a=f.readline()
            if a=='':
                break
            elif '\ttranscript\t' in a:
                flag+=1
                exon.append(0)
            elif '\texon\t' in a:
                exon[flag]+=1
    exon=[str(i) for i in exon]
    return exon

#count the length
def CountLenth(newline):
    line=newline.split('\t')
    return abs(int(line[4])-int(line[3]))

def GetLength(filepath):
    length=[]
    with open(filepath,"r") as f:
        while True:
            a=f.readline()
            if a=='':
                break
            if '\ttranscript\t' in a:
                leng=str(CountLenth(a))
                length.append(leng)
    return length

#get the FPKM
def GetFpkm(filepath):
    fpkm=[]
    with open(filepath,'r') as f:
        while True:
            a=f.readline()
            if a=='':
                break
            if '\ttranscript\t' in a:
                FPKM=a.split('"')[-4]
                fpkm.append(FPKM)
    return fpkm

#get the class_code
def GetClasscode(filepath):
    class_code = {}
    with open(filepath, 'r')as f:
        while True:
            line=f.readline()
            if line=='':
                break
            if '\ttranscript\t' in line:
                if re.search("class_code \"[\w\W]\"",line):
                    a=re.search("class_code \"[\W\w]\"",line)
                    d=a.group()
                    class_code[d]=class_code.get(d,0)+1
    return class_code

# filter single exon and length
def filter(file):
    with open(file, 'r') as f:
        with open(file.rstrip('.gtf') + '.filter.gtf', 'w') as o:
            with open('filterout.gtf','w') as m:
                flag = 0
                line = []
                length=0
                while True:
                    a = f.readline()
                    if '\ttranscript\t' in a:
                        if flag > 1 and length>=200:
                            o.writelines(line)
                        elif flag==1 or length<200:
                            m.writelines(line)
                        flag = 0
                        line=[]
                        length=CountLenth(a)
                        line.append(a)
                    elif '\texon\t' in a:
                        flag += 1
                        line.append(a)
                    elif a == '':
                        if flag > 1 and length>=200:
                            o.writelines(line)
                        elif flag==1:
                            m.writelines(line)
                        break

# get the stats
def GetStats(filepath):
    stats=[]
    with open(filepath, 'r') as f:
        lines = f.readlines()
    for i in [10,11,12,13,14,15]:
        data = lines[i].lstrip().split()
        if i == 13:
            stats.append(data[3])
            stats.append(data[5])
        else:
            stats.append(data[2])
            stats.append(data[4])
    return stats

def fileFun(filelist,func,output):
    if 'classcode' in func:
        code = ['class_code "="', 'class_code "c"', 'class_code "j"', 'class_code "e"', 'class_code "i"',
                'class_code "o"',
                'class_code "p"', 'class_code "r"', 'class_code "u"', 'class_code "x"', 'class_code "s"']
        with open(output + '_class_code', 'w') as f:
            f.write('classcode' + '\t' + '\t'.join(code) + '\n')
            for i in filelist:
                a = GetClasscode(i)
                line = [i.split('/')[-2]]
                for j in code:
                    line.append(str(a.get(j, 0)))
                f.write('\t'.join(line) + '\n')
        print 'Class code have beed counted!'

    if 'fpkm' in func:
        with open(output+'_FPKM','w') as f:
            for i in filelist:
                line=[i.split('/')[-1]+'_fpkm']
                line.extend(GetFpkm(i))
                f.write('\t'.join(line)+'\n')
        print 'FPKM have beed counted!'

    if 'length' in func:
        with open(output+'_length','w') as f:
            for i in filelist:
                line=[i.split('/')[-1]+'_length']
                line.extend(GetLength(i))
                f.write('\t'.join(line)+'\n')
        print 'Length have beed counted!'

    if 'exon' in func:
        with open(output+'_exon','w') as f:
            for i in filelist:
                line=[i.split('/')[-1]+'_exon']
                line.extend(GetExon(i))
                f.write('\t'.join(line)+'\n')
        print 'Exon have beed counted!'

    if 'filter' in func:
        for i in filelist:
            filter(i)
        print 'Transcripts that have single exon or whose length shorter than 200bp have been moved!'

    if 'stats' in func:
        with open(output+'_stats','w') as f:
            f.write('sample\tBase Sensitivity\tBase Precision\tExon Sensitivity\tExon Precision\tIntron Sensitivity\tIntron Precision\tTranscript Sensitivity\tTranscript Precision\tLocus Sensitivity\tLocus Precision\n')
            for i in filelist:
                line = [i.split('/')[-2]]
                line.extend(GetStats(i))
                f.write('\t'.join(line) + '\n')
        print 'Stats have been counted!'


if __name__=='__main__':
    start = time.time()
    if len(sys.argv)<4:
        print 'parametes isn`t sufficient!\n'
        print 'path\tfunc\toutput\tsuffix\n'
        print"func\nfilter:remove single exon or length less than 200bp transcript\n \
                exon: count exon\n length: count length\n fpkm: count fpkm\n classcode: count classcode"
        sys.exit()
    elif len(sys.argv)==4:
        path=sys.argv[1]
        func=sys.argv[2]
        output=sys.argv[3]
        fileFun(openFileinDir(path), func, output)
    elif len(sys.argv)==5:
        path = sys.argv[1]
        func = sys.argv[2]
        output = sys.argv[3]
        suffix=sys.argv[4]
    end=time.time()
    print 'Time spent:'+str((end-start))
