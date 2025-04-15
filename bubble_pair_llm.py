from openai import OpenAI
client = OpenAI()



system_prompt = ["""You are an AI assistant. You will be given a list of tree levels. Each level is a list of nodes.
                 You will find out which level pairs are derived from the same AST node.
                 Input: A list of tree levels separated by square brackets, the nodes in a level are separated by commas.
                 Output: A list of pairs as json, the format should be json[siblings]:[[pair1], [pair2],...[pair_n]]. Each pair should be two list of sibling nodes.
                 - Think which level pairs represent same language construct (e.g. similar expressions). Suggest those pairs.
                 - Limit the list to best 20 suggestions."""]

    

system_message = [{'role': 'system', 'content': system_prompt[0]}]

def bubble_pair_api(trees, feedback=""):
    
    chat_log = [{'role': 'user', 'content': f'{trees}'}]
    prompt = system_message + chat_log
    gpt = client.chat.completions.create(
        model="gpt-4o",
        messages=prompt,
        seed = 101,
        response_format={"type": "json_object"},
        temperature=0
    )
    response = gpt.choices[0].message.content
    print(response)
    return response

if __name__ == '__main__':
    print("Welcome to the interactive GPT chat. Type 'quit' to exit.")
        
    chat_log = []
    start = len(system_message)
    while True:
        user_prompt = input("You: ")
        if user_prompt.lower() == 'quit':
            break
        chat_log.append({'role': 'user', 'content': user_prompt})
        response = bubble_pair_api(chat_log)
        print(f"AI: {response}")
        chat_log.append({'role': 'assistant', 'content': response})
        if len(chat_log) > 10:
            chat_log.pop(0)
            chat_log.pop(0)

