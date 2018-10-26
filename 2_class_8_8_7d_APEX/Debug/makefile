################################################################################
# Automatically-generated file. Do not edit!
################################################################################

PROJECT := ..

WORKSPACE = ../..
WORKING = $(PROJECT)/..
# "sh.exe" was not found in search path; using Windows cmd.exe

# Could not find "rm.exe" on the search path;
# the command "C:\STJ\SW_INSTALL\metaware\MetaWare\ide\utils\rm.exe" will be used instead.

-include ../makefile.init

RM := C:\STJ\SW_INSTALL\metaware\MetaWare\ide\utils\rm.exe -f

# All of the sources participating in the build are defined here
-include sources.mk
-include subdir.mk
-include objects.mk


# Add inputs and outputs from these tool invocations to the build variables 
MAPFILE += \


# All Target
all: 2_class_8_8_7d_APEX.elf

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(CC_DEPS)),)
-include $(CC_DEPS)
endif
ifneq ($(strip $(C++_DEPS)),)
-include $(C++_DEPS)
endif
ifneq ($(strip $(CL_DEPS)),)
-include $(CL_DEPS)
endif
ifneq ($(strip $(CXX_DEPS)),)
-include $(CXX_DEPS)
endif
ifneq ($(strip $(ASM_DEPS)),)
-include $(ASM_DEPS)
endif
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(MET_DEPS)),)
-include $(MET_DEPS)
endif
ifneq ($(strip $(CPP_DEPS)),)
-include $(CPP_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs



# Tool invocations
2_class_8_8_7d_APEX.elf: $(OBJS) $(USER_OBJS)
	@echo 'Building target: $@'
	@echo 'Invoking: MetaWare Linker for ARCompact'
	ccac  -Xdsp_divsqrt=radix2 -Hldopt=-q -Xswap -Xbitscan -e_start -arcv2em -Xmpy_option=mpyd -Xdsp2 -Xcode_density -Hccm -Os -Xdsp_complex -Xbarrel_shifter -core2 -Xshift_assist -Xdiv_rem=radix2 -Xstack_check -Xdsp_accshift=limited -o "2_class_8_8_7d_APEX.elf" $(OBJS) $(USER_OBJS) $(LIBS)
	@echo 'Finished building target: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) $(OBJS)
	-$(RM) $(CC_DEPS)$(C++_DEPS)$(CL_DEPS)$(EXECUTABLES)$(CXX_DEPS)$(ASM_DEPS)$(MAPFILE)$(S_DEPS)$(MET_DEPS)$(CPP_DEPS)$(C_DEPS) 2_class_8_8_7d_APEX.elf
	-@echo ' '

.PHONY: all clean dependents
.SECONDARY:

-include ../makefile.targets
