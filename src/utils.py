def compile_messages(
    messages: list[dict], default_prompt_header=True, default_prompt_footer=True
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
        full_prompt += (
            "### Instruction:\n"
            "The prompt below is a question to answer, a task to complete, or a conversation"
            "to respond to; decide which and write an appropriate response.\n"
            "### Prompt:"
        )

    for message in messages:
        content = message["content"].strip()
        if message["role"] == "user":
            full_prompt += f"\n{content}"
        if message["role"] == "assistant":
            assistant_message = "\n### Response: " + content
            full_prompt += assistant_message

    if default_prompt_footer:
        full_prompt += "\n### Response:"

    return full_prompt.strip()


def compile_qa_messages(messages: list[dict]) -> tuple[str, str]:
    context = ""
    prompt = ""
    for message in messages:
        if message["role"] == "system":
            system_message = "### Instruction:\n" + message["content"] + "\n"
            context += system_message

    for message in messages:
        if message["role"] == "system":
            continue
        content = message["content"].strip()
        if "### Context:" in content:
            context += f"{content.replace('### Context:', '').strip()}\n"
        elif message["role"] == "user":
            prompt += f"{content}\n"
        elif message["role"] == "assistant":
            context += f"### Response: {content}\n"

    return prompt, context


def valid_gpt4all_model(model_name: str, models: dict) -> bool:
    for i in models:
        if model_name.lower() == i["filename"].lower():
            return True
    else:
        return False
