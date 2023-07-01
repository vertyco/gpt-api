def compile_messages(
    messages: list, default_prompt_header=True, default_prompt_footer=True
) -> str:
    # Yoinked from https://github.com/nomic-ai/gpt4all/blob/main/gpt4all-bindings/python/gpt4all/gpt4all.py#L260
    """
    Helper method for building a prompt using template from list of messages.

    Args:
        messages:  List of dictionaries. Each dictionary should have a "role" key
            with value of "system", "assistant", or "user" and a "content" key with a
            string value. Messages are organized such that "system" messages are at top of prompt,
            and "user" and "assistant" messages are displayed in order. Assistant messages get formatted as
            "Response: {content}".
        default_prompt_header: If True (default), add default prompt header after any system role messages and
            before user/assistant role messages.
        default_prompt_footer: If True (default), add default footer at end of prompt.

    Returns:
        Formatted prompt.
    """
    full_prompt = ""

    for message in messages:
        if message["role"] == "system":
            system_message = message["content"] + "\n"
            full_prompt += system_message

    if default_prompt_header:
        full_prompt += """### Instruction:
        The prompt below is a question to answer, a task to complete, or a conversation
        to respond to; decide which and write an appropriate response.
        \n### Prompt: """

    for message in messages:
        if message["role"] == "user":
            if message["content"].startswith("Context"):
                user_message = "\n### Context: " + message["content"]
            else:
                user_message = "\n### User: " + message["content"]
            full_prompt += user_message
        if message["role"] == "assistant":
            assistant_message = "\n### Response: " + message["content"]
            full_prompt += assistant_message

    if default_prompt_footer:
        full_prompt += "\n### Response:"

    return full_prompt
