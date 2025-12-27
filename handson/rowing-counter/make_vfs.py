
import zephyr, vfs, os

def is_flash_mounted():
    mounts = vfs.mount()
    for mount in mounts:
        if mount[1] == "/flash":
            return True
    return False

if is_flash_mounted():
    print("Flash mounted.")
else:
    print("Flash not mounted. Mounting...")
    fa = zephyr.FlashArea(zephyr.FlashArea.ID_ExtStorage, 4096)
    try:
        vfs.mount(fa, "/flash")
    except OSError:
        print("Formatting flash...")
        vfs.VfsLfs2.mkfs(fa)
        vfs.mount(fa, "/flash")

flash_files = os.listdir("/flash")
if not 'lib' in flash_files:
    print("Creating lib directory in flash...")
    os.mkdir("/flash/lib")
