###################################################################
# File Name: set_operation.py
# Author: renqian
# mail: renqian@yucebio.com
# Created Time: Wed 20 Sep 2017 07:45:30 PM CST
#=============================================================
#!/usr/bin/env python3
import os,sys
import collections

#path=collections.namedtuple('path',('group','path'))
def pathwalk(path,suffix):
    paths=[]
    for dirs,dirnames,filenames in os.walk(path):
        for file in filenames:
            if file.endswith(suffix):
                pa=os.path.join(dirs,file)
                name=dirs.split('/')[-1]
                paths.append((name,pa))
    return paths

def readfile(pa):
    up=[]
    down=[]
    with open(pa,'r')as f:
        for line in f.readlines():
            if 'Gene' in line:
                continue
            gene=line.split()[0]
            logfc=float(line.split()[1])
            if logfc > 1:
                up.append(gene)
            elif logfc < 1:
                down.append(gene)
    return (up,down)

from optparse import OptionParser
def parseCommand():
    usage = "\n\twe talk this later"
    parser = OptionParser(usage = usage, version = "v0.2.3")
    # <requried>
    parser.add_option("-r", "--rootpath", dest = "rootpath",
        type=str,
        help = "root path of banches of groups. eg, path/G1,path/G2,path/G3")
    parser.add_option("-i", "--ignore", dest = "ignore",
        type=str,
        help = "group should be ignored: G1,G2")
    # <options 
    parser.add_option('-s',"--suffix", dest = "suffix",
        type = str,
        help = "file should have the same suffix")
    parser.add_option("-o",'--output',dest='output',type=str,
                    help='output path')
    return parser.parse_args()
def main(rootpath,ignore,suffix,output):
    namepath=pathwalk(rootpath,suffix)
    updict={}
    downdict={}
    names=[]
    up=set()
    down=set()
    for name, path in namepath:
        if name in ignore:
            continue
        print(name)
        updict[name],downdict[name]=readfile(path)
        names.append(name)
        up=up|set(updict[name])
        down=down|set(downdict[name]) 
    with open(output+'/up.txt','w')as f:
        fupdict={}
        for gene in up:
            uplist=[]
            for name in sorted(updict.keys()):
                if gene in updict[name]:
                    uplist.append(name)
            fupdict.setdefault('_'.join(uplist),[]).append(gene)
        for name in fupdict.keys():
            f.write('%s\t%s\n'%(name,'\t'.join(fupdict[name])))
    with open(output+'/down.txt','w')as f:
        fdwdict={}
        for gene in down:
            dwlist=[]
            for name in sorted(downdict.keys()):
                if gene in downdict[name]:
                    dwlist.append(name)
            fdwdict.setdefault('_'.join(dwlist),[]).append(gene)
        for name in fdwdict.keys():
            f.write('%s\t%s\n'%(name,'\t'.join(fdwdict[name])))

if __name__=='__main__':
    parse,arg=parseCommand()
    rootpath=parse.rootpath
    ignore=parse.ignore
    suffix=parse.suffix
    output=parse.output
    if not os.path.isdir(output):
        if os.path.exists(output):
            print('output should  be a dir')
            sys.exit()
        else:
            print('mkdir %s'%output)
            os.mkdir(output)
    try:
        main(rootpath,ignore,suffix,output)
    except:
        raise KeyError
