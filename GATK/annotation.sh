#!/bin/bash
PATH=$PATH:/mnt/nfs/software/bin
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/mnt/nfs/software/lib
export PERL5LIB=/mnt/nfs/software/lib/perl5:/mnt/nfs/software/lib/perl/5.18.2:/home/yangjie/perl5/lib/perl5
perl /mnt/nfs/user/limiao/dev/AnnoDB_v3/annodb.pl --mode indel  --if vcf --of xls --buildver GRCh38 --remove --outfile $1 $2
