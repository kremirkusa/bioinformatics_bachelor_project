from Bio import SeqIO

def parse_agp(agp_file):
    haplotype_map = {}
    #scaff = "scaffold_1"
    with open(agp_file, 'r') as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            scaffold, start, end, part_number, type_, contig, *rest = line.strip().split("\t")
            if type_ == 'W':  
                haplotype = contig
                if haplotype[1] not in haplotype_map:
                    haplotype_map[haplotype[1]] = []
                haplotype_map[haplotype[1]].append((scaffold, int(start), int(end)))
            else:
                continue
    return haplotype_map

def split_fasta_by_haps(fasta_file, haplotype_map, output_prefix_h1, output_prefix_h2):
    sequences = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))
    with open(f"{output_prefix_h1}.fa", "w") as h1_output_handle, open(f"{output_prefix_h2}.fa", "w") as h2_output_handle:
        for haplotype, regions in haplotype_map.items():
            for scaffold, start, end in regions:
                seq = sequences[scaffold].seq[start-1:end]
                seq_record = SeqIO.SeqRecord(seq, id=f"{scaffold}:{start}-{end}", description="")
                if haplotype== "1":
                    SeqIO.write(seq_record, h1_output_handle, "fasta")
                elif haplotype== "2":
                    SeqIO.write(seq_record, h2_output_handle, "fasta")


agp_file = "scaff_durian_scaffolds_final.agp"
fasta_file = "scaff_durian_scaffolds_final.fa"
output_prefix_h1 = "scaff_hap1"
output_prefix_h2 = "scaff_hap2"

# MAIN
haplotype_map = parse_agp(agp_file)
split_fasta_by_haps(fasta_file, haplotype_map, output_prefix_h1, output_prefix_h2)
