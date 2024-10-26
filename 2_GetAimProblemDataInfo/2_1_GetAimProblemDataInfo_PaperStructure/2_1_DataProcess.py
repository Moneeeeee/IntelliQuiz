import json
import os


def transform_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    transformed_data = []

    # 获取试卷结构
    paper_id = input_file.split('_')[-1].split('.')[0]
    summaries = data['summariesByPaperIndex']['0']['summaryByProblemType']

    for problem_type, summary in summaries.items():
        transformed_data.append({
            'paper_id': paper_id,
            'problem_type': problem_type,
            'total': summary['total'],
            'total_score': summary['totalScore'],
            'total_in_pools': summary['totalInPools']
        })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transformed_data, f, ensure_ascii=False, indent=4)
        print(f"数据已保存为 {output_file}")


def process_files():
    current_directory = os.getcwd()
    for filename in os.listdir(current_directory):
        if filename.startswith("2_GetAimProblemDataInfo_PaperStructure_") and filename.endswith(".json"):
            input_file = os.path.join(current_directory, filename)
            paper_id = filename.split('_')[-1].split('.')[0]
            output_file = os.path.join(current_directory,
                                       f"2_1_GetAimProblemDataInfo_PaperStructure_Processed_{paper_id}.json")
            transform_data(input_file, output_file)


# 执行文件处理
process_files()
