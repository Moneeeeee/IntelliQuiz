import os
import json


def clean_data(input_file, output_file):
    # 读取输入JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 提取所需信息
    problem_set_id = int(input_file.split('_')[-1].split('.')[0])
    member_links = []

    for member in data["members"]:
        member_link = {
            "MemberLink": f"https://pintia.cn/problem-sets/{problem_set_id}/examinees/{member['user']['id']}/info",
            "ProblemSetID": problem_set_id,
            "name": member["studentUser"]["name"]
        }
        member_links.append(member_link)

    # 保存清洗后的数据为新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(member_links, f, ensure_ascii=False, indent=4)
        print(f"数据已保存为 {output_file}")


def process_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.startswith("2_3_GetAimProblemDtaInfo_MembersLink_") and filename.endswith(".json"):
            input_file = os.path.join(directory, filename)
            problem_set_id = filename.split('_')[-1].split('.')[0]
            output_file = os.path.join(directory,
                                       f"2_3_GetAimProblemDtaInfo_MembersLink_Processed_{problem_set_id}.json")
            clean_data(input_file, output_file)


# 执行批量处理
if __name__ == "__main__":
    current_directory = os.getcwd()  # 获取当前目录
    process_files_in_directory(current_directory)
