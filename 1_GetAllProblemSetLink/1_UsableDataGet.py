import json

# 定义输入和输出文件路径
input_file = '1_AllProblemSetLink.json'
output_file = '1_UsableProblemDataInfo.json'

# 读取JSON文件中的数据
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# 提取所需字段并添加link，同时过滤name中包含"2023年C语言"的记录
def extract_and_filter_fields(data):
    extracted_data = []
    for item in data:
        if "2023年C语言" in item["name"]:
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
    print(f"Filtered data saved to {output_file_path}")

# 主函数
if __name__ == "__main__":
    # 读取输入文件中的数据
    data = read_json_file(input_file)

    # 提取所需字段并添加link，同时过滤name中包含"2023年C语言"的记录
    filtered_data = extract_and_filter_fields(data)

    # 保存提取和过滤后的数据到JSON文件
    save_json_file(filtered_data, output_file)
