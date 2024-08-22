from openai import OpenAI
client = OpenAI()



system_prompt = ["You are an AI assistant. You will help to build parse trees from flat tree levels.\
    The tree levels will be separated by square brackets. Each node represents a terminal or non-terminal (might be whitespace as well). \
    Your job is to add structures to these tree levels by grouping smaller segments. The group should add structure to the tree in line with the language's grammar. \
    Repeatedly adding structures to the initial flat level will build the complete parse trees. So suggest segments capturing expressions, sub-expressions, any nesting concepts, etc. \
    Ideally these segments will have minimum 2 to maximum 10 tokens. Show list of unique groups as json, the format should be json[siblings]:[[node1, node2, ...],...group_20]. \
    Discard groups with more than 10 tokens, also keep the group list small to ensure valid json output. Refine your suggestions based on the system feedback."]
    # Look at the steps for 'while' language examples below.",
    # "[while boolexpr & boolexpr do L = numexpr],\
    # [if ~boolexpr then L = numexpr else L = numexpr]",
    # "'~boolexpr' can be grouped as boolexpr, the output could be: {~}, {boolexpr}. \
    # 'boolexpr & boolexpr' can be grouped as boolexpr, the output could be: {boolexpr}, { }, {&}, {}, {boolexpr} \
    # 'L = numexpr' can be grouped as parse tree node stmt, so the siblings are: {L}, { }, {=}, { }, {numexpr}",
    # "[L = L ; if boolexpr then stmt else stmt]",
    # "'L = L' can be grouped as parse tree node stmt, so the siblings are: {L}, { }, {=}, { }, {L} \
    # 'if boolexpr then stmt else stmt' can be grouped as parse tree node stmt, so the siblings are: {if}, { }, {boolexpr}, { }, {then}, { }, {stmt}, { }, {else}, { }, {stmt}"]

messages = [{'role': 'system', 'content': system_prompt[0]}]
i =1
while i < len(system_prompt):
    messages.append({'role': 'system', 'name': 'example_tree_levels', 'content': system_prompt[i]})
    messages.append({'role': 'system', 'name': 'example_sibling_group', 'content': system_prompt[i+1]})
    i += 2
# messages.append({'role': 'system', 'content': 'Given some flat tree levels, suggest unique groups to build the parse trees. Discard long groups (len>10) from output, do not show too many groups (limit output within 10 groups). Refine your suggestions based on the feedback after each iteration. \
#                  Only show list of siblings as json output. The format should be json[siblings]:[[node1, node2, ...],...]'})
chat_log = []
def bubble_api(trees, feedback):

    if feedback:
        chat_log.append({'role': 'system', 'name': 'feedback', 'content': f"Correct groups for the last user query: {[f.bubbled_elems for f in feedback.values()]}."})
    elif chat_log:
        chat_log.append({'role': 'system', 'name': 'feedback', 'content': f"None of the groups suggested by the assistant is valid. Don't repeat those, suggest new groups of 2-10 tokens"})
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

