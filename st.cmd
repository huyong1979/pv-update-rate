#!/epics/iocs/pure-elauncher/bin/linux-x86_64/scriptlaunch

epicsEnvSet("EPICS_CA_ADDR_LIST", "10.0.153.255")
epicsEnvSet("EPICS_CA_AUTO_ADDR_LIST", "NO")
#epicsEnvSet("PATH", "/opt/conda_envs/ap-2019-2.0/bin:$PATH")
epicsEnvSet("EPICS_BASE", "/usr/lib/epics")

cd "/epics/iocs/pure-elauncher"
dbLoadDatabase("dbd/scriptlaunch.dbd",0,0)
scriptlaunch_registerRecordDeviceDriver(pdbbase)

#dbLoadRecords("$(EPICS_BASE)/db/iocAdminSoft.db", "IOC=SR-APHLA{IOC:PMRFCFD2}")
#dbLoadRecords ("$(EPICS_BASE)/db/save_restoreStatus.db", "P=SR-APHLA{IOC:PMRFCFD2}")
cd "/epics/iocs/pvUpdateRate/"
dbLoadRecords("updateRate.db", "PV=LN-TS{EVR:1B}EvtHCnt-I")
dbLoadRecords("updateRate.db", "PV=SR:C28-TS{EVR:G1A}EvtACnt-I")
dbLoadRecords("updateRate.db", "PV=SR-TS{EVR:CRB4A}EvtACnt-I")

#cd $(TOP)
#set_savefile_path("./as", "/save")
#set_requestfile_path("./as", "/req")
#set_pass0_restoreFile("settings_pass0.sav")
#set_pass1_restoreFile("settings_pass1.sav")

iocInit()

#LN-TS{EVR:1B}EvtHCnt-I: event 17, supposed ~ 2Hz
system "python pv_rate.py LN-TS{EVR:1B}EvtHCnt-I 1.8 2.1 LN-BI{ACMI:1}FaultCode:3-Sts BTS-BI{ACMI:2}FaultCode:3-Sts &"
#LN-TS{EVR:1B}EvtHCnt-I: event 32, supposed ~ 1Hz
system "python pv_rate.py SR:C28-TS{EVR:G1A}EvtACnt-I 0.8 1.2 &"
#SR-TS{EVR:CRB4A}EvtACnt-I: event 25, supposed ~ 1Hz
system "python pv_rate.py SR-TS{EVR:CRB4A}EvtACnt-I 0.8 1.2 &"

#makeAutosaveFileFromDbInfo("./as/req/settings_pass0.req", "autosaveFields_pass0")
#create_monitor_set("settings_pass0.req", 30 , "")
#makeAutosaveFileFromDbInfo("./as/req/settings_pass1.req", "autosaveFields_pass1")
#create_monitor_set("settings_pass1.req", 30 , "")
