#!/bin/bash

#Get name of Model headerfile. Assumption: Only 1 file in directory
new_file_name=$(find . -maxdepth 1 -type f -name '*.h' -print -quit)

sed -i "29s|.*|#include \"$(basename $new_file_name)\"|" main.cpp

# Get the array name from the .h file
array_name=$(grep -oh "conv.*_tflite" $new_file_name | head -1)

# Replace the array name in the main.cpp file
sed -i "s/GetModel(.*)/GetModel($array_name)/" main.cpp

#copy file into include folder
cp "$new_file_name" /home/lennard/STM32CubeIDE/workspace_1.10.1/test1/Core/Inc

rm "$new_file_name"
