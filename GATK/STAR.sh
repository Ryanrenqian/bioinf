STAR=/mnt/nfs/user/renqian/bin/STAR-2.5.3a/bin/Linux_x86_64/STAR

genomedir=/mnt/cfs/prj17a/QG77000/renqian/ref/star
fa=/mnt/cfs/prj17a/QG77000/renqian/database/GRCh38.p7.fa
gtf=/mnt/cfs/prj17a/QG77000/renqian/database/Homo_sapiens.GRCh38.87.gtf
readlength=151

# $STAR --runThreadN 8 --runMode genomeGenerate --genomeDir $genomedir --genomeFastaFiles $fa --sjdbGTFfile $gtf --sjdbOverhang $readlength-1

read1=/mnt/cfs/prj17a/QG77000/renqian/raw_data/patient_10/*1.fastq.gz
read2=/mnt/cfs/prj17a/QG77000/renqian/raw_data/patient_10/*2.fastq.gz

#mapping

echo STAR --runThreadN 8 \
	--runMode alignReads \
	--genomeDir $genomedir \
	--readFilesIn $read1 $read2 --readFilesCommand zcat \
	--sjdbGTFfile $gtf \
	--chimSegmentMin 30 \
	--outFileNamePrefix startest
echo mapping

$STAR --runThreadN 8 \
	--twopassMode Basic \
	--chimSegmentMin 12 \
	--chimJunctionOverhangMin 12 \
	--chimSegmentReadGapMax parameter 3 \
	--alignIntronMax 100000 \
	--genomeDir $genomedir \
	--readFilesIn $read1 $read2 \
	--readFilesCommand zcat \
	--sjdbGTFfile $gtf \
	--limitBAMsortRAM 31532137230 \
	--outFileNamePrefix star
