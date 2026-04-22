
# Running a local LLM for agentic coding

Testing if this can work on a RTX 5060 TI 16GB for MicroPython development.

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

