import sys

lineCount=0
fileIndex=0
idBreakList=[]
switchPrepare=False
targetFile=open('%s/read1_tx/mapped.sorted.bed_chunk%d'%(sys.argv[1],fileIndex),'w')
with open('%s/read1_tx/mapped.sorted.bed'%(sys.argv[1]),'r') as f:
    for line in f:
        lineCount+=1
        splitLine=line.strip().split('\t')
        readId=splitLine[3]
        if switchPrepare:
        #check if it is a new read
            #not a new read
            if prepareId==readId:
                targetFile.write(line)
            #new read, perform switch
            else:
                #close the current file
                targetFile.close()
                #add index and open a new one
                fileIndex+=1
                targetFile=open('%s/read1_tx/mapped.sorted.bed_chunk%d'%(sys.argv[1],fileIndex),'w')
                targetFile.write(line)
                #reset lineCount and switch prepare
                switchPrepare=False
                lineCount=0
                #store Id breaker
                idBreakList.append(prepareId)
        else:
            targetFile.write(line)
            if lineCount>=80000000:
                switchPrepare=True
                prepareId=readId
                
targetFile.close()
print ('haha')



#open the second file
idBreakList.append('ZZZZZZZZ')
fileIndex=0
switchPrepare=False
targetFile=open('%s/read2_tx/mapped.sorted.bed_chunk%d'%(sys.argv[1],fileIndex),'w')
flagId=idBreakList[fileIndex]
with open('%s/read2_tx/mapped.sorted.bed'%(sys.argv[1]),'r') as f:
    for line in f:
        lineCount+=1
        splitLine=line.strip().split('\t')
        readId=splitLine[3]
        #perform switch
        if readId>flagId:
            #close the current file
            targetFile.close()
            #add index and open a new one
            fileIndex+=1
            targetFile=open('%s/read2_tx/mapped.sorted.bed_chunk%d'%(sys.argv[1],fileIndex),'w')
            #reset flagId
            flagId=idBreakList[fileIndex]
        targetFile.write(line)
            
                
targetFile.close()