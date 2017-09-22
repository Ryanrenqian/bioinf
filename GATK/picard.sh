picard=/mnt/nfs/software/share/picard-tools-1.134/picard.jar
java -jar $picard AddOrReplaceReadGroups I=$1 O=rg_added_sorted.bam SO=coordinate RGID=id RGLB=library RGPL=platform RGPU=machine RGSM=sample 
java -jar $picard MarkDuplicates I=rg_added_sorted.bam O=dedupped.bam  CREATE_INDEX=true VALIDATION_STRINGENCY=SILENT M=output.metrics 

