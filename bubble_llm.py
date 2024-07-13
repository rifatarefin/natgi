from openai import OpenAI
client = OpenAI()



system_prompt = ["You are an AI assistant. You will find structure from some programming language examples. Initially there are partial structures\
    in the examples in the form of parse trees, the trees would be in newick format. Remember all nodes in the trees are labeled, whitespace and braces also appear as node labels.\
    The root has label 'stmt'. The individual trees will be separated by square brackets. Your job is to find the remaining hierarchies by grouping short contiguous sequence of sibling nodes. \
    Grouping these siblings will add hierarchy to the parse tree, comparable to a production rule in a context-free grammar. Look at the steps for 'while' language examples below.",
    "[(while, ,boolexpr, ,&, ,boolexpr, ,do, ,L, ,=, ,((,numexpr,+,numexpr,))numexpr)stmt],\
    [(if, ,~,boolexpr, ,then, ,L, ,=, ,numexpr, ,else, ,L, ,=, ,((,numexpr,+,numexpr,))numexpr)stmt]",
    "'L = numexpr' can be grouped as parse tree node stmt, so the siblings are: {L}, { }, {=}, { }, {numexpr}",
    "[(while, ,boolexpr, ,&, ,boolexpr, ,do, ,(L, ,=, ,((,numexpr,+,numexpr,))numexpr)stmt)stmt],\
    [(if, ,~,boolexpr, ,then, ,(L, ,=, ,numexpr)stmt, ,else, ,(L, ,=, ,((,numexpr,+,numexpr,))numexpr)stmt)stmt]",
    "'boolexpr & boolexpr' can be grouped as parse tree node boolexpr, so the siblings are: {boolexpr}, { }, {&}, { }, {boolexpr}. '~boolexpr' can also be grouped as boolexpr, the outputcould be: {~}, {boolexpr}",
    "[((L, ,=, ,L)stmt, ,;, ,if, ,(numexpr, ,=,=, ,numexpr)boolexpr, ,then, ,stmt, ,else, ,(L, ,=, ,((,numexpr,+,numexpr,))numexpr)stmt)stmt]",
    "'if boolexpr then stmt else stmt' can be grouped as parse tree node stmt, so the siblings are: {if}, { }, {boolexpr}, { }, {then}, { }, {stmt}, { }, {else}, { }, {stmt}",]

messages = [{'role': 'system', 'content': system_prompt[0]}]
i =1
while i < len(system_prompt):
    messages.append({'role': 'system', 'name': 'example_trees', 'content': system_prompt[i]})
    messages.append({'role': 'system', 'name': 'example_sibling_group', 'content': system_prompt[i+1]})
    i += 2
messages.append({'role': 'system', 'content': 'Now group sibling nodes that will add hierarchies to the following trees.  \
                 Show maximum 10 unique groups, maximum 10 siblings per group. The shorter the group the better. \
                 Only show list of siblings as json output. The format should be json[siblings]:[[node1, node2, ...],...group10]'})
chat_log = []
def bubble_api(trees):

    chat_log.append({'role': 'user', 'content': f'Consider these trees\n{trees}'})
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

