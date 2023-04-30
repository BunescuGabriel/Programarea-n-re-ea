import ntplib
from datetime import datetime, timezone, timedelta


ntp_client = ntplib.NTPClient()
while True:
    gmt_offset_hours=int(input('Introduceti fusul orar:'))
    time_offset = timedelta(hours=gmt_offset_hours)
    response = ntp_client.request('pool.ntp.org')
    current_time = datetime.fromtimestamp(response.tx_time, timezone.utc) + time_offset
    
    print(f"Time by GHT {current_time.strftime('%Y-%m-%d %H-%M-%S %Z')}")
