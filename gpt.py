from openai import OpenAI
import re
import os
import glob

client = OpenAI()

seed_name = "X"
system_prompt = """You will generate a context-free grammar (CFG) in Backus-Naur Form (BNF) from the given example programs. 
Ensure that:
1. The grammar **always** follows the same structure.
2. The **Production Rules** must be enclosed within `<production-rules>` and `</production-rules>` tags.
3. Do **not** add any extra explanations—only return the production rules inside the tags.
"""

tinyc_seed_dir="Seed_Programs/tinyc/tinyc-train-r1"
# Read all files from the directory and store their content with a newline at the end
programs = []
for file_path in sorted(glob.glob(os.path.join(tinyc_seed_dir, "*.ex*"))):  
    if os.path.isfile(file_path):  # Ensure it's a file
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()  # Remove extra spaces/newlines
                programs.append(content + "\n")  # Ensure a newline at the end
        except UnicodeDecodeError:
            print(f"⚠️ Skipping non-text file: {file_path}")  # Handle binary files gracefully

#for filename in sorted(os.listdir(tinyc_seed_dir)):  # Sort for consistency
#    file_path = os.path.join(tinyc_seed_dir, filename)
#    if os.path.isfile(file_path):  # Ensure it's a file
#        with open(file_path, "r", encoding="utf-8") as file:
#            content = file.read().strip()  # Remove trailing spaces/newlines
#            programs.append(content + "\n")  # Ensure a newline at the end

# Combine all program contents into one string
user_prompt = "Example programs:\n" + "".join(programs)
#print('user_prompt=', user_prompt)
#exit()

#user_prompt = """Example programs:\n\
#     while true & true do L = (L+n)\n\
#     while ~false do while ~~L == n do skip\n\
#     while false do if L == L & false & true & true then skip else if ~true & L == n then skip else skip
#     """
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
# Save to a text file
output_file = "grammar_output_for_"+seed_name+".txt"
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

