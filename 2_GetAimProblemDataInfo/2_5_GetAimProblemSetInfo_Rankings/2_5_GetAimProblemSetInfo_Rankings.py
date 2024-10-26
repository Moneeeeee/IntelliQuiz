import os
import pickle
import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup

# 配置Edge选项
options = Options()
# options.add_argument('--headless')  # 无头模式，不打开浏览器，如果需要看到实际操作请去掉这一行

# 启动Edge浏览器
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

# 定义Cookies文件路径
cookies_file = 'cookies.pkl'

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

# 爬取API数据并保存为JSON文件
def scrape_api_data(url, output_file):
    session = requests.Session()
    load_cookies_to_session(session, cookies_file)

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    response = session.get(url, headers=headers)

    print(f"响应状态码: {response.status_code}")

    if response.status_code == 200:
        try:
            data = response.json()
            # 保存数据为JSON文件
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"数据已保存为 {output_file}")
        except json.JSONDecodeError:
            # 如果响应不是有效的JSON格式，使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            rankings = []

            # 解析排名数据
            rows = soup.select('table tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) > 1:
                    ranking = {
                        'rank': cells[0].get_text(strip=True),
                        'name': cells[1].get_text(strip=True),
                        'score': cells[2].get_text(strip=True),
                        'time': cells[3].get_text(strip=True)
                    }
                    rankings.append(ranking)

            # 保存解析后的数据为JSON文件
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(rankings, f, ensure_ascii=False, indent=4)
                print(f"数据已保存为 {output_file}")
    else:
        print(f"Failed to retrieve the data from {url}. Status code: {response.status_code}")

# 遍历JSON文件中的所有rankinglink并爬取数据
def main():
    input_file = '../2_4_Combine/2_2_GetAimProblemDataInfo_Entry_Combined_V0.02.json'
    with open(input_file, 'r', encoding='utf-8') as f:
        problem_sets = json.load(f)

    # 登录网站
    login()

    # 遍历每个rankinglink，爬取API数据并保存为JSON文件
    for problem_set in problem_sets:
        ranking_link = problem_set['rankinglink']
        problem_set_id = problem_set['ProblemSetID']
        output_file = f'rankings_data_{problem_set_id}.json'
        scrape_api_data(f"{ranking_link}?page=0&limit=50", output_file)

    # 关闭浏览器
    driver.quit()

# 执行主函数
if __name__ == "__main__":
    main()
