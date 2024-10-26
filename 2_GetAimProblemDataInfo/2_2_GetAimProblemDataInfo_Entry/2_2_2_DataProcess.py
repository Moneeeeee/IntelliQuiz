import os
import json


def process_data(input_file, output_file):
    # 读取输入JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 提取所需的信息
    user_group_id = data['userGroupProblemSets'][0]['userGroupId']
    problem_set_id = data['userGroupProblemSets'][0]['problemSetId']
    link = f"https://pintia.cn/problem-sets/{problem_set_id}/examinees?userGroupId={user_group_id}"

    # 创建新的数据结构
    result = {
        "link": link
    }

    # 保存结果为新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"数据已保存为 {output_file}")


def process_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.startswith("2_2_GetAimProblemDataInfo_Entry_") and filename.endswith(".json"):
            input_file = os.path.join(directory, filename)
            paper_id = filename.split('_')[-1].split('.')[0]
            output_file = os.path.join(directory, f"2_2_GetAimProblemDataInfo_Entry_Processed_{paper_id}.json")
            process_data(input_file, output_file)


# 执行批量处理
if __name__ == "__main__":
    current_directory = os.getcwd()  # 获取当前目录
    process_files_in_directory(current_directory)
