# OrangeHRM Automated Testing Documentation V2.3.1
# OrangeHRM 自动化测试文档 V2.3.1

## English Documentation

### Overview
This project implements automated testing for the OrangeHRM demo site using Selenium WebDriver with Python. The test suite includes login functionality, employee management, and leave application features.

### Version History
#### V2.3 (Current Version / 当前版本)
- Bug fixes and other improvement

#### V2.2
- Bug fixes and other improvement

#### V2.1
- Bug fixes and other improvement

#### V2.0
- Added stress testing
- Bug fixes and other improvement

#### V1.1
- **Bug Fixes / 错误修复**
  - Fixed login verification issues / 修复登录验证问题
  - Resolved element location problems / 解决元素定位问题
  - Fixed leave application navigation / 修复请假申请导航问题
  - Corrected employee ID handling / 修正员工ID处理

- **Improvements / 改进**
  - Enhanced logging system with bilingual support / 增强日志系统，支持双语
  - Improved element waiting strategies / 改进元素等待策略
  - Added more detailed error messages / 添加更详细的错误信息
  - Optimized test execution stability / 优化测试执行稳定性
  - Updated documentation with bilingual support / 更新文档，支持双语

- **Technical Updates / 技术更新**
  - Switched from Chrome to Edge browser / 从Chrome浏览器切换到Edge浏览器
  - Updated element location methods / 更新元素定位方法
  - Enhanced error handling mechanisms / 增强错误处理机制
  - Improved test environment setup / 改进测试环境设置

### Features (V1.1)
1. **Login Test**
   - Automated login with valid credentials
   - Verification of successful login
   - Error handling for failed login attempts

2. **Employee Management Test**
   - Navigation to PIM module
   - Adding new employee with:
     - Full name (First, Middle, Last)
     - Employee ID
     - Profile picture upload
   - Verification of successful employee creation

3. **Leave Management Test**
   - Navigation to Leave module
   - Clicking the leave application button
   - Verify that the leave management page is displayed

### Requirements
- Python 3.x
- Edge Browser
- Required Python packages:
  pytest
  selenium
  webdriver_manager
  allure-pytest

### Installation
1. Clone the repository
2. Install required packages:

   pip install -r requirements.txt

### Running Tests
Open cmd in the root directory to execute the test:
   python run_tests.py

### Project Structure
- `test_orangehrm.py`: Main test script
- `logger_config.py`: Logging configuration
- `Image/`: Directory for test images
- `requirements.txt`: Package dependencies

### Test Coverage
Current test script includes the following functional tests:

1. **Login Function Test**
   - Login with valid credentials
   - Verify successful login

2. **Employee Management Test**
   - Add new employee
   - Verify employee information saving

3. **Leave Management Test**
   - Navigate to leave page
   - Click leave application button
   - Verify successful navigation

### Test Reports and Logs
After test execution, you can find test reports and logs in the following locations:

- HTML Report: `report.html`
- Allure Report: `./allure-results/`
- Test Logs: `./Logs/test_execution_YYYY-MM-DD-HH-MM-SS.log`

Log files contain the following information:
- Test start and end times
- Execution status of each test step
- Test environment setup and cleanup information
- Important events during test execution

### Notes
1. Ensure stable network connection in test environment
2. Make sure Edge browser is installed before testing
3. Test data will be reset after each test execution
4. Recommended to run in test environment to avoid affecting production
5. Log files are automatically saved in the `Logs` directory
6. If you encounter pytest-html related errors, ensure all dependencies are properly installed

### Maintenance Guide
1. **Test Case Updates**
   - Add new test methods in `test_orangehrm.py`
   - Use `@allure.feature` and `@allure.story` decorators for test descriptions
   - Add logging for key steps

2. **Test Plan Updates**
   - Update corresponding content in `test_plan.md`
   - Ensure test plan aligns with test scripts

### Troubleshooting
If you encounter issues, please check:

1. Environment configuration is correct
2. All dependencies are properly installed
3. Network connection is stable
4. Edge browser version is compatible
5. Check error messages in log files
6. Ensure pytest-html package is installed

---

## 中文文档

### 概述
本项目使用 Python 的 Selenium WebDriver 实现了 OrangeHRM 演示站点的自动化测试。测试套件包括登录功能、员工管理和请假申请等功能。

### 版本历史
#### V2.3
 - Bug修复和其他改进

#### V2.2
 - Bug修复和其他改进

#### V2.1
 - Bug修复和其他改进

#### V2.0（当前版本）
 - 增加了压力测试
 - Bug修复和其他改进

#### V1.1
- **错误修复**
  - 修复登录验证问题
  - 解决元素定位问题
  - 修复请假申请导航问题
  - 修正员工ID处理

- **功能改进**
  - 增强日志系统，支持双语
  - 改进元素等待策略
  - 添加更详细的错误信息
  - 优化测试执行稳定性
  - 更新文档，支持双语

- **技术更新**
  - 从Chrome浏览器切换到Edge浏览器
  - 更新元素定位方法
  - 增强错误处理机制
  - 改进测试环境设置

### 功能特性 (V1.1)
1. **登录测试**
   - 使用有效凭据自动登录
   - 登录成功验证
   - 登录失败错误处理

2. **员工管理测试**
   - PIM 模块导航
   - 新增员工功能：
     - 完整姓名（名、中间名、姓）
     - 员工 ID
     - 头像上传
   - 员工创建成功验证

3. **请假管理测试**
   - 请假模块导航
   - 点击请假申请按钮
   - 验证成功进入请假管理界面

### 环境要求
- Python 3.x
- Edge 浏览器
- 所需 Python 包：
  pytest
  selenium
  webdriver_manager
  allure-pytest

### 安装步骤
1. 克隆代码仓库
2. 安装所需包：
   pip install -r requirements.txt

### 运行测试
在根目录下打开cmd执行测试：
python run_tests.py

### 项目结构
- `test_orangehrm.py`: 主测试脚本
- `logger_config.py`: 日志配置
- `Image/`: 测试图片目录
- `requirements.txt`: 包依赖文件

### 测试覆盖范围
当前测试脚本包含以下功能测试：

1. **登录功能测试**
   - 使用有效凭据登录
   - 验证登录成功

2. **员工管理功能测试**
   - 添加新员工
   - 验证员工信息保存

3. **请假管理功能测试**
   - 导航到请假页面
   - 点击请假申请按钮
   - 验证成功进入请假界面

### 注意事项
1. 确保测试环境网络稳定
2. 测试前确保 Edge 浏览器已安装
3. 测试数据会在每次测试执行时重置
4. 建议在测试环境中运行，避免影响生产环境
5. 日志文件会自动保存在 `Logs` 目录下
6. 如果遇到 pytest-html 相关错误，请确保已正确安装所有依赖包

### 维护说明
1. **测试用例更新**
   - 在 `test_orangehrm.py` 中添加新的测试方法
   - 使用 `@allure.feature` 和 `@allure.story` 装饰器添加测试描述
   - 在关键步骤添加日志记录

2. **测试计划更新**
   - 在 `test_plan.md` 中更新相应的测试计划内容
   - 确保测试计划与测试脚本保持一致

### 问题排查
如遇到问题，请检查：

1. 环境配置是否正确
2. 依赖是否完整安装
3. 网络连接是否正常
4. Edge 浏览器版本是否兼容
5. 查看日志文件中的错误信息
6. 确保已安装 pytest-html 包

## 项目结构
.
├── test_plan.md          # IEEE 829 测试计划文档
├── test_orangehrm.py     # 自动化测试脚本
├── logger_config.py      # 日志配置文件
├── requirements.txt      # 项目依赖
├── Logs/                 # 测试日志目录
└── README.md            # 项目说明文档

## 环境要求

- Python 3.8+
- Edge 浏览器
- pip（Python 包管理器）

## 安装步骤

1. 克隆项目到本地
2. 创建并激活虚拟环境（推荐）：
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
3. 安装依赖：
   pip install -r requirements.txt
   
   如果安装过程中遇到问题，可以尝试单独安装以下包：
   pip install selenium==4.18.1
   pip install webdriver-manager==4.0.1
   pip install pytest==8.0.2
   pip install pytest-html==4.1.1
   pip install pytest-xdist==3.5.0
   pip install allure-pytest==2.13.2


## 运行测试

1. 运行所有测试（生成HTML报告）：
   pytest test_orangehrm.py -v --html=report.html

2. 运行特定测试：
   pytest test_orangehrm.py -v -k "test_login" --html=report.html

3. 生成 Allure 报告：
   pytest test_orangehrm.py --alluredir=./allure-results
   allure serve ./allure-results

4. 如果只想运行测试而不生成报告：
   pytest test_orangehrm.py -v

## 测试覆盖范围

当前测试脚本包含以下功能测试：

1. 登录功能测试
   - 使用有效凭据登录
   - 验证登录成功

2. 员工管理功能测试
   - 添加新员工
   - 验证员工信息保存

3. 请假管理功能测试
   - 申请请假
   - 验证请假申请提交

## 测试报告和日志

测试执行完成后，可以在以下位置找到测试报告和日志：

- HTML 报告：`report.html`
- Allure 报告：`./allure-results/`
- 测试日志：`./Logs/test_execution_YYYY-MM-DD-HH-MM-SS.log`

日志文件包含以下信息：
- 测试开始和结束时间
- 每个测试步骤的执行状态
- 测试环境设置和清理信息
- 测试执行过程中的重要事件

## 注意事项

1. 确保测试环境网络稳定
2. 测试前确保 Chrome 浏览器已安装
3. 测试数据会在每次测试执行时重置
4. 建议在测试环境中运行，避免影响生产环境
5. 日志文件会自动保存在 `Logs` 目录下，每次运行测试都会创建新的日志文件
6. 如果遇到 pytest-html 相关错误，请确保已正确安装所有依赖包

## 维护说明

1. 测试用例更新
   - 在 `test_orangehrm.py` 中添加新的测试方法
   - 使用 `@allure.feature` 和 `@allure.story` 装饰器添加测试描述
   - 在关键步骤添加日志记录

2. 测试计划更新
   - 在 `test_plan.md` 中更新相应的测试计划内容
   - 确保测试计划与测试脚本保持一致

## 问题反馈

如遇到问题，请检查：

1. 环境配置是否正确
2. 依赖是否完整安装
3. 网络连接是否正常
4. Chrome 浏览器版本是否兼容
5. 查看日志文件中的错误信息
6. 确保已安装 pytest-html 包 
