import pytest
import time
import psutil
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import allure
from logger_config import setup_logger
import concurrent.futures
import statistics
import sys

# Set up logger / 设置日志记录器
logger = setup_logger()

# Default number of iterations / 默认迭代次数
DEFAULT_ITERATIONS = 10

def get_iterations():
    """Get number of iterations from environment variable / 从环境变量获取迭代次数"""
    try:
        iterations = int(os.environ.get('STRESS_TEST_ITERATIONS', DEFAULT_ITERATIONS))
        return max(1, min(100, iterations))  # Ensure value is between 1 and 100
    except (ValueError, TypeError):
        return DEFAULT_ITERATIONS

class PerformanceMetrics:
    """Performance metrics collection class / 性能指标收集类"""
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.cpu_usage = []
        self.memory_usage = []
        self.response_times = []
        self.test_results = []

    def start_test(self):
        """Start collecting metrics / 开始收集指标"""
        self.start_time = time.time()
        self.cpu_usage = []
        self.memory_usage = []
        self.response_times = []

    def record_metrics(self):
        """Record current system metrics / 记录当前系统指标"""
        self.cpu_usage.append(psutil.cpu_percent())
        self.memory_usage.append(psutil.virtual_memory().percent)

    def record_response_time(self, response_time):
        """Record response time / 记录响应时间"""
        self.response_times.append(response_time)

    def end_test(self, success):
        """End test and calculate metrics / 结束测试并计算指标"""
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        avg_cpu = statistics.mean(self.cpu_usage) if self.cpu_usage else 0
        avg_memory = statistics.mean(self.memory_usage) if self.memory_usage else 0
        avg_response = statistics.mean(self.response_times) if self.response_times else 0
        
        self.test_results.append({
            'duration': duration,
            'avg_cpu': avg_cpu,
            'avg_memory': avg_memory,
            'avg_response': avg_response,
            'success': success
        })

    def get_summary(self):
        """Get test summary / 获取测试摘要"""
        if not self.test_results:
            return "No tests executed / 没有执行测试"
        
        successful_tests = sum(1 for r in self.test_results if r['success'])
        total_tests = len(self.test_results)
        success_rate = (successful_tests / total_tests) * 100
        
        avg_duration = statistics.mean(r['duration'] for r in self.test_results)
        avg_cpu = statistics.mean(r['avg_cpu'] for r in self.test_results)
        avg_memory = statistics.mean(r['avg_memory'] for r in self.test_results)
        avg_response = statistics.mean(r['avg_response'] for r in self.test_results)
        
        return {
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'success_rate': success_rate,
            'avg_duration': avg_duration,
            'avg_cpu': avg_cpu,
            'avg_memory': avg_memory,
            'avg_response': avg_response
        }

@pytest.fixture(scope="class")
def metrics():
    """Performance metrics fixture / 性能指标fixture"""
    return PerformanceMetrics()

@pytest.fixture(scope="function")
def driver():
    """Set up test environment / 设置测试环境"""
    logger.info("Starting test environment setup / 开始设置测试环境")
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
        
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
        driver.implicitly_wait(30)
        
        logger.info("Test environment setup completed / 测试环境设置完成")
        yield driver
        
    except Exception as e:
        logger.error(f"Test environment setup failed: {str(e)} / 测试环境设置失败: {str(e)}")
        raise
    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                logger.error(f"Error closing browser: {str(e)} / 关闭浏览器时发生错误: {str(e)}")

def wait_for_element(driver, by, value, timeout=30):
    """Wait for element to be present / 等待元素出现"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        logger.error(f"Timeout waiting for element: {value} / 等待元素超时: {value}")
        raise

def wait_for_element_clickable(driver, by, value, timeout=30):
    """Wait for element to be clickable / 等待元素可点击"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        return element
    except TimeoutException:
        logger.error(f"Timeout waiting for clickable element: {value} / 等待可点击元素超时: {value}")
        raise

def login(driver, metrics):
    """Login function with performance monitoring / 带性能监控的登录函数"""
    start_time = time.time()
    try:
        driver.get("https://opensource-demo.orangehrmlive.com/")
        metrics.record_metrics()
        
        username_field = wait_for_element(driver, By.CSS_SELECTOR, "input[name='username']")
        password_field = wait_for_element(driver, By.CSS_SELECTOR, "input[name='password']")
        
        username_field.send_keys("Admin")
        password_field.send_keys("admin123")
        
        login_button = wait_for_element_clickable(driver, By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Wait for successful login / 等待登录成功
        try:
            wait_for_element(driver, By.CSS_SELECTOR, "h6.oxd-text")
            logger.info("Login successful / 登录成功")
            end_time = time.time()
            metrics.record_response_time(end_time - start_time)
            return True
        except TimeoutException:
            error_msg = "Login verification failed - timeout waiting for dashboard / 登录验证失败 - 等待仪表板超时"
            logger.error(error_msg)
            return False
        
    except Exception as e:
        error_msg = f"Login failed: {str(e)} / 登录失败: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False

def add_employee(driver, metrics, iteration):
    """Add employee function with performance monitoring / 带性能监控的添加员工函数"""
    start_time = time.time()
    try:
        # Navigate to PIM module / 导航到PIM模块
        pim_menu = wait_for_element_clickable(driver, By.XPATH, "//span[text()='PIM']")
        time.sleep(1)  # Add delay before clicking PIM menu
        pim_menu.click()
        time.sleep(2)  # Add delay after clicking PIM menu
        
        # Click Add Employee / 点击添加员工
        add_employee_button = wait_for_element_clickable(driver, By.XPATH, "/html/body/div/div[1]/div[2]/div[2]/div/div[2]/div[1]/button")
        time.sleep(1)  # Add delay before clicking Add button
        add_employee_button.click()
        time.sleep(2)  # Add delay after clicking Add button
        
        # Fill in employee details / 填写员工信息
        first_name = wait_for_element(driver, By.NAME, "firstName")
        middle_name = wait_for_element(driver, By.NAME, "middleName")
        last_name = wait_for_element(driver, By.NAME, "lastName")
        
        # Set name with iteration number / 设置带迭代次数的名字
        iteration_str = str(iteration).zfill(3)  # Convert iteration to 3-digit string
        name = f"Castorice{iteration_str}"
        first_name.send_keys(name)
        time.sleep(0.5)  # Add delay between input fields
        middle_name.send_keys(name)
        time.sleep(0.5)  # Add delay between input fields
        last_name.send_keys(name)
        time.sleep(0.5)  # Add delay between input fields
        
        # Upload image / 上传头像
        image_input = wait_for_element(driver, By.CSS_SELECTOR, "input[type='file']")
        image_path = os.path.join(os.path.dirname(__file__), "image", "1.jpg")
        image_input.send_keys(image_path)
        time.sleep(1)  # Add delay after uploading image
        
        # Set Employee ID with iteration / 设置带迭代次数的员工ID
        employee_id_xpath = "/html/body/div/div[1]/div[2]/div[2]/div/div/form/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/input"
        employee_id = wait_for_element(driver, By.XPATH, employee_id_xpath)
        employee_id.clear()
        time.sleep(0.5)  # Add delay after clearing
        employee_id.send_keys(f"418{iteration_str}")
        time.sleep(1)  # Add delay after filling all fields
        
        # Save employee / 保存员工信息
        save_button = wait_for_element_clickable(driver, By.XPATH, "//button[@type='submit']")
        time.sleep(1)  # Add delay before clicking Save button
        save_button.click()
        time.sleep(2)  # Add delay after clicking Save button
        
        # Wait for success message and continue / 等待成功消息并继续
        success_message = wait_for_element(driver, By.XPATH, "//p[contains(@class, 'oxd-text--toast-message')]")
        if success_message:
            logger.info(f"Employee Castorice{iteration_str} added successfully / 员工 Castorice{iteration_str} 添加成功")
            end_time = time.time()
            metrics.record_response_time(end_time - start_time)
            return True
        
        return False
        
    except Exception as e:
        logger.error(f"Add employee failed: {str(e)} / 添加员工失败: {str(e)}")
        return False

def test_full_process_stress(driver, metrics):
    """Stress test for full process / 全流程压力测试"""
    iterations = get_iterations()
    logger.info(f"Starting full process stress test with {iterations} iterations / 开始执行{iterations}次全流程压力测试")
    
    try:
        # Login once at the beginning / 开始时登录一次
        if not login(driver, metrics):
            error_msg = "Initial login failed / 初始登录失败"
            logger.error(error_msg)
            return  # Keep browser open on failure
        
        # Add a small delay after login / 登录后添加短暂延迟
        time.sleep(2)
        
        for i in range(iterations):
            logger.info(f"Starting iteration {i + 1}/{iterations} / 开始第 {i + 1}/{iterations} 次迭代")
            metrics.start_test()
            
            try:
                # Navigate to PIM module / 导航到PIM模块
                pim_menu = wait_for_element_clickable(driver, By.XPATH, "//span[text()='PIM']")
                time.sleep(1)  # Add delay before clicking PIM menu
                pim_menu.click()
                time.sleep(2)  # Add delay after clicking PIM menu
                
                # Add employee / 添加员工
                if not add_employee(driver, metrics, i):
                    error_msg = f"Add employee failed in iteration {i + 1} / 第 {i + 1} 次迭代添加员工失败"
                    logger.error(error_msg)
                    return  # Keep browser open on failure
                
                # Return to dashboard / 返回仪表板
                dashboard_menu = wait_for_element_clickable(driver, By.XPATH, "//span[text()='Dashboard']")
                time.sleep(1)  # Add delay before clicking Dashboard menu
                dashboard_menu.click()
                time.sleep(2)  # Add delay after clicking Dashboard menu
                
                metrics.end_test(True)
                logger.info(f"Completed iteration {i + 1}/{iterations} / 完成第 {i + 1}/{iterations} 次迭代")
                
            except Exception as e:
                error_msg = f"Error in iteration {i + 1}: {str(e)} / 第 {i + 1} 次迭代发生错误: {str(e)}"
                logger.error(error_msg, exc_info=True)
                metrics.end_test(False)
                return  # Keep browser open on failure
            
            # Add a delay between iterations / 在迭代之间添加延迟
            if i < iterations - 1:
                time.sleep(3)
        
        # Log final success message / 记录最终成功消息
        logger.info(f"Successfully completed all {iterations} iterations / 成功完成所有 {iterations} 次迭代")
        driver.quit()  # Close browser on success
                
    except Exception as e:
        error_msg = f"Test process failed: {str(e)} / 测试过程失败: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return  # Keep browser open on failure

def test_performance_summary(metrics):
    """Generate performance test summary / 生成性能测试摘要"""
    summary = metrics.get_summary()
    
    logger.info("Performance Test Summary / 性能测试摘要:")
    logger.info(f"Total Tests: {summary['total_tests']} / 总测试次数: {summary['total_tests']}")
    logger.info(f"Success Rate: {summary['success_rate']:.2f}% / 成功率: {summary['success_rate']:.2f}%")
    logger.info(f"Average Duration: {summary['avg_duration']:.2f}s / 平均持续时间: {summary['avg_duration']:.2f}秒")
    logger.info(f"Average CPU Usage: {summary['avg_cpu']:.2f}% / 平均CPU使用率: {summary['avg_cpu']:.2f}%")
    logger.info(f"Average Memory Usage: {summary['avg_memory']:.2f}% / 平均内存使用率: {summary['avg_memory']:.2f}%")
    logger.info(f"Average Response Time: {summary['avg_response']:.2f}s / 平均响应时间: {summary['avg_response']:.2f}秒")
    
    # Add performance metrics to Allure report / 将性能指标添加到Allure报告
    allure.attach(
        f"""
        Performance Test Results / 性能测试结果:
        Total Tests: {summary['total_tests']}
        Success Rate: {summary['success_rate']:.2f}%
        Average Duration: {summary['avg_duration']:.2f}s
        Average CPU Usage: {summary['avg_cpu']:.2f}%
        Average Memory Usage: {summary['avg_memory']:.2f}%
        Average Response Time: {summary['avg_response']:.2f}s
        """,
        name="Performance Summary / 性能摘要",
        attachment_type=allure.attachment_type.TEXT
    )

if __name__ == "__main__":
    logger.info("Starting stress test suite / 开始执行压力测试套件")
    iterations = get_iterations()
    pytest.main(["-v", "--html=stress_report.html", "--self-contained-html", "-n", "auto"])
    logger.info("Stress test suite completed / 压力测试套件执行完成") 