# unzip rainbowcrack-1.7-linux64.zip
# chmod -R 777 rainbowcrack-1.7-linux64/
# cd rainbowcrack-1.7-linux64
./rtgen md5 loweralpha-numeric 5 5 0 3800 600000 0
./rtsort .
./rcrack . md5_loweralpha-numeric#5-5_0_3800x600000_0.rt -l ../hash5.txt

./rtgen md5 loweralpha-numeric 6 6 0 3800 600000 0
./rtsort .
./rcrack . md5_loweralpha-numeric#6-6_0_3800x600000_0.rt -l ../salted6.txt
# cd ..