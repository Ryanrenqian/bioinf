 
export PATH="$PATH:/mnt/nfs/user/yangjie/bin/cytoscape/Cytoscape_v3.4.0:/mnt/nfs/software/bin:/mnt/nfs/user/renqian/bin:/mnt/nfs/user/renqian/bin/RNASeqReadSimulator/src"
export PERL5LIB=/mnt/nfs/software/lib/perl5:/mnt/nfs/software/lib/perl/5.18.2:/home/yangjie/perl5/lib/perl5

STARFusion=/mnt/nfs/user/renqian/bin/STAR-Fusion/STAR-Fusion
 ref=/mnt/cfs/prj17a/QG77000/renqian/ref/ctat_genome_lib_build_dir

#  Notice!! This is solution for bam files
# $STARFusion --genome_lib_dir $ref \
#	-J Chimeric.out.junction \
#	--output_dir star_fusion_outdir

# This is solution for fq files
 fq1=$1
 fq2=$2
 $STARFusion --genome_lib_dir $ref \
	--left_fq $fq1 \
	--right_fq $fq2 \
	--output_dir star_fusion_outdir

