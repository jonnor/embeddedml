
# Running a local LLM for agentic coding

Testing if this can work on a RTX 5060 TI 16GB for MicroPython development.

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

