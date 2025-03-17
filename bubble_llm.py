from openai import OpenAI
client = OpenAI()



system_prompt = ["""You are an AI assistant. You will help to build parse trees from flat tree levels.
    You will combine adjacent nodes from a tree level. Those nodes will be placed under a new parent node at that position.
    You will suggest node groups in a way that will build the complete parse tree iteratively.
    Input: A list of tree levels separated by square brackets.
    Output: A list of unique groups as json, the format should be json[siblings]:[[node1, node2, ...],...group_n].
    Ensure that:
    1. The groups should reflect the language's parse tree structure (grammar).
    2. Consider each group as the RHS of a production rule in the language's grammar.
    2. Look for common language concepts for nesting, within a **concise** length of 2-10 tokens. Tokens are within double quotes. Discard **long** groups (more than 10 tokens).
    3. Each group should be a valid subset of a tree level, **don't** suggest an entire level from the input.
    4. Look for the distinguishing part between two similar tree levels, those groups are more promising.
    5. Limit the group list to best 25 suggestions."""]
    # The tree levels will be separated by square brackets. Each node represents a terminal or non-terminal (might be whitespace as well). \
    # Your job is to add structures to these tree levels by grouping smaller segments. The segments should introduce a new level in the tree according \
    # to the language's grammar. The process should continue iteratively and eventually build the complete parse tree. \
    # So suggest segments capturing expressions, sub-expressions, any nesting concepts, etc. that can structure a tree level. \
    # Look for diverse structure patterns, each pattern should match a rule of the language's grammar.\
    # Ideally these segments will be short, comprising minimum 2 to maximum 15 tokens, so start from the shortest segments. \
    # Show list of unique groups as json, the format should be json[siblings]:[[node1, node2, ...],...group_n]. \
    # Discard groups with more than 10 tokens, also limit the group list to 25 suggestions. Refine your suggestions based on the system feedback."""]
   
    # Look at the steps for 'while' language examples below.",
    # "[while boolexpr & boolexpr do L = numexpr],\
    # [if ~boolexpr then L = numexpr else L = numexpr]",
    # "'~boolexpr' can be grouped as boolexpr, the output could be: {~}, {boolexpr}. \
    # 'boolexpr & boolexpr' can be grouped as boolexpr, the output could be: {boolexpr}, { }, {&}, {}, {boolexpr} \
    # 'L = numexpr' can be grouped as parse tree node stmt, so the siblings are: {L}, { }, {=}, { }, {numexpr}",
    # "[L = L ; if boolexpr then stmt else stmt]",
    # "'L = L' can be grouped as parse tree node stmt, so the siblings are: {L}, { }, {=}, { }, {L} \
    # 'if boolexpr then stmt else stmt' can be grouped as parse tree node stmt, so the siblings are: {if}, { }, {boolexpr}, { }, {then}, { }, {stmt}, { }, {else}, { }, {stmt}"]

system_message = [{'role': 'system', 'content': system_prompt[0]}]
# i =1
# while i < len(system_prompt):
#     messages.append({'role': 'system', 'name': 'example_tree_levels', 'content': system_prompt[i]})
#     messages.append({'role': 'system', 'name': 'example_sibling_group', 'content': system_prompt[i+1]})
#     i += 2
# messages.append({'role': 'system', 'content': 'Given some flat tree levels, suggest unique groups to build the parse trees. Discard long groups (len>10) from output, do not show too many groups (limit output within 10 groups). Refine your suggestions based on the feedback after each iteration. \
#                  Only show list of siblings as json output. The format should be json[siblings]:[[node1, node2, ...],...]'})
chat_log = []
def bubble_api(trees, feedback):
    global chat_log
    if feedback:
        chat_log.append({'role': 'system', 'name': 'feedback', 'content': f"These suggestions were wrong:\n{feedback}"})
    # elif chat_log:
    #     chat_log.append({'role': 'system', 'name': 'feedback', 'content': f"None of the suggested group at last turn is valid. Don't repeat those. \
    #                      Look for common language concepts, considering diverse lengths within 2-10 tokens, don't output an entire level from input."})
    chat_log.append({'role': 'user', 'content': f'{trees}'})
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
    chat_log.append({'role': 'assistant', 'content': response})
    if len(chat_log) > 12:
        chat_log = chat_log[3:]
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

