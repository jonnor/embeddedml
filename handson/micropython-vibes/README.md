
# Running a local LLM for agentic coding

Testing if this can work on a RTX 5060 TI 16GB for MicroPython development.

## Dual RTX 5060 TI 16G

Motivating goal. Get 27B running at 50+ tps and prefill of 500+ tps.

NOTE: this might require MTP to get even close.
Testing MTP will probably be done separately, when getting into llama-cpp mainline.

TODO

- Test llama.cpp with NVFP4

## Verifying practical performance

Would want to run some evals

https://github.com/kyuz0/pi-bench
based on SWE mini
Has reference results for Qwen 3.6 27B

## Asus PCIE bifurcation support - UNTESTED

Has data for X570 boards, all other chipsets
https://www.asus.com/support/faq/1037507/

?? Seems that maybe the "PCIE RAID" setting on CROSSHAIR VIII HERO is actually code for x4x4x4x4, when used on PCIE16_1 only ?
And x4x4 plus x4x4 when using both _1 and _2 ?

HYPER M.2 X16 Card

## vLLM quants for Qwen 3.6 27B

Need safetensor format?
Though supposedly it is possible to load GGUF also??
vLLM models with integer quantization often have `AWQ` or `GPTQ` in the name.

Qwen3.6-27B KLDs - INTs and NVFPs 
https://www.reddit.com/r/LocalLLaMA/comments/1ssyukx/qwen3627b_klds_ints_and_nvfps/
Has overview of KL divergence vs file size.

!! sakamakismile/Qwen3.6-27B-Text-NVFP4-MTP does the worst
And cyankiwi/Qwen3.6-27B-AWQ-INT4 the best for low models.
Intel not tested, neither QuantTrio 6bit

Best for small models: Lorbus/Qwen3.6-27B-int4-AutoRound and cyankiwi/Qwen3.6-27B-AWQ-INT4

cyankiwi did a silent update of their model. No details on neither original nor update.

Lorbus provides some information.

```
https://huggingface.co/Intel/Qwen3.6-27B-int4-AutoRound
19 GB

https://huggingface.co/Lorbus/Qwen3.6-27B-int4-AutoRound
19 GB
"made with Intel Autoround"

https://huggingface.co/cyankiwi/Qwen3.6-27B-AWQ-INT4
20 GB

https://huggingface.co/QuantTrio/Qwen3.6-27B-AWQ
22 GB

https://huggingface.co/rdtand/Qwen3.6-27B-PrismaQuant-5.5bit-vllm
22 GB

https://huggingface.co/QuantTrio/Qwen3.6-27B-AWQ-6Bit
27 GB

https://huggingface.co/cyankiwi/Qwen3.6-27B-AWQ-BF16-INT4
28 GB

https://huggingface.co/unsloth/Qwen3.6-27B-NVFP4/tree/main
28GB
```

Someone running vLLM on dual 5060 ti 16 gb.
https://huggingface.co/cyankiwi/Qwen3.6-27B-AWQ-BF16-INT4/discussions/5

## Benchmarking llama-cpp concurrency

Using guidellm to compare directly with vLLM

```
wget -O models/Qwen3.6-27B-Q4_K_M.gguf https://huggingface.co/unsloth/Qwen3.6-27B-MTP-GGUF/resolve/main/Qwen3.6-27B-Q4_K_M.gguf?download=true
```

First with standard split-mode layer

! must use HuggingFace name for guidellm to work

```
; Qwen3.6 27B 
[Qwen/Qwen3.6-27B]
load-on-startup = true
model = /models/Qwen3.6-27B-Q4_K_M.gguf
; --fit system handles ngl automatically, no manual n-cpu-moe needed
fit = false
ngl = 99
;fit-target = 300
;fit-ctx = 200000
ctx-size = 210000
parallel = 3
; model config
; Based on Unsloth recommendations https://unsloth.ai/docs/models/qwen3.6
temp = 1.0
top-p = 0.95
top-k = 20
min-p = 0.0
presence-penalty = 1.5
repeat-penalty = 1.0
chat-template-kwargs = {"enable_thinking": false}
; performance config
; no-mmap = true
; split-mode = tensor
spec-type = draft-mtp
spec-draft-n-max = 2
flash-attn = true
; batch-size = 2048
; ubatch-size = 2048
cache-type-k = q8_0
cache-type-v = q8_0
main-gpu = 0
```

Running without API key for guidellm
```
./llama-server --port 8080 --host 0.0.0.0 --models-preset /models/llama-preset.ini --models-max 1
```

```
podman run \
  --rm -it \
  -v "/home/jon/guidellm/results:/results:rw" \
  -e GUIDELLM_TARGET=http://host.containers.internal:8080 \
  -e GUIDELLM_PROFILE=concurrent \
  -e GUIDELLM_RATE=1,2,4,8,16 \
  -e GUIDELLM_MAX_SECONDS=30 \
  -e GUIDELLM_DATA="type=synthetic_text,prompt_tokens=256,output_tokens=128" \
  ghcr.io/vllm-project/guidellm:latest
```

```
│ [16:38:55]   100% concurrent@1  (complete)   Req:    0.2 req/s,    3.99s Lat,     1.0 Conc,       8 Comp,        0 Inc,        0 Err                                                       │
│                                              Tok:   32.9 gen/s,  101.7 tot/s, 572.0ms TTFT,   26.9ms ITL,   268 Prompt,      128 Gen                                                       │
│ [16:39:29]   100% concurrent@2  (complete)   Req:    0.3 req/s,    6.81s Lat,     2.0 Conc,       9 Comp,        1 Inc,        0 Err                                                       │
│                                              Tok:   36.4 gen/s,  112.8 tot/s, 781.9ms TTFT,   47.5ms ITL,   268 Prompt,      128 Gen                                                       │
│ [16:40:07]   100% concurrent@4  (complete)   Req:    0.3 req/s,   11.90s Lat,     3.8 Conc,      10 Comp,        3 Inc,        0 Err                                                       │
│                                              Tok:   37.8 gen/s,  117.1 tot/s, 3645.9ms TTFT,   65.0ms ITL,   268 Prompt,      128 Gen                                                      │
│ [16:40:44]   100% concurrent@8  (complete)   Req:    0.3 req/s,   17.76s Lat,     5.8 Conc,      10 Comp,        7 Inc,        0 Err                                                       │
│                                              Tok:   38.1 gen/s,  117.9 tot/s, 9928.9ms TTFT,   61.7ms ITL,   268 Prompt,      128 Gen                                                      │
│ [16:41:20]   100% concurrent@16 (complete)   Req:    0.3 req/s,   19.79s Lat,     5.9 Conc,       9 Comp,       15 Inc,        0 Err                                                       │
│                                              Tok:   41.7 gen/s,  128.9 tot/s, 11723.1ms TTFT,   63.5ms ITL,   268 Prompt,      128 Gen    
```

Trying with split mode tensor.
!! does not work with router and preset file

But running server directly does work?

```
./llama-server --port 8080 --host 0.0.0.0 --model /models/Qwen3.6-27B-Q4_K_M.gguf --alias Qwen/Qwen3.6-27B7 --ctx-size 100000 --parallel 3 --split-mode tensor --fit off 
```


```
ℹ Server Throughput Statistics (All Requests)
|============|=======|======|=========|==============|===============|==============|
| Benchmark  | Requests             ||| Input Tokens | Output Tokens | Total Tokens |
| Strategy   | Concurrency || Per Sec | Per Sec      | Per Sec       | Per Sec      |
|            | Mdn   | Mean | Mean                                               ||||
|------------|-------|------|---------|--------------|---------------|--------------|
| concurrent | 1.0   | 1.0  | 0.3     | 82.9         | 39.9          | 122.8        |
| concurrent | 2.0   | 2.0  | 0.2     | 46.7         | 22.5          | 69.2         |
| concurrent | 4.0   | 4.0  | 0.5     | 200.4        | 91.6          | 292.0        |
| concurrent | 8.0   | 8.0  | 0.5     | 237.9        | 90.3          | 328.2        |
| concurrent | 16.0  | 16.0 | 0.5     | 316.3        | 89.8          | 406.0        |
|============|=======|======|=========|==============|===============|==============|
```

Way under half of vLLM, to 1/4. But this is without MTP speculative decoding.


Trying with speculative decoting.

```
./llama-server --port 8080 --host 0.0.0.0 --model /models/Qwen3.6-27B-Q4_K_M.gguf --alias Qwen/Qwen3.6-27B --ctx-size 100000 --parallel 3 --split-mode tensor --fit of
f --spec-type draft-mtp --spec-draft-n-max 2
```

```
ℹ Server Throughput Statistics (All Requests)
|============|=======|======|=========|==============|===============|==============|
| Benchmark  | Requests             ||| Input Tokens | Output Tokens | Total Tokens |
| Strategy   | Concurrency || Per Sec | Per Sec      | Per Sec       | Per Sec      |
|            | Mdn   | Mean | Mean                                               ||||
|------------|-------|------|---------|--------------|---------------|--------------|
| concurrent | 1.0   | 1.0  | 0.4     | 124.6        | 60.0          | 184.6        |
| concurrent | 2.0   | 2.0  | 0.2     | 83.6         | 34.7          | 118.2        |
| concurrent | 4.0   | 4.0  | 0.1     | 126.3        | 46.0          | 172.4        |
| concurrent | 8.0   | 8.0  | 0.1     | 188.3        | 38.6          | 227.0        |
| concurrent | 16.0  | 16.0 | 0.1     | 321.0        | 33.5          | 354.5        |
|============|=======|======|=========|==============|===============|==============|
```

Better for low concurrency, but even worse for higher in terms of output tokens.


## Testing quad 5060 ti on x570

Still waiting for bifurcation PCIE adapters.
Must use the chipset slot for now (M2_2 or PCIE_16).
Maybe move NVME into SATA enclosure? Or could even use USB...

First try.
Using 4th card plugged into M.2 
Showing in lspci, but not in nvidia-smi.

Was unable to booth with NVME in SATA adapter.
Disk was not seen in BIOS.
Using USB-C NVME adapter worked, but only with USB-C to Type A adapter - not with C to C cable.

After forcing the M2 slots to Gen 4 in BIOS,
can boot.

! was seeing a bit sluggish behavior when connecting over SSH.

```
nvidia-smi --query-gpu=index,name,pcie.link.gen.current,pcie.link.gen.max,pcie.link.width.current,pcie.link.width.max --format=csv
index, name, pcie.link.gen.current, pcie.link.gen.max, pcie.link.width.current, pcie.link.width.max
0, NVIDIA GeForce RTX 5060 Ti, 4, 4, 4, 8
1, NVIDIA GeForce RTX 5060 Ti, 4, 4, 4, 8
2, NVIDIA GeForce RTX 5060 Ti, 4, 4, 8, 8
3, NVIDIA GeForce RTX 5060 Ti, 4, 4, 8, 8
```

```
docker run --rm --name vllm   --gpus '"device=0,1,2,3"'   -v /home/jon/models/vllm/cache/huggingface:/root/.cache/huggingface   --env "HF_TOKEN=$HF_TOKEN"   -p 8000:8000   --ipc=host   vllm/vllm-openai:latest   --model sakamakismile/Qwen3.6-27B-Text-NVFP4-MTP   --served-model-name qwen36-nvfp4-mtp   --tensor-parallel-size 4   --pipeline-parallel-size 1   --max-model-len 104800   --max-num-batched-tokens 8192   --max-num-seqs 1   --gpu-memory-utilization 0.90   --kv-cache-dtype fp8   --quantization modelopt   --speculative-config '{"method":"mtp","num_speculative_tokens":3}'   --reasoning-parser qwen3   --language-model-only   --generation-config vllm   --disable-custom-all-reduce   --enable-auto-tool-choice   --tool-call-parser qwen3_coder   --attention-backend TRITON_ATTN
```

Did not get up and running in 3 minutes
```
(EngineCore pid=243) INFO 05-31 13:50:02 [shm_broadcast.py:698] No available shared memory broadcast block found in 60 seconds. This typically happens when some processes are hanging or doing some time-consuming work (e.g. compilation, weight/kv cache quantization).
```

Trying llama.cpp


```
docker run --rm --gpus '"device=1,2,0,3"' -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda13-b9404
```

```
root@dc2b7dc07c14:/app# ./llama-bench -m /models/Qwen3.6-27B-UD-Q4_K_XL.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048
ggml_cuda_init: found 4 CUDA devices (Total VRAM: 63532 MiB):
  Device 0: NVIDIA GeForce RTX 5060 Ti, compute capability 12.0, VMM: yes, VRAM: 15888 MiB
  Device 1: NVIDIA GeForce RTX 5060 Ti, compute capability 12.0, VMM: yes, VRAM: 15888 MiB
  Device 2: NVIDIA GeForce RTX 5060 Ti, compute capability 12.0, VMM: yes, VRAM: 15866 MiB
  Device 3: NVIDIA GeForce RTX 5060 Ti, compute capability 12.0, VMM: yes, VRAM: 15888 MiB
load_backend: loaded CUDA backend from /app/libggml-cuda.so
load_backend: loaded CPU backend from /app/libggml-cpu-haswell.so
| model                          |       size |     params | backend    | ngl | threads | n_ubatch | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | ------: | -------: | -: | ---------: | ----------: | --------------: | -------------------: |
/app/ggml/src/ggml-cuda/ggml-cuda.cu:103: CUDA error
libggml-base.so.0(+0x1b176)[0x7faf850e2176]
libggml-base.so.0(ggml_print_backtrace+0x21a)[0x7faf850e25fa]
libggml-base.so.0(ggml_abort+0x15b)[0x7faf850e27db]
/app/libggml-cuda.so(_Z15ggml_cuda_errorPKcS0_S0_iS0_+0xb5)[0x7faf7b2be955]
/app/libggml-cuda.so(+0x29627b)[0x7faf7b2bf27b]
```

Failed with error.
! no longer listed in nvidia-smi.

Tried swapping cable.

Was able to run llama-bench default.
Low performance, 737 / 22.

```
./llama-bench -m /models/Qwen3.6-27B-UD-Q4_K_XL.gguf -pg 7500,512 -t 8 -fa 1 -b 2048 -ub 2048 -sm tensor

| model                          |       size |     params | backend    | ngl | n_ubatch |     sm | fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | -----: | -: | --------------: | -------------------: |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |     2048 | tensor |  1 |           pp512 |       415.29 ± 18.86 |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |     2048 | tensor |  1 |           tg128 |         37.22 ± 0.33 |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |     2048 | tensor |  1 |    pp7500+tg512 |        274.90 ± 0.47 |
```

Poor results, worse than dual GPU.
Utilization is around 50-60%.
Or sometimes 90% on two GPUS, and 50% on the other.

Testing just the two x8 GPUs
```
docker run --rm --gpus '"device=3,2"' -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda13-b9404
groups: cannot find name for group ID 992

 ./llama-bench -m /models/Qwen3.6-27B-UD-Q4_K_XL.gguf -pg 7500,512 -t 8 -fa 1 -b 2048 -ub 2048 -sm tensor

| model                          |       size |     params | backend    | ngl | n_ubatch |     sm | fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | -----: | -: | --------------: | -------------------: |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |     2048 | tensor |  1 |           pp512 |       970.25 ± 81.96 |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |     2048 | tensor |  1 |           tg128 |         38.30 ± 0.23 |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |     2048 | tensor |  1 |    pp7500+tg512 |        414.68 ± 1.12 |
```

Testing just the two x4 GPUs

```
jon@soundsensing-test-gpu-2:~$ docker run --rm --gpus '"device=0,1"' -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda13-b9404
groups: cannot find name for group ID 992

root@5b55834c1a58:/app# ./llama-bench -m /models/Qwen3.6-27B-UD-Q4_K_XL.gguf -pg 7500,512 -t 8 -fa 1 -b 2048 -ub 2048 -sm tensor

| model                          |       size |     params | backend    | ngl | n_ubatch |     sm | fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | -----: | -: | --------------: | -------------------: |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |     2048 | tensor |  1 |           pp512 |       801.94 ± 55.38 |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |     2048 | tensor |  1 |           tg128 |         38.04 ± 0.12 |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |     2048 | tensor |  1 |    pp7500+tg512 |        379.96 ± 0.88 |
```
Slight reduction in prefill, but generation is same.

Testing x8 GPU with x4

```
docker run --rm --gpus '"device=2,0"' -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda13-b9404
groups: cannot find name for group ID 992
root@f07113dcdf53:/app# ./llama-bench -m /models/Qwen3.6-27B-UD-Q4_K_XL.gguf -pg 7500,512 -t 8 -fa 1 -b 2048 -ub 2048 -sm tensor
ggml_cuda_init: found 2 CUDA devices (Total VRAM: 31754 MiB):
  Device 0: NVIDIA GeForce RTX 5060 Ti, compute capability 12.0, VMM: yes, VRAM: 15888 MiB
  Device 1: NVIDIA GeForce RTX 5060 Ti, compute capability 12.0, VMM: yes, VRAM: 15866 MiB
load_backend: loaded CUDA backend from /app/libggml-cuda.so
load_backend: loaded CPU backend from /app/libggml-cpu-haswell.so
| model                          |       size |     params | backend    | ngl | n_ubatch |     sm | fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | -----: | -: | --------------: | -------------------: |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |     2048 | tensor |  1 |           pp512 |       828.30 ± 58.91 |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |     2048 | tensor |  1 |           tg128 |         38.50 ± 0.14 |
```

Close to x4+x4.

Same devices just reversed order

```
docker run --rm --gpus '"device=0,2"' -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda13-b9404

./llama-bench -m /models/Qwen3.6-27B-UD-Q4_K_XL.gguf -pg 7500,512 -t 8 -fa 1 -b 2048 -ub 2048 -sm tensor

| model                          |       size |     params | backend    | ngl | n_ubatch |     sm | fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | -----: | -: | --------------: | -------------------: |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |     2048 | tensor |  1 |           pp512 |       825.58 ± 58.06 |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |     2048 | tensor |  1 |           tg128 |         38.51 ± 0.13 |
```

Order does not seem to matter.

Testing other x4 GPU.

```
docker run --rm --gpus '"device=1,2"' -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda13-b9404

| model                          |       size |     params | backend    | ngl | n_ubatch |     sm | fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | -----: | -: | --------------: | -------------------: |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |     2048 | tensor |  1 |           pp512 |       804.79 ± 55.02 |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |     2048 | tensor |  1 |           tg128 |         38.02 ± 0.15 |
```

Very minor difference.

Retesting vLLM. Now that the GPUs themselves seem stable.

```
docker run --rm --name vllm   --gpus '"device=0,1,2,3"'   -v /home/jon/models/vllm/cache/huggingface:/root/.cache/huggingface   --env "HF_TOKEN=$HF_TOKEN"   -p 8000:8000   --ipc=host   vllm/vllm-openai:latest   --model sakamakismile/Qwen3.6-27B-Text-NVFP4-MTP   --served-model-name qwen36-nvfp4-mtp   --tensor-parallel-size 4   --pipeline-parallel-size 1   --max-model-len 104800   --max-num-batched-tokens 8192   --max-num-seqs 1   --gpu-memory-utilization 0.90   --kv-cache-dtype fp8   --quantization modelopt   --speculative-config '{"method":"mtp","num_speculative_tokens":3}'   --reasoning-parser qwen3   --language-model-only   --generation-config vllm   --disable-custom-all-reduce   --enable-auto-tool-choice   --tool-call-parser qwen3_coder   --attention-backend TRITON_ATTN
```

Seeing 70-100 for "Avg generation throughput" on Python codegen and bible text.

Trying higher concurrency configuration
```
docker run --rm --name vllm   --gpus '"device=0,1,2,3"'   -v /home/jon/models/vllm/cache/huggingface:/root/.cache/huggingface   --env "HF_TOKEN=$HF_TOKEN"   -p 8000:8000   --ipc=host   vllm/vllm-openai:latest   --model sakamakismile/Qwen3.6-27B-Text-NVFP4-MTP   --served-model-name qwen36-nvfp4-mtp   --tensor-parallel-size 4   --pipeline-parallel-size 1   --max-model-len 104800   --max-num-batched-tokens 8192   --max-num-seqs 8   --gpu-memory-utilization 0.90   --kv-cache-dtype fp8   --quantization modelopt   --speculative-config '{"method":"mtp","num_speculative_tokens":3}'   --reasoning-parser qwen3   --language-model-only   --generation-config vllm   --disable-custom-all-reduce   --enable-auto-tool-choice   --tool-call-parser qwen3_coder   --attention-backend TRITON_ATTN
```



https://huggingface.co/datasets/likaixin/InstructCoder
is just 150 MB

https://docs.vllm.ai/en/stable/benchmarking/cli/#interactive-timeline


Have to not use --served-model-name to use with guidellm...

```
docker run --rm --name vllm   --gpus '"device=0,1,2,3"'   -v /home/jon/models/vllm/cache/huggingface:/root/.cache/huggingface   --env "HF_TOKEN=$HF_TOKEN"   -p 8000:8000   --ipc=host   vllm/vllm-openai:latest   --model sakamakismile/Qwen3.6-27B-Text-NVFP4-MTP  --tensor-parallel-size 4   --pipeline-parallel-size 1   --max-model-len 104800   --max-num-batched-tokens 8192   --max-num-seqs 8   --gpu-memory-utilization 0.90   --kv-cache-dtype fp8   --quantization modelopt   --speculative-config '{"method":"mtp","num_speculative_tokens":3}'   --reasoning-parser qwen3   --language-model-only   --generation-config vllm   --disable-custom-all-reduce   --enable-auto-tool-choice   --tool-call-parser qwen3_coder   --attention-backend TRITON_ATTN
```

```
podman run \
  --rm -it \
  -v "./results:/results:rw" \
  -e GUIDELLM_TARGET=http://host.containers.internal:8000 \
  -e GUIDELLM_PROFILE=sweep \
  -e GUIDELLM_MAX_SECONDS=30 \
  -e GUIDELLM_DATA="type=synthetic_text,prompt_tokens=256,output_tokens=128" \
  ghcr.io/vllm-project/guidellm:latest
```

Seeing GPU utilization at 95%.
Power per GPU only 70-80watt.

! Not sure how to interpret the output...


```
podman run \
  --rm -it \
  -v "/home/jon/guidellm/results:/results:rw" \
  -e GUIDELLM_TARGET=http://host.containers.internal:8000 \
  -e GUIDELLM_PROFILE=concurrent \
  -e GUIDELLM_RATE=1,2,4,8,16 \
  -e GUIDELLM_MAX_SECONDS=30 \
  -e GUIDELLM_DATA="type=synthetic_text,prompt_tokens=256,output_tokens=128" \
  ghcr.io/vllm-project/guidellm:latest
```

```
ℹ Server Throughput Statistics (All Requests)
|============|=======|======|=========|==============|===============|==============|
| Benchmark  | Requests             ||| Input Tokens | Output Tokens | Total Tokens |
| Strategy   | Concurrency || Per Sec | Per Sec      | Per Sec       | Per Sec      |
|            | Mdn   | Mean | Mean                                               ||||
|------------|-------|------|---------|--------------|---------------|--------------|
| concurrent | 1.0   | 1.0  | 0.6     | 176.4        | 84.9          | 261.3        |
| concurrent | 2.0   | 2.0  | 1.0     | 309.4        | 145.8         | 455.1        |
| concurrent | 4.0   | 4.0  | 1.5     | 464.6        | 217.4         | 682.0        |
| concurrent | 8.0   | 8.0  | 2.0     | 681.4        | 306.7         | 988.1        |
| concurrent | 16.0  | 16.0 | 2.0     | 758.4        | 306.5         | 1064.9       |
|============|=======|======|=========|==============|===============|==============|
```

Over 50 generated tok/s for 4 concurrent. Nice!
Not much performance improvement after 8 concurrent.
Expected since had `--max-num-seqs 8`.

85 tok/s for single request is also good.
This is around what people report on a RTX 5090.
https://www.reddit.com/r/LocalLLaMA/comments/1sr8gyf/qwen3527b_on_rtx_5090_served_via_vllm_77_tps/


Note that agentic coding workflows probably will be more input heavy.

Retesting with just the two internal GPUs.

```
docker run --rm --name vllm   --gpus '"device=2,3"'   -v /home/jon/
models/vllm/cache/huggingface:/root/.cache/huggingface   --env "HF_TOKEN=$HF_TOKEN"   -p 8000:8000
   --ipc=host   vllm/vllm-openai:latest   --model sakamakismile/Qwen3.6-27B-Text-NVFP4-MTP  --tens
or-parallel-size 2 --pipeline-parallel-size 1   --max-model-len 104800   --max-num-batched-tokens 
8192   --max-num-seqs 8   --gpu-memory-utilization 0.90   --kv-cache-dtype fp8   --quantization modelopt   --speculative-config '{"method":"mtp","num_speculative_tokens":3}'   --reasoning-parser qwen3   --language-model-only   --generation-config vllm   --disable-custom-all-reduce   --enable-auto-tool-choice   --tool-call-parser qwen3_coder   --attention-backend TRITON_ATT
```

Seeing over 100 watt per GPU now.

```
ℹ Server Throughput Statistics (All Requests)
|============|=======|======|=========|==============|===============|==============|
| Benchmark  | Requests             ||| Input Tokens | Output Tokens | Total Tokens |
| Strategy   | Concurrency || Per Sec | Per Sec      | Per Sec       | Per Sec      |
|            | Mdn   | Mean | Mean                                               ||||
|------------|-------|------|---------|--------------|---------------|--------------|
| concurrent | 1.0   | 1.0  | 0.5     | 140.7        | 67.7          | 208.4        |
| concurrent | 2.0   | 2.0  | 0.8     | 255.1        | 119.6         | 374.6        |
| concurrent | 4.0   | 4.0  | 1.5     | 439.0        | 209.5         | 648.6        |
| concurrent | 8.0   | 8.0  | 2.1     | 686.3        | 311.8         | 998.1        |
| concurrent | 16.0  | 16.0 | 2.1     | 753.9        | 314.0         | 1067.8       |
|============|=======|======|=========|==============|===============|==============|
```

67 tok/s in single case, down from 85 tok/s.
60 tok/s for 2 concurrent, and still around 50 tok/s for 5 concurrent. 

So in a concurrent scenario, actually able match quad GPU!?

This combined with low power usage per GPU of quad indicates
that PCIE Gen 4 x4 is actually a bottleneck in this configuration.

`TODO: test in practice with concurrent agentic coding tools`

## Testing triple 5060 ti on x570 with llama-cpp

Want to enable higher performance with concurrency, for multi-user setups.
And enable running higher quants.

Only two cards can run PCIE Gen 4 x8.
The other two will have to run PCIE Gen 4 x4, via chipset and M2 slot.

!? PCIE16_3 might share lanes with M2 slot? Though manual does not mention it...

Might want to try uneven split using llama-cpp options?

The main PCIE16_1 supports x8/x4/x4 bifurcation.
Which if one has the right adapter would allow x8/x4/x4 + x4 from chipset. 
With one NVME still left on M.2 directly to CPU.

In theory, it is possible to use x8/x4/x4 with x4/x4/x4 say Occulink.

eGPU adaptors for x8 Oculink also exists, but much more rare than x4.
Often called 8i, like Oculink SFF-8611/8612 8i.

Testing on ROG Crosshair VIII Hero.
X570 with x8 x8 in PCIE 1 and 2.
And third card using M2 slot via Oculink (x4).

```
nvidia-smi --query-gpu=index,name,pcie.link.gen.current,pcie.link.gen.max,pcie.link.width.current,pcie.link.width.max --format=csv
index, name, pcie.link.gen.current, pcie.link.gen.max, pcie.link.width.current, pcie.link.width.max
index, name, pcie.link.gen.current, pcie.link.gen.max, pcie.link.width.current, pcie.link.width.max
0, NVIDIA GeForce RTX 5060 Ti, 4, 4, 4, 8
1, NVIDIA GeForce RTX 5060 Ti, 4, 4, 8, 8
2, NVIDIA GeForce RTX 5060 Ti, 4, 4, 8, 8
-bash: index,: command not found
```

```
docker run --rm --gpus '"device=0,1,2"' -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda13-b9404

./llama-bench -m /models/Qwen3.6-27B-UD-Q4_K_XL.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048

| model                          |       size |     params | backend    | ngl | threads | n_ubatch | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | ------: | -------: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |       6 |     2048 |  1 |        300 |      100000 |           pp512 |       775.90 ± 39.49 |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |       6 |     2048 |  1 |        300 |      100000 |           tg128 |         22.19 ± 0.04 |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |       6 |     2048 |  1 |        300 |      100000 |    pp7500+tg512 |        268.88 ± 0.67 |

build: 241cbd41d (9404)
```

! BAD. Worse than dual 5060 ti on jon-workstation.
GPU utilization is low, around 30-40%.
Could it be because the x4 card is index 0, and that causes bottlenecks?

Trying to reorder
```
docker run --rm --gpus '"device=1,2,0"' -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda13-b9404
```

Can see that GPU 2 got slightly more layers, 6 GB vs 5 GB usage.

```
./llama-bench -m /models/Qwen3.6-27B-UD-Q4_K_XL.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048
| model                          |       size |     params | backend    | ngl | threads | n_ubatch | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | ------: | -------: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |       6 |     2048 |  1 |        300 |      100000 |           pp512 |       773.71 ± 45.00 |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |       6 |     2048 |  1 |        300 |      100000 |           tg128 |         22.19 ± 0.04 |
```

Same bad performance.

Doing a reference with two GPUs both on x8 x8
```
docker run --rm --gpus '"device=1,2"' -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda13-b9404

./llama-bench -m /models/Qwen3.6-27B-UD-Q4_K_XL.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048

| model                          |       size |     params | backend    | ngl | threads | n_ubatch | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | ------: | -------: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |       6 |     2048 |  1 |        300 |      100000 |           pp512 |       780.44 ± 38.85 |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |       6 |     2048 |  1 |        300 |      100000 |           tg128 |         22.20 ± 0.04 |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |       6 |     2048 |  1 |        300 |      100000 |    pp7500+tg512 |        276.09 ± 0.93 |
```

Same performance as 3 GPUs. And worse by 10% compared to workstation.
What gives?

! CPU memory was defaulting to 2133 Mhz. Have now set to official 3200 Mhz

```
docker run --rm --gpus '"device=1,2"' -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda13-b9404

./llama-bench -m /models/Qwen3.6-27B-UD-Q4_K_XL.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048

| model                          |       size |     params | backend    | ngl | threads | n_ubatch | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | ------: | -------: | -: | ---------: | ----------: | --------------: | -------------------: |
^Aa^[[O| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |       6 |     2048 |  1 |        300 |      100000 |           pp512 |       777.32 ± 39.60 |
^[[I^[[O| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |       6 |     2048 |  1 |        300 |      100000 |           tg128 |         22.21 ± 0.04 |
```

Same bad. Also with 3 GPUs.

Plugged out the GPU that was on Occulink.
```
Same performance...
```

Driver and CUDA version on host

```
| NVIDIA-SMI 610.43.02              KMD Version: 610.43.02     CUDA UMD Version: 13.3     |

Linux soundsensing-test-gpu-2 6.12.90+deb13.1-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.90-2 (2026-05-27) x86_64 GNU/Linux
```

Tested default configuration (above)
```
nvoc info -d all
driver: 610.43.02
gpu 0: NVIDIA GeForce RTX 5060 Ti
gpu clock: 2812MHz
gpu offset: 0MHz
mem clock: 13801MHz
mem offset: 0MHz
temp: 46°C
power: 84W
power limit: 180W (100%)
power range: 150W-180W (180W hard limit)
gpu 1: NVIDIA GeForce RTX 5060 Ti
gpu clock: 2775MHz
gpu offset: 0MHz
mem clock: 13801MHz
mem offset: 0MHz
temp: 48°C
power: 106W
power limit: 180W (100%)
power range: 150W-180W (180W hard limit)
```

Trying to overclock

```
sudo nvoc -o 150 -m 3000 -d 0,1
```

```
./llama-bench -m /models/Qwen3.6-27B-UD-Q4_K_XL.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048
ggml_cuda_init: found 2 CUDA devices (Total VRAM: 31754 MiB):
  Device 0: NVIDIA GeForce RTX 5060 Ti, compute capability 12.0, VMM: yes, VRAM: 15866 MiB
  Device 1: NVIDIA GeForce RTX 5060 Ti, compute capability 12.0, VMM: yes, VRAM: 15888 MiB
load_backend: loaded CUDA backend from /app/libggml-cuda.so
load_backend: loaded CPU backend from /app/libggml-cpu-haswell.so
| model                          |       size |     params | backend    | ngl | threads | n_ubatch | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | ------: | -------: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |       6 |     2048 |  1 |        300 |      100000 |           pp512 |       810.57 ± 44.36 |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |       6 |     2048 |  1 |        300 |      100000 |           tg128 |         24.46 ± 0.05 |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |       6 |     2048 |  1 |        300 |      100000 |    pp7500+tg512 |        301.35 ± 1.09 |
```
Got slight boost.
But still worse than workstation, even when that has no OC. Especially prefill.


Trying split mode tensor with dual GPU
```
./llama-bench -m /models/Qwen3.6-27B-UD-Q4_K_XL.gguf -pg 7500,512 -t 8 -fa 1 -b 2048 -ub 2048 -sm tensor
ggml_cuda_init: found 2 CUDA devices (Total VRAM: 31754 MiB):
  Device 0: NVIDIA GeForce RTX 5060 Ti, compute capability 12.0, VMM: yes, VRAM: 15866 MiB
  Device 1: NVIDIA GeForce RTX 5060 Ti, compute capability 12.0, VMM: yes, VRAM: 15888 MiB
load_backend: loaded CUDA backend from /app/libggml-cuda.so
load_backend: loaded CPU backend from /app/libggml-cpu-haswell.so
| model                          |       size |     params | backend    | ngl | n_ubatch |     sm | fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | -----: | -: | --------------: | -------------------: |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |     2048 | tensor |  1 |           pp512 |      1068.37 ± 70.97 |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |     2048 | tensor |  1 |           tg128 |         42.34 ± 0.25 |
| qwen35 27B Q4_K - Medium       |  16.39 GiB |    26.90 B | CUDA       |  99 |     2048 | tensor |  1 |    pp7500+tg512 |        446.52 ± 1.15 |

```

Big improvement in throughput.
Also seeing power draws of 100-170 watt instead of 60-100.

Adding back eGPU.

```
sudo nvoc -o 150 -m 3000 -d 0,1,2
```

```
docker run --rm --gpus '"device=1,2,0"' -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda13-b9404
```

```
/app/ggml/src/ggml-backend-meta.cpp:1052: GGML_ASSERT(split_state.ne[j] * tensor->src[i]->ne[src_ss[i].axis] == sum * tensor->ne[split_state.axis]) failed
```
Crashed - maybe splitting over 3 does not work?

## Testing triple GPU on vLLM

For reference dual case
```
docker run --rm --name vllm \
  --gpus '"device=0,1"' \
  -v /home/jon/models/vllm/cache/huggingface:/root/.cache/huggingface \
  --env "HF_TOKEN=$HF_TOKEN" \
  -p 8000:8000 \
  --ipc=host \
  vllm/vllm-openai:latest \
  --model sakamakismile/Qwen3.6-27B-Text-NVFP4-MTP \
  --served-model-name qwen36-nvfp4-mtp \
  --tensor-parallel-size 2 \
  --max-model-len 104800 \
  --max-num-batched-tokens 8192 \
  --max-num-seqs 1 \
  --gpu-memory-utilization 0.90 \
  --kv-cache-dtype fp8 \
  --quantization modelopt \
  --speculative-config '{"method":"mtp","num_speculative_tokens":3}' \
  --reasoning-parser qwen3 \
  --language-model-only \
  --generation-config vllm \
  --disable-custom-all-reduce \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder \
  --attention-backend TRITON_ATTN
```

Testing via OpenWebUI.
Getting up to 75 tok/s for first chapter of Bible.
And for a Python TODO app.
Seing utilization of 95%.

Trying 3 GPU with tensor parallel

```
docker run --rm --name vllm \
  --gpus '"device=0,1,2"' \
  -v /home/jon/models/vllm/cache/huggingface:/root/.cache/huggingface \
  --env "HF_TOKEN=$HF_TOKEN" \
  -p 8000:8000 \
  --ipc=host \
  vllm/vllm-openai:latest \
  --model sakamakismile/Qwen3.6-27B-Text-NVFP4-MTP \
  --served-model-name qwen36-nvfp4-mtp \
  --tensor-parallel-size 3 \
  --max-model-len 104800 \
  --max-num-batched-tokens 8192 \
  --max-num-seqs 1 \
  --gpu-memory-utilization 0.90 \
  --kv-cache-dtype fp8 \
  --quantization modelopt \
  --speculative-config '{"method":"mtp","num_speculative_tokens":3}' \
  --reasoning-parser qwen3 \
  --language-model-only \
  --generation-config vllm \
  --disable-custom-all-reduce \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder \
  --attention-backend TRITON_ATTN
```

```
(Worker_TP0 pid=285) ERROR 05-30 19:59:18 [multiproc_executor.py:870]   File "/usr/local/lib/python3.12
/dist-packages/vllm/distributed/utils.py", line 55, in ensure_divisibility                             
(Worker_TP0 pid=285) ERROR 05-30 19:59:18 [multiproc_executor.py:870]     assert numerator % denominato
r == 0, "{} is not divisible by {}".format(                                                            
(Worker_TP0 pid=285) ERROR 05-30 19:59:18 [multiproc_executor.py:870]            ^^^^^^^^^^^^^^^^^^^^^^
^^^^^^                                                                                                 
(Worker_TP0 pid=285) ERROR 05-30 19:59:18 [multiproc_executor.py:870] AssertionError: 16 is not divisib
le by 3   
```
Errors. Likely need to have 4 GPUs.


Trying pipeline-parallel with 3 GPUs.
```
docker run --rm --name vllm \
  --gpus '"device=0,1,2"' \
  -v /home/jon/models/vllm/cache/huggingface:/root/.cache/huggingface \
  --env "HF_TOKEN=$HF_TOKEN" \
  -p 8000:8000 \
  --ipc=host \
  vllm/vllm-openai:latest \
  --model sakamakismile/Qwen3.6-27B-Text-NVFP4-MTP \
  --served-model-name qwen36-nvfp4-mtp \
  --tensor-parallel-size 1 \
  --pipeline-parallel-size 3 \
  --max-model-len 104800 \
  --max-num-batched-tokens 8192 \
  --max-num-seqs 1 \
  --gpu-memory-utilization 0.90 \
  --kv-cache-dtype fp8 \
  --quantization modelopt \
  --speculative-config '{"method":"mtp","num_speculative_tokens":3}' \
  --reasoning-parser qwen3 \
  --language-model-only \
  --generation-config vllm \
  --disable-custom-all-reduce \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder \
  --attention-backend TRITON_ATTN
```

```
(APIServer pid=1) NotImplementedError: Pipeline parallelism is not supported for this model. Supported models implement the `SupportsPP` interface.
```

"vLLM does not currently support enabling both pipeline parallelism and speculative decoding at the same time."
Mar 10, 2026
https://github.com/vllm-project/vllm/issues/36643


## Testing slower PCIE connectivity dual 5060

With PCIE Gen 4 x8/x8 (reference)
```
[jon@jon-workstation ~]$ docker run --rm --gpus '"device=0,1"' -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda13-b9404
root@668a6b054548:/app# ./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048
| model                          |       size |     params | backend    | ngl | n_ubatch | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           pp512 |      2779.09 ± 17.41 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           tg128 |        121.38 ± 0.24 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |    pp7500+tg512 |       1342.96 ± 1.26 |

root@668a6b054548:/app# ./llama-bench -m /models/Qwen3.6-27B-UD-Q4_K_XL.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048
| model                          |       size |     params | backend    | ngl | n_ubatch | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35 27B Q4_K - Medium       |  16.67 GiB |    27.32 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           pp512 |        990.27 ± 9.11 |
| qwen35 27B Q4_K - Medium       |  16.67 GiB |    27.32 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           tg128 |         24.84 ± 0.01 |
| qwen35 27B Q4_K - Medium       |  16.67 GiB |    27.32 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |    pp7500+tg512 |        303.08 ± 0.05 |

build: 241cbd41d (9404)
```

With PCIE Gen 3 x8/x8. To simulate bandwidth of PCIE Gen 4 x4/x4.
BIOS had no setting for the number of lanes.
```
nvidia-smi --query-gpu=index,name,pcie.link.gen.current,pcie.link.gen.max,pcie.link.width.current,pcie.link.width.max --format=csv
index, name, pcie.link.gen.current, pcie.link.gen.max, pcie.link.width.current, pcie.link.width.max
0, NVIDIA GeForce RTX 5060 Ti, 3, 3, 8, 8
1, NVIDIA GeForce RTX 5060 Ti, 3, 3, 8, 16
```

```
[jon@jon-workstation ~]$ docker run --rm --gpus '"device=0,1"' -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda13-b9404

root@9e827c5226f1:/app# ./llama-bench -m /models/Qwen3.6-27B-UD-Q4_K_XL.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048

| model                          |       size |     params | backend    | ngl | n_ubatch | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35 27B Q4_K - Medium       |  16.67 GiB |    27.32 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           pp512 |        934.58 ± 8.43 |
| qwen35 27B Q4_K - Medium       |  16.67 GiB |    27.32 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           tg128 |         22.46 ± 0.00 |
| qwen35 27B Q4_K - Medium       |  16.67 GiB |    27.32 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |    pp7500+tg512 |        276.69 ± 0.04 |

build: 241cbd41d (9404)
```

Around 10% performance drop.

Trying overclock to see if able to regain some performance.

```
sudo nvoc -o 150 -m 3000 -d 0,1
```

```
./llama-bench -m /models/Qwen3.6-27B-UD-Q4_K_XL.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048
| model                          |       size |     params | backend    | ngl | n_ubatch | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35 27B Q4_K - Medium       |  16.67 GiB |    27.32 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           pp512 |        984.50 ± 8.45 |
| qwen35 27B Q4_K - Medium       |  16.67 GiB |    27.32 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           tg128 |         24.79 ± 0.01 |
| qwen35 27B Q4_K - Medium       |  16.67 GiB |    27.32 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |    pp7500+tg512 |        302.20 ± 0.04 |
```

Back up to original speeds.
Good indicator that adding a third card can make sense?

## Parallell processing with llama-cpp

Was able to reach 3x parallel with 70k context each.
Larger values gets out-of-memory in VRAM.

With 3 clients, getting up to 70 tok/second generation.
Which is nice boost of 45 tok/second for the single client with `parallel=1` configuration.
However, single client now only gets around 35 tok/second.
GPU utilization only at 50-60%.

```
; Qwen3.6 27B - general tasks (instruct / no thinking)
[qwen3.6-27b-instruct]
load-on-startup = true
model = /models/Qwen3.6-27B-UD-Q4_K_XL.gguf
; --fit system handles ngl automatically, no manual n-cpu-moe needed
fit = false
ngl = 99
;fit-target = 300
;fit-ctx = 200000
ctx-size = 210000
parallel = 3
; model config
; Based on Unsloth recommendations https://unsloth.ai/docs/models/qwen3.6
temp = 1.0
top-p = 0.95
top-k = 20
min-p = 0.0
presence-penalty = 1.5
repeat-penalty = 1.0
chat-template-kwargs = {"enable_thinking": false}
; performance config
; no-mmap = true
; split-mode = tensor
spec-type = draft-mtp
spec-draft-n-max = 2
flash-attn = true
; batch-size = 2048
; ubatch-size = 2048
cache-type-k = q8_0
cache-type-v = q8_0
main-gpu = 0
```

Tried increasing batch size, hoping to improve throughput
```
batch-size = 2048
ubatch-size = 2048
```
or 
```
batch-size = 1024
ubatch-size = 1024
```
But instead had to go down to `parallel = 2` and `ctx-size = 120000`.
Thoughput did not improve either. Stuck under 50 tok/second combined. Bad tradeoff.


## Overclocking memory

People say that 5060 TI can go up to +3000 Mhz compared to stock.
Might get 15-20% extra bandwidth.

28 Gbps Stock
30 Gbps Safe, realistic, recommended
31–32 Gbps Possible but may hurt GPU clocks

Use https://github.com/martinstark/nvoc

Should test with for example cuda_memtest

Defaults

```
 nvoc info -d 0,1
driver: 595.71.05
gpu 0: NVIDIA GeForce RTX 5060 Ti
gpu clock: 2595MHz
gpu offset: 0MHz
mem clock: 13801MHz
mem offset: 0MHz
temp: 48°C
power: 25W
power limit: 180W (100%)
power range: 150W-180W (180W hard limit)
gpu 1: NVIDIA GeForce RTX 5060 Ti
gpu clock: 2580MHz
gpu offset: 0MHz
mem clock: 13801MHz
mem offset: 0MHz
temp: 41°C
power: 16W
power limit: 180W (100%)
power range: 150W-180W (206W hard limit)
```

Stock configuration
```
./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048
ggml_cuda_init: found 2 CUDA devices (Total VRAM: 31691 MiB):
| model                          |       size |     params | backend    | ngl | n_ubatch | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           pp512 |      2484.71 ± 13.77 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           tg128 |        102.80 ± 0.15 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |    pp7500+tg512 |       1158.17 ± 0.38 |
```

```
nvoc -o 100 -m 2000 -d 0,1
```

```
./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048
ggml_cuda_init: found 2 CUDA devices (Total VRAM: 31691 MiB):
| model                          |       size |     params | backend    | ngl | n_ubatch | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           pp512 |      2571.02 ± 14.35 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           tg128 |        108.13 ± 0.16 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |    pp7500+tg512 |       1214.55 ± 0.64 |

build: ff6b1062a (8864)
```

```
sudo nvoc -o 150 -m 3000 -d 0,1
```

```
root@1e046dcd4327:/app# ./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048
ggml_cuda_init: found 2 CUDA devices (Total VRAM: 31691 MiB):

| model                          |       size |     params | backend    | ngl | n_ubatch | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           pp512 |      2624.25 ± 13.68 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           tg128 |        111.16 ± 0.14 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |    pp7500+tg512 |       1245.52 ± 0.80 |
```

7.5% boost in overall performance


Same config with 27B NVFP4 - q8 context cache
```
./llama-bench -m /models/Abiray-Qwen3.6-27B-NVFP4.gguf -pg 7500,512 -t 6 -ctk q8_0 -ctv q8_0  --fit-ctx 100000 --fit-target 500 -fa 1

| model                          |       size |     params | backend    | ngl | type_k | type_v | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -----: | -----: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35 27B NVFP4               |  17.50 GiB |    26.90 B | CUDA       |  99 |   q8_0 |   q8_0 |  1 |        500 |      100000 |           pp512 |        827.40 ± 4.70 |
| qwen35 27B NVFP4               |  17.50 GiB |    26.90 B | CUDA       |  99 |   q8_0 |   q8_0 |  1 |        500 |      100000 |           tg128 |         24.51 ± 0.01 |
| qwen35 27B NVFP4               |  17.50 GiB |    26.90 B | CUDA       |  99 |   q8_0 |   q8_0 |  1 |        500 |      100000 |    pp7500+tg512 |        284.80 ± 0.12 |

```

Increasing batch size - was beneficial on 35B A3B.
Also gave good improvement in prefill with 27B.
```
./llama-bench -m /models/Abiray-Qwen3.6-27B-NVFP4.gguf -pg 7500,512 -t 6 -ctk q8_0 -ctv q8_0  --fit-ctx 100000 --fit-target 500 -fa 1 -b 2048 -ub 2048
```


```
root@ec2cde828cfd:/app# ./llama-bench -m /models/Abiray-Qwen3.6-27B-NVFP4.gguf -pg 7500,512 -t 6 -ctk q8_0 -ctv q8_0  --fit-ctx 100000 --fit-target 500 -fa 1

| model                          |       size |     params | backend    | ngl | type_k | type_v | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -----: | -----: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35 27B NVFP4               |  17.50 GiB |    26.90 B | CUDA       |  99 |   q8_0 |   q8_0 |  1 |        500 |      100000 |           pp512 |      1409.64 ± 14.70 |
| qwen35 27B NVFP4               |  17.50 GiB |    26.90 B | CUDA       |  99 |   q8_0 |   q8_0 |  1 |        500 |      100000 |           tg128 |         25.40 ± 0.02 |
| qwen35 27B NVFP4               |  17.50 GiB |    26.90 B | CUDA       |  99 |   q8_0 |   q8_0 |  1 |        500 |      100000 |    pp7500+tg512 |        324.86 ± 0.14 |

build: 0f3cb3fc8 (9294)
```
Significant increase in more recent llama-cpp for 27B MVFP4.


## OpenWebUI as router

Have OpenAI compatible completions endpoints under `/api`
https://docs.openwebui.com/reference/api-endpoints/#-chat-completions

Supports API key

https://docs.openwebui.com/features/authentication-access/api-keys/#why-api-keys

- Need to `Enable API Keys` in admin settings
- Non-admins also need group permissions
- Then (after refreshing) a user can create API key under `Profile -> Settings -> Account`

Might be possible to change the defaults here, using envvars.

https://docs.openwebui.com/reference/env-configuration/#user_permissions_features_api_keys


```
export export OPENWEBUI_TOKEN=sk-XXXXXXX

curl -H "Authorization: Bearer $OPENWEBUI_TOKEN" jon-workstation.local:3000/api/models
```

```
curl -v -X POST http://jon-workstation.local:3000/api/chat/completions \
-H "Authorization: Bearer $OPENWEBUI_TOKEN" \
-H "Content-Type: application/json" \
-d '{
      "model": "qwen36-nvfp4-mtp",
      "messages": [
        {
          "role": "user",
          "content": "Why is the sky blue?"
        }
      ]
    }'
```

Completions API is broken on 0.9.5: https://github.com/open-webui/open-webui/issues/24553

Worked in 0.9.4 with curl. However, pi still gave 400 error.
Seeing in OpenWebUI the log

```
2026-05-24 12:57:05.675 | ERROR    | open_webui.main:process_chat:2010 - Error processing chat payload: "auto" tool choice requires --enable-auto-tool-choice and --tool-call-parser to be set
```

Adding `--enable-auto-tool-choice --tool-call-parser qwen3_coder` to vLLM config made it work.

## vLLM on dual 5060ti 16GB

https://www.reddit.com/r/LocalLLaMA/comments/1sysyz2/qwen36_27b_on_dual_rtx_5060_ti_16gb_with_vllm_60/

Supposed to hit over 50 tok/sec generation
Uses the NVFP4 format. Dedicated support on Blackwell.

Uses this model.
https://huggingface.co/sakamakismile/Qwen3.6-27B-Text-NVFP4-MTP

https://insiderllm.com/guides/fp4-inference-llamacpp-nvfp4-mxfp4/
"Quality vs Q4_K_M untested".

https://docs.vllm.ai/en/stable/deployment/docker/


```
docker run --rm \
  --name open-webui \
  -p 3000:8080 \
  -v open-webui:/app/backend/data \
  --add-host=host.docker.internal:host-gateway \
  -e OPENAI_API_BASE_URL=http://host.docker.internal:8000/v1 \
  ghcr.io/open-webui/open-webui:0.9.4
```

`FIXME: avoid needing --ipc=host`

```
docker run --rm --name vllm \
  --gpus '"device=0,1"' \
  -v /home/jon/models/vllm/cache/huggingface:/root/.cache/huggingface \
  --env "HF_TOKEN=$HF_TOKEN" \
  -p 8000:8000 \
  --ipc=host \
  vllm/vllm-openai:latest \
  --model sakamakismile/Qwen3.6-27B-Text-NVFP4-MTP \
  --served-model-name qwen36-nvfp4-mtp \
  --tensor-parallel-size 2 \
  --max-model-len 104800 \
  --max-num-batched-tokens 8192 \
  --max-num-seqs 1 \
  --gpu-memory-utilization 0.90 \
  --kv-cache-dtype fp8 \
  --quantization modelopt \
  --speculative-config '{"method":"mtp","num_speculative_tokens":3}' \
  --reasoning-parser qwen3 \
  --language-model-only \
  --generation-config vllm \
  --disable-custom-all-reduce \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder \
  --attention-backend TRITON_ATTN
```

Tokens per second varies a lot with MTP.
But often above 40 and up to 55 occationally.
So considerably faster than the tests with llama-cpp on Q4.

Had one crash of the server after a while due to out-of-RAM when running with --gpu-memory-utilization 0.95


## 27B with NVFP4 on llama-cpp - UNTESTED

NVFP4 has dedicated support on Blackwell.
Theoretically 4x faster over FP8 computation.

However such quants are relatively rare, and less commonly used/tested.
https://huggingface.co/Freenixi/Abiray-Qwen3.6-27B-NVFP4-GGUF/tree/main

llama.cpp support landed mid-April 2026.
https://github.com/ggml-org/llama.cpp/pull/21896
1.46× in prefill, but same token generation speed.

Build with NVFP4 MTP was released on May 23
https://github.com/ggml-org/llama.cpp/releases/tag/b9297

Not yet available as Docker build
https://github.com/ggml-org/llama.cpp/pkgs/container/llama.cpp/versions?filters%5Bversion_type%5D=tagged

## 27B with MTP on llama-cpp - two attempts

On dual 5060 ti 16 GB. Using a basic configuration, see llama-preset.ini.

May 15.
Got 21 tok/s out without MTP, and 35 tok/second with on programming tasks via llama-cpp webui.
Prefill around 900 tok/s, which is nice and fast. Above target!

May 29.
Updated to build `b9404`.
With Qwen3.6-27B-UD-Q4_K_XL.gguf, MTP and layer split mode, get 48-50 on Python codegen via llama-cpp webui.

Roughly matches vLLM performance level.

## With two GPUs

Using `--gpu all` only seems to pass one GPU.


```
docker run --rm --gpus '"device=0,1"' -e CUDA_VISIBLE_DEVICES=0,1 -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda13
```

Can see both GPUs with nvidia-smi.

```
root@42ef09538303:/app# ./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048
ggml_cuda_init: found 2 CUDA devices (Total VRAM: 31692 MiB):
  Device 0: NVIDIA GeForce RTX 5060 Ti, compute capability 12.0, VMM: yes, VRAM: 15841 MiB
  Device 1: NVIDIA GeForce RTX 5060 Ti, compute capability 12.0, VMM: yes, VRAM: 15850 MiB
| model                          |       size |     params | backend    | ngl | n_ubatch | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           pp512 |      2456.17 ± 14.10 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           tg128 |         97.66 ± 0.11 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |    pp7500+tg512 |       1115.39 ± 0.84 |
```
Close to 2x in performance.


## With 32GB RAM set to 3200 Mhz

Overclocking main memory. These RAM sticks are rated only to 2666 Mhz.

First run, during `memtester`

```
root@21d66c9bbd61:/app# ./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048
| model                          |       size |     params | backend    | ngl | n_ubatch | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           pp512 |       845.49 ± 63.85 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           tg128 |         53.90 ± 0.66 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |    pp7500+tg512 |        492.36 ± 3.29 |
```

Second run, nothing else running

```
root@21d66c9bbd61:/app# ./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048
| model                          |       size |     params | backend    | ngl | n_ubatch | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           pp512 |      1080.55 ± 17.79 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           tg128 |         70.05 ± 0.11 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |    pp7500+tg512 |        643.91 ± 1.56 |

build: ff6b1062a (8864)

```

## llama-cpp on X570

AMD Ryzen 5 5600X. With single 5060 TI 16GB in x16 slot

```
[jon@jon-workstation ~]$ nvidia-smi --query-gpu=pcie.link.gen.current,pcie.link.gen.max,pcie.link.width.current,pcie.link.width.max --format=csv
pcie.link.gen.current, pcie.link.gen.max, pcie.link.width.current, pcie.link.width.max
1, 4, 8, 16
```
Shows gen 1 x8?!!
5060 TI has a x8 connector, motherboard is capable of gen 4.0.
Does not make sense??

However when re-running under load I get

```
nvidia-smi --query-gpu=pcie.link.gen.current,pcie.link.gen.max,pcie.link.width.current,pcie.link.width.max --format=csv
pcie.link.gen.current, pcie.link.gen.max, pcie.link.width.current, pcie.link.width.max
4, 4, 8, 16
```

TODO: force gen 4.0 in BIOS?


```
docker run --gpus all -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda13
```

```
./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048
```

```
| model                          |       size |     params | backend    | ngl | n_ubatch | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -------: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           pp512 |       650.14 ± 71.18 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |           tg128 |        49.38 ± 11.20 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |     2048 |  1 |        300 |      100000 |    pp7500+tg512 |       559.20 ± 12.81 |
```

Performance seems basically same as before. 550 on pp7500+tg512.


## llama-cpp router mode

To have multiple models available, and automating loading/unloading of them

```
docker run --gpus all -v /home/jon/models/:/models -p 8080:8080 ghcr.io/ggml-org/llama.cpp:server-cuda13 --port 8080 --host 0.0.0.0 --api-key $LLAMA_API_KEY --models-preset /models/llama-preset.ini --models-max 1
```

Can then select for example in the webui.
Switchover for Qwen 3.6 35B A3B is around 5 seconds.

Without --models-max 1 it would go out of memory.
WebUI can sometimes request old model after selecting a new one (if not yet loaded),
which easily caused this situation.

## Running llama-cpp with qwen3.6-35b-a3b

Unsloth has guide wrt parameters https://unsloth.ai/docs/models/qwen3.6

Instruct mode (non-thinking)
```
docker run --gpus all -v /home/jon/models/:/models -p 8080:8080 ghcr.io/ggml-org/llama.cpp:server-cuda -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf --port 8080 --host 0.0.0.0 --ctx-size 128000 --top-p 0.95 --top-k 20 --min-p 0.0 --temperature 1.0 --presence_penalty 1.5 --chat-template-kwargs '{"enable_thinking": false}' --api-key $LLAMA_API_KEY
```

## Benchmarking llama-cpp with qwen3.6-35b-a3b

On RTX5060 TI 16 GB.

docker run --gpus all -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda

root@e61717ad5b46:/app# ./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -n 512,1024,2048 --fit-target 1000 --fit-ctx 100000 -fa 1

| model                          |       size |     params | backend    | ngl | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |  1 |       1000 |      100000 |           pp512 |       676.42 ± 15.58 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |  1 |       1000 |      100000 |           tg512 |         57.81 ± 0.15 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |  1 |       1000 |      100000 |          tg1024 |         56.13 ± 0.06 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |  1 |       1000 |      100000 |          tg2048 |         57.51 ± 0.03 |

root@e61717ad5b46:/app# ./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -n 512,1024,2048 -p 2000,16000,64000 --fit-target 1000 --fit-ctx 100000 -fa 1

| model                          |       size |     params | backend    | ngl | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |  1 |       1000 |      100000 |          pp2000 |       641.45 ± 20.82 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |  1 |       1000 |      100000 |         pp16000 |       612.33 ± 10.21 |


TODO, try adjusting batching

  -b 512 -ub 256 \

TODO, try adjusting KV cache

  -ctk q8_0 \
  -ctv q8_0 \


https://njannasch.dev/blog/qwen-3-6-turboquant-local-inference/
5060ti connected over Occulink

Hit prefill 1,585 t/s and gen 89 t/s @ 7.5k, and 1,261 t/s and 46 t/s gen @ 108k.

  -ngl 99 -fa 1 -c 262144 \
  --cache-type-k q4_0 --cache-type-v q4_0 \
  --swa-full --ctx-checkpoints 64 --kv-unified \
  --context-shift --cache-reuse 512 \
  --perf --no-warmup --mlock \
  --slot-prompt-similarity 0.0 \
  -np 1 -b 512 -ub 256 -t 6 -tb 6 \
  --threads-http 8 --no-mmap --jinja \
  --port 11433 --host 0.0.0.0


## Tests with default CUDA 12

docker run --gpus all -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda

root@e61717ad5b46:/app# ./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -b 512 -ub 256 -t 6 --fit-ctx 100000 --fit-target 1000

| model                          |       size |     params | backend    | ngl | threads | n_batch | n_ubatch |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | ------: | ------: | -------: | ---------: | ----------: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |     512 |      256 |       1000 |      100000 |           pp512 |        444.12 ± 9.96 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |     512 |      256 |       1000 |      100000 |           tg128 |         56.20 ± 0.06 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |     512 |      256 |       1000 |      100000 |    pp7500+tg512 |        281.98 ± 4.06 |


root@e61717ad5b46:/app# ./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -ngl 30 -t 6 --fit-ctx 100000 --fit-target 1000

| model                          |       size |     params | backend    | ngl | threads |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | ------: | ---------: | ----------: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  30 |       6 |       1000 |      100000 |           pp512 |       672.23 ± 17.38 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  30 |       6 |       1000 |      100000 |           tg128 |         56.61 ± 0.06 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  30 |       6 |       1000 |      100000 |    pp7500+tg512 |        365.37 ± 3.06 |


root@e61717ad5b46:/app# ./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512  -b 512 -ub 256 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1

| model                          |       size |     params | backend    | ngl | threads | n_batch | n_ubatch | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | ------: | ------: | -------: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |     512 |      256 |  1 |        300 |      100000 |           pp512 |       483.99 ± 11.34 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |     512 |      256 |  1 |        300 |      100000 |           tg128 |         60.39 ± 0.07 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |     512 |      256 |  1 |        300 |      100000 |    pp7500+tg512 |        310.76 ± 5.02 |

root@e61717ad5b46:/app# ./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1

| model                          |       size |     params | backend    | ngl | threads | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | ------: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |  1 |        300 |      100000 |           pp512 |       748.82 ± 17.70 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |  1 |        300 |      100000 |           tg128 |         58.96 ± 0.09 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |  1 |        300 |      100000 |    pp7500+tg512 |        398.43 ± 3.94 |


## Tests with CUDA 13

docker run --gpus all -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda13

root@aafbe7f09c81:/app# ./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1

| model                          |       size |     params | backend    | ngl | threads | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | ------: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |  1 |        300 |      100000 |           pp512 |       748.60 ± 16.76 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |  1 |        300 |      100000 |           tg128 |         59.85 ± 0.08 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |  1 |        300 |      100000 |    pp7500+tg512 |        398.78 ± 3.98 |


./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 --cache-type-k q8_0 --cache-type-v q8_0
ggml_cuda_init: found 1 CUDA devices (Total VRAM: 15841 MiB):

| model                          |       size |     params | backend    | ngl | threads | type_k | type_v | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | ------: | -----: | -----: | -: | ---------: | ----------: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |   q8_0 |   q8_0 |  1 |        300 |      100000 |           pp512 |       745.83 ± 16.84 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |   q8_0 |   q8_0 |  1 |        300 |      100000 |           tg128 |         59.78 ± 0.12 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |   q8_0 |   q8_0 |  1 |        300 |      100000 |    pp7500+tg512 |        401.07 ± 4.02 |

No change.

TODO: try rebuilding for sm120 - the docker image is for sm121a ?

docker build \
  --build-arg CUDA_DOCKER_ARCH=native \
  --target full \
  -f .devops/cuda.Dockerfile \
  -t llama.cpp:full-cuda-native \
  .

docker run --gpus all -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it llama.cpp:full-cuda-native


root@c59b5397a73c:/app# ./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1

| model                          |       size |     params | backend    | ngl | threads | fa |       fitt |        fitc |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | ------: | -: | ---------: | ----------: | --------------: | -------------------: |
A       |  99 |       6 |  1 |        300 |      100000 |           pp512 |        520.73 ± 8.70 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |  1 |        300 |      100000 |           tg128 |         59.26 ± 0.08 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |  1 |        300 |      100000 |    pp7500+tg512 |        317.81 ± 2.66 |


Also gives details like
```
common_params_fit_impl: trying to fit one extra layer with overflow_type=LAYER_FRACTION_GATE
common_memory_breakdown_print: | memory breakdown [MiB]  | total    free     self   model   context   compute       unaccounted |
common_memory_breakdown_print: |   - CUDA0 (RTX 5060 Ti) | 15841 = 15630 + (15302 = 14736 +      72 +     493) + 17592186029324 |
common_memory_breakdown_print: |   - Host                |                   6371 =  6362 +       0 +       9                   |
common_params_fit_impl: memory for test allocation by device:
common_params_fit_impl: id=0, n_layer=41, n_part=14, overflow_type=3, mem= 15302 MiB
common_params_fit_impl: set ngl_per_device[0].(n_layer, n_part, overflow_type)=(41, 14, GATE), id_dense_start=0
common_params_fit_impl:   - CUDA0 (NVIDIA GeForce RTX 5060 Ti): 41 layers (14 overflowing),  15302 MiB used,    328 MiB free
common_fit_params: successfully fit params to free device memory
common_fit_params: fitting params to free memory took 4.12 seconds
```


TODO: try with FXP4 inference


now i have 960 tok/sec prefill speed and 40t/s generation speed. At ctx size 160K
https://www.reddit.com/r/LocalLLaMA/comments/1rg8gkx/qwen35_35b_a3b_45_ts_128k_ctx_on_single_16gb_5060/


## On gpu1


docker build   --build-arg CUDA_VERSION=13.0.0   --build-arg CUDA_DOCKER_ARCH=120   --target full   -f .devops/cuda.Dockerfile   -t llama.cpp:full-cuda-sm120   .
docker run --gpus all -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it llama.cpp:full-cuda-sm120


./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1

740,60
| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |  1 |        300 |      100000 |    pp7500+tg512 |        410.91 ± 4.01 |


./llama-bench -m /models/Qwen3.6-35B-A3B-MXFP4_MOE.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1
| qwen35moe 35B.A3B MXFP4 MoE    |  20.21 GiB |    34.66 B | CUDA       |  99 |       6 |  1 |        300 |      100000 |    pp7500+tg512 |        437.47 ± 6.55 |


root@2362e6a43d68:/app# ./llama-bench -m /models/Qwen3.6-35B-A3B-MXFP4_MOE.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 --cache-type-k q8_0 --cache-type-v q8_0

| qwen35moe 35B.A3B MXFP4 MoE    |  20.21 GiB |    34.66 B | CUDA       |  99 |       6 |   q8_0 |   q8_0 |  1 |        300 |      100000 |    pp7500+tg512 |        433.44 ± 5.98 |


### Standard image with CUDA 12
jon@soundsensing-gpu-1:~/llama.cpp$ docker run --gpus all -v /home/jon/models/:/models -p 8080:8080 --entrypoint /bin/bash -it ghcr.io/ggml-org/llama.cpp:full-cuda

./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1

| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |  1 |        300 |      100000 |    pp7500+tg512 |        409.92 ± 4.10 |



| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |         15 |       6 |  1 |        300 |      100000 |    pp7500+tg512 |        409.63 ± 4.09 |


root@c716f58dfc8e:/app# ./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048

| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |     2048 |  1 |        300 |      100000 |    pp7500+tg512 |        535.99 ± 2.22 |


root@c716f58dfc8e:/app# ./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -t 6 --fit-ctx 100000 --fit-target 300 -fa 1 -b 2048 -ub 2048

| qwen35moe 35B.A3B MXFP4 MoE    |  20.21 GiB |    34.66 B | CUDA       |  99 |       6 |     2048 |  1 |        300 |      100000 |    pp7500+tg512 |        544.18 ± 3.02 |


root@ff3818717a99:/app# ./llama-bench -m /models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -pg 7500,512 -t 6 --fit-ctx 128000 --fit-target 300 -fa 1 -b 2048 -ub 2048

| qwen35moe 35B.A3B Q4_K - Medium |  20.60 GiB |    34.66 B | CUDA       |  99 |       6 |     2048 |  1 |        300 |      128000 |    pp7500+tg512 |        535.59 ± 2.13 |


## Preliminary conclusions

- ! Batch size can make 20% difference
- No diff in CUDA image / custom build. Checked on UD-Q4_K_M
- MXFP4 might be 5% faster on Q4



## Using llama-cpp with qwen3.5-35b-a3b

Recommended parameters
https://unsloth.ai/docs/models/qwen3.5#qwen3.5-35b-a3b

```
temperature=1.0, top_p=0.95, top_k=20, min_p=0.0, presence_penalty=1.5, repetition_penalty=1.0
```

```
docker run --gpus all -v /home/jon/models/:/models -p 8080:8080 ghcr.io/ggml-org/llama.cpp:server-cuda -m /models/Qwen3.5-35B-A3B-UD-Q4_K_L.gguf --port 8080 --host 0.0.0.0 --ctx-size 65536 --top-p 0.95 --top-k 20 --min-p 0.0 --chat-template-kwargs '{"enable_thinking": false}' --api-key $LLAMA_API_KEY
```

Model loading takes around 1 minute.

All layers were offloaded to GPU.
```
load_tensors: offloaded 41/41 layers to GPU
```

Uses most of the GPU memory
```
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A          187893      C   /app/llama-server                     14542MiB |
+-----------------------------------------------------------------------------------------+
```


```
llama_kv_cache:      CUDA0 KV buffer size =  1280.00 MiB
llama_kv_cache: size = 1280.00 MiB ( 65536 cells,  10 layers,  4/1 seqs), K (f16):  640.00 MiB, V (f16):  640.00 MiB
```

Going to --ctx-size 100000 also seemed to work?


### OpenCode setup
Added the llama-cpp server as a provider and model in OpenCode following this guide.
https://www.youtube.com/watch?v=8GDL5nsy2Sw

opencode.json
```
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "llama-server jon-workstation",
      "options": {
        "baseURL": "http://jon-workstation.local:8080/v1"
      },
      "models": {
        "Qwen3.5-35B-A3B-UD-Q4_K_L.gguf": {
           "name": "Qwen3.5-35B-A3B",
           "limit":  {
              "context": 65536,
              "output": 32768
            }
         }
      }
    }
  }
}
```

### User experience

Tokens seem to be produced at an OK rate. However there are occational stutters.

When using 65k context, the compaction happens pretty often - seemingly when we get to around 50% of context. 
This takes over 1 minute. There is little to no user feedback in OpenCode, annoying.

```
TODO: re-test with 100-120k context length
```

The Qwen 3.5 model also seems to confuse CPython and MicroPython a bit,
and this gives some false starts sometimes, needs to try things multiple times.
This also happens a fair bit with Claude Sonnet 4.x... And even plain Google search does this.

```
QUESTION. Can skill files or similar guidance be used to get around this?
```

Both Qwen and GPT-OSS-120b likes to use the `uos` etc modules for MicroPython.
Does not understand that these are deprecated a few years ago.
This is a common type of problem with 

```
QUESTION: How to get models to understand that should use the standard, non-prefixed versions of libraries?

Maybe just give a full list of libraries that it can use / that are available - somewhere
```

