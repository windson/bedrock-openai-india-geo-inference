#!/usr/bin/env python3
"""Invoke GPT-5.6 Terra through Amazon Bedrock Runtime India Geo."""

import argparse
import sys

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

AWS_REGION = "ap-south-1"
ENDPOINT_URL = "https://bedrock-runtime.ap-south-1.amazonaws.com"
MODEL_ID = "in.openai.gpt-5.6-terra"


def invoke(prompt: str, max_tokens: int) -> dict:
    """Invoke Terra through its India Geo inference profile."""
    client = boto3.client(
        "bedrock-runtime",
        region_name=AWS_REGION,
        endpoint_url=ENDPOINT_URL,
        config=Config(
            retries={"total_max_attempts": 5, "mode": "adaptive"},
            connect_timeout=5,
            read_timeout=120,
        ),
    )
    return client.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": max_tokens},
    )


def response_text(response: dict) -> str:
    """Join text blocks from a Converse response."""
    content = response["output"]["message"]["content"]
    return "".join(block["text"] for block in content if "text" in block)


def minimum_sixteen(value: str) -> int:
    parsed = int(value)
    if parsed < 16:
        raise argparse.ArgumentTypeError("must be at least 16")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Invoke Terra with inference processed only in India."
    )
    parser.add_argument("prompt")
    parser.add_argument("--max-tokens", type=minimum_sixteen, default=256)
    args = parser.parse_args()

    try:
        response = invoke(args.prompt, args.max_tokens)
        print(response_text(response))
        usage = response.get("usage", {})
        print(
            f"\nmodel={MODEL_ID} region={AWS_REGION} "
            f"input_tokens={usage.get('inputTokens', 'n/a')} "
            f"output_tokens={usage.get('outputTokens', 'n/a')}",
            file=sys.stderr,
        )
        return 0
    except (BotoCoreError, ClientError, KeyError) as error:
        print(f"Inference failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
