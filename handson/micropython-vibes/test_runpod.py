
"""
Script for testing/verifying RunPod serving

Independent from OpenCode to be able to debug problems
"""

import os
from openai import OpenAI

# XXX: ensure ENDPOINT_ID is correct
endpoints = {
    'runpod/gpt-oss-120b': ('openai/gpt-oss-120b', "https://api.runpod.ai/v2/gpt-oss-120b/openai/v1"),
    'runpod/qwen3-32b': ('Qwen/Qwen3-32B-AWQ', "https://api.runpod.ai/v2/qwen3-32b-awq/openai/v1"),
    'runpod-custom/gpt-oss-20b': ('openai/gpt-oss-20b', "https://api.runpod.ai/v2/rssll5qi6dwhhj/openai/v1"),
    'runpod-custom/gpt-oss-120b': ('openai/gpt-oss-120b', "https://api.runpod.ai/v2/1y374m166648l2/openai/v1"),  
}

model = 'runpod/qwen3-32b'
model = 'runpod-custom/gpt-oss-120b'

model_name, endpoint_url = endpoints[model]

client = OpenAI(
    api_key=os.environ["RUNPOD_API_KEY"],
    base_url=endpoint_url,
)


response = client.chat.completions.create(
    model=model_name, # have to use correct name
    messages=[{"role": "user", "content": "say hi"}],
    max_tokens=10
)

print(response)


models = client.models.list()
print(f"✅ Connected! Models: {[m.id for m in models.data]}")
