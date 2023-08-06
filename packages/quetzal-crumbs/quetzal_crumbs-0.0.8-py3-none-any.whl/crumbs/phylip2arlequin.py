from optparse import OptionParser
import csv
from collections import defaultdict

# options
parser = OptionParser()
parser.add_option("--input", type="str", dest="input", help="phylip input file")
parser.add_option("--imap", type="str", dest="imap", help="mapping individuals to populations")
parser.add_option("--output", type="str", dest="output", help="arlequin output file")

(options, args) = parser.parse_args()

id_to_pop = {}
pop_set = set()

with open(options.imap, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        id_to_pop[row[0]]=row[1]
        pop_set.add(row[1])

id_to_seq = {}
with open(options.input, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    next(reader)
    for row in reader:
        caret_ID = row[0]
        ID = caret_ID[1:]
        id_to_seq[ID] = row[1]

pop_to_ids = defaultdict(list)
pop_to_seqs = defaultdict(list)
for id, pop in id_to_pop.items():
    pop_to_ids[pop].append(id)
    pop_to_seqs[pop].append(id_to_seq[id])

seq_to_ids = defaultdict(list)
for id, seq in id_to_seq.items():
    seq_to_ids[seq].append(id)

seq_to_arl_ID = {}
i = 0
for s in seq_to_ids:
    seq_to_arl_ID[s] = i;
    i += 1


nb_samples = len(pop_set)

output = (
"[Profile]\n\t" +
'''Title="Simulated DNA sequence data"''' + "\n"
"\tNbSamples=" + str(nb_samples) + "\n" +
"\tGenotypicData=0\n" +
"\tDataType=DNA\n" +
"\tLocusSeparator=NONE\n" +
"[Data]\n" +
"\t[[Samples]]")

for pop in pop_set:
    sample_size = len(pop_to_ids[pop])
    output = (output +
    "\n\t\tSampleName=" + '''"'''+ pop + '''"''' + "\n" +
    "\t\tSampleSize=" + str(sample_size) + "\n" +
    "\t\tSampleData={\n")
    for id in pop_to_ids[pop]:
        seq = id_to_seq[id]
        arl_id = seq_to_arl_ID[seq]
        count = pop_to_seqs[pop].count(seq)
        output = (output +
        str(arl_id) + "\t" + str(count) + "\t" + seq + "\n")
    output = output + "}\t"

output = ( output +
"\n\t[[Structure]]\n\n\t\t" +
'''StructureName="A group of simulated populations"''' + "\n"
"\t\tNbGroups=1\n\n" +
"\t\tGroup={\n")

for pop in pop_set:
    output = output + "\t\t\t" + '''"''' + pop + '''"''' + "\n"

output = output + "\t\t}"

outfile = open(options.output,'w')
outfile.write(output)
outfile.close()
