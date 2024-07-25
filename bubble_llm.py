from openai import OpenAI
client = OpenAI()



system_prompt = ["You are an AI assistant. You will help to complete some partially complete parse trees. You will be given some flat tree levels.\
    The tree levels will be separated by square brackets. Each node represents a terminal or non-terminal (might be whitespace as well). Your job is to find out which smaller node groups can add structure to those tree levels. \
    Grouping these small groups will add hierarchy to the parse tree. The goal is to form the final parse tree resembling the language's grammar. \
    Look for shorter groups first rather than longer groups. Because the short groups will incrementally build the parse trees. \Look at the steps for 'while' language examples below.",
    "[while boolexpr & boolexpr do L = numexpr],\
    [if ~boolexpr then L = numexpr else L = numexpr]",
    "'~boolexpr' can be grouped as boolexpr, the output could be: {~}, {boolexpr}. \
    'boolexpr & boolexpr' can be grouped as boolexpr, the output could be: {boolexpr}, { }, {&}, {}, {boolexpr} \
    'L = numexpr' can be grouped as parse tree node stmt, so the siblings are: {L}, { }, {=}, { }, {numexpr}",
    "[L = L ; if boolexpr then stmt else stmt]",
    "'L = L' can be grouped as parse tree node stmt, so the siblings are: {L}, { }, {=}, { }, {L} \
    'if boolexpr then stmt else stmt' can be grouped as parse tree node stmt, so the siblings are: {if}, { }, {boolexpr}, { }, {then}, { }, {stmt}, { }, {else}, { }, {stmt}"]

messages = [{'role': 'system', 'content': system_prompt[0]}]
i =1
while i < len(system_prompt):
    messages.append({'role': 'system', 'name': 'example_tree_levels', 'content': system_prompt[i]})
    messages.append({'role': 'system', 'name': 'example_sibling_group', 'content': system_prompt[i+1]})
    i += 2
messages.append({'role': 'system', 'content': 'Show maximum 10 unique groups. \
                 Only show list of siblings as json output. The format should be json[siblings]:[[node1, node2, ...],...group10]'})
chat_log = []
def bubble_api(trees):

    chat_log.append({'role': 'user', 'content': f'{trees}'})
    prompt = messages + chat_log
    gpt = client.chat.completions.create(
        model="gpt-4o",
        messages=prompt,
        seed = 12345,
        response_format={"type": "json_object"},
        temperature=0
    )
    response = gpt.choices[0].message.content
    print(response)
    chat_log.append({'role': 'assistant', 'content': response})
    if len(chat_log) > 10:
        chat_log.pop(0)
        chat_log.pop(0)
    return response

if __name__ == '__main__':
    print("Welcome to the interactive GPT chat. Type 'quit' to exit.")
        
    chat_log = []
    start = len(messages)
    while True:
        user_prompt = input("You: ")
        if user_prompt.lower() == 'quit':
            break
        chat_log.append({'role': 'user', 'content': user_prompt})
        response = bubble_api(chat_log)
        print(f"AI: {response}")
        chat_log.append({'role': 'assistant', 'content': response})
        if len(chat_log) > 10:
            chat_log.pop(0)
            chat_log.pop(0)

    # chat_log = system_prompt
    # while True:
    #     user_prompt = input("You: ")
    #     if user_prompt.lower() == 'quit':
    #         break
    #     response, chat_log = chat_with_gpt(user_prompt, chat_log)
    #     print(f"AI: {response}")

