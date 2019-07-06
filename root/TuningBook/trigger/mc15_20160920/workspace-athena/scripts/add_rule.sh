
#rucio add-rule --lifetime "$((30243600))" data15_13TeV.00280500.physics_EnhancedBias.merge.AOD.r7900_p2565/ 1 BNL-OSG2_SCRATCHDISK
#rucio add-rule --lifetime "$((30243600))" data15_13TeV.00284285.physics_Main.merge.AOD.f662_m1453_r7900_p2565/ 1 BNL-OSG2_SCRATCHDISK
DATASET=$1
rucio add-rule --lifetime "$((30243600))" ${DATASET}/ 1 BNL-OSG2_SCRATCHDISK



