# PROPERseqTools

## Overview
Protein-protein Interaction Sequencing (PROPER-seq) is a high-throughput sequencing technology that efficiently maps cell wide protein-protein interactions in vitro. Here, we distribute PROPERseqTools, a standardized data processing pipeline to identify protein-protein interactions from fastq files of PROPER-seq experiments.<br />
The schematic diagram below describes the various stages of the PROPERseqTools pipeline including pre-processing of the raw reads, alignment to the transcritome, identification of chimeric read pairs and identification of protein-protein interactions.
![](https://github.com/Zhong-Lab-UCSD/PROPERseqTools/blob/master/image.png)


## Software Requirements
Latest version of required software is recommended
- [Cutadapt](https://cutadapt.readthedocs.io/en/stable/)
- [fastp](https://github.com/OpenGene/fastp)
- [bwa](https://github.com/lh3/bwa)
- [samtools](http://www.htslib.org/)
- [bedtools](https://bedtools.readthedocs.io/en/latest/)
- Python 3.4 or later, the following python libraries are required:<br />
    - sys
    - collections
    - cigar
    - glob
    - scipy
    - rpy2
    - datetime
## Additional files required
**BWA Index of the transcriptome to be aligned**<br />
You will need to download or build the bwa index of the target trancriptome for PROPERseqTools to use. Here we provide the compressed bwa index built from [RefSeq GRCh38 transcriptome](https://drive.google.com/file/d/1lAV-dVVwVaPi-qVLXibaAvgjtd1e-QMT/view?usp=sharing)

**Transcript, gene and gene type dictionary file**<br />
You will also need a dictionary file that contains the information of transcript ids to their corresponding gene names/gene ids and corresponding gene types in a csv format with the first column being transcript ids, the second column being gene names and the third column being gene types. Here we provide an example dictionary file for [RefSeq GRCh38 genome](https://github.com/Zhong-Lab-UCSD/PROPERseqTools/blob/master/refSeq_tx_gene_type.csv)



## Usage
**Installation**
1. Clone the current github repository to your local machine. For example<br />
`git clone https://github.com/qizhijie/PROPERseqTools`
2. Add the following path of the cloned directory to your `.bashrc` file<br />
`export PATH=$PATH:/home/path/to/PROPERseqTools/bin`

**To excute PROPERseqTools, run**
<pre><code>
properseqTools -a /path/to/read1.fastq
               -b /path/to/read2.fastq
               -i /path/to/bwaIndex/transcriptome.fa
               -o /path/to/outputDir
           
</code></pre>



**Required parameters**
<pre><code>
-a     |String, Path to read1 fastq file
-b     |String, Path to read2 fastq file
-o     |String, Path to output directory
-i     |String, Path to bwa index of the target transcriptome
-g     |String, Path to transcirpt, gene and gene type dictionary file
</code></pre>
**Other parameters**
<pre><code>
-d     |Float, odds ratio cutoff used to identify protein-protein interactions, default=1
-p     |Float, false discovery rate cutoff used to identify protein-protein interactions, default=0.05
-c     |Float, read count cutoff coefficient used to identify protein-protein interactions, default=4
-t     |Int, Number of working threads, default=2
-r     |Char, (T or F), removal of intermediate files or not, default=T
-h     |Print usage message" 
           
</code></pre>

## PROPEPseqTools Output
A variety of output files are created for each sample as they are run through the pipeline. The highest level of the output directory contains the following files and subdirectories:
<pre><code>
proteinProteinInteractions.csv    |a file that contains the identified protein-protein interactions from the sample
chimericReadPairs.csv             |a file that contains the read ids of the identified chimeric read pairs from the sample
summary.csv                       |a file that contains the summary statistics of running the sample with PROPERseqTools
errorLog.txt                      |a file that contains error message from the pipeline if any
processedFastq/                   |a directory that contains the pre-processed fastq files from the sample
alignment/                        |a directory that contains the alignment files of the pre-processed fastq files from the sample
intermediateFiles/                |an optional directory contains all the intermediat files generated from running the pipeline, this direcotry only exists if '-r' option is set to 'F' 
           
</code></pre>

## Example Output
In this repository, we provide example outputs of this pipeline using the PROPER-seq data published in xxx.<br />
- [`proteinProteinInteractions.csv`](...) <br />
- [`chimericReadPairs.csv`](...)
- [`summary.csv`](...)
