import os
import time
import asyncio
from itertools import cycle
from openai import AsyncOpenAI, RateLimitError, APIConnectionError, APIStatusError

# ============================================================
# 1. CONFIGURE PROVIDERS
# ============================================================

PROVIDERS = [
    {
        "name": "groq1",
        "api_key": os.environ["GROQ_API_KEY_1"],
        "base_url": "https://api.groq.com/openai/v1",
        "model": "openai/gpt-oss-120b",
        "weight": 1,
        "disabled_until": 0,
        "failures": 0,
    },
    {
        "name": "groq2",
        "api_key": os.environ["GROQ_API_KEY_2"],
        "base_url": "https://api.groq.com/openai/v1",
        "model": "openai/gpt-oss-120b",
        "weight": 1,
        "disabled_until": 0,
        "failures": 0,
    },
    {
        "name": "groq3",
        "api_key": os.environ["GROQ_API_KEY_3"],
        "base_url": "https://api.groq.com/openai/v1",
        "model": "openai/gpt-oss-120b",
        "weight": 1,
        "disabled_until": 0,
        "failures": 0,
    }
]

# ============================================================
# 2. CREATE CLIENTS
# ============================================================

for p in PROVIDERS:
    p["client"] = AsyncOpenAI(
        api_key=p["api_key"],
        base_url=p["base_url"]
    )

# ============================================================
# 3. WEIGHTED ROUND-ROBIN POOL
# ============================================================

weighted_pool = []

for p in PROVIDERS:
    weighted_pool.extend([p] * p["weight"])

router = cycle(weighted_pool)

# ============================================================
# 4. HELPERS
# ============================================================

def provider_available(provider):
    return time.time() >= provider["disabled_until"]


def cooldown(provider, seconds=None):
    provider["failures"] += 1

    if seconds is None:
        # 1st failure: 60 sec
        # 2nd failure: 120 sec
        # 3rd failure: 240 sec...
        seconds = min(
            60 * (2 ** (provider["failures"] - 1)),
            3600
        )

    provider["disabled_until"] = time.time() + seconds

    print(
        f"{provider['name']} disabled for {seconds}s"
    )


def get_next_provider(exclude=None):
    exclude = exclude or set()

    for _ in range(len(weighted_pool)):

        provider = next(router)

        if provider["name"] in exclude:
            continue

        if provider_available(provider):
            return provider

    return None

# ============================================================
# 5. MAIN LLM FUNCTION
# ============================================================

async def llm(
    prompt=None,
    messages=None,
    temperature=0.7,
    max_tokens=None,
    show_provider=True
):

    if messages is None:
        if prompt is None:
            raise ValueError("Provide either prompt= or messages=")

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

    attempted = set()
    errors = []

    while len(attempted) < len(PROVIDERS):

        provider = get_next_provider(
            exclude=attempted
        )

        if provider is None:
            break

        attempted.add(provider["name"])

        try:

            if show_provider:
                print(
                    f"🚀 Trying {provider['name']} "
                    f"→ {provider['model']}"
                )

            kwargs = {
                "model": provider["model"],
                "messages": messages,
                "temperature": temperature
            }

            if max_tokens is not None:
                kwargs["max_tokens"] = max_tokens

            response = await provider[
                "client"
            ].chat.completions.create(**kwargs)

            # successful request
            provider["failures"] = 0

            if show_provider:
                print(
                    f"✅ Response from {provider['name']}"
                )

            return response.choices[0].message.content

        # -----------------------------------------
        # Rate limit / quota exhausted
        # -----------------------------------------

        except RateLimitError as e:

            cooldown(provider)

            errors.append(
                (
                    provider["name"],
                    "rate_limit"
                )
            )

            continue

        # -----------------------------------------
        # Connection problem
        # -----------------------------------------

        except APIConnectionError as e:

            cooldown(provider, 30)

            errors.append(
                (
                    provider["name"],
                    "connection_error"
                )
            )

            continue

        # -----------------------------------------
        # HTTP / API error
        # -----------------------------------------

        except APIStatusError as e:

            if e.status_code == 429:
                cooldown(provider)
                continue

            if e.status_code >= 500:
                cooldown(provider, 30)
                continue

            # 400 errors usually mean prompt/model
            # incompatibility, but allow fallback
            print(
                f"❌ {provider['name']} returned "
                f"{e.status_code}"
            )

            errors.append(
                (
                    provider["name"],
                    str(e)
                )
            )

            continue

        # -----------------------------------------
        # Other errors
        # -----------------------------------------

        except Exception as e:

            print(
                f"❌ {provider['name']} failed: {e}"
            )

            errors.append(
                (
                    provider["name"],
                    str(e)
                )
            )

            continue

    raise RuntimeError(
        f"All providers failed/exhausted.\n{errors}"
    )

# ============================================================
# 6. PROVIDER STATUS
# ============================================================

def provider_status():

    print("\nLLM Provider Status")
    print("-" * 60)

    for p in PROVIDERS:

        remaining = max(
            0,
            int(
                p["disabled_until"] -
                time.time()
            )
        )

        status = (
            "✅ available"
            if remaining == 0
            else f"❌ cooldown ({remaining}s)"
        )

        print(
            f"{p['name']:15} "
            f"{status:25} "
            f"weight={p['weight']}"
        )

# ============================================================
# 7. EXAMPLE
# ============================================================

# In Jupyter:
#
# response = await llm("Explain transformers in simple terms")
# print(response)
#
# Run again:
# response = await llm("Write a Python merge sort")
#
# Each request moves through the weighted round-robin pool.
#
# Check providers:
# provider_status()

print("LLM Load Balancer ready.")
print('Use: response = await llm("Your question")')


