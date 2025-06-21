#!/bin/bash


if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <hap1.fasta> <hap2.fasta> <data.meryl>"
    exit 1
fi

FILE1="$1"
FILE2="$2"
FILE3="$3"


for FILE in "$FILE1" "$FILE2" 
do
    if [ ! -f "$FILE" ]; then
        echo "Error: File '$FILE' not found!"
        exit 1
    fi
done

mkdir lengths_gaps
mkdir qv
mkdir t2t
mkdir gaps

cd lengths_gaps
echo "Calculating lengths and gaps..."
quast "$FILE1" -o hap1_lengths_gaps_output
quast "$FILE2" -o hap2_lengths_gaps_output

sleep 1

cd ../qv
echo "Calculating qv..."
merqury.sh "$FILE3" "$FILE1" "$FILE2" combined_stats

sleep 1

cd ../t2t
echo "Running t2t analysis..."
T2T_chromosomes.sh -a "$FILE1" -o hap1_telomere -t 26
T2T_chromosomes.sh -a "$FILE2" -o hap2_telomere -t 26
sleep 1

cd ../gaps
echo "Calculating gaps..."
python /home/mles/bioinformatika/skripte/gaps_positions.py "$FILE1" > hap1_gap_pos.txt
python /home/mles/bioinformatika/skripte/gaps_positions.py "$FILE2" > hap2_gap_pos.txt
fastagap -c -N "$FILE1" > hap1_fastagap_output.txt
fastagap -c -N "$FILE2" > hap2_fastagap_output.txt

