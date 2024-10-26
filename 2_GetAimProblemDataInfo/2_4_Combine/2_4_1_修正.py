import json

# Load the JSON file
file_path = '2_2_GetAimProblemDataInfo_Entry_Combined.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Modify the JSON structure
for entry in data:
    entry['overviewlink'] = f"https://pintia.cn/problem-sets/{entry['ProblemSetID']}"
    entry['submissionlink'] = f"https://pintia.cn/problem-sets/{entry['ProblemSetID']}/submissions"
    entry['rankinglink'] = f"https://pintia.cn/problem-sets/{entry['ProblemSetID']}/rankings"
    entry['examinees'] = f"https://pintia.cn/problem-sets/{entry['ProblemSetID']}/examinees"
    del entry['link']
# Save the modified JSON back to a file
modified_file_path = '2_2_GetAimProblemDataInfo_Entry_Combined_V0.02.json'
with open(modified_file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Modified file saved to {modified_file_path}")
