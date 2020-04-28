from collections import defaultdict
import sys
from cigar import Cigar


#read in refseq dic
dicIdGeneName={}
dicIdGeneType={}
with open('%s'%(sys.argv[3]),'r') as f:
    for line in f:
        splitLine=line.strip().split(',')
        dicIdGeneName[splitLine[0]]=splitLine[1]
        dicIdGeneType[splitLine[0]]=splitLine[2]
        
        
    
#read in read1 and read2 file
dicReadIdGene1=defaultdict(list)
dicReadIdGene2=defaultdict(list)
dicReadIdPos1=defaultdict(list)
dicReadIdPos2=defaultdict(list)
dicIdtoCigar1=defaultdict(list)
dicIdtoCigar2=defaultdict(list) 

#Count protein-coding mapped read pairs
dicRead1_count=defaultdict(int)
with open('%s/alignment/read1_tx/mapped.sorted.bed_chunk%s'%(sys.argv[1],sys.argv[2]),'r') as f:
    for line in f:
        splitLine=line.strip().split('\t')
        readId=splitLine[3]
        txId=splitLine[0]
        cigar1=splitLine[6]
        if dicIdGeneType[txId]=='mRNA':
            dicRead1_count[readId]+=1
            dicReadIdGene1[splitLine[3]].append(dicIdGeneName[splitLine[0]])
            dicReadIdPos1[splitLine[3]].append(splitLine[:3])
            dicIdtoCigar1[readId].append(cigar1)
            
idList=[]
with open('%s/alignment/read2_tx/mapped.sorted.bed_chunk%s'%(sys.argv[1],sys.argv[2]),'r') as f:
    for line in f:
        splitLine=line.strip().split('\t')
        readId=splitLine[3]
        txId=splitLine[0]
        cigar2=splitLine[6]
        if dicIdGeneType[txId]=='mRNA' and dicRead1_count[readId]>0:
            idList.append(readId)
            dicReadIdGene2[splitLine[3]].append(dicIdGeneName[splitLine[0]])
            dicReadIdPos2[splitLine[3]].append(splitLine[:3])
            dicIdtoCigar2[readId].append(cigar2)

idList=list(set(idList))            
#identify chimeric reads
targetFile=open('%s/intermediateFiles/chimericReadPairs_all_bwa.csv_%s'%(sys.argv[1],sys.argv[2]),'w')
targetFile.write('readId,R1Tx,R1start,R1end,R1Gene,R1Cigar,R2Tx,R2start,R2end,R2Gene,R2Cigar\n')
count=0
for readId in idList:
    geneList1=dicReadIdGene1[readId]
    geneList2=dicReadIdGene2[readId]
    #no common genes
    if len(set(geneList1)&set(geneList2))==0:
        [txId1,start1,end1]=dicReadIdPos1[readId][0]
        [txId2,start2,end2]=dicReadIdPos2[readId][0]
        if dicIdGeneType[txId1]=='mRNA' and dicIdGeneType[txId2]=='mRNA':
            #check cigar string
            cigar1,cigar2=Cigar(dicIdtoCigar1[readId][0]),Cigar(dicIdtoCigar2[readId][0])
            cigar1List=list(cigar1.items())
            cigar2List=list(cigar2.items())
            flag1=False
            flag2=False
            totalLength1=float(sum([x[0] for x in cigar1List]))
            totalLength2=float(sum([x[0] for x in cigar2List]))
            if cigar1List[0][1]=='M' and cigar1List[0][0]/totalLength1>=0.5:
                flag1=True
            if (cigar1List[0][1]=='S' or cigar1List[0][1]=='H') and cigar1List[0][0]/totalLength1<=0.2:
                if cigar1List[1][1]=='M' and cigar1List[1][0]/totalLength1>=0.5:
                    flag1=True
            if cigar2List[0][1]=='M' and cigar2List[0][0]/totalLength2>=0.5:
                flag2=True
            if (cigar2List[0][1]=='S' or cigar2List[0][1]=='H') and cigar2List[0][0]/totalLength2<=0.2:
                if cigar2List[1][1]=='M' and cigar2List[1][0]/totalLength2>=0.5:
                    flag2=True
            if flag1 and flag2:
                gene1,gene2=dicIdGeneName[txId1],dicIdGeneName[txId2]
                #write file
                targetFile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'
                                 %(readId,txId1,start1,end1,gene1,str(cigar1),txId2,start2,end2,gene2,str(cigar2)))
                count+=1

targetFile.close()

targetFile=open(sys.argv[4],'w')
targetFile.write('%d,%d'%(len(idList),count))
targetFile.close()
            


