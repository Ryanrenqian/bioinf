from scipy.stats import ttest_rel
import os,re,sys
datapath=''
def get_data(le,ve,ch,datapath):
    result=[]
    levels={'base':10,'exon':11,'intron':12,'intron_chain':13,\
          'transcript':14,'locus':15}
    choices={'sensitivity':2,'precision':4}
    version={'122':'v122','133':'v133'}
    if le=='intron_chain':
        choices={'sensitivity':3,'precision':5}

    for parent,dirnames,filenames in os.walk(datapath):
        for filename in filenames:

#            if re.match('[0-9]+\.[0-9]+$',filename):
#                filepath = os.path.join(parent, filename)
#                with open(filepath, 'rb') as f:
#                    lines = f.readlines()
#                col = levels[le]
#                row = choices[ch]
#                line = lines[col].lstrip()
#                ans = line.split()[row]
#                result.append(ans)

            if filename.startswith(version[ve]) & filename.endswith('stats'):
            #    if filename.endswith('N') | filename.endswith('T'):

                    filepath=os.path.join(parent,filename)
                    with open(filepath,'rb') as f:
                        lines=f.readlines()
                    col=levels[le]
                    row=choices[ch]
                    line=lines[col].lstrip()
                    ans=float(line.split()[row])
                    result.append(ans)
    #print result
    return result

def File(path):
    file = []
    for parent,dirnames,filenames in os.walk(path):
        for filename in filenames:
            if re.match('[0-9]+\.[0-9]+$',filename):
                file.append(filename)

    return file

def pair_ttest(le,ch,path):
    data1=get_data(le,'122',ch,path)
    data2=get_data(le,'133',ch,path)
    return ttest_rel(data1,data2)

def data_pair(le,ch):
    print 'V122'
    data1=get_data(le,'122',ch)
    print 'V133'
    data2=get_data(le,'133',ch)
    return data1,data2


#
if __name__=='__main__':
    path=sys.argv[1]
    levels={'base':10,'exon':11,'intron':12,'intron_chain':13,\
          'transcript':14,'locus':44.2}
    choices={'sensitivity':2,'precision':3}
    version={'122':'v122','133':'v133'}
#    with open('merge_taco_com','w') as f:
#        f.write('filename'+'\t'+'\t'.join(File(path))+'\n')
#        for le in levels.keys():
#            for ch in choices.keys():
#                a=le+' '+ch+'\t'+'\t'.join(get_data(le,ch,path))+"\n"
#                f.write(a)

    with open('gff_ttest','w') as f:
        for le in levels.keys():
            for ch in choices.keys():
                print
                #a=le+"\t"+ch+"\n"+str(pair_ttest(le,ch,path))+"\n"
                #f.write(a)