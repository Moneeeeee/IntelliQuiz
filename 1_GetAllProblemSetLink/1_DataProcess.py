import json
import os

# 定义输入和输出文件路径
input_file = '1_AllProblemSetInfo.json'
output_file = '1_AllProblemSetLink.json'

# 读取JSON文件中的数据
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# 提取所需字段并添加link
def extract_required_fields(data):
    extracted_data = []
    for item in data:
        extracted_item = {
            "id": item["id"],
            "name": item["name"],
            "startAt": item["startAt"],
            "endAt": item["endAt"],
            "createAt": item["createAt"],
            "link": f"https://pintia.cn/problem-sets/{item['id']}/overview"
        }
        extracted_data.append(extracted_item)
    return extracted_data

# 保存数据到JSON文件
def save_json_file(data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Extracted data saved to {output_file_path}")


# 主函数
if __name__ == "__main__":
    # 读取输入文件中的数据
    data = read_json_file(input_file)

    # 提取所需字段并添加link
    extracted_data = extract_required_fields(data)

    # 保存提取的数据到JSON文件
    save_json_file(extracted_data, output_file)
