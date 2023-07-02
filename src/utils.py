def compile_messages(messages: list[dict]) -> str:
    system = ""
    prompt = ""

    # Dump system messages first
    for message in messages:
        role = message["role"]
        content = message["content"]
        if role != "system":
            continue
        system += content

    if system:
        prompt += f"### Instruction:\n{system}\n### Prompt"

    # Dump context
    for message in messages:
        role = message["role"]
        content = message["content"]
        if role == "system":
            continue
        if "### Context:" in content:
            prompt += f"{content.strip()}\n"
        else:
            name = "Assistant" if role == "assistant" else "Human"
            prompt += f"### {name}:\n{content.strip()}\n"

    prompt += "### Response:\n"
    return prompt


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
            prompt += f"### Prompt:\n{content}\n"
        elif message["role"] == "assistant":
            prompt += f"### Response:\n{content}\n"

    return prompt, f"{system}{context}"


def valid_gpt4all_model(model_name: str, models: dict) -> bool:
    for i in models:
        if model_name.lower() == i["filename"].lower():
            return True
    else:
        return False
