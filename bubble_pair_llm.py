from openai import OpenAI
client = OpenAI()



system_prompt = ["""You are an AI assistant. You will be given a list of tree levels.
                 You will find out segment pairs from these levels in a way that a segment pair can be derived from the same AST node.
                 Input: A list of tree levels separated by square brackets, the nodes in a level are separated by commas.
                 Output: A list of pairs as json, the format should be json[siblings]:[[pair1], [pair2],...[pair_n]]. Each pair should be two list of sibling nodes.
                 - Each pair should contain two **different** lists of nodes, these nodes should represent identical AST parents.
                 - Remeber there could be recursive structure, suggest the smallest recursion free units.
                 - Discard if two lists in a pair are exactly the same.
                 - Suggestions should be different from suggestion history.
                 - Limit the list to best 20 suggestions."""]

    

system_message = [{'role': 'system', 'content': system_prompt[0]}]
old_trees = []
old_examples = []
def bubble_pair_api(trees, old_bubbles=""):
    
    
    # if old_bubbles:

    #     old_bubble_str = '\n'.join(
    #         str([elem.payload for elem in bubble.bubbled_elems])
    #         for bubble in old_bubbles
    #     )
    #     old_examples = [{'role': 'system', 'name': 'example_groups', 
    #                            'content': f"Here are some groups that were already applied to the trees:\n{old_bubble_str}"}]

    chat_log = [{'role': 'user', 'content': f'{trees}'}]
    global old_trees
    old_trees.append({'role': 'system', 'name': 'tree_transformation_history',
                               'content': f'{trees}'})
    global old_examples
    prompt = system_message + old_examples + chat_log
    gpt = client.chat.completions.create(
        model="gpt-4o",
        messages=prompt,
        seed = 101,
        response_format={"type": "json_object"},
        temperature=0
    )
    response = gpt.choices[0].message.content
    print(response)
    old_examples = [({'role': 'assistant_history', 'content': response})]
    old_trees = old_trees[-10:]  # Keep only the last 10 tree transformations
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

