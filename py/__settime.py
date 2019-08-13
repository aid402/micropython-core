import ntptime
def settime_th():
    t = ntptime.time() + (7 * 3600)
    import machine
    import utime
    tm = utime.localtime(t)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    machine.RTC().datetime(tm)
    print(utime.localtime())

settime_th()
