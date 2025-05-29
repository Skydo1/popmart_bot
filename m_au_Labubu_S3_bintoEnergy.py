from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def send_email(text):
    sender_email = "pmart4261@gmail.com"
    sender_password = "eiov bchh scrb zdhz"  # 使用的是 Gmail 的应用专用密码

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = "yyp.0526@outlook.com"
    msg['Subject'] = Header("Popmart mmmmmmmm 补货啦，快去抢购！", "utf-8")
    msg.attach(MIMEText(text, "plain", "utf-8"))

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, ["yyp.0526@outlook.com"], msg.as_string())
        print("✅ 邮件发送成功")
    except Exception as e:
        print(f"❌ 发送邮件失败: {e}")

# 商品页面 URL
PRODUCT_URL = "https://www.popmart.com/au/products/1990/THE-MONSTERS-Big-into-Energy-Series-Vinyl-Plush-Pendant-Blind-Box"
REFRESH_INTERVAL = 10  # 刷新间隔秒数

# 设置 Chrome 浏览器
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 初始 driver
driver = webdriver.Chrome(options=options)

# 控制变量
max_iterations = 40
count = 0

try:
    while True:
       
        if count % max_iterations == 0 and count != 0:
            print("🔁 达到刷新上限，重启浏览器中...")
            driver.quit()
            driver = webdriver.Chrome(options=options)

        driver.get(PRODUCT_URL)
        print(f"🔄 第 {count + 1} 次刷新页面中...")
        

        time.sleep(2)
        try:
            accept_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.policy_acceptBtn__ZNU71"))
            )
            print("found the button")
            # Use JavaScript to click it in case regular click doesn't work
            driver.execute_script("arguments[0].click();", accept_button)
        except:
            try:
                add_button = driver.find_element(By.XPATH, "//div[text()='ADD TO CART']")
                if add_button.is_displayed():
                    print("【✅ 有货啦！】")
                    send_email("popmart s3 一ge 一ge 一ge 有货了！！！")
                    break
            except:
                print(f"one 暂时无货")
                try:
                    box = driver.find_element(By.XPATH, "//div[text()='Whole Set']")
                    box.click()
                    add_button = driver.find_element(By.XPATH, "//div[text()='ADD TO CART']")
                    if add_button.is_displayed():
                        print("【✅ 有货啦！】")
                        send_email("popmart s3 一盒 一盒 一盒 有货了！！！")
                        break
                except Exception as e:
                    print(f" box 暂时无货")
                    time.sleep(REFRESH_INTERVAL)

        count += 1

finally:
    driver.quit()
