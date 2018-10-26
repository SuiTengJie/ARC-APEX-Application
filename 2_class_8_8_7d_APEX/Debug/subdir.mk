################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
$(PROJECT)/main.c 

OBJS += \
./main.o 

C_DEPS += \
./depend/main.u 


# Each subdirectory must supply rules for building sources it contributes
%.o: ../%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MetaWare ARC EM C/C++ Compiler'
	ccac -c -Xdsp_divsqrt=radix2 -Hinclude="C:/Users/tengjie/mide/workspace/2_class_8_8_7d_APEX/apexextensions.h" -Xswap -Xbitscan -arcv2em -Xmpy_option=mpyd -Xdsp2 -Hpc_width=32 -Xcode_density -Hccm -Xtimer0 -Xtimer1 -dmac -Xdsp_complex -Xbarrel_shifter -core2 -Xshift_assist -g -Xdiv_rem=radix2 -Hnocopyr -Xstack_check -I"$(PROJECT)" -Xdsp_accshift=limited -Humake -Hdepend="depend" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


