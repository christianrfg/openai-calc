from functools import partial

import streamlit as st
import tiktoken
from streamlit_extras.buy_me_a_coffee import button
from streamlit_extras.metric_cards import style_metric_cards

from functions import get_price

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

if __name__ == '__main__':
    # Page configurations
    st.set_page_config(
        page_title="OpenAI-Calc",
        page_icon="🧮",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Page title
    st.title("🧮 OpenAI-Calc")

    # Page badges
    st.markdown(
        """
        [![](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/christian-r-f-g)
        [![](https://img.shields.io/github/stars/christianrfg/openai-calc?style=social)](https://github.com/christianrfg/openai-calc)
        """
    )

    # Create buy me a coffee button
    button(username="fake-username")

    # Set style for metric cards
    style_metric_cards(border_left_color="#185ccd")

    # Project introduction
    st.markdown(
        """
        OpenAI-Calc is a powerful tool designed to assist you in estimating values for individual tasks executed within
        the OpenAI environment. With this tool, all you need to do is input your desired configurations or parameters, 
        and witness the magic unfold before your eyes.
        """.strip()
    )

    # OpenAI Input & Output
    st.subheader("⚙️ Specify Your Configurations")

    col1, col2 = st.columns(2)
    with col1:
        prompt_input = st.text_area(
            label='Insert your prompt input:',
            value=OPENAI_PROMPT_INPUT,
            height=200
        )
    with col2:
        prompt_output = st.text_area(
            label='Insert the expected prompt output:',
            value=OPENAI_PROMPT_OUTPUT,
            height=200,
            help="You can set this manually or generate with the input in OpenAI."
        )

    num_requests = st.number_input(
        label="Insert the number of requests:",
        min_value=1,
        value=100_000
    )

    # st.markdown('##')
    # st.subheader("Choose Configurations")
    # col1, col2 = st.columns(2)
    # with col1:
    #     num_requests = st.number_input(
    #         label="Insert the number of requests:",
    #         min_value=1,
    #         value=100_000
    #     )
    # with col2:
    #     options = st.multiselect(
    #         "Select OpenAI models:",
    #         options=[
    #             "Ada", "Babbage", "Curie", "Davinci", "GPT-3.5-Turbo (4K context)",
    #             "GPT-3.5-Turbo (8k context)", "GPT-4 (8K context)", "GPT-4 (32K context)"
    #         ],
    #         default=["Davinci", "GPT-3.5-Turbo (4K context)", "GPT-4 (8K context)"]
    #     )

    # Results
    st.subheader("⭐ Estimated Values")

    # Get number of tokens in input, output and the total of tokens
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens_input = len(encoding.encode(prompt_input))
    num_tokens_output = len(encoding.encode(prompt_output))
    num_tokens_total = (num_tokens_input + num_tokens_output) * num_requests

    # Display number of tokens
    st.markdown("Number of tokens:")
    col1, col2, col3, _ = st.columns(4)
    col1.metric(label="Input", value=num_tokens_input)
    col2.metric(label="Output", value=num_tokens_output)
    col3.metric(label="Total", value=num_tokens_total,
                help="(Nº of Tokens in Input + Nº of Tokens in Output) * Number of Requests.")

    # Get function to calculate price for each model
    get_price_partial = partial(
        get_price,
        num_requests=num_requests,
        num_tokens_input=num_tokens_input,
        num_tokens_output=num_tokens_output
    )

    # Get model's prices
    ada_price = get_price_partial(price_input=.0004, price_output=.0004)
    babbage_price = get_price_partial(price_input=.0005, price_output=.0005)
    curie_price = get_price_partial(price_input=.0020, price_output=.0020)
    davinci_price = get_price_partial(price_input=.02, price_output=.02)
    gpt3_4k_price = get_price_partial(price_input=.0015, price_output=.002)
    gpt3_16k_price = get_price_partial(price_input=.003, price_output=.003)
    gpt4_8k_price = get_price_partial(price_input=.03, price_output=.06)
    gpt4_32k_price = get_price_partial(price_input=.06, price_output=.12)

    # Display model's prices
    st.markdown('##')
    st.markdown("Price for each OpenAI model:")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Ada", value=f"${ada_price:.2f}")
    col1.metric(label="Babbage", value=f"${babbage_price:.2f}")
    col2.metric(label="Curie", value=f"${curie_price:.2f}")
    col2.metric(label="Davinci", value=f"${davinci_price:.2f}")
    col3.metric(label="GPT-3.5-Turbo (4K context)", value=f"${gpt3_4k_price:.2f}")
    col3.metric(label="GPT-3.5-Turbo (16k context)", value=f"${gpt3_16k_price:.2f}")
    col4.metric(label="GPT-4 (8K context)", value=f"${gpt4_8k_price:.2f}")
    col4.metric(label="GPT-4 (32K context)", value=f"${gpt4_32k_price:.2f}")