
import sys

i=0
haList1=[]
with open('%s/%sprocessedFastq/R1.cutadapt.fastp.fastq'%(sys.argv[1],sys.argv[2]),'r') as f:
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
with open('%s/%sprocessedFastq/R2.cutadapt.fastp.fastq'%(sys.argv[1],sys.argv[2]),'r') as f:
    for line in f:
        i+=1
        if i==1:
            splitLine=line.strip().split()
            readId=splitLine[0][1:]
            haList2.append(readId)
        if i==4:
            i=0
bb= (len(set(haList1)&set(haList2)))


targetFile=open('%s/%ssummary.csv'%(sys.argv[1],sys.argv[2]),'a')
targetFile.write('#read_pairs_used_for_alignment,%d\n'%(bb))
targetFile.close()
