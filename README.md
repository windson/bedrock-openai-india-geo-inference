# Amazon Bedrock OpenAI inference in India

This project provides two standalone GPT-5.6 inference samples that process inference only within India using Amazon Bedrock Runtime and India Geo inference profiles.

## India-only invocation matrix

| Endpoint invocation type | Model | Standalone sample | India Geo model ID | Processing locations |
| --- | --- | --- | --- | --- |
| `bedrock-runtime` | GPT-5.6 Terra | [`bedrock_runtime_terra.py`](bedrock_runtime_terra.py) | `in.openai.gpt-5.6-terra` | Mumbai (`ap-south-1`) or Hyderabad (`ap-south-2`) |
| `bedrock-runtime` | GPT-5.6 Luna | [`bedrock_runtime_luna.py`](bedrock_runtime_luna.py) | `in.openai.gpt-5.6-luna` | Mumbai (`ap-south-1`) or Hyderabad (`ap-south-2`) |

Both samples call `bedrock-runtime.ap-south-1.amazonaws.com` and fix the model to its `in.` India Geo inference profile. AWS can route processing between Mumbai and Hyderabad, but processing remains within India.

## Why there are no Mantle samples

The general `bedrock-mantle` endpoint is available in Mumbai, but GPT-5.6 Terra and Luna were not present in its live Mumbai model catalog when validated. Mantle is not available in Hyderabad and does not accept India Geo inference IDs. A successful Mantle sample for these models therefore cannot currently satisfy an India-only requirement, so this project intentionally excludes it.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The samples use the normal boto3/AWS credential chain, such as `aws configure`, AWS IAM Identity Center, or an IAM role. No Bedrock API key is required.

## Run

### Terra

```bash
python bedrock_runtime_terra.py "Summarize Amazon Bedrock in one sentence."
```

### Luna

```bash
python bedrock_runtime_luna.py "Reply with a short greeting."
```

The caller requires `bedrock:InvokeModel` for the India Geo inference profile, its destination foundation models, and the account's Bedrock default project.

## Validation

Validated on September 3, 2026:

- `bedrock_runtime_terra.py` returned `Runtime Terra OK`.
- `bedrock_runtime_luna.py` returned `Runtime Luna OK`.
- Both India Geo profiles were active from Mumbai and Hyderabad.
- Each profile listed only Mumbai and Hyderabad destination model ARNs.
- Static checks confirm both scripts are fixed to the Mumbai Runtime endpoint and an `in.` India Geo model ID.

## Official AWS references

- [Amazon Bedrock OpenAI models in India](https://aws.amazon.com/about-aws/whats-new/2026/08/amazon-bedrock-openai-india-v1/)
- [GPT-5.6 Terra model card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-56-terra.html)
- [GPT-5.6 Luna model card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-56-luna.html)
- [Regional availability by endpoints](https://docs.aws.amazon.com/bedrock/latest/userguide/endpoints-region-availability.html)
- [Bedrock cross-Region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html)
