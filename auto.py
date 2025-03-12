import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def fill_google_form(num_iterations=5):
    """
    Tự động điền Google Form ngẫu nhiên và gửi nhiều lần
    :param num_iterations: Số lần lặp lại gửi form
    """
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdF5tNxvCbjdqeOwfdp33ftBJmaTK0VN2ACH9ulKuCiDz0eig/viewform"
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)  # Giữ trình duyệt mở
    
    for i in range(num_iterations):
        try:
            print(f"Lần gửi form thứ {i+1}...")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            wait = WebDriverWait(driver, 10)
            driver.get(form_url)
            time.sleep(2)  # Chờ trang tải
            
            def select_random_option(xpath, label):
                """ Chọn một đáp án ngẫu nhiên trong nhóm câu hỏi """
                try:
                    print(f"Đang điền: {label}")
                    options = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
                    valid_options = [opt for opt in options if opt.is_displayed() and "Mục khác" not in opt.text]
                    if valid_options:
                        choice = random.choice(valid_options)  # Chọn ngẫu nhiên một đáp án
                        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", choice)
                        time.sleep(0.5)
                        wait.until(EC.element_to_be_clickable(choice)).click()
                        time.sleep(1)
                except Exception as e:
                    print(f"Không thể chọn {label}: {e}")
            
            # Danh sách câu hỏi
            questions = [
                ("//div[@role='radio'][not(contains(text(),'Mục khác'))]", "Câu hỏi trắc nghiệm")
            ]
            
            for xpath, label in questions:
                select_random_option(xpath, label)
                time.sleep(1)
                driver.execute_script("window.scrollBy(0, 200);")  # Cuộn từng bước
                time.sleep(1)
            
            # Cuộn xuống nút gửi form sau khi đã điền xong tất cả
            try:
                print("Đang cuộn xuống để gửi form...")
                submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Gửi')]")))
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", submit_button)
                time.sleep(1)
                submit_button.click()
                print("Đã gửi form thành công!")
            except Exception as e:
                print(f"Không thể gửi form: {e}")
            
            time.sleep(3)
            driver.quit()
        except Exception as e:
            print(f"Lỗi trong lần gửi thứ {i+1}: {e}")

# Chạy script
fill_google_form(num_iterations=10)
