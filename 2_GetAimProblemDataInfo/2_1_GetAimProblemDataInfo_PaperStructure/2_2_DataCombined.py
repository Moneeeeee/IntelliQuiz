import os
import json

def merge_processed_files(directory, output_file):
    merged_data = []

    # 遍历当前目录中的所有文件
    for filename in os.listdir(directory):
        if filename.startswith("2_1_GetAimProblemDataInfo_PaperStructure_Processed_") and filename.endswith(".json"):
            input_file = os.path.join(directory, filename)
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                merged_data.extend(data)

    # 保存合并后的数据为新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)
        print(f"数据已保存为 {output_file}")

# 执行合并
if __name__ == "__main__":
    current_directory = os.getcwd()  # 获取当前目录
    output_file = '2_1_GetAimProblemDataInfo_PaperStructure_Combined.json'  # 合并后的输出文件
    merge_processed_files(current_directory, output_file)
