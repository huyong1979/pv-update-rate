import sys
from datetime import datetime
import time
#from math import floor, fabs
from cothread import WaitForQuit
from cothread.catools import camonitor, FORMAT_TIME, caput, caget
import traceback

if len(sys.argv) < 4:
    print("usage: %s pv_name low_rate high_rate other_pvs"%sys.argv[0])
    sys.exit()

pv_name = sys.argv[1]
low_rate = float(sys.argv[2])
high_rate = float(sys.argv[3])
other_pvs = []
other_pvs_prevVAL = []
if len(sys.argv) > 4:
    other_pvs = sys.argv[4:]
    other_pvs_prevVAL = caget(other_pvs)
#print(other_pvs)

prev_value = caget(pv_name, format=FORMAT_TIME) 
#previous timestamp of pv
pv_prevTS = prev_value.raw_stamp[0] + prev_value.raw_stamp[1]*1.0e-9 
local_prevTS = time.time() #previous local timestamp
str_prevTS = datetime.now() # a string
error_count = 0

def callback(value):
    try:
        global other_pvs_prevVAL
        global prev_value
        global pv_prevTS
        global local_prevTS
        global str_prevTS
        global error_count
        #print("\n%s: pv value is %d"%(datetime.now(), value))

        str_currTS = datetime.now()
        local_currTS = time.time() #current local timestamp
        rate = 1.0/(local_currTS - local_prevTS)
        if rate < low_rate or rate > high_rate:
            print("\n%s:\n\tthe update rate of %s is %.3fHz (%.3f-sec), out of [%.3f, %.3f]"
                    %(str_currTS, value.name, rate, 1.0/rate, low_rate, high_rate))
            print("\tprevious localtime and value: %s, %s"%(str_prevTS,prev_value))
            print("\tcurrent  localtime and value: %s, %s"%(str_currTS, value))

            if len(other_pvs) > 0: #if there is any other PV in the argument
                other_pvs_currVAL = caget(other_pvs)
                print("\t%s previous value(s): %s"%(other_pvs, other_pvs_prevVAL))
                print("\t%s current  value(s): %s"%(other_pvs, other_pvs_currVAL))
                other_pvs_prevVAL = other_pvs_currVAL

        caput(str(pv_name)+"_Rate", rate)
        str_prevTS  = str_currTS 
        local_prevTS  = local_currTS
        prev_value = value

        pv_currTS = value.raw_stamp[0] + value.raw_stamp[1]*1.0e-9
        if (pv_currTS - pv_prevTS)==0: 
            print("\n%s: the timestamp of %s is not updated"%(str_currTS, value.name))       
            print "\t%s is the time from the PV"%str(datetime.fromtimestamp(pv_currTS))
        pv_prevTS = pv_currTS
    except:
        error_count += 1
        caput(str(pv_name)+"_Error", error_count)
        traceback.print_exc()
        return

def main():
    camonitor(pv_name, callback, format=FORMAT_TIME)
    WaitForQuit()

if __name__ == '__main__':
    main()
