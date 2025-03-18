import subprocess
import sys
import os
from logger_config import setup_logger

# Set up logger / 设置日志记录器
logger = setup_logger()

def run_full_process_test():
    """Run single full process test / 运行单次全流程测试"""
    logger.info("Starting full process test / 开始执行全流程测试")
    try:
        result = subprocess.run([
            "pytest",
            "test_orangehrm.py",
            "-v",
            "--html=report.html",
            "--self-contained-html"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("Full process test completed successfully / 全流程测试执行成功")
        else:
            logger.error(f"Full process test failed: {result.stderr} / 全流程测试失败: {result.stderr}")
            
    except Exception as e:
        logger.error(f"Error running full process test: {str(e)} / 运行全流程测试时发生错误: {str(e)}")

def run_stress_test(iterations):
    """Run stress test with specified iterations / 运行指定次数的压力测试"""
    logger.info(f"Starting stress test with {iterations} iterations / 开始执行{iterations}次压力测试")
    try:
        # Set environment variable for iterations / 设置迭代次数的环境变量
        env = os.environ.copy()
        env['STRESS_TEST_ITERATIONS'] = str(iterations)
        
        result = subprocess.run([
            "pytest",
            "stress_test_orangehrm.py",
            "-v",
            "--html=stress_report.html",
            "--self-contained-html",
            "-n", "auto"
        ], capture_output=True, text=True, env=env)
        
        if result.returncode == 0:
            logger.info("Stress test completed failed / 压力测试执行失败")
        else:
            logger.error(f"Stress test completed successfully: {result.stderr} / 压力测试成功: {result.stderr}")
            
    except Exception as e:
        logger.error(f"Error running stress test: {str(e)} / 运行压力测试时发生错误: {str(e)}")

def get_user_choice():
    """Get user's choice for test mode / 获取用户选择的测试模式"""
    while True:
        print("\n=== OrangeHRM Test Suite / OrangeHRM测试套件 ===")
        print("1. Run Full Process Test / 运行全流程测试")
        print("2. Run Stress Test / 运行压力测试")
        print("3. Exit / 退出")
        
        choice = input("\nPlease select an option (1-3) / 请选择选项 (1-3): ")
        
        if choice == "1":
            return "full"
        elif choice == "2":
            while True:
                try:
                    iterations = int(input("\nEnter number of iterations (1-100) / 输入测试次数 (1-100): "))
                    if 1 <= iterations <= 100:
                        return ("stress", iterations)
                    else:
                        print("Please enter a number between 1 and 100 / 请输入1到100之间的数字")
                except ValueError:
                    print("Please enter a valid number / 请输入有效的数字")
        elif choice == "3":
            return "exit"
        else:
            print("Invalid option. Please try again. / 无效选项，请重试。")

def main():
    """Main function / 主函数"""
    try:
        while True:
            choice = get_user_choice()
            
            if choice == "exit":
                print("\nExiting test suite / 退出测试套件")
                break
            elif choice == "full":
                run_full_process_test()
            elif isinstance(choice, tuple) and choice[0] == "stress":
                run_stress_test(choice[1])
                
            input("\nPress Enter to continue / 按Enter继续...")
            
    except KeyboardInterrupt:
        print("\nTest suite interrupted by user / 测试套件被用户中断")
        logger.info("Test suite interrupted by user / 测试套件被用户中断")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)} / 发生错误: {str(e)}")
        logger.error(f"Error in main function: {str(e)} / 主函数中发生错误: {str(e)}")

if __name__ == "__main__":
    main() 