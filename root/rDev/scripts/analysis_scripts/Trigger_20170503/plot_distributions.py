
from TrigEgammaDevelopments.helper import createEmulation_trigger_20170221_v6
# Create emulation Ringer tool

algEmu, chains_emulated =  createEmulation_trigger_20170221_v6( )
chains=[ pair[0] for key, pair in chains_emulated.iteritems() ]
print chains


from TrigEgammaDevelopments.tools import DistributionTool
algDist = DistributionTool('DistributionTool')
algDist.setDiscriminantList( chains )
algDist.doTrigger = True

from RingerCore import  restoreStoreGate
sg1 =  restoreStoreGate( 'data/distributions_probes.root' )
sg2 =  restoreStoreGate( 'data/distributions_fakes.root'  )
#algDist.setStoreSvc(sg1)

from ROOT import kRed,kAzure
#algDist.plot(dirname = 'DistributionProbes', basecolor=kAzure+7)
algDist.setStoreSvc(sg1)
algDist.plot(dirname = 'DistributionProbes', basecolor=kAzure+7, 
    pdftitle = 'MC15c and data16_13TeV comparison (Probes Distributions)',\
    pdfoutput = 'probes_distributions')

algDist.setStoreSvc(sg2)
algDist.plot(dirname = 'DistributionFakes', basecolor=kRed-7, 
    pdftitle = 'MC15c and data16_13TeV comparison (Fake Distributions)',\
    pdfoutput = 'fakes_distributions')





