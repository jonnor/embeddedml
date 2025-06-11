
## Python runtime options

- Google Colab
! no solution for mpremote for file access, need alternative for file transfers
- Python on local machine.
Thonny, distro, official download, conda
!shell might differ. Windows can use WSL2
!Python version might differ. Specify Python 3.10 / 3.11 / 3.12
!OS differs. I am not interested in debugging Windows/Mac OS
Thonny comes with Python 3.10 bundle on all platforms

Things we need

- git. For getting example code. Github download ZIP can be used as backup
- mpremote. For transferring files. Thonny or Viper IDE alternative
- micropython. For running the preprocessing on PC
With emlearn-micropython modules.
Solution: Download prebuilt binary with extmod from emlearn-micropython
! Mac OS native modules seem not-supported. Must use extmod
! not yet tested on Windows/WSL or Mac OS.
- Learning materials. har_trees from emlearn-micropython, incl Python packages

- C compiler. Used for building the package. Or programs when using C bindings
! might not be preinstalled on peoples computer. Large downloads
... could be deferred by simplifying

Questions

- How does Thonny work with virtual envs?
Seems to have built-in support.
NOTE: need to create empty directory manually



## Testing Thonny


### emlearn fails to install with bundled Python

Trying to install requirements.txt from har_trees
Fails when installing emlearn

I/home/jon/projects/embeddedml/presentations/TinyMLDays2025/emlearn_venv/include -I/home/thonny/pythonny310/include/python3.10 -c bindings/eml_audio.cpp -o build/temp.linux-x86_64-cpython-310/bindings/eml_audio.o -DVERSION_INFO=\"0.21.2\" -std=c++14 -fvisibility=hidden
      In file included from /home/jon/projects/embeddedml/presentations/TinyMLDays2025/emlearn_venv/lib/python3.10/site-packages/pybind11/include/pybind11/attr.h:13,
                       from /home/jon/projects/embeddedml/presentations/TinyMLDays2025/emlearn_venv/lib/python3.10/site-packages/pybind11/include/pybind11/detail/class.h:12,
                       from /home/jon/projects/embeddedml/presentations/TinyMLDays2025/emlearn_venv/lib/python3.10/site-packages/pybind11/include/pybind11/pybind11.h:12,
                       from bindings/eml_audio.cpp:5:
      /home/jon/projects/embeddedml/presentations/TinyMLDays2025/emlearn_venv/lib/python3.10/site-packages/pybind11/include/pybind11/detail/common.h:274:10: fatal error: Python.h: No such file or directory
        274 | #include <Python.h>

!! directory does not exist
/home/thonny/pythonny310/include/python3.10

!! people might not have a C compiler


### Thonny support for micropython

Seems possible to add an "interpreter", by pointing to the binary
Not so relevant for us, we will use it as a subprocess, in ML pipeline

But nothing that helps to actually install a MicroPython binary.

## Getting micropython installed for PC

Want micropython on PC to run preprocessing.
Especially to use emlearn-micropython .mpy files
If not for emlearn-micropython extensions, could just use CPython, assume/check values are compatible

Would be great to have a MicroPython that can just be downloaded and executed.
Ideally installable pip, like the other tools

Need to cover at least

- Linux, using something like manylinux
- Windows via WSL, using Linux build
- Mac OS

! also need to build the C natmods for all the relevant platforms
For that reason, would need to have similar kind of build setup also in emlearn-micropython, and use for natmods.
Might be easier to prototype a generic micropython build there also, then move out to dedicated repo later (or ideally - micropython repo itself).


## Just do everything in/with Docker ?

Everyone has the same OS inside. Including me
Can be tested in advance, highly reproducible.
Familiar Linux environment.

#### USB access from Docker quite manual

? how to transfer files back and forth
USB device access from Docker
?? mpbuild has some code for this. Unsure if compatible with all operating systems

December 2024
https://blog.golioth.io/usb-docker-windows-macos/
Requires manual setup of USB/IP

https://docs.docker.com/desktop/features/usbip/

#### Use a full VM
VirtualBox etc.

Vagrant etc is nice for building an image

### Using networked communication instead of USB

WebREPL is supported with Tonny
https://bhave.sh/micropython-webrepl-thonny/

WebREPL is supported within Viper IDE

WebREPL improvement RFC
https://github.com/micropython/micropython/issues/13540

## Testing on Mac OS

Scaleway, AWS, MacinCloud offers Mac Mini for daily rental

https://github.com/sickcodes/Docker-OSX

### Building emlearn-micropython native modules on Mac OS

Might not be supported/working ?

    python3 /Users/runner/work/emlearn-micropython/emlearn-micropython/micropython/tools/mpy_ld.py '-vvv' --arch x64 --qstrs build/emlearn_trees.config.h  -o build/emlearn_trees.native.mpy build/trees.o
    qstr vals: __del__, addleaf, addnode, addroot, emlearn_trees_c, emltrees, new, outputs, predict, setdata
    Traceback (most recent call last):
      File "/Users/runner/work/emlearn-micropython/emlearn-micropython/micropython/tools/mpy_ld.py", line 1516, in <module>
        main()
      File "/Users/runner/work/emlearn-micropython/emlearn-micropython/micropython/tools/mpy_ld.py", line 1512, in main
        do_link(args)
      File "/Users/runner/work/emlearn-micropython/emlearn-micropython/micropython/tools/mpy_ld.py", line 1462, in do_link
        load_object_file(env, f, fn)
      File "/Users/runner/work/emlearn-micropython/emlearn-micropython/micropython/tools/mpy_ld.py", line 1084, in load_object_file
        elf = elffile.ELFFile(f)
      File "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/elftools/elf/elffile.py", line 73, in __init__
        self._identify_file()
      File "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/elftools/elf/elffile.py", line 631, in _identify_file
        elf_assert(magic == b'\x7fELF', 'Magic number does not match')
      File "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/elftools/common/utils.py", line 80, in elf_assert
        _assert_with_exception(cond, msg, ELFError)
      File "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/elftools/common/utils.py", line 143, in _assert_with_exception
        raise exception_type(msg)
    elftools.common.exceptions.ELFError: Magic number does not match

### Running Linux built x64 modules on Mac OS

 

## Serial device drivers

!! Need to check what drivers are needed on Windows, Mac OS for the


## Testing Colab + Viper

https://mybinder.org/ is an alternative

- Download trained model, changed preprocessing etc
- Upload new data files, etc

