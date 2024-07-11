

# Web
microdot seems to be the best MicroPython backend library
https://github.com/miguelgrinberg/microdot

# Time sync
MicroPython supports `ntptime` for getting time over NPT
https://github.com/micropython/micropython-lib/blob/master/micropython/net/ntptime/ntptime.py

# Compression

How to serve compressed files?
Especially for static assets, which should be pre-compressed on disk.
Need to set the Content-Encoding header.

microdot has direct support for compression.
Suggests using a separate gzstatic/ folder/route, and let the files have standard file extensions.
Practical!


# Plotting

Custom bundle of Plot.ly can be 1 MB (minified). 312kB with gzip.
```
npm run custom-bundle -- --out smaller --traces scatter --transforms none
```

Very powerful. But of course a rather big package.

? What is the performance like when using MicroPython / MicroDot to serve this?
Loading time. Memory usage.

Chart.js is 180 kB uncompressed. 56kB with gzip
Has scatter, time-series, tooltip support.
Also supports data decimation.

Zoom/pan available in separate plugin
https://www.chartjs.org/chartjs-plugin-zoom/latest/guide/
Supports dynamic data loading
https://www.chartjs.org/chartjs-plugin-zoom/latest/samples/fetch-data.html


# Styling

picocss is a minimal and pragmatic CSS system, based on standard semantic HTML to a large degree
https://picocss.com/docs/container

84 kB uncompressed, 12 kB when gzip compressed.

# HTML generation

Here is a small library that also supports MicroPython
https://github.com/j4mie/hotmetal/
