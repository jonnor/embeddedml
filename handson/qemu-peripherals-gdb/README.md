
An attempt to simulate memory-mapped periphreals in QEMU by using GDB.

**DOES NOT WORK!?**.
Hardware breakpoints do not seem to trigger in qemu-system-arm,
and the entire system relies on this.


## Testing

```
./run.sh
```

```
qemu-system-arm -M mps2-an385 -cpu cortex-m3 -kernel firmware.elf -nographic -semihosting -S -gdb tcp::1234
```
