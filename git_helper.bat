@echo off
REM Git Helper Batch Script for Windows
REM Makes common Git operations easier for ML projects

echo 🤖 ML Git Helper for Windows
echo ==============================

:menu
echo.
echo Choose an action:
echo 1. Check Git status
echo 2. Quick daily commit
echo 3. Push to GitHub
echo 4. Create new branch
echo 5. Setup repository
echo 6. View commit history
echo 7. Exit
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto status
if "%choice%"=="2" goto daily_commit
if "%choice%"=="3" goto push
if "%choice%"=="4" goto new_branch
if "%choice%"=="5" goto setup
if "%choice%"=="6" goto history
if "%choice%"=="7" goto exit
echo Invalid choice. Please try again.
goto menu

:status
echo.
echo 📋 Git Status:
git status
echo.
pause
goto menu

:daily_commit
echo.
echo 📝 Daily Commit
set /p message="Enter commit message: "
echo Staging all changes...
git add .
git commit -m "🔧 %message%"
echo.
echo ✅ Commit created!
set /p push_choice="Push to GitHub? (y/n): "
if /i "%push_choice%"=="y" (
    git push
    echo ✅ Pushed to GitHub!
)
echo.
pause
goto menu

:push
echo.
echo 🚀 Pushing to GitHub...
git push
echo ✅ Push complete!
echo.
pause
goto menu

:new_branch
echo.
echo 🌿 Create New Branch
set /p branch_name="Enter branch name: "
git checkout -b feature/%branch_name%
echo ✅ Created and switched to branch: feature/%branch_name%
echo.
pause
goto menu

:setup
echo.
echo 🚀 Repository Setup
echo.
echo Checking if Git is initialized...
if not exist .git (
    echo Initializing Git repository...
    git init
    git branch -M main
    echo ✅ Git initialized!
) else (
    echo ✅ Git already initialized!
)
echo.
set /p remote_url="Enter GitHub repository URL (or press Enter to skip): "
if not "%remote_url%"=="" (
    git remote add origin %remote_url%
    echo ✅ Remote repository added!
    set /p push_choice="Push to GitHub now? (y/n): "
    if /i "%push_choice%"=="y" (
        git push -u origin main
        echo ✅ Pushed to GitHub!
    )
)
echo.
pause
goto menu

:history
echo.
echo 📚 Recent Commit History:
git log --oneline -10
echo.
pause
goto menu

:exit
echo.
echo 👋 Happy coding! Keep building your ML skills!
echo.
pause
exit
