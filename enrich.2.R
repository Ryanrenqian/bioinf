#!/usr/bin/env Rscript

library(getopt)

#read arguments
opt=getopt(matrix(c(
        'help', 'h', 0, "logical",
        'genelist', 'l', 1, "character",
	'background', 'g', 1, "character",
        'type', 't', 1, "integer",
        'geneset', 'p', 1, "character",
        'genesetdesc', 'b', 1, "character",
        'geneinfo', 'f', 2, "character",
        'outputgene', 'u', 2, "logical",
        'image', 'm', 2, "logical",
        'species', 's', 2, "integer",
        'output', 'o', 1, "character",
		'qvalue', 'e', 2, "double",
		'number', 'n', 2, "integer",
		'width', 'w', 2, "integer"
        ),ncol=4,byrow=TRUE))

if( !(is.null(opt$help)) || is.null(opt$genelist) || is.null(opt$type) )
{
        cat( paste0(
                "Geneset Enrichment Calculator using clusterProfiler. Version 1.1        limiao@yucebio.com\n\n", 
                "Usage: Rscript enrich.R [arguments]\n",
                "-h     --help			Show this help.\n",
                "-l     --genelist		Input gene list file.(Gene	...)\n",
                "-t     --type			Calculation type. 1: GO; 2: KEGG.\n",
                "-p     --geneset		Gene set file(Geneset	Gene)\n",
                "-b     --genesetdesc		Gene set description file(Geneset Description)\n",
                "-f     --geneinfo		NCBI Gene info file. Required for type 2\n",
                "-u     --outputgene		Output gene name in each geneset\n",
                "-m     --image			Plot image\n",
                "-w     --width			Width of the plot. Default 14.\n",
                "-s     --species		Species. 1: Human; 2: Mouse\n",
                "-o     --output		Output file name.\n",
                "-e     --qvalue		q-value threshold. Default: 0.05\n",
                "-n     --number		Number of KEGG plot. Default 5\n"
        ))
        quit()
}

qvalue = 0.05
if(!(is.null(opt$qvalue))) {
	qvalue = opt$qvalue
}

maxplot = 5
if(!(is.null(opt$number))) {
	maxplot = opt$number
}

plotwidth = 14
if(!(is.null(opt$width))) {
	plotwidth = opt$width
}

if(opt$species == 2) {
	annodb = "org.Mm.eg.db"
	organism = "mouse"
	species = "mmu"
	graphpath = "/mnt/nfs/database/mm10/kegg/graph"
} else {
	annodb = "org.Hs.eg.db"
	organism = "human"
	species = "hsa"
	graphpath = "/mnt/nfs/database/hg19/kegg/graph"
}

library(clusterProfiler)

mergespec <- function(x, spec) {
	return(paste0(spec, ":", x))
}

convertgeneid <- function(x) {
	geneid <- unlist(strsplit(x, "/", fixed = T))
	gene <- gsub(paste0(species, ':'), '', geneid)
	gene <- bitr(gene, fromType="ENTREZID", toType="SYMBOL", annoDb=annodb)$SYMBOL
	geneid <- paste(gene, seq='', collapse='')
	return(geneid)
}

savetable <- function(ego, filename, cutoff) {
	output <- summary(ego)
	o <- order(output$qvalue)
	
	output <- output[output$qvalue<cutoff,]
	if(is.null(opt$outputgene)) {
		outputfile <- data.frame(output$ID, output$Description, output$pvalue, output$qvalue, output$Count)
		colnames(outputfile) <- c("ID", "Description", "pvalue", "qvalue", "Count")
	} else {
		# for KEGG, convert gene id to symbol
		if(opt$type == 2) {
			output$geneID <- sapply(as.character(output$geneID), convertgeneid)
		}
		outputfile <- data.frame(output$ID, output$Description, output$pvalue, output$qvalue, output$Count, output$geneID)
		colnames(outputfile) <- c("ID", "Description", "pvalue", "qvalue", "Count", "Gene")
	}
	write.table(outputfile, file=filename, row.names = F, quote=F, sep = "\t")
	return(output)
}

savegraph <- function(ego, filename) {
	pdf(file=filename, width=plotwidth)
	plot(dotplot(ego, showCategory=20))
	#cnetplot(ego, categorySize="pvalue", foldChange=genelist$logFC, vertex.label.cex=0.3)
	if(opt$type == 1) {
		try(plotGOgraph(ego))
	}
	dev.off()
}
back <-read.delim(opt$background, header=T)
genelist <- read.delim(opt$genelist, header=T)
geneset <- read.delim(opt$geneset, header=F, comment.char = "!")
genesetdesc <- read.delim(opt$genesetdesc, header=F)
if(opt$type == 1) {
	gene <- back$Gene
	#gene <- genelist$Gene
	term2gene <- data.frame(geneset[5], geneset[3])
	term2name <- data.frame(genesetdesc[1], genesetdesc[2])
} else {
	## old gene symbol to gene id convert script
	# ncbi.L1 <- readLines(opt$geneinfo, n = 1)
	# ncbi.colname <- unlist(strsplit(substring(ncbi.L1, 10, 234), ' '))
	# ncbi <- read.delim(opt$geneinfo, skip=1, header=FALSE, stringsAsFactors=FALSE)
	# colnames(ncbi) <- ncbi.colname
	# m <- match(genelist$Gene, ncbi$Symbol)
	# gene <- ncbi$GeneID[m]
	# gene <- gene[!is.na(gene)]
	
	## new convert script
	gene <- bitr(back$Gene, fromType="SYMBOL", toType="ENTREZID", annoDb=annodb)$ENTREZID
	#gene <- bitr(genelist$Gene, fromType="SYMBOL", toType="ENTREZID", annoDb=annodb)$ENTREZID
	term2gene <- geneset
	term2name <- genesetdesc
	gene <- sapply(gene, mergespec, spec=species)
}
print('___________---------------------------_________________')
x = enricher(gene, TERM2GENE=term2gene, TERM2NAME=term2name, pvalueCutoff = 1, qvalueCutoff = 1)
print(x)
#output = savetable(x, paste0(opt$output, ".unfiltered", ".xls"), 1)

x = enricher(gene, TERM2GENE=term2gene, TERM2NAME=term2name, pvalueCutoff = qvalue, qvalueCutoff = qvalue)
#output = savetable(x, opt$output, qvalue)
#savegraph(x, paste0(opt$output, ".pdf"))

if(!is.null(opt$image)) {
	library(pathview)
	if(opt$type == 1) {
		background <- bitr(back$Gene, fromType="SYMBOL", toType="ENTREZID", annoDb=annodb)$ENTREZID
		#background <- bitr(genelist$Gene, fromType="SYMBOL", toType="ENTREZID", annoDb=annodb)$ENTREZID
		genes <- genelist$Gene#[abs(genelist$logFC) > 0]
		gene <- bitr(genes, fromType="SYMBOL", toType="ENTREZID", annoDb=annodb)$ENTREZID
		#remove genes not in GO
		#gogenes <- bitr(gene, fromType="ENTREZID", toType="GO", annoDb=annodb)$ENTREZID
		#gene <- gene[gene %in% gogenes]
		ego <- enrichGO(gene = gene, organism = organism, ont = "MF", pAdjustMethod = "BH", pvalueCutoff = qvalue, qvalueCutoff = qvalue, readable = TRUE)
		savetable(ego, paste0(opt$output, ".f", ".xls"), qvalue)
		savegraph(ego, paste0(opt$output, ".f", ".pdf"))
		
		ego <- enrichGO(gene = gene, organism = organism, ont = "BP", pAdjustMethod = "BH", pvalueCutoff = qvalue, qvalueCutoff = qvalue, readable = TRUE)
		savetable(ego, paste0(opt$output, ".p", ".xls"), qvalue)
		savegraph(ego, paste0(opt$output, ".p", ".pdf"))
		ego <- enrichGO(gene = gene, organism = organism, ont = "CC", pAdjustMethod = "BH", pvalueCutoff = qvalue, qvalueCutoff = qvalue, readable = TRUE)
		savetable(ego, paste0(opt$output, ".c", ".xls"), qvalue)
		savegraph(ego, paste0(opt$output, ".c", ".pdf"))
	} else {
		pdf(file=paste0(opt$output, ".pdf"), width=plotwidth)
	        plot(dotplot(x, showCategory=20))
		dev.off()
		geneid <- bitr(genelist, fromType="SYMBOL", toType="ENTREZID", annoDb=annodb)
		#geneid <- bitr(genelist$Gene, fromType="SYMBOL", toType="ENTREZID", annoDb=annodb)
        colnames(geneid) <- c("Gene", "ENTREZID")
        geneid  <- merge(geneid, genelist, by = "Gene")
		genes <- geneid$logFC
		names(genes) <- geneid$ENTREZID
		if(length(output$ID) > maxplot) {
			totallen = maxplot
		} else {
			totallen = length(output$ID)
		}
		for(i in 1:totallen) {
			pathway <- strsplit(as.character(output$ID[i]), ":")[[1]][2]
			xmlfile <- paste0(graphpath, "/", pathway, ".xml")
			if(!file.exists(xmlfile)) {
			#	command <- paste0("wget -O ", xmlfile, " http://rest.kegg.jp/get/", pathway, "/kgml")
			#	system(command)
			}
			pngfile <- paste0(graphpath, "/", pathway, ".png")
			if(!file.exists(pngfile)) {
			#	command <- paste0("wget -O ", xmlfile, " http://rest.kegg.jp/get/", pathway, "/image")
			#	system(command)
			}
			#pathview(gene.data = genes, pathway.id = pathway, species = species, kegg.dir = graphpath, limit = list(gene=max(abs(genes)), cpd=1))
			pathview(gene.data = genes, pathway.id = pathway, species = species, kegg.dir = graphpath, limit = list(gene=5, cpd=1))
		}
	}
}
