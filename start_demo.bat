@echo off
REM JoyClaw 快速启动脚本 (Windows)
REM 使用方式：双击运行或在命令行执行 start_demo.bat

echo ============================================================
echo   JoyClaw AI Agent 快速启动
echo ============================================================
echo.

REM 检查 Python 3
python3 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 python3，请确保已安装 Python 3.8+
    pause
    exit /b 1
)

echo [1] 简单工具演示（无需 API Key）
echo [2] 完整 AI Agent 演示
echo [3] 本地功能测试
echo.
set /p choice="请选择 (1-3): "

if "%choice%"=="1" (
    echo.
    echo 运行简单工具演示...
    python3 examples\simple_demo.py
) else if "%choice%"=="2" (
    echo.
    echo 运行完整 AI Agent 演示...
    python3 examples\demo.py 5
) else if "%choice%"=="3" (
    echo.
    echo 运行本地功能测试...
    python3 test_local_features.py
) else (
    echo [错误] 无效选项
    pause
    exit /b 1
)

echo.
echo ============================================================
echo 演示完成！
echo ============================================================
pause
