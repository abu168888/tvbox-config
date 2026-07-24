@echo off
chcp 65001 >nul
cls
echo ============================================
echo   阿不 TVBox - 自动维护任务设置
echo ============================================
echo.
echo 🕐 此脚本将创建 Windows 定时任务:
echo    任务名称：TVBox-Auto-Maintain-Abu
echo    触发时间：每天凌晨 3:00
echo    执行内容：自动检测失效源并修复
echo.
echo ⚠️ 需要管理员权限
echo.

:: 获取当前目录
set SCRIPT_DIR=%~dp0
set PYTHON_PATH=C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe

:: 检查 Python 是否存在
if not exist "%PYTHON_PATH%" (
    echo ❌ 未找到 Python 3.12
    echo.
    echo 请修改此脚本中的 PYTHON_PATH 变量为你的实际路径
    pause
    exit /b 1
)

:: 尝试以管理员权限运行
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ 检测到需要管理员权限
    echo    正在请求提权...
    powershell -Command "Start-Process cmd.exe -ArgumentList '/c', '%~f0' -Verb RunAs"
    exit /b
)

:: 删除旧任务（如果存在）
schtasks /delete /tn "TVBox-Auto-Maintain-Abu" /f >nul 2>&1

:: 创建新任务
echo 🔧 正在创建定时任务...
schtasks /create /tn "TVBox-Auto-Maintain-Abu" /tr "\"%PYTHON_PATH%" \"%SCRIPT_DIR%monitor.py\"" /sc daily /st 03:00 /ru SYSTEM /f

if %errorlevel% equ 0 (
    echo.
    echo ============================================
    echo   ✅ 定时任务创建成功!
    echo ============================================
    echo.
    echo 📅 下次执行时间：明天凌晨 3:00
    echo.
    echo 📊 查看任务状态命令:
    echo    schtasks /query /tn "TVBox-Auto-Maintain-Abu"
    echo.
    echo 🛑 如需删除任务:
    echo    schtasks /delete /tn "TVBox-Auto-Maintain-Abu" /f
    echo.
    echo 💡 测试立即运行:
    echo    python monitor.py
    echo.
) else (
    echo.
    echo ============================================
    echo   ❌ 创建失败
    echo ============================================
    echo.
    echo 可能原因:
    echo   1. 未以管理员身份运行
    echo   2. Python 路径错误
    echo   3. 系统策略限制
    echo.
)

pause
