import FWCore.ParameterSet.Config as cms

configurationMetadata = cms.untracked.PSet(
        version = cms.untracked.string('$Revision: 1.1 $'),
        name = cms.untracked.string('$Source: /cvs_server/repositories/CMSSW/CMSSW/Configuration/GenProduction/python/PYTHIA6EvtGen_ppMuMuX_7TeV_cff.py,v $'),
        annotation = cms.untracked.string('Winter10: Pythia6-MinBias at 7TeV + EvtGen with 2 Muon preselection')
)

from Configuration.GenProduction.PythiaUESettings_cfi import *


process.source = cms.Source("EmptySource")
process.generator = cms.EDFilter("Pythia6GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(7000.0),
    crossSection = cms.untracked.double(48440000000.0),
#    filterEfficiency = cms.untracked.double(0.00240),
    maxEventsToPrint = cms.untracked.int32(0),
    ExternalDecays = cms.PSet(
        EvtGen = cms.untracked.PSet(
             operates_on_particles = cms.vint32( 0 ), # 0 (zero) means default list (hardcoded)
                                                      # you can put here the list of particles (PDG IDs)
                                                      # that you want decayed by EvtGen
             use_default_decay = cms.untracked.bool(True),
             decay_table = cms.FileInPath('GeneratorInterface/ExternalDecays/data/DECAY_NOLONGLIFE.DEC'),
             particle_property_file = cms.FileInPath('GeneratorInterface/ExternalDecays/data/evt.pdl'),
             user_decay_file = cms.FileInPath('GeneratorInterface/ExternalDecays/data/DECAY_NOLONGLIFE.DEC'),
             list_forced_decays = cms.vstring(),
        ),
        parameterSets = cms.vstring('EvtGen')
    ),
    PythiaParameters = cms.PSet(
        pythiaUESettingsBlock,
        processParameters = cms.vstring('MSEL=1           ! User defined processes', 
            'MSTJ(22)=4       ! Decay unstable particles in a cylinder', 
            'PARJ(73)=1500.   ! max. radius for MSTJ(22)=4', 
            'PARJ(74)=3000.   ! max. Z for MSTJ(22)=4', 
            'MDCY(C130,1)=1   ! decay k0-longs', 
            'MDCY(C211,1)=1   ! decay pions', 
            'MDCY(C321,1)=1   ! decay kaons'),
        # This is a vector of ParameterSet names to be read, in this order
        parameterSets = cms.vstring(
             'pythiaUESettings',
             'processParameters')
    )
)

process.mumugenfilter = cms.EDFilter("MCParticlePairFilter",
    Status = cms.untracked.vint32(1, 1),
    MinPt = cms.untracked.vdouble(2.5, 2.5),
    MaxEta = cms.untracked.vdouble(2.5, 2.5),
    MinEta = cms.untracked.vdouble(-2.5, -2.5),
    ParticleCharge = cms.untracked.int32(-1),
    ParticleID1 = cms.untracked.vint32(13),
    ParticleID2 = cms.untracked.vint32(13)
)



ProductionFilterSequence = cms.Sequence(generator*mumugenfilter)
