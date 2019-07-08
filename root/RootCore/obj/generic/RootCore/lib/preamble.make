RC_CXX       = c++
RC_LD        = c++
RC_CXXFLAGS  = -I/home/atlas/ringer/root/RootCore/Root -I/home/atlas/ringer/root/RootCore -O2 -Wall -fPIC -pthread -std=c++11 -m64 -I/home/caducovas/root/include -I/home/atlas/ringer/root/RootCore/include -g -Wno-tautological-undefined-compare -DROOTCORE -pthread -std=c++11 -m64 -I/home/atlas/root/include -pipe -W -Wall -Wno-deprecated -pedantic -Wwrite-strings -Wpointer-arith -Woverloaded-virtual -Wno-long-long -Wdeprecated-declarations -DROOTCORE_PACKAGE=\"RootCore\" 
RC_DICTFLAGS = -I/home/atlas/ringer/root/RootCore/Root -I/home/atlas/ringer/root/RootCore -O2 -Wall -fPIC -pthread -std=c++11 -m64 -I/home/caducovas/root/include -I/home/atlas/ringer/root/RootCore/include -g -Wno-tautological-undefined-compare -DROOTCORE -pthread -std=c++11 -m64 -I/home/atlas/root/include -pipe -W -Wall -Wno-deprecated -pedantic -Wwrite-strings -Wpointer-arith -Woverloaded-virtual -Wno-long-long -Wdeprecated-declarations -DROOTCORE_PACKAGE=\"RootCore\" 
RC_INCFLAGS  = -I/home/atlas/ringer/root/RootCore/Root -I/home/atlas/ringer/root/RootCore -I/home/caducovas/root/include -I/home/atlas/ringer/root/RootCore/include -DROOTCORE -I/home/atlas/root/include -DROOTCORE_PACKAGE=\"RootCore\"
RC_LIBFLAGS  = -shared -m64 -L/home/caducovas/root/lib -lCore -lImt -lRIO -lNet -lHist -lGraf -lGraf3d -lGpad -lROOTVecOps -lTree -lTreePlayer -lRint -lPostscript -lMatrix -lPhysics -lMathCore -lThread -lMultiProc -lROOTDataFrame -pthread -lm -ldl -rdynamic 
RC_BINFLAGS  = -L/home/atlas/ringer/root/RootCore/obj/generic/RootCore/lib -L/home/atlas/ringer/root/RootCore/lib/generic -m64 -L/home/caducovas/root/lib -lCore -lImt -lRIO -lNet -lHist -lGraf -lGraf3d -lGpad -lROOTVecOps -lTree -lTreePlayer -lRint -lPostscript -lMatrix -lPhysics -lMathCore -lThread -lMultiProc -lROOTDataFrame -pthread -lm -ldl -rdynamic


all_RootCore : dep_RootCore package_RootCore

package_RootCore :  postcompile_RootCore

postcompile_RootCore : 
	$(SILENT)rc --internal postcompile_pkg RootCore


dep_RootCore :
