
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

## TODO

- Add basic test to CI
- Fix the version being outdated?
- Setup publishing to PyPi
- Test on Ubuntu, MacOS, WSL
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

Early work in 2025 in branch `cpython-run-micropython-file,`.
Was focused on Pyodide.

### Building on Mac OS

https://github.com/micropython/micropython/issues/17450
CC ../shared/runtime/gchelper_generic.c
error: Interference usage of base pointer/frame pointer.

