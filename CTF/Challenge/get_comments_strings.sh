#!bin/bash
for filename in CyberSecurityAct/*; do
    strings "$filename" | grep ==
done > output_strings.txt