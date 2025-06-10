import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def send_email(text):
    sender_email = "pmart4261@gmail.com"
    sender_password = "eiov bchh scrb zdhz"  # Gmail 应用专用密码

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = "yyp.0526@outlook.com"
    msg['Subject'] = Header("Popmart mmmmmmmm 补货啦，快去抢购！/n https://www.popmart.com/au/products/1990/THE-MONSTERS-Big-into-Energy-Series-Vinyl-Plush-Pendant-Blind-Box", "utf-8")
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

# 设置 Chrome 浏览器选项
options = uc.ChromeOptions()
#options.add_argument('--headless')  # 如需无头可以取消注释
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 使用 undetected-chromedriver 初始化 driver
driver = uc.Chrome(options=options)

# 控制变量
max_iterations = 40
count = 0
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)


try:
    while True:
        got_stock = False 
        if count % max_iterations == 0 and count != 0:
            print("🔁 达到刷新上限，重启浏览器中...")
            driver.quit()
            # 设置 Chrome 浏览器选项
            options = uc.ChromeOptions()
            #options.add_argument('--headless')  # 如需无头可以取消注释
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            # 使用 undetected-chromedriver 初始化 driver
            driver = uc.Chrome(options=options)

        driver.get(PRODUCT_URL)
        print(f"🔄 第 {count + 1} 次刷新页面中...")

        time.sleep(2)
        try:
            accept_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.policy_acceptBtn__ZNU71"))
            )
            print("found the button")
            driver.execute_script("arguments[0].click();", accept_button)
        except:
            pass

        try:
            print("here")
            single = driver.find_element(By.XPATH, "//div[text()='Single Box']")
            print(single)
            single.click()
            
            add_button = driver.find_element(By.XPATH, "//div[text()='ADD TO CART']")
            if add_button.is_displayed():
                send_email("popmart s3 一ge 一ge 一ge 有货了！！！")
                add_button.click()
                time.sleep(2)
                print("🧩 检测到【一个】有货并加入购物车")
                got_stock = True

        except Exception as e:
            #print(e)
            print(f"one 暂时无货")
        
        try:
            print("box")
            box = driver.find_element(By.XPATH, "//div[text()='Whole Set']")
            box.click()
            print(box)
            add_button = driver.find_element(By.XPATH, "//div[text()='ADD TO CART']")
            if add_button.is_displayed():
                send_email("popmart s3 一盒 一盒 一盒 有货了！！！")
                add_button.click()
                time.sleep(2)
                print("🧩 检测到【一盒】有货并加入购物车")
                got_stock = True
        except Exception as e:
            #print(e)
            print(f" box 暂时无货")
        
        if got_stock:
            try:
                sign_in_btn = driver.find_element(By.XPATH, '//div[text()="Sign in / Register"]')
                sign_in_btn.click()

                email_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="email"]')))
                email_input.clear()
                actions.move_to_element(email_input).click().send_keys("yyp.0526@outlook.com").perform()

                continue_btn = wait.until(EC.element_to_be_clickable((
                    By.XPATH, '//button[contains(@class, "index_loginButton__") and text()="CONTINUE"]')))
                continue_btn.click()

                password_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="password"]')))
                password_input.clear()
                actions.move_to_element(password_input).click().send_keys("Skydo0526?").perform()

                time.sleep(0.5)
                signin_btn = driver.find_element(By.XPATH, '//button[contains(@class, "index_loginButton__") and text()="SIGN IN"]')
                driver.execute_script("arguments[0].click();", signin_btn)

                time.sleep(200)
               
            except Exception as e:
                print(f"❌ 登录失败: {e}")
                time.sleep(40)
                break

        time.sleep(REFRESH_INTERVAL)
        count += 1

finally:
    driver.quit()
