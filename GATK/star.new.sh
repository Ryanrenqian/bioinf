fq1=$1
fq2=$2
STAR=/mnt/nfs/user/renqian/bin/STAR-2.5.3a/bin/Linux_x86_64/STAR
ref=/mnt/cfs/prj17a/QG77000/renqian/ref/star
$STAR --genomeDir $ref \
	--readFilesIn $fq1 $fq2 --readFilesCommand zcat \
	--twopassMode Basic \
	--outReadsUnmapped None \
	--chimSegmentMin 12 \
	--chimJunctionOverhangMin 12 \
	--alignSJDBoverhangMin 10 \
	--alignMatesGapMax 100000 \
	--alignIntronMax 100000 \
	--chimSegmentReadGapMax parameter 3 \
	--alignSJstitchMismatchNmax 5 -1 5 5 \
	--runThreadN 8 \
	--outSAMtype BAM Unsorted 
