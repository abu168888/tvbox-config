@echo off
chcp 65001 >nul
cd /d %~dp0
cls

echo ============================================
echo   阿不 TVBox - 全自动部署脚本 (V2)
echo ============================================
echo.
echo [1/4] 检查 Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js 未安装或无法运行
    pause
    exit /b 1
)
echo ✅ Node.js 已就绪

echo.
echo [2/4] 安装 Vercel CLI...
call npm install -g vercel@latest
if %errorlevel% neq 0 (
    echo ⚠️ 全局安装失败，尝试使用 npx...
)

echo.
echo [3/4] 登录 Vercel...
call npx --yes vercel whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ 未检测到 Vercel 登录，正在尝试登录...
    echo.
    echo ============================================
    echo   ⚠️ 重要提示
    echo ============================================
    echo.
    echo 接下来会自动打开浏览器
    echo 请用 GitHub/GitLab/Bitbucket 账号登录授权
    echo.
    echo 这是第三方平台的安全要求，无法跳过
    echo.
    pause
    
    call npx --yes vercel login
) else (
    echo ✅ 已登录 Vercel
)

echo.
echo [4/4] 部署到生产环境...
echo.
echo 📡 正在部署，请稍候 (约 1-2 分钟)...
echo.

call npx --yes vercel --prod --confirm

if %errorlevel% equ 0 (
    echo.
    echo ============================================
    echo   ✅ 部署成功!
    echo ============================================
    echo.
    echo 🎉 你的专属 TVBox 配置地址是:
    echo    (请查看上方终端输出中的 Production URL)
    echo.
) else (
    echo.
    echo ============================================
    echo   ❌ 部署失败
    echo ============================================
)

echo.
pause
