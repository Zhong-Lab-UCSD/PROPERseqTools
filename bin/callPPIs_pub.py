from collections import defaultdict
import scipy
import glob
import scipy.stats as stats
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
import sys

targetFile=open('%s/%sproteinProteinInteractions.csv'%(sys.argv[1],sys.argv[5]),'a')

def getIntCount(filePath):
    dicIntCount_positive=defaultdict(int)
    dicProteinCount_positive=defaultdict(int)
    fileList=glob.glob(filePath)
    for filePath in fileList:
        with open(filePath,'r') as f:
            next(f)
            for line in f:
                splitLine=line.strip().split(',')
                gene1,gene2=splitLine[4],splitLine[9]
                if gene1>gene2:
                    pair=';'.join([gene1,gene2])
                else:
                    pair=';'.join([gene2,gene1])
                dicProteinCount_positive[gene1]+=1
                dicProteinCount_positive[gene2]+=1
                dicIntCount_positive[pair]+=1        
    #sort
    sorted_x_positive = sorted(dicIntCount_positive.items(), key=lambda kv: kv[1],reverse=True)
    return dicIntCount_positive,dicProteinCount_positive,sorted_x_positive

def identifyPPIs_chimericAdj(sorted_x_positive1_9,dicIntCount_positive1_9,dicProteinCount_positive1_9,coEff,pCutOff,oddsCutoff):
    factor=sum([x[1] for x in sorted_x_positive1_9])/len(sorted_x_positive1_9)
    chimTotal=sum([x[1] for x in sorted_x_positive1_9])
    pvalueList=[]
    sorted_x_1_select=[]
    selectList_1=[]
    posRCList_1=[]
    orList_1=[]
    chiList=[]
    for ha in sorted_x_positive1_9:
        [gene1,gene2]=ha[0].split(';')
        a=dicIntCount_positive1_9[ha[0]]
        b=dicProteinCount_positive1_9[gene1]/2-a
        c=dicProteinCount_positive1_9[gene2]/2-a
        d=chimTotal-a-b-c
        b,c=max(0,b),max(0,c)
        oddsRatio=(a+1)*(d+1)/(b+1)/(c+1)
        chi2, p, dof, ex=stats.chi2_contingency([[a+1,b+1],[c+1,d+1]])
        orList_1.append(oddsRatio)
        pvalueList.append(p)
        sorted_x_1_select.append(ha)
        selectList_1.append(ha[0])
        posRCList_1.append(a)
        chiList.append(chi2)


    stats1 = importr('stats')
    pvalueList_adj_1=stats1.p_adjust(FloatVector(pvalueList), method = 'BH')

    lolCount=0
    count=0
    list1=[]
    rcList1=[]
    pvalueSig_1=[]
    orSig_1=[]
    chiSig=[]
    for i in range(len(selectList_1)):
        ha=selectList_1[i]
        count+=1
        gene1,gene2=ha.split(';')
        pAdj=pvalueList_adj_1[i]
        rcc=posRCList_1[i]
        orr=orList_1[i]
        chichi=chiList[i]
        if pAdj<=pCutOff and rcc>coEff*factor and 'MTRNR' not in gene1 and 'MTRNR' not in gene2 and orr>oddsCutoff:
            lolCount+=1
            list1.append(ha)
            pvalueSig_1.append(pAdj)
            orSig_1.append(orList_1[i])
            rcList1.append(rcc)
            chiSig.append(chichi)
    print (len(set(list1)))
    return list1,rcList1,orSig_1,chiSig,pvalueSig_1


dicIntCount_positive_8b,dicProteinCount_positive_8b,sorted_x_positive_8b=getIntCount(
    '%s/%schimericReadPairs.csv'%(sys.argv[1],sys.argv[5]))


list_PPI,rcList_PPI,orList_PPI,chiList_PPI,pvalueList_PPI=identifyPPIs_chimericAdj(
    sorted_x_positive_8b,dicIntCount_positive_8b,dicProteinCount_positive_8b,float(sys.argv[4]),float(sys.argv[2]),float(sys.argv[3]))

#write into the file
targetFile.write('Protein1,Protein2,ReadCount,FDR,oddsRatio,chiSquareStat\n')
for i in range(len(list_PPI)):
    ha=list_PPI[i]
    [gene1,gene2]=ha.split(';')
    oddsRatio=str(orList_PPI[i])
    chichi=str(chiList_PPI[i])
    pp=str(pvalueList_PPI[i])
    rc=str(dicIntCount_positive_8b[ha])
    infoList=','.join([gene1,gene2,rc,pp,oddsRatio,chichi])
    targetFile.write(infoList)
    targetFile.write('\n')
    
targetFile.close()


targetFile=open('%s/%ssummary.csv'%(sys.argv[1],sys.argv[5]),'a')
targetFile.write('#protein-protein_interactions,%d\n'%(len(list_PPI)))
targetFile.close()
