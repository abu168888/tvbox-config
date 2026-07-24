@echo off
chcp 65001 >nul
cls
echo ============================================
echo   阿不 TVBox - Vercel 一键自动部署
echo ============================================
echo.
echo 🎯 目标：全自动部署到 Vercel 并获得公网地址
echo ⏱️ 预计耗时：2-3 分钟
echo.
pause

:: 步骤 1: 检查并安装 Node.js
echo [1/5] 检查 Node.js...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js 未安装，正在尝试下载...
    start https://nodejs.org/
    echo.
    echo 💡 请在浏览器中下载安装后重新运行此脚本
    pause
    exit /b 1
) else (
    echo ✅ Node.js 已安装
    for /f "tokens=*" %%i in ('node --version') do echo    版本：%%i
)

:: 步骤 2: 安装 Vercel CLI
echo.
echo [2/5] 安装 Vercel CLI...
npm install -g vercel
if %errorlevel% neq 0 (
    echo ❌ Vercel CLI 安装失败
    pause
    exit /b 1
)
echo ✅ Vercel CLI 安装完成

:: 步骤 3: 检查是否已登录
echo.
echo [3/5] 检查 Vercel 登录状态...
vercel whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ 未检测到 Vercel 登录信息
    echo.
    echo ============================================
    echo   ⚠️ 重要提示（仅需一次）
    echo ============================================
    echo.
    echo 接下来会自动打开浏览器，请用 GitHub 账号登录 Vercel
    echo 这是第三方平台的强制安全策略，无法跳过
    echo.
    echo 登录后系统会自动完成后续所有步骤
    echo.
    pause
    
    :: 尝试自动登录
    vercel login
    if %errorlevel% neq 0 (
        echo ❌ 登录失败，请手动执行：vercel login
        pause
        exit /b 1
    )
    echo ✅ 登录成功
) else (
    echo ✅ 已登录 Vercel
)

:: 步骤 4: 执行部署
echo.
echo [4/5] 部署到 Vercel 生产环境...
echo    请稍候，这可能需要 1-2 分钟...
echo.

vercel --prod --confirm

if %errorlevel% neq 0 (
    echo.
    echo ============================================
    echo   ❌ 部署失败
    echo ============================================
    echo.
    echo 可能原因:
    echo   1. 网络连接问题
    echo   2. Vercel 服务暂时不可用
    echo.
    echo 建议稍后重试
    echo.
    pause
    exit /b 1
)

:: 步骤 5: 提取并显示 URL
echo.
echo [5/5] 获取你的公网配置地址...
echo.

:: 等待一下确保部署完成
timeout /t 3 /nobreak >nul

echo ============================================
echo   ✅ 部署成功！恭喜！
echo ============================================
echo.
echo 🎉 你的专属 TVBox 公网配置地址是:
echo.
echo    https://tvbox-abu.vercel.app/config.json
echo    (实际域名以上方终端输出为准)
echo.
echo 📱 在电视盒子 TVBox 中:
echo    1. 设置 → 配置地址
echo    2. 输入上面的完整 URL
echo    3. 确定 → 刷新资源列表
echo.
echo ============================================
echo   🎬 立即开始观影吧！
echo ============================================
echo.
pause
