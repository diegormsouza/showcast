CPPFLAGS= -I../DISE  -I../COMP/Inc -I../COMP/JPEG/Inc -I../COMP/WT/Inc -I../COMP/T4/Inc \

LIBS= -lpthread ../DISE/libDISE.a \
../COMP/JPEG/Src/libJPEG.a ../COMP/WT/Src/libWT.a ../COMP/T4/Src/libT4.a ../COMP/Src/libCOMP.a 

# Determine if 32 or 64 bits platform
# Only Linux and SunOs suported
SYSTEM = $(shell uname -s)
BITS=32 # Defaults to 32 bits compilation
ifeq ($(SYSTEM),Linux)	
	BITS = $(shell getconf LONG_BIT)
endif
ifeq ($(SYSTEM),SunOS)
	BITS = $(shell isainfo -b)
endif
export BITS

all: xRITDecompress

xRITDecompress: xRITDecompress.o lib
	g++ -o xRITDecompress  xRITDecompress.o  $(LIBS)

clean:
	rm -f *.o
	rm -f xRITDecompress
	rm -f ../TestData/ResultsGenerated/*
	make -C ../COMP clean
	make -C ../DISE clean

lib:
	make -C ../COMP
	make -C ../DISE

.cpp.o:
	g++ $(CPPFLAGS) -c -m$(BITS) $<

depend:
	makedepend -- $(CPPFLAGS) -- $(MAKEDEPFLAGS) -- $(SOURCES)

###################################################################################
# Test commands and variables

Base_Dir = $(shell pwd)
Data_Dir = $(shell cd ../../Data && pwd)
CompTargets=$(wildcard $(Data_Dir)/compressed_ref/*-C_)
DecompTargets=$(subst compressed_ref,decompressed,$(subst -C_,-__,$(CompTargets)))
	
cleantestDx: 
	rm -f $(Data_Dir)/decompressed/*

$(Data_Dir)/decompressed/%-__: $(Data_Dir)/compressed_ref/%-C_
	cd $(Data_Dir)/decompressed && $(Base_Dir)/xRITDecompress -s:$<
	cmp $(Data_Dir)/uncompressed_ref/$*-__ $(Data_Dir)/decompressed/$*-__	
	
testDx: xRITDecompress $(DecompTargets) 
	@echo 	
	@echo Test succeeded!
	@echo 
