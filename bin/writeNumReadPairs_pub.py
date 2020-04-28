#STATS from the exceRpt smallRNA-seq pipeline v.4.6.3 for sample serum_1.fastq. Run started at 2020-02-27--00:20:14
#input_read_pairs
#read_pairs_used_for_alignment
#protein-coding_gene_mapped_read_pairs
#chimeric read pairs
#protein-protein_interactions
import sys

i=0
haList1=[]
with open('%s/processedFastq/R1.cutadapt.fastp.fastq'%(sys.argv[1]),'r') as f:
    for line in f:
        i+=1
        if i==1:
            splitLine=line.strip().split()
            readId=splitLine[0][1:]
            haList1.append(readId)
        if i==4:
            i=0
            
            
i=0
haList2=[]
with open('%s/processedFastq/R2.cutadapt.fastp.fastq'%(sys.argv[1]),'r') as f:
    for line in f:
        i+=1
        if i==1:
            splitLine=line.strip().split()
            readId=splitLine[0][1:]
            haList2.append(readId)
        if i==4:
            i=0
bb= (len(set(haList1)&set(haList2)))


targetFile==open('%s/summary.csv'%(sys.argv[1]),'a')
targetFile.write('#read_pairs_used_for_alignment,%d\n'%(bb))
targetFile.close()
