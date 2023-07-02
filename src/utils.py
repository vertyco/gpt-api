def compile_messages(messages: list[dict]) -> str:
    system = ""
    context = ""
    prompt = ""
    for message in messages:
        if message["role"] == "system":
            system += message["content"] + "\n"

    for message in messages:
        if message["role"] == "system":
            continue
        content = message["content"].strip()
        if "### Context:" in content:
            context += f"{content.replace('### Context:', '').strip()}\n"
        elif message["role"] == "user":
            prompt += f"### Prompt: {content}\n"
        elif message["role"] == "assistant":
            prompt += f"### Response: {content}\n"

    final = ""
    if system:
        final += f"### Instruction: {system}\n"
    if context:
        final += f"### Context: {context}\n"
    if prompt:
        final += prompt

    final += "\n### Response:"

    return final.strip()


def compile_qa_messages(messages: list[dict]) -> tuple[str, str]:
    system = ""
    context = ""
    prompt = ""
    for message in messages:
        if message["role"] == "system":
            system += message["content"] + "\n"

    for message in messages:
        if message["role"] == "system":
            continue
        content = message["content"].strip()
        if "### Context:" in content:
            context += f"{content.replace('### Context:', '').strip()}\n"
        elif message["role"] == "user":
            prompt += f"### Prompt: {content}\n"
        elif message["role"] == "assistant":
            prompt += f"### Response: {content}\n"

    return prompt, f"{system}{context}"


def valid_gpt4all_model(model_name: str, models: dict) -> bool:
    for i in models:
        if model_name.lower() == i["filename"].lower():
            return True
    else:
        return False
