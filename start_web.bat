@echo off
REM JoyClaw Web 启动脚本 (Windows)

echo ============================================================
echo   JoyClaw Web 服务启动
echo ============================================================
echo.

REM 检查 Python 3
python3 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 python3
    pause
    exit /b 1
)

echo 启动 Web 服务...
echo 访问地址: http://localhost:5000
echo.
echo 按 Ctrl+C 停止服务
echo ============================================================
echo.

cd web
python3 app.py

pause
