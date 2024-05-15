#!/bin/bash

awk '/SegmentType/' test.txt > column_01.txt
awk '/SegmentTime/' test.txt > column_02.txt
awk '/BeginTime/' test.txt > column_03.txt
awk '/EndTime/' test.txt > column_04.txt
awk '/BeginLoad/' test.txt > column_05.txt
awk '/EndLoad/' test.txt > column_06.txt
awk '/NumofSeqPoints/' test.txt > column_07.txt
awk '/Aquisition_rate/' test.txt > column_08.txt

awk '{print $1}' column_01.txt > coldata_01.txt
awk '{print $1}' column_02.txt > coldata_02.txt
awk '{print $1}' column_03.txt > coldata_03.txt
awk '{print $1}' column_04.txt > coldata_04.txt
awk '{print $1}' column_05.txt > coldata_05.txt
awk '{print $1}' column_06.txt > coldata_06.txt
awk '{print $1}' column_07.txt > coldata_07.txt
awk '{print $1}' column_08.txt > coldata_08.txt

paste coldata_01.txt coldata_02.txt coldata_03.txt coldata_04.txt coldata_05.txt coldata_06.txt coldata_07.txt coldata_08.txt -d "," > new_Nano_data.txt

sed -i '1iSegmentType,SegmentTime,BeginTime,EndTime,BeginLoad,EndLoad,NumofSeqPoints,Aquisition_rate' new_Nano_data.txt