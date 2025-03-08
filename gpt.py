from openai import OpenAI
import re
import os
import glob
import sys

client = OpenAI()

def  read_programs(seed_dir):
    # Read all files from the directory and store their content with a newline at the end
    programs = []
    for file_path in sorted(glob.glob(os.path.join(seed_dir, "*.ex*"))):  
        if os.path.isfile(file_path):  # Ensure it's a file
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read().strip()  # Remove extra spaces/newlines
                    programs.append(content + "\n")  # Ensure a newline at the end
            except UnicodeDecodeError:
                print(f"⚠️ Skipping non-text file: {file_path}")  # Handle binary files gracefully

    return programs
    
def save_output_grammar(output_text, seed_name):
    os.makedirs("results", exist_ok=True)
    # Save to a text file
    output_file = "results/grammar_output_for_"+seed_name+".txt"
    #with open(output_file, "w", encoding="utf-8") as file:
    #        file.write(output_text)
    # Extract only the "Production Rules" section
    #match = re.search(r"### Production Rules\n\n```bnf\n(.*?)\n```", output_text, re.DOTALL)
    match = re.search(r"<production-rules>(.*?)</production-rules>", output_text, re.DOTALL)
    print(match)
    if match:
        print("HI")
        production_rules = match.group(1).strip()
    else:
        production_rules = "Production rules not found."
    
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(production_rules)
    
    print(f"Production Rules saved to {output_file}")


def gpt_grammar_generation(seed_dir, seed_name):
    programs = read_programs(seed_dir)
    system_prompt = """You will generate a context-free grammar (CFG) in Backus-Naur Form (BNF) from the given example programs. 
    Ensure that:
    1. The grammar **always** follows the same structure.
    2. The **Production Rules** must be enclosed within `<production-rules>` and `</production-rules>` tags.
    3. **Whitespaces** should be included as terminal tokens in the grammar rules.
    4. Do **not** add any extra explanations—only return the production rules inside the tags.
    """
    # Combine all program contents into one string
    user_prompt = "Example programs:\n" + "".join(programs)
    
    completion = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
      ]
    )
    
    #print(completion.choices[0].message.content)
    output_text = completion.choices[0].message.content
    print(output_text)
    save_output_grammar(output_text, seed_name)

if __name__ == "__main__":
    seed_dir = sys.argv[1] #"Seed_Programs/tinyc/tinyc-train-r1"
    seed_name = sys.argv[2]
    gpt_grammar_generation(seed_dir, seed_name)
