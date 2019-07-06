
import os

basepath = 'runs'

INDS = [
    # ringer v6 without crack fix
    # 'data17_13TeV/00325713/user.jodafons.data17_13TeV.00325713.express_express.merge.m1807.all_lbs.r1001_GLOBAL.root'
    #,'data17_13TeV/00325713/user.jodafons.data17_13TeV.00325713.express_express.merge.m1807.lb0188.r1001_GLOBAL.root'
    #,'data17_13TeV/00325713/user.jodafons.data17_13TeV.00325713.physics_Main.merge.m1807.lb0188.r1001_GLOBAL.root'
    #,'data17_13TeV/00325790/user.jodafons.data17_13TeV.00325790.physics_Main.merge.m1807.lb0205.r1001_GLOBAL.root' 
    ## ringer v6 with crack fix
    ##,'data17_13TeV/00326657/user.jodafons.data17_13TeV.00326657.express_express.merge.AOD.x515_m1812.r1001_GLOBAL.root'
     #'data17_13TeV/00326439/user.jodafons.data17_13TeV.00326439.physics_Main.merge.AOD.f828_m1812.r1007_GLOBAL.root'
     #'data17_13TeV/00326446/user.jodafons.data17_13TeV.00326446.physics_Main.merge.AOD.f828_m1812.r1007_GLOBAL.root'
    #,'data17_13TeV/00326468/user.jodafons.data17_13TeV.00326468.physics_Main.merge.AOD.f829_m1812.r1007_GLOBAL.root'
    #,'data17_13TeV/00326551/user.jodafons.data17_13TeV.00326551.physics_Main.merge.AOD.f832_m1812.r1007_GLOBAL.root'
    #,'data17_13TeV/00326657/user.jodafons.data17_13TeV.00326657.physics_Main.merge.AOD.f832_m1812.r1007_GLOBAL.root'
    #,'data17_13TeV/00326695/user.jodafons.data17_13TeV.00326695.physics_Main.merge.AOD.f832_m1812.r1007_GLOBAL.root'
    #,'data17_13TeV/00326834/user.jodafons.data17_13TeV.00326834.physics_Main.merge.AOD.f832_m1812.r1007_GLOBAL.root'
    #'data17_13TeV/00326870/user.jodafons.data17_13TeV.00326870.physics_Main.merge.AOD.f832_m1812.r1007_GLOBAL.root'
    #,'data17_13TeV/00326923/user.jodafons.data17_13TeV.00326923.physics_Main.merge.AOD.f832_m1812.r1007_GLOBAL.root'
    #'data17_13TeV/user.jodafons.data17_13TeV.Jun_2017.00326439_00326446_00326468_00326551_00326657_00326695_00326834_00326870__00326923.physics_Main.merge.root',
    'data17_13TeV/user.jodafons.data17_13TeV_Jun_2017_00326439_00326446_00326468_00326551_00326657_00326695.physics_Main.merge.root'
    ]



template1 = """
python plot_trigger_template_1.py \
    -i {INDS} \
    -o {OUTDS} \
    -p \
    --PDF_title {PDF_TITLE} \
    --PDF_output {PDF_OUTPUT} \
"""

for inds in INDS:
  inds = basepath+'/'+inds
  ds_name = inds.split('/')[-1].replace('.root','')
  t = ds_name.split('.')
  pdf_title = t[2]+'_'+t[3]+'_'+t[4]
  cmd =template1.format(INDS=inds, OUTDS=ds_name+'_plots', PDF_TITLE=pdf_title, PDF_OUTPUT=pdf_title)
  print cmd
  os.system(cmd)






template2 = """
python plot_trigger_template_2.py \
    -i {INDS_1} {INDS_2} \
    -o {OUTDS} \
    -p \
    -k {META_KEY} \
    --PDF_title {PDF_TITLE} \
    --PDF_output {PDF_OUTPUT} \
"""


INDS = [
    'data16_13TeV/00311244/user.jodafons.data16_13TeV.00311244.physics_Main.merge.p3134.ATR-15949.r1001_GLOBAL.root',
    'data16_13TeV/00311244/user.jodafons.data16_13TeV.00311244.physics_Main.merge.p3134.ATR-16426.r1001_GLOBAL.root',
    'data16_13TeV/00311244/user.jodafons.data16_13TeV.00311244.physics_Main.merge.p3134.ATR-16455.r1001_GLOBAL.root',

]

cmd1 = emplate2.format(INDS_1=INDS[0],INDS_2=INDS[1],META_KEY="EFF:0:%s:ATR-15949,EFF:1:%s:ATR-16426",\
          OUTDS='data16_13TeV.00311244.physics_Main.ATR-15949_and_ATR-16426_plots',\
          PDF_TITLE='data16_13TeV.00311244.physics_Main.ATR-15949_and_ATR-16426',\
          PDF_OUTPUT='data16_13TeV.00311244.physics_Main.ATR-15949_and_ATR-16426')

cmd2 = template2.format(INDS_1=INDS[0],INDS_2=INDS[1],META_KEY="EFF:0:%s:ATR-16426,EFF:1:%s:ATR-16455",\
          OUTDS='data16_13TeV.00311244.physics_Main.ATR-16426_and_ATR-16455_plots',\
          PDF_TITLE='data16_13TeV.00311244.physics_Main.ATR-16426_and_ATR-16455',\
          PDF_OUTPUT='data16_13TeV.00311244.physics_Main.ATR-16426_and_ATR-16455')


#os.system(cmd1)
#os.system(cmd2)





