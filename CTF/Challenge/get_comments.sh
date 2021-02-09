#!bin/bash
if [ $1 == 'exif' ];
then
    exiftool -r CyberSecurityAct | grep == > output_exif.txt
elif [ $1 == 'strings' ];
then
    for filename in CyberSecurityAct/*; do
        strings "$filename" | grep ==
    done > output_strings.txt
fi