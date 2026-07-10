
Need MicroPython Unix port for tutorial.
In particular for HTTP server with Microdot.

Currently very difficult to install using official mechanism.
Docker is only easy alternative. But rather annoying.
TRY: make a Python package with wheels, so participants can just use pip

## Goals

Core

- Be able to do pip install micropython-unix
- Can then use "micropython" binary to run programs. Same as if built from source

Bonus

- Use "python -m micropython_unix" to run programs
- Use "import micropython_unix; micropython_unix.run_main(args)"

Out-of-scope

- Later. Test micropython.run_main(args) in Pyodide
- Later. Be able to create a stateful MicroPython interpreter from Python 

Intermediates

- How to build Python package locally is documented.
From source directory, or from git repo URL
- Automatic build and publish wheels using Github Actions.
For Linux, MacOS

## Status

Proof of Concept working.
RFC and MR created in upstream MicroPython: https://github.com/micropython/micropython/issues/19426

## TODO

- Get Windows to build also
- Test on Windows
- Rename to micropython
- Add basic test to CI

Later
- Move to ports/python ?
- Test with native modules, at least on Linux

## Testing

```
python -m pip install .
which micropython
micropython check.py 
```

python -c 'import micropython_run'

Installing from git
```
pip install "git+https://github.com/jonnor/micropython.git@unix-python-package-1#subdirectory=ports/unix"
```

## Notes

Early work in 2025 in branch `cpython-run-micropython-file`
Was focused on Pyodide.

### Testing on Linux

Ubuntu 22.04 has Python 3.10

Centos 9 has Python 3.9 by default. Not not work, no wheels built for that.
But 3.12 is installable from offical repos.
dnf -y install python3.12 python3.12-pip 

### Building on Mac OS

https://github.com/micropython/micropython/issues/17450
CC ../shared/runtime/gchelper_generic.c
error: Interference usage of base pointer/frame pointer.

### Building for Emscripten/Pyodide/WASM

CIBW_PLATFORM=pyodide cibuildwheel --platform pyodide --output-dir wheelhouse .


### Publishing packages for Pyodide

https://pyodide-build.readthedocs.io/en/latest/how-to/publishing.html

> WebAssembly wheels built by pyodide-build are standard Python wheels — they follow the same packaging format and can be published to PyPI like any other wheel.

import micropip
await micropip.install("your-package")

## Source distribution (sdist)

Will need to include everything needed to build?
Entire git repo. Plus submodules?


## Testing Windows

Can build micropython Windows port following the instructions in README.
On Arch Linux. Can also run it successfully with wine:

```
wine build-standard/micropython.exe
```

Running CPython on wine

Can use the portable version of CPython in wine

```
wget https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip
mkdir -p ~/.wine/drive_c/python311
unzip python-3.11.9-embed-amd64.zip -d ~/.wine/drive_c/python311

wine ~/.wine/drive_c/python311/python.exe

curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py
wine ~/.wine/drive_c/python311/python.exe get-pip.py

sed -i 's/#import site/import site/' ~/.wine/drive_c/python311/python311._pth

```

To exit: `Ctrl+Z then Enter`

Can run Windows package!
```
wine ~/.wine/drive_c/python311/python.exe -m pip install /home/jon/Downloads/jonnor_micropython_unix-1.28.0.2-cp311-cp311-win_amd64.whl

wine ~/.wine/drive_c/python311/python.exe -m micropython_unix
```

## Installing in Jupyter 

