#!/usr/bin/env python

import hid, re, sys, time

VID=0x04d8
PID=0xf5d1

CMD_SETSTATE=0x10
CMD_GETSTATE=0x11
CMD_SETLEVEL=0x20
CMD_GETLEVEL=0x21

def get_level(myhid):
    try:
        myhid.write([0x0, CMD_GETLEVEL])
        time.sleep(0.1)
        d = myhid.read(5)
	if len(d)>1:
            level=d[1] | (d[2] << 8)
        else:
            level=0
        return level

    except IOError as ex:
        print(ex)

def set_level(myhid,level):
    maxwait=10
    try:
        timestart=time.time()
        myhid.write( [ 0x0, CMD_SETLEVEL, level-((level>>8)<<8), level>>8 ] )   # Send desired level
        myhid.write( [ 0x0, CMD_SETSTATE, 3 ] ) # Execute state change
        while time.time()-timestart<maxwait:
            state=get_state(myhid)
            if state[1]==0:
                break
            time.sleep(0.1)
        while get_level(myhid)!=level:
            time.sleep(0.1)
    except IOError as ex:
        print(ex)

def get_state(myhid):
    try:
        myhid.write([0x0,CMD_GETSTATE])
        ret = myhid.read(5);
        return ret

    except IOError as ex:
        print(ex)


try:
    myhid = hid.device()
    myhid.open(VID, PID) # TREZOR VendorID/ProductID

    # enable non-blocking mode
    myhid.set_nonblocking(1)
    if len(sys.argv)>1:
        if re.match(r"^[0-9]+$",sys.argv[1]) and int(sys.argv[1])>=0 and int(sys.argv[1])<1024:
            set_level(myhid,int(sys.argv[1]))
            if get_level(myhid)!=int(sys.argv[1]):
                time.sleep(0.2)
            print(get_level(myhid))
        else:
            print("")
            print("Usage: {} <0-1023>".format(sys.argv[0]))
            print("")
            print("        Run without any brightness value to get the current brightness.")
            print("")
    else:
        print(get_level(myhid))
    myhid.close()

except IOError as ex:
    print(ex)
    print("Can't find the USB Dimmer for Spike-A Flat.  Is it plugged in?")
    print("If so, it may be in an errored state.  Please check the connection,")
    print("or try unplugging / replugging the device.")
