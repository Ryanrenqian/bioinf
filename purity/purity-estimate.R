library('estimate')
args<-commandArgs(T)
file=args[1]
filterCommonGenes(input.f=file, output.f="gene.gct", id="GeneSymbol")
estimateScore("gene.gct", "purity_estimate_score.gct")
plotPurity(scores="purity_estimate_score.gct", samples="LUAD_G1_01T")
