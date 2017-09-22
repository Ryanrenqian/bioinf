# prepare lib
path=/mnt/cfs/prj17a/QG77000/renqian/database/GRCh38_gencode_v26_CTAT_lib_July192017
prep=/mnt/nfs/user/renqian/bin/STAR-Fusion/FusionFilter/prep_genome_lib.pl
genome=$path/ref_genome.fa
gtf=$path/ref_annot.gtf
blast=$path/blast_pairs.gene_syms.outfmt6.gz
fusi=$path/fusion_lib.dat.gz
export PATH="$PATH:/mnt/nfs/user/yangjie/bin/cytoscape/Cytoscape_v3.4.0:/mnt/nfs/software/bin:/mnt/nfs/user/renqian/bin:/mnt/nfs/user/renqian/bin/RNASeqReadSimulator/src"
export PERL5LIB=/mnt/nfs/software/lib/perl5:/mnt/nfs/software/lib/perl/5.18.2:/home/yangjie/perl5/lib/perl5
$prep --genome_fa $genome --gtf $gtf --blast_pairs $blast --fusion_annot_lib $fusi

info=/mnt/nfs/user/renqian/bin/STAR-Fusion/FusionFilter/util/index_pfam_domain_info.pl
$info --pfam_domains $path/PFAM.domtblout.dat.gz --genome_lib_dir /mnt/cfs/prj17a/QG77000/renqian/ref/star-fusion


