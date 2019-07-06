

cd constants_v6/
cp /home/jodafons/CERN-DATA/Online/rgconfigs/trigger/mc15_201609XX_v3/TrigL2CaloRingerConstants.py TrigL2CaloRingerConstants_v3.py
cp /home/jodafons/CERN-DATA/Online/rgconfigs/trigger/mc15_201612XX_v4/TrigL2CaloRingerConstants.py TrigL2CaloRingerConstants_v4.py
python merge_v3_v4.py

mv TrigL2CaloRingerConstants.py TrigL2CaloRingerConstants_v6.py
cp TrigL2CaloRingerConstants_v6.py ..
cd ..


