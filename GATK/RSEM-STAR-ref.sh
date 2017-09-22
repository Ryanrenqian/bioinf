# path
RSEM=/mnt/nfs/user/renqian/bin/RSEM-1.3.0
STAR=/mnt/nfs/software/share/STAR-STAR_2.4.1d/bin/Linux_x86_64

refgtf=/mnt/cfs/prj17a/QG77000/renqian/database/Homo_sapiens.GRCh38.87.gtf
refdata=/mnt/cfs/prj17a/QG77000/renqian/database/GRCh38.p7.fa
refoutput=/mnt/cfs/prj17a/QG77000/renqian/ref
mkdir -p $refoutput/ref
refname=STAR_GRCh38

# build ref
$RSEM/rsem-prepare-reference --gtf $refgtf \
	--star \
	--star-path $STAR  \
	-p 5 -q\
	$refdata \
	$refoutput/$refname

