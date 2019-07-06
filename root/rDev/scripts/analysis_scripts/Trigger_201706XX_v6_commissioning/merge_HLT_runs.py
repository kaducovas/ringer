
import os

basepath = 'runs'

INDS = [
     'data17_13TeV/00326439/user.jodafons.data17_13TeV.00326439.physics_Main.merge.AOD.f828_m1812.r1007_GLOBAL.root',
     'data17_13TeV/00326446/user.jodafons.data17_13TeV.00326446.physics_Main.merge.AOD.f828_m1812.r1007_GLOBAL.root',
     'data17_13TeV/00326468/user.jodafons.data17_13TeV.00326468.physics_Main.merge.AOD.f829_m1812.r1007_GLOBAL.root',
     'data17_13TeV/00326551/user.jodafons.data17_13TeV.00326551.physics_Main.merge.AOD.f832_m1812.r1007_GLOBAL.root',
     'data17_13TeV/00326657/user.jodafons.data17_13TeV.00326657.physics_Main.merge.AOD.f832_m1812.r1007_GLOBAL.root',
     'data17_13TeV/00326695/user.jodafons.data17_13TeV.00326695.physics_Main.merge.AOD.f832_m1812.r1007_GLOBAL.root',
     #'data17_13TeV/00326834/user.jodafons.data17_13TeV.00326834.physics_Main.merge.AOD.f832_m1812.r1007_GLOBAL.root',
     #'data17_13TeV/00326870/user.jodafons.data17_13TeV.00326870.physics_Main.merge.AOD.f832_m1812.r1007_GLOBAL.root',
     #'data17_13TeV/00326923/user.jodafons.data17_13TeV.00326923.physics_Main.merge.AOD.f832_m1812.r1007_GLOBAL.root',
    ]


OUTPUT = 'merged_all.root'
files=[]
os.system('lsetup "root 6.08.06-x86_64-slc6-gcc62-opt"')

for idx, ds in enumerate(INDS):
  output = 'tmp_'+str(idx)+'.root'
  run_number = int(ds.split('/')[1])

  cmd1 = "rootmkdir -p {OUTPUT}:HLT/Egamma".format(OUTPUT=output)
  cmd2 = "rootcp -r {INDS}:run_{RUNNUMBER}/HLT/Egamma/* {OUTPUT}:HLT/Egamma".format(INDS=basepath+'/'+ds,RUNNUMBER=str(run_number),OUTPUT=output)
  
  os.system( cmd1 )
  print cmd2
  os.system( cmd2 )
  files.append( output )



