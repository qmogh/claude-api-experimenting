from anthropic import Anthropic
import random

client = Anthropic()

tools = [
    {
        "name": "get_weather",
        "description": "Get weather for a city",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "get_time",
        "description": "Get current time for a city",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    },
    {
        "name": "roll_d_20",
        "description": "Make a joke to the user",
        "input_schema": {
            "type": "object",
            "properties": {},
    },
    }
]

def get_weather(city):
    return f"Sunny in {city}"

def get_time(city):
    return f"3pm in {city}"

def d_20():
    return f"The number is {random.randint(1, 20)}"


messages = [
    {"role": "user", "content": "What's the weather in NYC and time in SF? Also, can you roll a d20?"}
]

while True:
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=500,
        messages=messages,
        tools=tools,
    )

    content = response.content

    if response.stop_reason != "tool_use":
        text = next((c.text for c in content if c.type == "text"), "")
        print("Final Answer:")
        print(text)
        break

    messages.append({"role": "assistant", "content": content})

    tool_results = []
    for block in content:
        if block.type != "tool_use":
            continue

        if block.name == "get_weather":
            result = get_weather(**block.input)
        elif block.name == "get_time":
            result = get_time(**block.input)
        elif block.name == "roll_d_20":
            result = d_20(**block.input)
        else:
            result = f"Unknown tool: {block.name}"

        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": result,
        })

    messages.append({"role": "user", "content": tool_results})