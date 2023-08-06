""" Align a group of sequences and calculate a contact map.

Run syntax: "python step1.py <seq_fn> <pdb_fn> <out_prefix>"
Example: "python step1.py bgl3_parents.fasta 1gnx.pdb bgl3"

Command Line Args:
    seq_fn: name of sequences file read by muscle
    pdb_fn: name of PDB file used to make contact map. If "search", script will
        search PDB database and find structure with closest identity to first
        parent sequence
    out_prefix: prefix on output files

Outputs:
    <out_prefix>_AA.fasta: name of aligned amino acid sequences file, used in
        step 2 and step 4
    <out_prefix>_contacts.json: name of calculated contacts file, used in
        step 2
    <out_prefix>_CDN.fasta: name of aligned codon sequences file, used in
        step 4
    renumbered_<pdb_fn>: name of renumber pdb file
    <out_prefix_PDB.fasta>: name of pdb alignment file

It takes as input a sequence fasta file and a PDB structure file. The sequence
fasta should list the parent amino acid sequences for SCHEMA-RASPP, with
(preferably only) the name of each sequence in the headers. The PDB structure
will be aligned to the output multiple sequence alignment and renumbered
accordingly.

The main output files are "<out_prefix>_AA.fasta",
"<out_prefix>_contacts.json", and "<out_prefix>_CDN.fasta", which are used in
later steps. "renumbered_<pdb_fn>" and "<out_prefix>_PDB.fasta" are also output
for logging purposes.

You can also replace all instances of "sys.argv" in the code with the input
filenames directly, then run "python step1.py".

Contacts are defined as pairs of residues in the PDB file that have a distance
of 4.5 angstroms measured at their closest atoms. <pdb_fn> must be in PDB
format, but is not required to be from the Protein Data Bank. Programs such
as MODELLER can generate predicted structures for a given sequence, which
can then be used as an input pdb file.

BioPython and Muscle are required packages. The Romero Lab group server has
both installed.
"""

import json
import os
import sys

from Bio import Seq, SeqRecord, SeqIO

from tools import step1_tools

seq_fn = sys.argv[1]  # name of sequences file read by muscle
pdb_fn = sys.argv[2]  # name of PDB file used to make contact map
out_prefix = sys.argv[3]  # prefix of output files

if pdb_fn == 'search':
    print('Searching pdb database for closest structure match to first parent',
          flush=True)
    p1 = list(SeqIO.parse(seq_fn, 'fasta'))[0]
    pdb_fn = step1_tools.get_pdb(str(p1.seq))

step1_tools.run_muscle(seq_fn, out_prefix + '_AA.fasta')

# Load muscle output fasta file
print('Loading muscle output', flush=True)
alignment_SRs = list(SeqIO.parse(f'{out_prefix}_AA.fasta', 'fasta'))
names = [str(i.id) for i in alignment_SRs]
AA_seqs = [str(i.seq) for i in alignment_SRs]
AA_alignment = list(zip(*AA_seqs))  # list of AAs at each position

# Load sequence from pdb and temporarily add to AA alignment
print('Loading pdb file', flush=True)
pdb_AAs = step1_tools.read_PDB(pdb_fn)
pdb_Seq = step1_tools.get_PDB_seq(pdb_AAs)
pdb_Seq = Seq.Seq(pdb_Seq)
pdb_SeqRecord = SeqRecord.SeqRecord(pdb_Seq, name='PDB')
temp_SRs = [pdb_SeqRecord] + alignment_SRs

# Align pdb sequence to AA aligned sequences
print('Aligning pdb sequence to AA aligned sequencing', flush=True)
SeqIO.write(temp_SRs, 'temp_seqs.fasta', 'fasta')
step1_tools.run_muscle('temp_seqs.fasta', f'{out_prefix}_PDB.fasta')
os.remove('temp_seqs.fasta')
pdb_align_SRs = SeqIO.parse(f'{out_prefix}_PDB.fasta', 'fasta')
pdb_align_seqs = [str(i.seq) for i in pdb_align_SRs]
pdb_alignment = list(zip(*pdb_align_seqs))

# Renumber pdb residues and save new pdb
print('Renumbering pdb file', flush=True)
pdb_AAs_residue = iter(pdb_AAs)
pos = 0    # PDB will be 1-indexed for consistency with other PDB files
for pdb_AA, *parent_AAs in pdb_alignment:
    valid_parent_pos = any([a != '-' for a in parent_AAs])
    if valid_parent_pos:
        pos += 1
    if pdb_AA != '-':
        AA = next(pdb_AAs_residue)
        assert step1_tools.seq1(AA.resName) == pdb_AA
        if valid_parent_pos:
            AA.resSeq = pos
        else:
            AA.resSeq = None
step1_tools.write_PDB(pdb_AAs, 'renumbered_' + pdb_fn)

# Calculate contacts
print('Calculating contacts', flush=True)
pdb_AAs = list(step1_tools.read_PDB('renumbered_' + pdb_fn))
for AA in pdb_AAs:
    AA.resSeq -= 1   # make index start from 0
contacts = []
for index, AA1 in enumerate(pdb_AAs):
    for AA2 in pdb_AAs[index+1:]:
        if AA1.d(AA2) < 4.5:
            contacts.append((AA1.resSeq, AA2.resSeq))
with open(out_prefix + '_contacts.json', 'w') as f:
    json.dump(contacts, f)

# Add stop codons if necessary
if AA_alignment[-1] != tuple(['*'] * len(alignment_SRs)):
    AA_alignment.append(tuple(['*'] * len(alignment_SRs)))

# Make and save codon alignments
print('Making codon alignment', flush=True)
CDN_align = [step1_tools.get_pos_CDNs(pos) for pos in AA_alignment]
CDN_seqs = [''.join(CDN_pos) for CDN_pos in zip(*CDN_align)]
step1_tools.save_SeqRecords(CDN_seqs, names, f'{out_prefix}_CDN.fasta')
