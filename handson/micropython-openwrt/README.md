
# MicroPython on OpenWRT

Testing to use MicroPython on an OpenWRT capable router.

Specifically the GL iNet A1300 Slate Next.
This devices only has 128 MB of FLASH ROM.
So regular Python is a bit too large, making MicroPython very useful.

## Default GL iNet distribution

Shipped version of GL iNet is 4.5.22
https://dl.gl-inet.com/router/a1300/stable
4.5.22 is latest =/

Can SSH in, using root and admin password.

opkg install micropython
Got MicroPython 1.19

- Available disk 51.81% (66.31 MB).
- Architecture. ARMv7 Processor rev 5 (v7l)
- OpenWrt Version OpenWrt 21.02.2 r16495-bf0c965af0
- Kernel Version 5.4.179

## Switching to upstream OpenWRT

OpenWrt seems to have 25.12.5
https://firmware-selector.openwrt.org/?version=25.12.5&target=ipq40xx%2Fgeneric&id=glinet_gl-a1300

https://openwrt.org/toh/gl.inet/gl-a1300

Trying to install via sysupgrade.
By uploading to web interface.
"Error when testing sysupgrade"

Installed manually via sysupgrade -n
```
scp -O Downloads/openwrt-25.12.5-ipq40xx-generic-glinet_gl-a1300-squashfs-sysupgrade.bin root@192.168.8.1:

root@GL-A1300:~# sysupgrade openwrt-25.12.5-ipq40xx-generic-glinet_gl-a1300-squashfs-sysupgrade.bin 
Thu Jul 16 17:41:18 UTC 2026 upgrade: Image not in /tmp, copying...
Thu Jul 16 17:41:18 UTC 2026 upgrade: The device is supported, but the config is incompatible to the new image (1.0->1.1). Please upgrade without keeping config (sysupgrade -n).
Thu Jul 16 17:41:18 UTC 2026 upgrade: Config cannot be migrated from swconfig to DSA

sysupgrade -n openwrt-25.12.5-ipq40xx-generic-glinet_gl-a1300-squashfs-sysupgrade.bin 
Thu Jul 16 17:41:46 UTC 2026 upgrade: Image not in /tmp, copying...
Thu Jul 16 17:41:46 UTC 2026 upgrade: Commencing upgrade. Closing all shell sessions.
Connection to 192.168.8.1 closed by remote host.
Connection to 192.168.8.1 closed.
```

## MicroPython in OpenWRT 25.12

root@OpenWrt:~# apk update
root@OpenWrt:~# apk search micropython
root@OpenWrt:~# apk add micropython-mbedtls
root@OpenWrt:~# micropython 
MicroPython v1.23.0 on 2026-07-11; linux [GCC 14.3.0] version
Use Ctrl-D to exit, Ctrl-E for paste mode

Much better! Though 1.23 was released in May 2024. So 2 years old.

The git version of OpenWRT has recent MicroPython versions
https://github.com/openwrt/packages/tree/master/lang/python/micropython

Probably will not be available until OpenWRT 26.xx though.

## Bluetooth

Using an ASUS BT500 USB via the Type A plug.

Install drivers
```
apk add kmod-btusb

wget https://gitlab.com/kernel-firmware/linux-firmware/-/raw/main/rtl_bt/rtl8761bu_fw.bin
wget https://gitlab.com/kernel-firmware/linux-firmware/-/raw/main/rtl_bt/rtl8761bu_config.bin

cp rtl8761bu_* /lib/firmware/rtl_bt/
```

```
hciconfig hci0 up
hciconfig -a
```

```
btmon
```

```
hcidump --raw
```
Gives a stream of packets, in hex


## Reading Bluetooth from MicroPython

Would be useful to do BLE -> MQTT forwarding.
Allows the OpenWRT router to be used as an IoT gateway.

```
hcidump --raw > /tmp/hci_pipe
```

Read from MicroPython
```
f = open('/tmp/hci_pipe', 'r')
while True:
    line = f.readline()
    if not line:
        break
    line = line.strip()
    if line.startswith('>'):
        hexbytes = line[1:].split()
        data = bytes(int(b, 16) for b in hexbytes)
```
Works!

!! open on a FIFO is blocking until writer writes

This asyncio version is non-blocking, yields

```
import asyncio, select

async def read_pipe():
    f = open('/tmp/hci_pipe', 'r+')
    poller = select.poll()
    poller.register(f, select.POLLIN)

    buf = ''
    while True:
        events = poller.poll(0)  # non-blocking check
        if not events:
            await asyncio.sleep(0.02)  # yield to event loop
            print('yield')
            continue
        line = f.readline()
        if not line:
            await asyncio.sleep(0.05)
            continue
        line = line.strip()
        if line.startswith('>'):
            hexbytes = line[1:].split()
            data = bytes(int(b, 16) for b in hexbytes)
            # handle advertisement here
            print(data)

asyncio.run(read_pipe())
```

### Services on OpenWrt

https://openwrt.org/docs/guide-developer/procd-init-script-example

