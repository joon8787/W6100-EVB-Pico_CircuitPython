# Write your code here :-)
import supervisor
import board
import busio
import digitalio
import time

import adafruit_wiznet5k.adafruit_wiznet5k as wiznet
import adafruit_requests as requests

print("Hello World!")

# SPI0: SCK=GP18, MOSI=GP19, MISO=GP16
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)
cs = digitalio.DigitalInOut(board.GP17)
reset = digitalio.DigitalInOut(board.GP20)
print("SPI 인터페이스 초기화 성공!")

eth = wiznet.WIZNET5K(spi, cs, reset=reset, is_dhcp=False)
print("WIZnet5k 시작 중...")

# PHY 링크 상태 확인 루프
print("PHY 링크 상태 확인 중...")
while True:
    link = eth.link_status
    if link:
        print("✅ PHY Link: 연결됨 (Link Up)")
        break
    else:
        print("❌ PHY Link: 끊김 (Link Down)")
    time.sleep(1)


print("WIZnet5k Static IP 설정 중...")

# Static IP 구성 (예시)
ip_address = (192, 168, 0, 77)
subnet_mask = (255, 255, 255, 0)
gateway = (192, 168, 0, 1)
dns_server = (8, 8, 8, 8)  # Google Public DNS
mac = "02:08:DC:01:02:03"

# WIZNET5K 초기화 (is_dhcp=False)
eth = wiznet.WIZNET5K(spi, cs, reset=reset, is_dhcp=False,mac=mac)

# 정적 IP 수동 설정
eth.ifconfig = (ip_address, subnet_mask, gateway, dns_server)

# IP 설정 확인
ip, subnet, gateway, dns = eth.ifconfig
mac = eth.mac_address
mac_str = ":".join("{:02X}".format(b) for b in mac)

# IP 주소들 출력
print("📡 네트워크 설정:")
print("  MAC Address : ", mac_str)
print("  IP Address  : ", ".".join(str(b) for b in ip))
print("  Subnet Mask : ", ".".join(str(b) for b in subnet))
print("  Gateway     : ", ".".join(str(b) for b in gateway))
print("  DNS Server  : ", ".".join(str(b) for b in dns))
