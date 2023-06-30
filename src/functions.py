def get_price(
        num_requests: int,
        num_tokens_input: int,
        num_tokens_output: int,
        price_input: float,
        price_output: float
):
    return ((num_tokens_input * price_input / 1000) + (num_tokens_output * price_output / 1000)) * num_requests
