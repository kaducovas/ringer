THISDIR=`pwd`
#DIRLIST=`find . -name "cmt" -print0`
DIRLIST=`find . -name "cmt" -printf "%h "`
echo $DIRLIST
for  THDIR in `echo $DIRLIST`; do
	echo $THDIR $THISDIR
	cd $THDIR/cmt
  rm install.x86_64-slc6-gcc48*
	cd ..
	rm -rf x86_64*
  rm -rf genConf
	cd $THISDIR
done

rm -rf InstallArea/
