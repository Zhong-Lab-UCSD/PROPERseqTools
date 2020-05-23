import sys


targetFile=open(sys.argv[1],'w')
count=0
lineStore=[]
yeye=0
fCount=0
total=0
with open(sys.argv[2],'r') as f:
    for line in f:
        count+=1
        total+=1
        lineStore.append(line)
        if count==4:
            readLength=len(line)-1
            if readLength>=20:
                for ha in lineStore:
                    targetFile.write(ha)
                yeye+=1
            else:
                fCount+=1
            count=0
            lineStore=[]            
targetFile.close()
total=total/4
if sys.argv[4]=='yes':
    targetFile=open('%s/%ssummary.csv'%(sys.argv[3],sys.argv[5]),'a')
    targetFile.write('#input_read_pairs,%d\n'%(total))
    targetFile.close()