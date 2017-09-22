import re,os,sys

def classcode(PATH):
    class_code = {}
    with open(PATH, 'r')as f:
        while True:
            line=f.readline()
            if line=='':
                break
            if '\ttranscript\t' in line and 'chr1' in line:
                if re.search("class_code \"[\w\W]\"",line):
                    a=re.search("class_code \"[\W\w]\"",line)
                    d=a.group()
                    class_code[d]=class_code.get(d,0)+1
    return class_code

def write_data(version,class_code,filename):
    with open(version+'merge_chr1_class_code.txt','a') as o:
        title=['sample']
        for key in class_code.keys():
            title.append(key)
        o.write('\t'.join(title)+'\n')
        line1=[]
        for key in class_code.keys():
            line1.append(str(class_code[key]))
        o.write(filename+'\t'+'\t'.join(line1)+'\n')

def walkdir(PATH):
    for parent,dirnames,filenames in os.walk(PATH):
        for filename in filenames:
            if filename.endswith('.gtf'):
    #            print parent
    #            print filename
                file=parent.split('/')[-2]
                name=parent.split('/')[-1]
            #    print name
                if filename.startswith('v122'):
                    version=name
                    filepath=os.path.join(parent,filename)
            #        print filepath
                    write_data(version,classcode(filepath),filename=file)
                elif filename.startswith('v133'):
                    version=name
                    filepath=os.path.join(parent,filename)
                    write_data(version,classcode(filepath),filename=file)

if __name__=='__main__':
    path=sys.argv[1]
#    print path
 #   walkdir(path)
    write_data('133merge',classcode(path),'133merge')

