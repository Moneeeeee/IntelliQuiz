import os
import json

def merge_json_files(file_list, output_file):
    merged_data = []

    for file in file_list:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            merged_data.append(data)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)
        print(f"数据已保存为 {output_file}")

def main():
    file_list = [
        '1_UsableProblemDataInfo.json',
        '2_2_GetAimProblemDataInfo_Entry_Combined.json',
        '2_3_GetAimProblemDtaInfo_MembersLink_Combined.json',
        '2_1_GetAimProblemDataInfo_PaperStructure_Combined.json'
    ]

    output_file = 'combined_data.json'
    merge_json_files(file_list, output_file)

if __name__ == "__main__":
    main()
