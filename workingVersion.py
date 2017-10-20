from DIRAC.Core.Base import Script
Script.parseCommandLine()

from ILCDIRAC.Interfaces.API.DiracILC import DiracILC
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
from ILCDIRAC.Interfaces.API.NewInterface.Applications import Marlin
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
import time

dIlc = DiracILC()
lcoutput = []
for i in range (1,301):
    lcoutput = "aa_%d.root"%i
    job = UserJob()
    job.setDestination('LCG.CERN.ch')
    job.setInputSandbox( ["LFN:/ilc/user/k/kacarevic/hgamgam/PandoraPFA/PandoraLikelihoodData9EBin_CLIC_ILD.xml","LFN:/ilc/user/k/kacarevic/hgamgam/PandoraPFA/PandoraSettingsFast.xml","LFN:/ilc/user/k/kacarevic/hgamgam/PandoraPFA/MarlinRecoRootFiles/steering.xml","LFN:/ilc/user/k/kacarevic/hgamgam/PandoraPFA/clic_ild_cdr.gear","LFN:/ilc/user/k/kacarevic/hgamgam/PandoraPFA/MarlinRecoRootFiles/lib.tar.gz"] ) 
    job.setInputData("LFN:/ilc/user/k/kacarevic/hgamgam/Marlin/newPandora/aa/aa_%d.slcio"%i)
    job.setOutputSandbox(["*.log", "*.sh", "*.py","*.out","*.xml","*.steer "])
    job.setJobGroup( "myRoot" )
    job.setName( "root_aa_%d"%i)
    marl = Marlin ()
    marl.setVersion('ILCSoft-2016-09-27_gcc48')
    marl.setInputFile(["LFN:/ilc/user/k/kacarevic/hgamgam/Marlin/newPandora/aa/aa_%d.slcio"%i])
   # marl.setNumberOfEvents(10)
    marl.setSteeringFile("steering.xml")
    marl.setGearFile("clic_ild_cdr.gear")
    marl.setExtraCLIArguments( "--MyProcessor.RootFilename=%s" % lcoutput )
    res = job.append(marl)
    if not res['OK']:
        print res['Message']
        quit() #do something, like quit
    job.setOutputData( lcoutput, "hgamgam/Marlin/rootFiles/aa/workingVersion", "CERN-SRM")
    print lcoutput
    job.dontPromptMe()
    print job.submit(dIlc)
    time.sleep(0.5)
