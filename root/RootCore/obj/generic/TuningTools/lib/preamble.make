RC_CXX       = c++
RC_LD        = c++
RC_CXXFLAGS  = -I/home/caducovas/ringer/root/TuningTools/Root -I/home/caducovas/ringer/root/TuningTools -O2 -Wall -fPIC -pthread -std=c++11 -m64 -I/home/caducovas/root/include -I/home/caducovas/ringer/root/RootCore/include -g -Wno-tautological-undefined-compare -DROOTCORE -pthread -std=c++11 -m64 -I/home/caducovas/root/include -pipe -W -Wall -Wno-deprecated -pedantic -Wwrite-strings -Wpointer-arith -Woverloaded-virtual -Wno-long-long -Wdeprecated-declarations -std=c++11 -fPIC -DUSING_MULTI_THREAD -std=c++11 -fPIC -lboost_python -L/home/caducovas/ringer/root/RootCore/../InstallArea/boost/lib -isystem/home/caducovas/ringer/root/RootCore/../InstallArea/boost/include -lpython2.7 -isystem/usr/include/python2.7 -isystem/home/caducovas/.local/lib/python2.7/site-packages//numpy/core/include -fopenmp -lgomp -DUSING_MULTI_THREAD -DROOTCORE_PACKAGE=\"TuningTools\" 
RC_DICTFLAGS = -I/home/caducovas/ringer/root/TuningTools/Root -I/home/caducovas/ringer/root/TuningTools -O2 -Wall -fPIC -pthread -std=c++11 -m64 -I/home/caducovas/root/include -I/home/caducovas/ringer/root/RootCore/include -g -Wno-tautological-undefined-compare -DROOTCORE -pthread -std=c++11 -m64 -I/home/caducovas/root/include -pipe -W -Wall -Wno-deprecated -pedantic -Wwrite-strings -Wpointer-arith -Woverloaded-virtual -Wno-long-long -Wdeprecated-declarations -std=c++11 -fPIC -DUSING_MULTI_THREAD -std=c++11 -fPIC -lboost_python -L/home/caducovas/ringer/root/RootCore/../InstallArea/boost/lib -isystem/home/caducovas/ringer/root/RootCore/../InstallArea/boost/include -lpython2.7 -isystem/usr/include/python2.7 -isystem/home/caducovas/.local/lib/python2.7/site-packages//numpy/core/include -fopenmp -lgomp -DUSING_MULTI_THREAD -DROOTCORE_PACKAGE=\"TuningTools\" 
RC_INCFLAGS  = -I/home/caducovas/ringer/root/TuningTools/Root -I/home/caducovas/ringer/root/TuningTools -I/home/caducovas/root/include -I/home/caducovas/ringer/root/RootCore/include -DROOTCORE -I/home/caducovas/root/include -DUSING_MULTI_THREAD -DUSING_MULTI_THREAD -DROOTCORE_PACKAGE=\"TuningTools\"
RC_LIBFLAGS  = -shared -m64 -L/home/caducovas/root/lib -lCore -lImt -lRIO -lNet -lHist -lGraf -lGraf3d -lGpad -lROOTVecOps -lTree -lTreePlayer -lRint -lPostscript -lMatrix -lPhysics -lMathCore -lThread -lMultiProc -lROOTDataFrame -pthread -lm -ldl -rdynamic -lRingerCore -fPIC -lboost_python -L/home/caducovas/ringer/root/RootCore/../InstallArea/boost/lib -lpython2.7 -L/usr//lib -lgomp -DUSING_MULTI_THREAD
RC_BINFLAGS  = -L/home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/lib -L/home/caducovas/ringer/root/RootCore/lib/generic -lTuningTools -lRingerCore -lTree -lGpad -lHist -m64 -L/home/caducovas/root/lib -lCore -lImt -lRIO -lNet -lHist -lGraf -lGraf3d -lGpad -lROOTVecOps -lTree -lTreePlayer -lRint -lPostscript -lMatrix -lPhysics -lMathCore -lThread -lMultiProc -lROOTDataFrame -pthread -lm -ldl -rdynamic


all_TuningTools : dep_TuningTools package_TuningTools

package_TuningTools :  /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/lib/libTuningTools.so postcompile_TuningTools

/home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/lib/libTuningTools.so :  /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/FeedForward.o /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/util.o /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/Standard.o /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/NeuralNetwork.o /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/RProp.o /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/boost_expose.o /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/TuningToolPyWrapper.o /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/Backpropagation.o /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/PatternRec.o /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/TuningToolsCINT.o | /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/lib
	$(SILENT)echo Linking `basename $@`
	$(SILENT)$(RC_LD) /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/FeedForward.o /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/util.o /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/Standard.o /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/NeuralNetwork.o /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/RProp.o /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/boost_expose.o /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/TuningToolPyWrapper.o /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/Backpropagation.o /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/PatternRec.o /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/TuningToolsCINT.o $(RC_LIBFLAGS) -L/home/caducovas/ringer/root/RootCore/lib/generic -o $@

/home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/%.o : /home/caducovas/ringer/root/TuningTools/Root/%.cxx | /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/FeedForward.d
	$(SILENT)echo Compiling `basename $@`
	$(SILENT)rc --internal check_dep_cc TuningTools $@
	$(SILENT)$(RC_CXX) $(RC_CXXFLAGS) $(INCLUDES) -c $< -o $@

/home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/%.d : /home/caducovas/ringer/root/TuningTools/Root/%.cxx | /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj
	$(SILENT)echo Making dependency for `basename $<`
	$(SILENT)rc --internal make_dep $(RC_CXX) $(RC_CXXFLAGS) $(INCLUDES)  -- $@ $< 

/home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj : 
	$(SILENT)echo Making directory $@
	$(SILENT)mkdir -p $@

/home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/TuningToolsCINT.o : /home/caducovas/ringer/root/TuningTools/Root/LinkDef.h /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/TuningToolsCINT.headers | /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/TuningToolsCINT.d
	$(SILENT)echo Compiling `basename $@`
	$(SILENT)rc --internal check_dep_cc TuningTools $@
	$(SILENT)rc --internal rootcint $(ROOTSYS)/bin/rootcint $(RC_INCFLAGS) /home/caducovas/ringer/root/TuningTools/Root/LinkDef.h /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/TuningToolsCINT.cxx /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/TuningToolsCINT.headers /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/lib TuningTools
	$(SILENT)$(RC_CXX) $(RC_DICTFLAGS) $(INCLUDES) -c /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/TuningToolsCINT.cxx -o $@

/home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/TuningToolsCINT.headers : /home/caducovas/ringer/root/TuningTools/Root/LinkDef.h | /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj
	$(SILENT)echo Making dependency for `basename $<`
	$(SILENT)rc --internal make_dep $(RC_CXX) $(RC_CXXFLAGS) $(INCLUDES) -D__CINT__ -D__MAKECINT__ -D__CLING__ -Wno-unknown-pragmas -- $@ $< 

/home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/TuningToolsCINT.d : /home/caducovas/ringer/root/TuningTools/Root/LinkDef.h | /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj
	$(SILENT)echo Making dependency for `basename $<`
	$(SILENT)rc --internal make_dep $(RC_CXX) $(RC_CXXFLAGS) $(INCLUDES)  -- $@ $< 

/home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/lib : 
	$(SILENT)echo Making directory $@
	$(SILENT)mkdir -p $@

postcompile_TuningTools :  /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/lib/libTuningTools.so
	$(SILENT)rc --internal postcompile_pkg TuningTools


dep_TuningTools : /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/Backpropagation.d /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/RProp.d /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/FeedForward.d /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/TuningToolsCINT.d /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/NeuralNetwork.d /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/Standard.d /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/TuningToolsCINT.headers /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/TuningToolPyWrapper.d /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/PatternRec.d /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/boost_expose.d /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/util.d


-include  /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/Backpropagation.d /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/RProp.d /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/FeedForward.d /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/TuningToolsCINT.d /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/NeuralNetwork.d /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/Standard.d /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/TuningToolsCINT.headers /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/TuningToolPyWrapper.d /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/PatternRec.d /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/boost_expose.d /home/caducovas/ringer/root/RootCore/obj/generic/TuningTools/obj/util.d
