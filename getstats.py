def get_data(filepath):
    result=[]
    with open(filepath, 'rb') as f:
        lines = f.readlines()
    for i in [10,11,12,13,14,15]:
        print i
        data = lines[i].lstrip().split()
        if i == 13:
            result.append(data[3])
            result.append(data[5])
        else:
            result.append(data[2])
            result.append(data[4])
    return result

def lowcount(filepath):
    count=0
    with open(filepath,'r') as  f:
        lines=f.readlines()
        for i in range(1,len(lines)):
            num=0
            for j in lines[i].split()[1:]:
                if float(j)<20:
                    num+=1
            if num>0:
                count+=1
    print count
    print float(count)/float(len(lines))

lowcount('/mnt/cfs/project/test_freshman/renqian/all-patient/fr/assembly/Amerge_stats')