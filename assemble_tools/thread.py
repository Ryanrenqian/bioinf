import os, sys, threading, time, re


def openFileinDir(PATH, suffix='.gtf'):
    filelist = []
    if os.path.isdir(PATH):
        for parents, dirnames, filenames in os.walk(PATH):
            for filename in filenames:
                if filename.endswith(suffix):
                    filelist.append(os.path.join(parents, filename))
    elif os.path.isfile(PATH):
        filelist.append(PATH)
    return filelist


def GetClasscode(filepath):
    class_code = {}
    with open(filepath, 'r')as f:
        while True:
            line = f.readline()
            if line == '':
                break
            if '\ttranscript\t' in line:
                if re.search("class_code \"[\w\W]\"", line):
                    a = re.search("class_code \"[\W\w]\"", line)
                    d = a.group()
                    class_code[d] = class_code.get(d, 0) + 1
    return class_code


def thread_classcode(filelist, output):
    start = time.time()
    code = ['class_code "="', 'class_code "c"', 'class_code "j"', 'class_code "e"', 'class_code "i"', 'class_code "o"',
            'class_code "p"', 'class_code "r"', 'class_code "u"', 'class_code "x"', 'class_code "s"']
    with open(output + '_class_code', 'a') as f:
        f.write('sample' + '\t' + '\t'.join(code) + '\n')
        for i in filelist:
            a = GetClasscode(i)
            line = [i.split('/')[-1]]
            for j in code:
                line.append(str(a.get(j, 0)))
            f.write('\t'.join(line) + '\n')
    end = time.time()
    print ('classcode has been count with %s!!!') % (str(start - end))


def GetFpkm(filepath):
    fpkm = []
    with open(filepath, 'r') as f:
        while True:
            a = f.readline()
            if a == '':
                break
            if '\ttranscript\t' in a:
                FPKM = a.split('"')[-4]
                fpkm.append(FPKM)
    return fpkm


def thread_FPKM(filelist, output):
    start = time.time()
    with open(output + '_FPKM', 'a') as f:
        for i in filelist:
            line = [i.split('/')[-1] + '_fpkm']
            line.extend(GetFpkm(i))
            f.write('\t'.join(line) + '\n')
    end = time.time()
    print ('FPKM has been count with %s!!!') % (str(end - start))


def CountLenth(newline):
    line = newline.split('\t')
    return int(line[4]) - int(line[3])


def GetLength(filepath):
    length = []
    with open(filepath, "r") as f:
        while True:
            a = f.readline()
            if a == '':
                break
            if '\ttranscript\t' in a:
                leng = str(CountLenth(a))
                length.append(leng)
    return length


def thread_length(filelist, output):
    start = time.time()
    with open(output + '_length', 'a') as f:
        for i in filelist:
            line = [i.split('/')[-1] + '_exon']
            line.extend(GetLength(i))
            f.write('\t'.join(line) + '\n')
    end = time.time()
    print ('Length has been count with %s!!!') % (str(end - start))


def GetExon(filepath):
    with open(filepath, 'r') as f:
        exon = []
        flag = -1
        #    print flag
        while True:
            a = f.readline()
            if a == '':
                break
            elif '\ttranscript\t' in a:
                flag += 1
                exon.append(0)
            elif '\texon\t' in a:
                exon[flag] += 1
    exon = [str(i) for i in exon]
    return exon


def thread_exon(filelist, output):
    start = time.time()
    with open(output + '_exon', 'a') as f:
        for i in filelist:
            line = [i.split('/')[-1] + '_exon']
            line.extend(GetExon(i))
            f.write('\t'.join(line) + '\n')
    end = time.time()
    print ('Exon has been count with %s!!!') % (str(end - start))


def GetStats(filepath):
    stats = []
    with open(filepath, 'r') as f:
        lines = f.readlines()
    for i in [10, 11, 12, 13, 14, 15]:
        data = lines[i].lstrip().split()
        if i == 13:
            stats.append(data[3])
            stats.append(data[5])
        else:
            stats.append(data[2])
            stats.append(data[4])
    return stats


def thread_stats(filelist):
    with open(output + '_stats', 'w') as f:
        f.write(
            'sample\tBase Sensitivity\tBase Precision\tExon Sensitivity\tExon Precision\tIntron Sensitivity\tIntron Precision\tTranscript Sensitivity\tTranscript Precision\tLocus Sensitivity\tLocus Precision\n')
        for i in filelist:
            line = [i.split('/')[-2]]
            line.extend(GetStats(i))
            f.write('\t'.join(line) + '\n')
    print 'stats has been counted!!!'


def thread_filter(filelist):
    pass


def threadrun(func, filelist, output):
    if 'classcode' in func:
        threading.Thread(target=thread_classcode, args=(filelist, output,), name='classcode').run()
    if 'fpkm' in func:
        threading.Thread(target=thread_FPKM, args=(filelist, output,), name='fpkm').run()
    if 'length' in func:
        threading.Thread(target=thread_length, args=(filelist, output,), name='length').run()
    if 'exon' in func:
        threading.Thread(target=thread_exon, args=(filelist, output,), name='exon').run()
    if 'filter' in func:
        threading.Thread(target=thread_filter, args=(filelist, output,), name='filter').run()
    if 'stats' in func:
        threading.Thread(target=thread_stats, args=(filelist, output,), name='stats').run()
        # print 'thread is finished'


if __name__ == '__main__':
    start = time.time()
    if len(sys.argv) < 4:
        print 'parametes isn`t sufficient!'
        sys.exit()
    elif len(sys.argv) == 4:
        path = sys.argv[1]
        func = sys.argv[2]
        output = sys.argv[3]
        threadrun(func=func, filelist=openFileinDir(path), output=output)
    elif len(sys.argv) == 5:
        path = sys.argv[1]
        func = sys.argv[2]
        output = sys.argv[3]
        suffix = sys.argv[4]
        threadrun(func=func, filelist=openFileinDir(path, suffix), output=output)
