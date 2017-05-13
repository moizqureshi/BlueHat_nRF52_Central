from bluepy.btle import Scanner, DefaultDelegate

scanner = Scanner()
devices = scanner.scan(5.0)

for dev in devices:
    if (dev.scanData.get(255, None).encode("hex")[:28] == "ffff0123456789abcdefffffffff"):
        print "Device ID: %s, RSSI: %d dB" % (dev.scanData.get(255, None).encode("hex")[29:36], dev.rssi)
        print "BlueHat Data: %s" % dev.scanData.get(255, None).encode("hex")[37:]
