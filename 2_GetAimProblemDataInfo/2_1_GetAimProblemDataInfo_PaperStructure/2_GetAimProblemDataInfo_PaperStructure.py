import os
import pickle
import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# 配置Edge选项
options = Options()
# options.add_argument('--headless')  # 无头模式，不打开浏览器，如果需要看到实际操作请去掉这一行

# 启动Edge浏览器
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

# 定义Cookies文件路径
cookies_file = '../../cookies.pkl'


# 加载Cookies
def load_cookies(driver, cookies_file):
    if os.path.exists(cookies_file):
        with open(cookies_file, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                driver.add_cookie(cookie)


# 保存Cookies
def save_cookies(driver, cookies_file):
    with open(cookies_file, 'wb') as cookiesfile:
        pickle.dump(driver.get_cookies(), cookiesfile)


# 登录函数
def login():
    driver.get('https://pintia.cn/auth/login')
    time.sleep(2)  # 等待页面加载
    load_cookies(driver, cookies_file)  # 加载Cookies
    driver.refresh()
    time.sleep(2)
    try:
        driver.find_element(By.CSS_SELECTOR, 'div.pc-image img[alt="Avatar"]')  # 检查头像图片元素
        print("已经登录！")
    except:
        try:
            driver.find_element(By.CSS_SELECTOR, 'div.teacher_tayqy[title="助教"]')  # 检查特定的div元素
            print("已经登录！")
        except:
            print("未登录，继续登录...")
            username_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="邮箱地址或手机号"]')
            password_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="密码"]')
            username_input.send_keys('caohai@sdu.edu.cn')  # 替换为实际账号
            password_input.send_keys('sduwh2024')  # 替换为实际密码
            password_input.send_keys(Keys.RETURN)
            print("请手动完成滑块验证，然后按回车键继续...")
            input()  # 等待用户完成滑块验证
            time.sleep(5)
            try:
                driver.find_element(By.CSS_SELECTOR, 'div.pc-image img[alt="Avatar"]')
                print("登录成功！")
            except:
                try:
                    driver.find_element(By.CSS_SELECTOR, 'div.teacher_tayqy[title="助教"]')
                    print("登录成功！")
                except:
                    print("登录失败！")
                    driver.quit()
                    exit(1)
            save_cookies(driver, cookies_file)  # 登录成功后保存Cookies


# 从网站加载Cookies到requests会话
def load_cookies_to_session(session, cookies_file):
    if os.path.exists(cookies_file):
        with open(cookies_file, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                session.cookies.set(cookie['name'], cookie['value'])


# 爬取试卷结构
def scrape_test_structure(problem_set_id):
    # 使用requests会话保持登录状态
    session = requests.Session()
    load_cookies_to_session(session, cookies_file)

    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://pintia.cn/',
        'X-Requested-With': 'XMLHttpRequest',
    }

    # API请求
    url = f'https://pintia.cn/api/problem-sets/{problem_set_id}/problem-set-paper-summary'
    response = session.get(url, headers=headers)

    # 打印响应状态码和内容
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")

    if response.status_code == 200:
        try:
            data = response.json()

            # 保存数据为JSON文件
            filename = f'2_GetAimProblemDataInfo_PaperStructure_{problem_set_id}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"数据已保存为 {filename}")

            # 打印完整的JSON数据
            print(json.dumps(data, indent=4, ensure_ascii=False))

            # 获取试卷结构
            summaries = data.get('summariesByPaperIndex', {}).get('0', {}).get('summaryByProblemType', {})

            # 打印每种题型的详细信息
            for problem_type, summary in summaries.items():
                print(f"题型: {problem_type}")
                print(f"总数: {summary.get('total')}")
                print(f"总分: {summary.get('totalScore')}")
                print(f"题库总数: {summary.get('totalInPools')}")
                print()
        except json.JSONDecodeError:
            print("响应内容不是有效的JSON格式")
    else:
        print("请求失败")


# 主函数
def main():
    # 读取1_UsableProblemDataInfo.json文件
    with open('../../1_GetAllProblemSetLink/1_UsableProblemDataInfo.json', 'r', encoding='utf-8') as f:
        problem_sets = json.load(f)

    # 登录网站
    login()

    # 遍历每个链接，爬取试卷结构
    for problem_set in problem_sets:
        problem_set_id = problem_set['id']
        scrape_test_structure(problem_set_id)

    # 关闭浏览器
    driver.quit()


# 执行主函数
if __name__ == "__main__":
    main()
