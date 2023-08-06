import ntplib

def is_bcg_network() -> bool:
    try:
        ntplib.NTPClient().request('ntp.bcg.com', version=3)
        return True
    except:
        return False