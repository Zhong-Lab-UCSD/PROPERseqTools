from datetime import datetime
import sys

# get current date
datetime_object = datetime.now()
targetFile=open('%s/%sintermediateFiles/runStart.txt'%(sys.argv[1],sys.argv[2]),'w')
targetFile.write('#Run starts at %s. Job ID:%s\n'%(str(datetime_object),sys.argv[2][:-1]))
targetFile.close()