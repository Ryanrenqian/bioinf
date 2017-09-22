GATK=/mnt/nfs/software/share/GenomeAnalysisTK-3.6/GenomeAnalysisTK.jar
ref=/mnt/cfs/prj17a/QG77000/renqian/database/GRCh38.p7.fa
java -jar $GATK -T SplitNCigarReads -R $ref -I dedupped.bam -o split.bam -rf ReassignOneMappingQuality -RMQF 255 -RMQT 60 -U ALLOW_N_CIGAR_READS
 java -jar GenomeAnalysisTK.jar \
	    -T IndelRealigner \
	       -R $ref \
	          -I split.bam \
		     -known indels.vcf \
		        -targetIntervals intervalListFromRTC.intervals \
			   -o realignedBam.bam
 java -jar GenomeAnalysisTK.jar \
	    -T PrintReads \
	       -R reference.fasta \
	          -I realignedBam.bam \
		     -BQSR recalibration_report.grp \
		        -o BQSR.bam
# variant calling
java -jar GenomeAnalysisTK.jar -T HaplotypeCaller -R $ref -I BQSR.bam -dontUseSoftClippedBases -stand_call_conf 20.0 -o ${1}.vcf
# variant filter
java -jar GenomeAnalysisTK.jar -T VariantFiltration -R hg_19.fasta -V input.vcf -window 35 -cluster 3 -filterName FS -filter "FS > 30.0" -filterName QD -filter "QD < 2.0" -o ${1}.filter.vcf 
