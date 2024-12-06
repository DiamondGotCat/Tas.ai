script_version = "1.0.0"
from openai import OpenAI
from shlex import join
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
messages = []

def spacer():
    print("")

def addUser(message):
    messages.append({"role": "user", "content": message})

def addAssistant(message):
    messages.append({"role": "assistant", "content": message})

def addSystem(message):
    messages.append({"role": "system", "content": message})

def getResponse(messages, client, model) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

def generateTasks(messages):
    global client
    prompt = """
    Your Tasks:
    1. Please think the Next Tasks of assistant Only.
    2. Please output Tasks Only.
    3. Do not Output in Code Block, Please Output in Plain Text.
    4. Do not Output Answer Task (example: "3. Answer").

    Task Format:
    ```
    1. Thinking about Python
    2. Create Example Code
    ```
    """
    return getResponse(messages=[{"role": "system", "content": prompt}, {"role": "user", "content": f"{messages}"}], client=client, model="gpt-4o-mini").split("\n")

def runTasks(tasks, messages):
    global client
    for task in tasks:
        print(f"({task})")
        addSystem(f"---Task{task}---")
        addAssistant(getResponse(messages, client=client, model="gpt-4o"))
        addSystem("---TaskEND---")

def main():
    print("Tas.AI - Task-base AI")
    print(f"V{script_version}")
    spacer()

    while True:
        prompt = input(">>> ")
        addUser(prompt)
        addSystem("Please Generate Tasks.")
        tasks = generateTasks(messages)
        print("[TASKS]\n" + "\n".join(tasks) + "\n[RUN]")
        addAssistant(f"{tasks}")
        addSystem("Please Start Tasks.")
        runTasks(tasks, messages)
        addSystem("End Tasks.")
        addSystem("Please Answer.")
        result = getResponse(messages, client=client, model="gpt-4o")
        print(f"[ASSISTANT]\n{result}")
        addAssistant(result)

try:
    main()
except KeyboardInterrupt:
    pass
