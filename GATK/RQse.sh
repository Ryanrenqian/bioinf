PATH=$PATH:/mnt/nfs/software/bin
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/mnt/nfs/software/lib
export PYTHONUSERBASE=/mnt/nfs/software
in=$1
python2 /mnt/nfs/software/bin/py/infer_experiment.py -i $in -r /mnt/nfs/user/yangjie/bin/RSeQC-2.6.4/database/hg38_GENCODE_v24_basic.bed -s 1000000
