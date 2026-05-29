
# Running a local LLM for agentic coding

Testing if this can work on a RTX 5060 TI 16GB for MicroPython development.

## Dual RTX 5060 TI 16G

Motivating goal. Get 27B running at 50+ tps and prefill of 500+ tps.

NOTE: this might require MTP to get even close.
Testing MTP will probably be done separately, when getting into llama-cpp mainline.

TODO

- Test llama.cpp with NVFP4
- Try power limiting to 150w per card

## Verifying practical performance

Would want to run some evals

https://github.com/kyuz0/pi-bench
based on SWE mini
Has reference results for Qwen 3.6 27B

## Testing triple/quad 5060 ti on x570 - TODO

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

