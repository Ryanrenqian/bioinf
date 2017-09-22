java=/mnt/nfs/software/share/jre1.8.0_91/bin/java
GATK=/mnt/nfs/software/share/GenomeAnalysisTK-3.6/GenomeAnalysisTK.jar
ref=/mnt/cfs/prj17a/QG77000/renqian/database/GRCh38.p7.fa
indel=/mnt/cfs/prj17a/QG77000/renqian/database/Homo_sapiens_assembly38.known_indels.vcf
# $java -jar $GATK -T SplitNCigarReads -R $ref -I dedupped.bam -o split.bam -rf ReassignOneMappingQuality -RMQF 255 -RMQT 60 -U ALLOW_N_CIGAR_READS
name=$1
# java -Xmx1g -jar $GATK -T RealignerTargetCreator -R $ref -o intervalListFromRTC.intervals -known $indel
# java -jar $GATK -T IndelRealigner -R $ref -I split.bam -known $indel -targetIntervals intervalListFromRTC.intervals -o realignedBam.bam
# java -jar $GATK   -T PrintReads -R $ref  -I split.bam -BQSR recalibration_report.grp -o BQSR.bam
# variant calling
$java -jar $GATK -T HaplotypeCaller -R $ref -I split.bam -dontUseSoftClippedBases -stand_call_conf 20.0 -o ${1}.vcf
# variant filter
$java -jar $GATK -T VariantFiltration -R $ref -V ${1}.vcf -window 35 -cluster 3 -filterName FS -filter "FS > 30.0" -filterName QD -filter "QD < 2.0" -o ${name}.filter.vcf 
