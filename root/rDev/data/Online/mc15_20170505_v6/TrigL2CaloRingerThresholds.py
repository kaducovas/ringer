def ThresholdsMap():
  s=dict()
  s["tuning"]={'ElectronHighEnergyVeryLooseConf': {'et1_eta4': {'threshold': [-0.005066666666666666, -0.6328541666666667, -0.6665000000000002], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (2.37, 2.5)}}, 'et1_eta3': {'threshold': [-0.010133333333333333, 0.02541666666666694, -0.07749999999999975], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (1.54, 2.37)}}, 'et1_eta2': {'threshold': [-0.002533333333333333, -0.758333333333334, -0.7425000000000007], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (1.37, 1.54)}}, 'et1_eta1': {'threshold': [-0.016466666666666664, -0.08066666666666782, -0.28650000000000114], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (0.8, 1.37)}}, 'et1_eta0': {'threshold': [-0.012666666666666665, -0.03910416666666716, -0.1915000000000005], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (0.0, 0.8)}}, 'et3_eta1': {'threshold': [-0.022799999999999994, -0.003336914062499584, -0.3054999999999995], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (0.8, 1.37)}}, 'et3_eta0': {'threshold': [-0.02406666666666666, 0.1722708333333333, -0.13450000000000012], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (0.0, 0.8)}}, 'et3_eta3': {'threshold': [-0.015199999999999997, 0.4556874999999988, 0.28349999999999914], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (1.54, 2.37)}}, 'et3_eta2': {'threshold': [-0.006333333333333333, -0.6538333333333335, -0.6855000000000003], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (1.37, 1.54)}}, 'et3_eta4': {'threshold': [-0.005066666666666666, -0.8388854166666663, -0.8754999999999998], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (2.37, 2.5)}}, 'et0_eta4': {'threshold': [-0.0076, -0.6920312500000007, -0.7425000000000007], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (2.37, 2.5)}}, 'et0_eta0': {'threshold': [-0.008866666666666667, 0.027098958333333745, -0.058499999999999615], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (0.0, 0.8)}}, 'et0_eta1': {'threshold': [-0.010133333333333333, 0.0752916666666672, -0.03949999999999949], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (0.8, 1.37)}}, 'et0_eta2': {'threshold': [0, -2.0155000000000003, -2.0155000000000003], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (1.37, 1.54)}}, 'et0_eta3': {'threshold': [-0.005066666666666666, 0.07608333333333261, 0.03649999999999925], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (1.54, 2.37)}}, 'et4_eta0': {'threshold': [-0.025333333333333326, 0.01116666666666713, -0.3054999999999995], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (0.0, 0.8)}}, 'et4_eta1': {'threshold': [-0.025333333333333326, -0.11866048177083413, -0.4575000000000005], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (0.8, 1.37)}}, 'et4_eta2': {'threshold': [-0.02659999999999999, -0.0015000000000011948, -0.28650000000000114], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (1.37, 1.54)}}, 'et4_eta3': {'threshold': [-0.01773333333333333, -0.11589583333333321, -0.34349999999999975], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (1.54, 2.37)}}, 'et4_eta4': {'threshold': [-0.008866666666666667, -0.9493229166666677, -1.0275000000000007], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (2.37, 2.5)}}, 'et2_eta4': {'threshold': [-0.0076, -0.7852499999999993, -0.8564999999999997], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (2.37, 2.5)}}, 'et2_eta2': {'threshold': [-0.015199999999999997, -0.35418750000000077, -0.514500000000001], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (1.37, 1.54)}}, 'et2_eta3': {'threshold': [-0.012666666666666665, -0.061722330729167295, -0.21050000000000063], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (1.54, 2.37)}}, 'et2_eta0': {'threshold': [-0.01773333333333333, 0.05510416666666633, -0.17250000000000038], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (0.0, 0.8)}}, 'et2_eta1': {'threshold': [-0.018999999999999996, 0.007907226562499285, -0.22950000000000076], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (0.8, 1.37)}}}, 'ElectronHighEnergyTightConf': {'et1_eta4': {'threshold': [-0.0012666666666666666, -0.6364166666666665, -0.6285], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (2.37, 2.5)}}, 'et1_eta3': {'threshold': [-0.008866666666666667, 0.2245208333333332, 0.1314999999999999], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (1.54, 2.37)}}, 'et1_eta2': {'threshold': [-0.0037999999999999996, -0.31123339843749964, -0.3244999999999996], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (1.37, 1.54)}}, 'et1_eta1': {'threshold': [-0.012666666666666665, 0.24858626302083295, 0.09349999999999963], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (0.8, 1.37)}}, 'et1_eta0': {'threshold': [-0.01393333333333333, 0.45172916666666557, 0.28349999999999914], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (0.0, 0.8)}}, 'et3_eta1': {'threshold': [-0.021533333333333328, 0.489729166666667, 0.22650000000000053], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (0.8, 1.37)}}, 'et3_eta0': {'threshold': [-0.018999999999999996, 0.7679072265624993, 0.530499999999999], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (0.0, 0.8)}}, 'et3_eta3': {'threshold': [-0.01393333333333333, 0.30685416666666654, 0.15050000000000002], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (1.54, 2.37)}}, 'et3_eta2': {'threshold': [-0.011399999999999999, -0.03475000000000024, -0.15350000000000025], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (1.37, 1.54)}}, 'et3_eta4': {'threshold': [-0.0037999999999999996, -0.7063369140625005, -0.7235000000000006], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (2.37, 2.5)}}, 'et0_eta4': {'threshold': [-0.005066666666666666, -0.5437916666666663, -0.5714999999999996], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (2.37, 2.5)}}, 'et0_eta0': {'threshold': [-0.008866666666666667, 0.2990364583333337, 0.2075000000000004], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (0.0, 0.8)}}, 'et0_eta1': {'threshold': [-0.010133333333333333, 0.12700358072916587, 0.01749999999999912], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (0.8, 1.37)}}, 'et0_eta2': {'threshold': [0, -1.6545000000000007, -1.5595000000000008], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (1.37, 1.54)}}, 'et0_eta3': {'threshold': [-0.005066666666666666, 0.08155696614583263, 0.03649999999999925], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (1.54, 2.37)}}, 'et4_eta0': {'threshold': [-0.022799999999999994, 0.713375, 0.41650000000000004], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (0.0, 0.8)}}, 'et4_eta1': {'threshold': [-0.025333333333333326, 0.29941373697916557, -0.020500000000001135], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (0.8, 1.37)}}, 'et4_eta2': {'threshold': [-0.03039999999999999, 0.06974999999999881, -0.28650000000000114], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (1.37, 1.54)}}, 'et4_eta3': {'threshold': [-0.015199999999999997, 0.2093369140624993, 0.03649999999999925], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (1.54, 2.37)}}, 'et4_eta4': {'threshold': [-0.006333333333333333, -1.0599583333333324, -1.1034999999999995], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (2.37, 2.5)}}, 'et2_eta4': {'threshold': [-0.005066666666666666, -0.6767916666666672, -0.7045000000000005], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (2.37, 2.5)}}, 'et2_eta2': {'threshold': [-0.01393333333333333, 0.05391666666666683, -0.09649999999999988], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (1.37, 1.54)}}, 'et2_eta3': {'threshold': [-0.010133333333333333, 0.2499098307291666, 0.1314999999999999], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (1.54, 2.37)}}, 'et2_eta0': {'threshold': [-0.015199999999999997, 0.6136250000000001, 0.43550000000000016], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (0.0, 0.8)}}, 'et2_eta1': {'threshold': [-0.016466666666666664, 0.3398382161458331, 0.1314999999999999], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (0.8, 1.37)}}}, 'ElectronHighEnergyLooseConf': {'et1_eta4': {'threshold': [-0.0037999999999999996, -0.6047499999999997, -0.6285], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (2.37, 2.5)}}, 'et1_eta3': {'threshold': [-0.010133333333333333, 0.0752916666666672, -0.03949999999999949], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (1.54, 2.37)}}, 'et1_eta2': {'threshold': [-0.006333333333333333, -0.6538333333333335, -0.6855000000000003], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (1.37, 1.54)}}, 'et1_eta1': {'threshold': [-0.015199999999999997, 0.1415937500000006, -0.03949999999999949], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (0.8, 1.37)}}, 'et1_eta0': {'threshold': [-0.01393333333333333, 0.21185416666666623, 0.055499999999999376], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (0.0, 0.8)}}, 'et3_eta1': {'threshold': [-0.020266666666666662, 0.12922395833333328, -0.13450000000000012], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (0.8, 1.37)}}, 'et3_eta0': {'threshold': [-0.022799999999999994, 0.300663085937499, -0.0015000000000010092], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (0.0, 0.8)}}, 'et3_eta3': {'threshold': [-0.015199999999999997, 0.045944335937499914, -0.13450000000000012], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (1.54, 2.37)}}, 'et3_eta2': {'threshold': [-0.006333333333333333, -0.5350833333333329, -0.5904999999999997], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (1.37, 1.54)}}, 'et3_eta4': {'threshold': [-0.005066666666666666, -0.8314635416666661, -0.8754999999999998], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (2.37, 2.5)}}, 'et0_eta4': {'threshold': [-0.006333333333333333, -0.6229583333333335, -0.6665000000000002], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (2.37, 2.5)}}, 'et0_eta0': {'threshold': [-0.008866666666666667, 0.09152083333333237, -0.0015000000000010092], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (0.0, 0.8)}}, 'et0_eta1': {'threshold': [-0.008866666666666667, 0.1105208333333325, 0.01749999999999912], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (0.8, 1.37)}}, 'et0_eta2': {'threshold': [0, -1.9774999999999994, -1.8824999999999994], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (1.37, 1.54)}}, 'et0_eta3': {'threshold': [-0.005066666666666666, 0.124177083333333, 0.09349999999999963], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (1.54, 2.37)}}, 'et4_eta0': {'threshold': [-0.022799999999999994, 0.16950000000000004, -0.1155], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (0.0, 0.8)}}, 'et4_eta1': {'threshold': [-0.02406666666666666, 0.0012708333333338057, -0.3054999999999995], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (0.8, 1.37)}}, 'et4_eta2': {'threshold': [-0.025333333333333326, 0.02304166666666724, -0.3054999999999995], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (1.37, 1.54)}}, 'et4_eta3': {'threshold': [-0.01773333333333333, -0.03870833333333422, -0.2485000000000009], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (1.54, 2.37)}}, 'et4_eta4': {'threshold': [-0.010133333333333333, -0.9495208333333346, -1.0465000000000009], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (2.37, 2.5)}}, 'et2_eta4': {'threshold': [-0.006333333333333333, -0.6360208333333331, -0.6855000000000003], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (2.37, 2.5)}}, 'et2_eta2': {'threshold': [-0.01393333333333333, -0.15508333333333302, -0.3054999999999995], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (1.37, 1.54)}}, 'et2_eta3': {'threshold': [-0.012666666666666665, 0.07127766927083361, -0.07749999999999975], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (1.54, 2.37)}}, 'et2_eta0': {'threshold': [-0.016466666666666664, 0.23639583333333253, 0.03649999999999925], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (0.0, 0.8)}}, 'et2_eta1': {'threshold': [-0.018999999999999996, 0.12190722656250001, -0.1155], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (0.8, 1.37)}}}, 'ElectronHighEnergyMediumConf': {'et1_eta4': {'threshold': [-0.005066666666666666, -0.771791666666668, -0.7995000000000011], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (2.37, 2.5)}}, 'et1_eta3': {'threshold': [-0.008866666666666667, -0.05335416666666684, -0.13450000000000012], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (1.54, 2.37)}}, 'et1_eta2': {'threshold': [-0.0076, -0.5251874999999995, -0.5904999999999997], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (1.37, 1.54)}}, 'et1_eta1': {'threshold': [-0.012666666666666665, 0.033277669270833365, -0.1155], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (0.8, 1.37)}}, 'et1_eta0': {'threshold': [-0.012666666666666665, 0.17702083333333274, 0.03649999999999925], 'configuration': {'etBin': (20.0, 30.0), 'etaBin': (0.0, 0.8)}}, 'et3_eta1': {'threshold': [-0.020266666666666662, 0.1568333333333335, -0.09649999999999988], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (0.8, 1.37)}}, 'et3_eta0': {'threshold': [-0.018999999999999996, 0.3879072265624999, 0.15050000000000002], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (0.0, 0.8)}}, 'et3_eta3': {'threshold': [-0.01393333333333333, 0.07736979166666695, -0.07749999999999975], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (1.54, 2.37)}}, 'et3_eta2': {'threshold': [-0.011399999999999999, -0.4575000000000009, -0.5525000000000012], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (1.37, 1.54)}}, 'et3_eta4': {'threshold': [-0.005066666666666666, -0.5889166666666663, -0.6285], 'configuration': {'etBin': (40.0, 50.0), 'etaBin': (2.37, 2.5)}}, 'et0_eta4': {'threshold': [-0.008866666666666667, -0.8397760416666665, -0.9135000000000001], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (2.37, 2.5)}}, 'et0_eta0': {'threshold': [-0.010133333333333333, 0.015322916666666797, -0.09649999999999988], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (0.0, 0.8)}}, 'et0_eta1': {'threshold': [-0.010133333333333333, -0.08858333333333396, -0.1915000000000005], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (0.8, 1.37)}}, 'et0_eta2': {'threshold': [0, -1.9965000000000002, -1.9965000000000002], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (1.37, 1.54)}}, 'et0_eta3': {'threshold': [-0.006333333333333333, -0.03627766927083309, -0.07749999999999975], 'configuration': {'etBin': (0.0, 20.0), 'etaBin': (1.54, 2.37)}}, 'et4_eta0': {'threshold': [-0.021533333333333328, 0.34218229166666636, 0.0744999999999995], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (0.0, 0.8)}}, 'et4_eta1': {'threshold': [-0.021533333333333328, -0.0013020833333343583, -0.267500000000001], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (0.8, 1.37)}}, 'et4_eta2': {'threshold': [-0.02406666666666666, 0.009583333333332326, -0.267500000000001], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (1.37, 1.54)}}, 'et4_eta3': {'threshold': [-0.01773333333333333, -0.01377083333333405, -0.22950000000000076], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (1.54, 2.37)}}, 'et4_eta4': {'threshold': [-0.008866666666666667, -0.9214166666666673, -1.0085000000000006], 'configuration': {'etBin': (50.0, 10000000.0), 'etaBin': (2.37, 2.5)}}, 'et2_eta4': {'threshold': [-0.0037999999999999996, -0.8127294921874991, -0.8374999999999996], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (2.37, 2.5)}}, 'et2_eta2': {'threshold': [-0.015199999999999997, -0.03831250000000061, -0.21050000000000063], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (1.37, 1.54)}}, 'et2_eta3': {'threshold': [-0.011399999999999999, 0.006218750000000017, -0.1155], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (1.54, 2.37)}}, 'et2_eta0': {'threshold': [-0.015199999999999997, 0.23362499999999936, 0.055499999999999376], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (0.0, 0.8)}}, 'et2_eta1': {'threshold': [-0.016466666666666664, 0.06836458333333324, -0.13450000000000012], 'configuration': {'etBin': (30.0, 40.0), 'etaBin': (0.8, 1.37)}}}}
  s["version"]=1
  s["date"]=0
  s["metadata"]={'LumiCut': 40, 'UseNoActivationFunctionInTheLastLayer': True, 'UseLumiTool': True, 'DoPileupCorrection': True, 'UseEtaVar': False, 'UseLumiVar': False}
  s["type"]=['Hypo']
  s["name"]=['v6E65653535_r0004']
  return s