RC_CXX       = c++
RC_LD        = c++
RC_CXXFLAGS  = -I/home/atlas/ringer/root/RingerCore/Root -I/home/atlas/ringer/root/RingerCore -O2 -Wall -fPIC -pthread -std=c++11 -m64 -I/home/caducovas/root/include -I/home/atlas/ringer/root/RootCore/include -g -Wno-tautological-undefined-compare -DROOTCORE -pthread -std=c++11 -m64 -I/home/atlas/root/include -pipe -W -Wall -Wno-deprecated -pedantic -Wwrite-strings -Wpointer-arith -Woverloaded-virtual -Wno-long-long -Wdeprecated-declarations -std=c++11 -fPIC -DUSING_MULTI_THREAD -DROOTCORE_PACKAGE=\"RingerCore\" 
RC_DICTFLAGS = -I/home/atlas/ringer/root/RingerCore/Root -I/home/atlas/ringer/root/RingerCore -O2 -Wall -fPIC -pthread -std=c++11 -m64 -I/home/caducovas/root/include -I/home/atlas/ringer/root/RootCore/include -g -Wno-tautological-undefined-compare -DROOTCORE -pthread -std=c++11 -m64 -I/home/atlas/root/include -pipe -W -Wall -Wno-deprecated -pedantic -Wwrite-strings -Wpointer-arith -Woverloaded-virtual -Wno-long-long -Wdeprecated-declarations -std=c++11 -fPIC -DUSING_MULTI_THREAD -DROOTCORE_PACKAGE=\"RingerCore\" 
RC_INCFLAGS  = -I/home/atlas/ringer/root/RingerCore/Root -I/home/atlas/ringer/root/RingerCore -I/home/caducovas/root/include -I/home/atlas/ringer/root/RootCore/include -DROOTCORE -I/home/atlas/root/include -DUSING_MULTI_THREAD -DROOTCORE_PACKAGE=\"RingerCore\"
RC_LIBFLAGS  = -shared -m64 -L/home/caducovas/root/lib -lCore -lImt -lRIO -lNet -lHist -lGraf -lGraf3d -lGpad -lROOTVecOps -lTree -lTreePlayer -lRint -lPostscript -lMatrix -lPhysics -lMathCore -lThread -lMultiProc -lROOTDataFrame -pthread -lm -ldl -rdynamic -fPIC -lgomp -DUSING_MULTI_THREAD
RC_BINFLAGS  = -L/home/atlas/ringer/root/RootCore/obj/generic/RingerCore/lib -L/home/atlas/ringer/root/RootCore/lib/generic -lRingerCore -lTree -lGpad -lHist -m64 -L/home/caducovas/root/lib -lCore -lImt -lRIO -lNet -lHist -lGraf -lGraf3d -lGpad -lROOTVecOps -lTree -lTreePlayer -lRint -lPostscript -lMatrix -lPhysics -lMathCore -lThread -lMultiProc -lROOTDataFrame -pthread -lm -ldl -rdynamic


all_RingerCore : dep_RingerCore package_RingerCore

package_RingerCore :  /home/atlas/ringer/root/RootCore/obj/generic/RingerCore/lib/libRingerCore.so postcompile_RingerCore

/home/atlas/ringer/root/RootCore/obj/generic/RingerCore/lib/libRingerCore.so :  /home/atlas/ringer/root/RootCore/obj/generic/RingerCore/obj/StoreGate.o /home/atlas/ringer/root/RootCore/obj/generic/RingerCore/obj/MsgStream.o | /home/atlas/ringer/root/RootCore/obj/generic/RingerCore/lib
	$(SILENT)echo Linking `basename $@`
	$(SILENT)$(RC_LD) /home/atlas/ringer/root/RootCore/obj/generic/RingerCore/obj/StoreGate.o /home/atlas/ringer/root/RootCore/obj/generic/RingerCore/obj/MsgStream.o $(RC_LIBFLAGS) -L/home/atlas/ringer/root/RootCore/lib/generic -lHist -lGpad -lTree -o $@

/home/atlas/ringer/root/RootCore/obj/generic/RingerCore/obj/%.o : /home/atlas/ringer/root/RingerCore/Root/%.cxx | /home/atlas/ringer/root/RootCore/obj/generic/RingerCore/obj/StoreGate.d
	$(SILENT)echo Compiling `basename $@`
	$(SILENT)rc --internal check_dep_cc RingerCore $@
	$(SILENT)$(RC_CXX) $(RC_CXXFLAGS) $(INCLUDES) -c $< -o $@

/home/atlas/ringer/root/RootCore/obj/generic/RingerCore/obj/%.d : /home/atlas/ringer/root/RingerCore/Root/%.cxx | /home/atlas/ringer/root/RootCore/obj/generic/RingerCore/obj /home/atlas/ringer/root/RootCore/obj/generic/RingerCore/obj
	$(SILENT)echo Making dependency for `basename $<`
	$(SILENT)rc --internal make_dep $(RC_CXX) $(RC_CXXFLAGS) $(INCLUDES)  -- $@ $< 

/home/atlas/ringer/root/RootCore/obj/generic/RingerCore/obj : 
	$(SILENT)echo Making directory $@
	$(SILENT)mkdir -p $@

/home/atlas/ringer/root/RootCore/obj/generic/RingerCore/lib : 
	$(SILENT)echo Making directory $@
	$(SILENT)mkdir -p $@

postcompile_RingerCore :  /home/atlas/ringer/root/RootCore/obj/generic/RingerCore/lib/libRingerCore.so
	$(SILENT)rc --internal postcompile_pkg RingerCore


dep_RingerCore : /home/atlas/ringer/root/RootCore/obj/generic/RingerCore/obj/StoreGate.d /home/atlas/ringer/root/RootCore/obj/generic/RingerCore/obj/MsgStream.d


-include  /home/atlas/ringer/root/RootCore/obj/generic/RingerCore/obj/StoreGate.d /home/atlas/ringer/root/RootCore/obj/generic/RingerCore/obj/MsgStream.d
