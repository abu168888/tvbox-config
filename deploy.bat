@echo off
chcp 65001 >nul
title TVBox GitHub Pages 部署

echo ============================================================
echo    TVBox 配置 - GitHub Pages 部署
echo ============================================================
echo.

REM 检查 Git
where git >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到 Git，请先安装: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ✅ Git 已安装
echo.

REM 初始化仓库
cd /d "%~dp0"
git init >nul 2>&1
git add .
git commit -m "Initial TVBox config" >nul 2>&1

echo 📦 正在推送到 GitHub...
git branch -M main >nul 2>&1
git remote add origin https://github.com/abu168888/tvbox-config.git 2>nul || echo "Remote already exists"
git push -f origin main >nul 2>&1

if errorlevel 1 (
    echo ⚠️ 推送失败，可能需要先登录 GitHub
    echo.
    echo 请访问：https://github.com/settings/tokens
    echo 创建 Personal Access Token，然后运行:
    echo git remote set-url origin https://your-token@github.com/abu168888/tvbox-config.git
    pause
    exit /b 1
)

echo ✅ 推送成功！
echo.
echo ============================================================
echo    🎉 部署完成！
echo ============================================================
echo.
echo 📺 电视盒子配置地址:
echo   http://abu168888.github.io/tvbox-config/tvbox.json
echo.
echo 🚀 CDN 加速地址:
echo   https://cdn.jsdelivr.net/gh/abu168888/tvbox-config@main/tvbox.json
echo.
echo 🔧 开启 GitHub Pages:
echo   访问：https://github.com/abu168888/tvbox-config/settings/pages
echo   选择分支：main → 文件夹：/ (root) → Save
echo.
echo ⏰ 自动更新（可选）:
echo   如需每日凌晨 2 点自动监控并推送，请查看 monitor.py 文档
echo.
echo ============================================================

pause
