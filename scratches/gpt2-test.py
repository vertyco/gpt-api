import transformers
from transformers import pipeline

# Initialize the text generation pipeline
text_generator = pipeline("text-generation", model="gpt2")
transformers.logging.set_verbosity(transformers.logging.ERROR)

# Initialize the conversation history
conversation_history = ""

while True:
    # Get the user's message
    user_message = input("User: ")

    # If the user types 'quit', end the conversation
    if user_message.lower() == "quit":
        break

    # Add the user's message to the conversation history
    conversation_history += f"User: {user_message}\n"

    # Generate a response
    prompt = conversation_history + "Assistant: "
    output = text_generator(prompt, max_length=1000, do_sample=True)

    # Extract the assistant's message from the generated text
    assistant_message = output[0]["generated_text"].replace("Assistant: ", "")

    # Add the assistant's message to the conversation history
    conversation_history += f"Assistant: {assistant_message}\n"

    # Print the assistant's message
    print(f"Assistant: {assistant_message}")
