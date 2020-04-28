from datetime import datetime
import sys

# get current date
datetime_object = datetime.now()
targetFile=open('%s/intermediateFiles/runStart.txt'%(sys.argv[1]),'w')
targetFile.write('#Run starts at %s. Job ID:\n'%(str(datetime_object)))
targetFile.close()