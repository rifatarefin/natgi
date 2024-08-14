from openai import OpenAI
client = OpenAI()


system_prompt = ["You are an AI assistant. You will label the internal nodes in the parse tree of any arbitrary program. The root node of the parse tree\
    has label stmt. You will be given a pair of substrings derivable from the same non-terminal symbol. Your job is to label the non-terminal symbol. Look at \
    some example substring pairs and their labels.",
    "'(n+n)','n'",
    "numexpr, this non-terminal can derive both the substrings (n+n) and n",
    "'L = (n+n)','while true do L = (n+n)'",
    "stmt, this non-terminal can derive both the substrings 'L = (n+n)' and 'while true do L = (n+n)'",
    "'(n+n) == n','true'",
    "boolexpr, this non-terminal can derive both the substrings '(n+n) == n' and 'true'",]

messages = [{'role': 'system', 'content': system_prompt[0]}]
i =1
while i < len(system_prompt):
    messages.append({'role': 'system', 'name': 'example_substrings', 'content': system_prompt[i]})
    messages.append({'role': 'system', 'name': 'example_non-terminal', 'content': system_prompt[i+1]})
    i += 2
messages.append({'role': 'system', 'content': 'Now suggest a non-terminal symbol that can derive the given substrings. The output must be a single label, never any explanation.'})

def generate_label_api(str_pair):

    messages.append({'role': 'user', 'content': f"'{str_pair[0]}','{str_pair[1]}'"})
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        seed=12345,
        max_tokens=5,
        # response_format={"type": "json_object"},
        temperature=0
    )
    messages.pop()
    return response.choices[0].message.content.split()[0]

if __name__ == '__main__':
    print("Welcome to the interactive GPT chat. Type 'quit' to exit.")
        
    chat_log = []
    start = len(messages)
    while True:
        user_prompt = input("You: ")
        if user_prompt.lower() == 'quit':
            break
        chat_log.append({'role': 'user', 'content': user_prompt})
        response = generate_label_api(chat_log)
        print(f"AI: {response}")
        chat_log.append({'role': 'assistant', 'content': response})
        if len(chat_log) > 10:
            chat_log.pop(0)
            chat_log.pop(0)


