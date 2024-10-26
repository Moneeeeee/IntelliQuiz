import os
import json

def process_and_merge_files(directory, output_file):
    merged_data = []

    # 遍历当前目录中的所有文件
    for filename in os.listdir(directory):
        if filename.startswith("2_2_GetAimProblemDataInfo_Entry_Processed_") and filename.endswith(".json"):
            input_file = os.path.join(directory, filename)
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 提取ProblemSetID
                problem_set_id = int(data['link'].split('/')[4])
                # 修改数据结构
                modified_data = {
                    "ProblemSetID": problem_set_id,
                    "link": data["link"]
                }
                merged_data.append(modified_data)

    # 保存合并后的数据为新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)
        print(f"数据已保存为 {output_file}")

# 执行合并
if __name__ == "__main__":
    current_directory = os.getcwd()  # 获取当前目录
    output_file = '2_2_GetAimProblemDataInfo_Entry_Combined.json'  # 合并后的输出文件
    process_and_merge_files(current_directory, output_file)
