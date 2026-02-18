# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(minimal)

target_sources(app PRIVATE src/main.c)

target_compile_options(app BEFORE PRIVATE -std=gnu99)


target_include_directories(app PRIVATE
    ../build/muselab_icesugar/software/include/
    ../venv/src/litex/litex/soc/software/include/
    ../venv/src/litex/litex/soc/cores/cpu/vexriscv/
)
