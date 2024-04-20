import os
import wandb
from openai import OpenAI

def call_api():
    client = OpenAI(api_key='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')
    gpt_assistant_prompt = "You are a knowledge management assistant. "  # Hardcoded prompt
    gpt_user_prompt = input("What prompt do you want me to respond to?")
    gpt_prompt = gpt_assistant_prompt + gpt_user_prompt  # Concatenate the prompts
    print(gpt_prompt)

    message = [{"role": "assistant", "content": gpt_assistant_prompt}, {"role": "user", "content": gpt_user_prompt}]
    temperature = 0.2
    max_tokens = 256
    frequency_penalty = 0.0

    response = client.chat.completions.create(
        model="gpt-4",
        messages=message,
        temperature=temperature,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty
    )
    print(response.choices[0].message)

call_api()
