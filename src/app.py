from functools import partial

import streamlit as st
import tiktoken

OPENAI_PROMPT_INPUT = """
The following is a list of companies and the categories they fall into:

Apple, Facebook, Fedex

Apple
Category:
""".strip()

OPENAI_PROMPT_OUTPUT = """
Technology

Facebook
Category: Social Media

Fedex
Category: Delivery
""".strip()


def get_price(
        num_requests: int,
        num_tokens_input: int,
        num_tokens_output: int,
        price_input: float,
        price_output: float
):
    return ((num_tokens_input * price_input / 1000) + (num_tokens_output * price_output / 1000)) * num_requests


if __name__ == '__main__':
    st.title("OpenAI-Calc")

    # Inputs
    st.header("Inputs")

    # OpenAI prompt input
    openai_prompt = st.text_area(
        label='Prompt:',
        value=OPENAI_PROMPT_INPUT,
        height=200
    )

    # OpenAI response
    openai_response = st.text_area(
        label='Response:',
        value=OPENAI_PROMPT_OUTPUT,
        height=200
    )

    # Number of requests
    num_requests = st.number_input(
        label="Number of requests:",
        min_value=1,
        value=10_000
    )

    # Results
    st.header("Results")

    # Count tokens
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens_input = len(encoding.encode(OPENAI_PROMPT_INPUT))
    num_tokens_output = len(encoding.encode(OPENAI_PROMPT_OUTPUT))
    st.text(f"Number of tokens in input: {num_tokens_input}")
    st.text(f"Number of tokens in input: {num_tokens_output}\n")

    # Prices
    get_price_partial = partial(
        get_price,
        num_requests=num_requests,
        num_tokens_input=num_tokens_input,
        num_tokens_output=num_tokens_output
    )

    ada_price = get_price_partial(price_input=.0004, price_output=.0004)
    st.text(f"Ada: ${ada_price:.2f}")

    babbage_price = get_price_partial(price_input=.0005, price_output=.0005)
    st.text(f"Babbage: ${babbage_price:.2f}")

    curie_price = get_price_partial(price_input=.0020, price_output=.0020)
    st.text(f"Curie: ${curie_price:.2f}")

    davinci_price = get_price_partial(price_input=.02, price_output=.02)
    st.text(f"Davinci: ${davinci_price:.2f}")

    gpt3_4k_price = get_price_partial(price_input=.0015, price_output=.002)
    st.text(f"GPT3 (4K context): ${gpt3_4k_price:.2f}")

    gpt3_16k_price = get_price_partial(price_input=.003, price_output=.003)
    st.text(f"GPT3 (16K context): ${gpt3_16k_price:.2f}")

    gpt4_8k_price = get_price_partial(price_input=.03, price_output=.06)
    st.text(f"GPT4 (8K context): ${gpt4_8k_price:.2f}")

    gpt4_32k_price = get_price_partial(price_input=.06, price_output=.12)
    st.text(f"GPT4 (32K context): ${gpt4_32k_price:.2f}")
