from Bio import SeqIO
import sys

def remove_part(fasta_file, from_pos, to_pos, output):
    seq_record = next(SeqIO.parse(fasta_file, "fasta"))
    modified_seq = seq_record.seq[:from_pos] + seq_record.seq[to_pos:]  
    with open(output, "w") as f:
        f.write(f">{seq_record.id}\n{modified_seq}\n")

def remove_N(fasta_file, output):
    for record in SeqIO.parse(fasta_file, "fasta"):
        seq_str = str(record.seq).upper()
        from_pos = seq_str.find("N")
        to_pos = seq_str.rfind("N")
        
        if from_pos != -1:
            print(f"{record.id}: First N at {from_pos}, Last N at {to_pos}")
            remove_part(fasta_file, from_pos, to_pos + 1, output)
        else:
            print(f"{record.id}: No Ns found")

def main(fasta_file, just_N, from_pos, to_pos, output="modified.fasta"):
    if just_N:
        remove_N(fasta_file, output)
    else:
        remove_part(fasta_file, from_pos, to_pos, output)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python remove_part.py file.fasta from_position to_position or python remove_parts.py file.fasta -N to only remove gaps")
    elif sys.argv[2] == "-N":
        main(sys.argv[1], True, None, None)
    else:
        main(sys.argv[1], False, int(sys.argv[2]), int(sys.argv[3]))