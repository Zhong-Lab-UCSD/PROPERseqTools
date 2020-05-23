import glob
from collections import defaultdict
import sys
chimNum=0
targetFile=open('%s/%schimericReadPairs.csv'%(sys.argv[1],sys.argv[2]),'w')
targetFile.write('readId,R1Tx,R1start,R1end,R1Gene,R1Cigar,R2Tx,R2start,R2end,R2Gene,R2Cigar\n')
dicMapInfo_count=defaultdict(int)
for i in [1]:
    fileList=glob.glob('%s/%sintermediateFiles/chimericReadPairs_all_bwa.csv_*'%(sys.argv[1],sys.argv[2]))
    for file in fileList:
        with open(file,'r') as f:
            next(f)
            for line in f:
                splitLine=line.strip().split(',')
                [tx1,start1,end1]=splitLine[1:4]
                [tx2,start2,end2]=splitLine[6:9]
                if tx1>tx2:
                    mapInfo=','.join([tx1,start1,tx2,end2])
                else:
                    mapInfo=','.join([tx2,start2,tx1,end1])
                if dicMapInfo_count[mapInfo]==0:
                    targetFile.write(line)
                    chimNum+=1
                dicMapInfo_count[mapInfo]+=1

targetFile.close()



mapSum=0
fileList=glob.glob('%s/%sintermediateFiles/mappedStats_*.txt'%(sys.argv[1],sys.argv[2]))
for file in fileList:
    with open(file,'r') as f:
        for line in f:
            splitLine=line.strip().split(',')
            mapSum+=int(splitLine[0])

targetFile=open('%s/%ssummary.csv'%(sys.argv[1],sys.argv[2]),'a')
targetFile.write('#protein-coding_gene_mapped_read_pairs,%d\n'%(mapSum))
targetFile.write('#chimeric_read_pairs,%d\n'%(chimNum))
targetFile.close()



