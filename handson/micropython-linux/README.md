

# MicroPython Linux application in a few megabytes

MicroPython. Using the Unix port
Build with Docker
Using multi-stage build with distroless

Routers such as OpenWRT / LEDE

### micropython/unix Docker image

docker inspect micropython/unix:v1.22 | grep Size
    "Size": 540399040,
    "VirtualSize": 540399040,

540 MB!!

Entirely unsuitable.
Probably because it inherits from some huge stock image

### MicroPython Alpine

Have a package
https://pkgs.alpinelinux.org/package/edge/testing/x86/micropython
Installed size 	476 kB
Was updated to 1.22 just a week after the release. Seems quite up to date.

Minimal Dockerfile

```
FROM alpine:3.19
RUN apk add micropython --update-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing --allow-untrusted
ENTRYPOINT ["/usr/bin/micropython"]
```

docker inspect

        "Size": 10 813 763,
        "VirtualSize": 10 813 763,

10 MB total. Starting to become acceptable

```
# du -sh /usr/bin/micropython
492.0K	/usr/bin/micropython

# ldd /usr/bin/micropython
	/lib/ld-musl-x86_64.so.1 (0x7ff24b970000)
	libffi.so.8 => /usr/lib/libffi.so.8 (0x7ff24b8e9000)
	libc.musl-x86_64.so.1 => /lib/ld-musl-x86_64.so.1 (0x7ff24b970000)
```



### MicroPython Distroless

https://github.com/GoogleContainerTools/distroless/blob/main/base/README.md

Image ended up at 15 MB!
Bigger than simple Alpine Linux. Does not make sense

### MicroPython APKO

https://dev.to/dansiviter/distroless-alpine-ci8
Uses the APKO to build a custom image
Was able to get image down to under 1 MB!

https://github.com/chainguard-dev/apko

Is packaged officially for Arch Linux

#### Mikrotik KNOT

Uses Qualcomm QCA9531. Released in 2014.
RouterOS architecture MIPSBE
This has CPU architecture MIPS 24Kc
A 32 bit architecture.
NOT the same as mips64le

References
https://lwn.net/Articles/838807/

OpenWRT has support for
https://openwrt.org/docs/techref/instructionset/mips_24kc

Large number of supported devices
Including some similar to Mikrotik KNOT, such as
GL.iNet GL-MT300N-V2, GL-MT1300, Minew G1

OpenWrt,RouterOS
mips_24kc,MIPSBE
mipsel_24kc,MIPSLE

Packages for mips_24kc

https://downloads.openwrt.org/snapshots/packages/mips_24kc/packages/
Including docker and docker-compose
Also including MicroPython

OpenWRT can run in QEMU for MIPS (including big endian).
The "malta" target is used
https://openwrt.org/docs/guide-user/virtualization/qemu#openwrt_in_qemu_mips

Downloading vmlinux and rootfs files from
https://downloads.openwrt.org/releases/23.05.2/targets/malta/be/

Unpacked the rootfs image

```
qemu-system-mips -M malta \
-hda openwrt-23.05.2-malta-be-rootfs-ext4.img \
-kernel openwrt-23.05.2-malta-be-vmlinux.elf \
-nographic -append "root=/dev/sda console=ttyS0"
```
Boots in about 60 seconds to a shell
No network available though. Would need to be setup with qemu


OpenWRT provides Docker images
https://github.com/openwrt/docker

Has imagebuilder images, designed for cross-compilation
And rootfs images, designed to test software inside the target image

Rootfs tags include malta/be

```
docker run --rm -v "$(pwd)"/bin/:/builder/bin -it openwrt/rootfs:mips_24kc
```
Downloads docker image, but cannot run because it is not x86_64
Might be able to run with docker QEMU integration?

```
git clone https://github.com/openwrt/docker openwrt-docker
cd openwrt-docker

docker build \
    --build-arg TARGET=malta/be \
    --build-arg DOWNLOAD_FILE="imagebuilder-.*Linux-x86_64.tar.xz" \
    -t openwrt/malta .
docker run -it openwrt/malta
```

Using imagebuilder
https://openwrt.org/docs/guide-user/additional-software/imagebuilder

```
buildbot@3351e954dd46:~$ make info
```

```
Current Target: "malta/be"
Current Architecture: "mips"
Current Revision: "r24707-4693514ca8"
Default Packages: base-files ca-bundle dropbear fstools libc libgcc libustream-mbedtls logd mtd netifd opkg uci uclient-fetch urandom-seed urngd busybox procd procd-ujail procd-seccomp wpad-basic-mbedtls kmod-mac80211-hwsim kmod-pcnet32 mkf2fs e2fsprogs dnsmasq firewall4 nftables kmod-nft-offload odhcp6c odhcpd-ipv6only ppp ppp-mod-pppoe
Available Profiles:

Default:
    Default
    Packages: 
    hasImageMetadata: 
```


```
make image \
PROFILE="Default" \
PACKAGES="micropython" \
FILES="files" \
DISABLED_SERVICES="dnsmasq firewall odhcpd"
```

Looks to install micropython-mbedtls
Looks to spit out OpenWRT image.
RootFS is 4 MB compressed, and Linux kernel is 10 MB. Seems legit

buildbot@3351e954dd46:~$ ls -la bin/targets/malta/be/
total 34876
drwxr-xr-x 2 buildbot buildbot     4096 Jan  2 15:07 .
drwxr-xr-x 3 buildbot buildbot     4096 Jan  2 15:07 ..
-rw-r--r-- 1 buildbot buildbot     3429 Jan  2 15:07 openwrt-malta-be-default.manifest
-rw-r--r-- 1 buildbot buildbot  4684646 Jan  2 15:07 openwrt-malta-be-default-rootfs.tar.gz
-rw-r--r-- 1 buildbot buildbot  4689816 Jan  2 15:07 openwrt-malta-be-rootfs.cpio.gz
-rw-r--r-- 1 buildbot buildbot  4787520 Jan  2 15:07 openwrt-malta-be-rootfs-ext4.img.gz
-rw-r--r-- 1 buildbot buildbot  3853365 Jan  2 15:07 openwrt-malta-be-rootfs-squashfs.img.gz
-rw-r--r-- 1 buildbot buildbot  4395874 Jan  2 15:07 openwrt-malta-be-uImage-gzip
-rw-r--r-- 1 buildbot buildbot  3057024 Jan  2 15:07 openwrt-malta-be-uImage-lzma
-rwxr-xr-x 1 buildbot buildbot 10216152 Jan  2 15:07 openwrt-malta-be-vmlinux.elf
-rw-r--r-- 1 buildbot buildbot      796 Jan  2 15:07 sha256sums

Copying images out of Docker
```
docker cp 3351e954dd46:/builder/bin/targets/malta/be/ images/
```

```
qemu-system-mips -M malta \
-hda openwrt-malta-be-rootfs-ext4.img \
-kernel openwrt-malta-be-vmlinux.elf \
-nographic -append "root=/dev/sda console=ttyS0"
```



