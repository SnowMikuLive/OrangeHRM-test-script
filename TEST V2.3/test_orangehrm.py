import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import allure
import time
from logger_config import setup_logger
import os

# Set up logger / 设置日志记录器
logger = setup_logger()

@pytest.fixture(scope="class")
def driver():
    """Set up test environment / 设置测试环境"""
    logger.info("开始设置测试环境 / Starting test environment setup")
    driver = None
    try:
        edge_options = Options()
        edge_options.add_argument("--start-maximized")
        edge_options.add_argument("--disable-notifications")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--disable-extensions")
        edge_options.add_argument("--disable-popup-blocking")
        edge_options.add_argument("--remote-debugging-port=9222")
        
        logger.debug("Edge options configured / Edge选项配置完成")
        
        # Use webdriver_manager to automatically download matching EdgeDriver / 使用 webdriver_manager 自动下载匹配的 EdgeDriver
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
        driver.implicitly_wait(30)
        
        logger.info("Test environment setup completed / 测试环境设置完成")
        yield driver
        
    except Exception as e:
        logger.error(f"Test environment setup failed: {str(e)} / 测试环境设置失败: {str(e)}")
        raise
    finally:
        logger.info("Cleaning up test environment / 清理测试环境")
        if driver:
            try:
                driver.quit()
            except Exception as e:
                logger.error(f"Error closing browser: {str(e)} / 关闭浏览器时发生错误: {str(e)}")

@pytest.fixture(scope="class")
def logged_in_driver(driver):
    """Login to system and return logged-in driver / 登录系统并返回已登录的driver"""
    logger.info("Starting login process / 开始执行登录操作")
    try:
        logger.debug("Opening login page / 打开登录页面")
        driver.get("https://opensource-demo.orangehrmlive.com/")
        time.sleep(5)
        
        logger.debug("Waiting for login form to load / 等待登录表单加载")
        username_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        password_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        
        logger.debug("Clearing input fields / 清除输入框")
        username_field.clear()
        password_field.clear()
        
        logger.debug("Entering login credentials / 输入登录凭据")
        username_field.send_keys("Admin")
        password_field.send_keys("admin123")
        
        logger.debug("Clicking login button / 点击登录按钮")
        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        
        logger.debug("Waiting for login to complete / 等待登录完成")
        time.sleep(5)
        
        # Verify successful login / 验证登录成功
        try:
            dashboard = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h6.oxd-text"))
            )
            if "Dashboard" in dashboard.text:
                logger.info("Login successful / 登录成功")
                return driver
            else:
                logger.error("Login failed: Dashboard element not found / 登录失败：未找到Dashboard元素")
                raise Exception("Login failed / 登录失败")
        except TimeoutException:
            logger.error("Login failed: Timeout waiting for Dashboard / 登录失败：等待Dashboard超时")
            raise Exception("Login failed / 登录失败")
            
    except Exception as e:
        logger.error(f"Error during login process: {str(e)} / 登录过程发生错误: {str(e)}")
        raise

class TestOrangeHRM:
    def wait_for_element(self, driver, by, value, timeout=30):
        """Wait for element to be present / 等待元素出现"""
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"Timeout waiting for element: {value} / 等待元素超时: {value}")
            raise

    def wait_for_element_clickable(self, driver, by, value, timeout=30):
        """Wait for element to be clickable / 等待元素可点击"""
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"Timeout waiting for element to be clickable: {value} / 等待元素可点击超时: {value}")
            raise

    @allure.feature("Login Functionality / 登录功能")
    @allure.story("Login with Valid Credentials / 使用有效凭据登录")
    def test_login(self, logged_in_driver):
        """Test login with valid credentials / 测试使用有效凭据登录系统"""
        logger.info("Starting login test / 开始执行登录测试")
        assert logged_in_driver is not None, "Login test failed / 登录测试失败"

    @allure.feature("Employee Management / 员工管理")
    @allure.story("Add New Employee / 添加新员工")
    def test_add_employee(self, logged_in_driver):
        """Test adding new employee / 测试添加新员工功能"""
        logger.info("Starting add employee test / 开始执行添加员工测试")
        
        try:
            logger.debug("Navigating to PIM menu / 导航到PIM菜单")
            # Wait for page to load / 等待页面加载完成
            time.sleep(5)
            
            # Locate PIM menu with precise selector / 使用更精确的选择器定位PIM菜单
            pim_menu = self.wait_for_element_clickable(logged_in_driver, By.CSS_SELECTOR, "a[href='/web/index.php/pim/viewPimModule']")
            pim_menu.click()
            time.sleep(5)  # Wait for PIM page to load completely / 增加等待时间确保PIM页面完全加载
            
            logger.debug("Waiting for PIM page to load / 等待PIM页面完全加载")
            # Wait for employee list page URL to load / 等待员工列表页面URL加载完成
            WebDriverWait(logged_in_driver, 30).until(
                lambda driver: "viewEmployeeList" in driver.current_url
            )
            
            logger.debug("Clicking add employee button / 点击添加员工按钮")
            # Locate Add button with precise XPath / 使用精确的XPath定位Add按钮
            add_button_xpath = "/html/body/div/div[1]/div[2]/div[2]/div/div[2]/div[1]/button"
            add_button = WebDriverWait(logged_in_driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, add_button_xpath))
            )
            
            # Try direct click first / 尝试直接点击
            try:
                add_button.click()
            except ElementClickInterceptedException:
                # If direct click fails, use JavaScript click / 如果直接点击失败，使用JavaScript点击
                logged_in_driver.execute_script("arguments[0].click();", add_button)
            
            time.sleep(3)
            
            logger.debug("Filling employee information / 填写员工信息")
            first_name = self.wait_for_element(logged_in_driver, By.NAME, "firstName")
            first_name.send_keys("Castorice")
            
            middle_name = self.wait_for_element(logged_in_driver, By.NAME, "middleName")
            middle_name.send_keys("Castorice")
            
            last_name = self.wait_for_element(logged_in_driver, By.NAME, "lastName")
            last_name.send_keys("Castorice")
            
            # Locate Employee ID input with precise XPath / 使用精确的XPath定位Employee ID输入框
            employee_id_xpath = "/html/body/div/div[1]/div[2]/div[2]/div/div/form/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/input"
            employee_id = self.wait_for_element(logged_in_driver, By.XPATH, employee_id_xpath)
            employee_id.clear()
            employee_id.send_keys("418000")  # Set Employee ID / 设置员工ID
            
            logger.debug("Uploading employee photo / 上传员工头像")
            try:
                # Wait for avatar upload button and click / 等待头像上传按钮出现并点击
                avatar_button = self.wait_for_element_clickable(logged_in_driver, By.CSS_SELECTOR, "button.oxd-icon-button.employee-image-action")
                avatar_button.click()
                time.sleep(2)
                
                # Locate file upload input / 定位文件上传输入框
                avatar_input = self.wait_for_element(logged_in_driver, By.CSS_SELECTOR, "input[type='file']")
                # Use absolute path for image upload / 使用绝对路径上传图片
                image_path = os.path.abspath("Image/1.jpg")
                avatar_input.send_keys(image_path)
                time.sleep(3)
            except Exception as e:
                logger.error(f"Failed to upload avatar: {str(e)} / 上传头像失败: {str(e)}")
            
            logger.debug("Saving employee information / 保存员工信息")
            save_button = self.wait_for_element_clickable(logged_in_driver, By.CSS_SELECTOR, "button[type='submit']")
            save_button.click()
            time.sleep(5)
            
            # Verify successful navigation to employee details page / 验证是否成功跳转到员工详情页面
            try:
                WebDriverWait(logged_in_driver, 30).until(
                    lambda driver: "viewPersonalDetails/empNumber/" in driver.current_url
                )
                logger.info("Add employee test successful: Navigated to employee details page / 添加员工测试执行成功：已跳转到员工详情页面")
                return  # Return after successful employee addition / 成功添加员工后直接返回
            except TimeoutException:
                logger.error("Failed to navigate to employee details page / 未能跳转到员工详情页面")
                raise Exception("Add employee failed: Failed to navigate to employee details page / 添加员工失败：未能跳转到员工详情页面")
            
        except Exception as e:
            logger.error(f"Add employee test failed: {str(e)} / 添加员工测试失败: {str(e)}")
            raise

    @allure.feature("Leave Management / 请假管理")
    @allure.story("Enter Leave Interface / 进入请假界面")
    def test_apply_leave(self, logged_in_driver):
        """Test leave functionality / 测试请假功能"""
        logger.info("Starting leave test / 开始执行请假测试")
        
        try:
            logger.debug("Navigating to leave menu / 导航到请假菜单")
            leave_menu = self.wait_for_element_clickable(logged_in_driver, By.XPATH, "//span[text()='Leave']")
            leave_menu.click()
            time.sleep(5)  # Wait for leave page to load / 等待请假页面加载
            
            logger.debug("Clicking leave button / 点击请假按钮")
            # Locate leave button with precise XPath / 使用精确的XPath定位请假按钮
            leave_button_xpath = "/html/body/div/div[1]/div[2]/div[2]/div/div[1]/div[2]/form/div[3]/button[2]"
            leave_button = self.wait_for_element_clickable(logged_in_driver, By.XPATH, leave_button_xpath)
            leave_button.click()
            
            logger.info("Leave test completed successfully / 请假测试执行成功")
            
        except Exception as e:
            logger.error(f"Leave test failed: {str(e)} / 请假测试失败: {str(e)}")
            raise

if __name__ == "__main__":
    logger.info("Starting test suite / 开始执行测试套件")
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
    logger.info("Test suite completed / 测试套件执行完成") 