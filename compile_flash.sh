#!/bin/bash
make -j4 all 
arm-none-eabi-g++ "../Core/Src/main.cpp" -mcpu=cortex-m7 -std=gnu++14 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F746xx -c -I../Core/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc -I../Drivers/STM32F7xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F7xx/Include -I../Drivers/CMSIS/Include -I"/home/lennard/STM32CubeIDE/workspace_1.12.0/test1/tensorflow_lite" -I"/home/lennard/STM32CubeIDE/workspace_1.12.0/test1/tensorflow_lite/third_party/flatbuffers/include" -I"/home/lennard/STM32CubeIDE/workspace_1.12.0/test1/tensorflow_lite/third_party/gemmlowp" -I"/home/lennard/STM32CubeIDE/workspace_1.12.0/test1/tensorflow_lite/third_party/kissfft" -I"/home/lennard/STM32CubeIDE/workspace_1.12.0/test1/tensorflow_lite/third_party/ruy" -O0 -ffunction-sections -fdata-sections -fno-exceptions -fno-rtti -fno-use-cxa-atexit -Wall -fstack-usage -MMD -MP -MF"Core/Src/main.d" -MT"Core/Src/main.o" --specs=nano.specs -mfpu=fpv5-sp-d16 -mfloat-abi=hard -mthumb -o "Core/Src/main.o"
arm-none-eabi-g++ -o "test1.elf" @"objects.list"   -mcpu=cortex-m7 -T"/home/lennard/STM32CubeIDE/workspace_1.12.0/test1/STM32F746ZGTX_FLASH.ld" --specs=nosys.specs -Wl,-Map="test1.map" -Wl,--gc-sections -static --specs=nano.specs -mfpu=fpv5-sp-d16 -mfloat-abi=hard -mthumb -Wl,--start-group -lc -lm -lstdc++ -lsupc++ -Wl,--end-group

#find elf file and convert it into bin
file_name=$(find . -maxdepth 1 -type f -name '*.elf' -print -quit)

arm-none-eabi-objcopy -O binary "$file_name" bin_file.bin

st-flash --connect-under-reset write bin_file.bin 0x08000000 

st-flash reset -v /dev/ttyACM0

