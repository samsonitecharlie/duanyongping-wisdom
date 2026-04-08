# 一键推送更新到GitHub Pages
# 使用方法：双击运行或在PowerShell中执行

Write-Host "=====================================" -ForegroundColor Green
Write-Host "  段永平智慧库 - 一键更新部署" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""

Set-Location "C:\Users\Charlie\Desktop\段永平智慧库"

Write-Host "[1/4] 检查文件变更..." -ForegroundColor Yellow
git status

Write-Host ""
Write-Host "[2/4] 添加所有变更..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "[3/4] 提交变更..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "更新内容 - $timestamp"

Write-Host ""
Write-Host "[4/4] 推送到GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "  ✅ 部署完成！" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "网站地址：https://samsonitecharlie.github.io/duanyongping-wisdom/" -ForegroundColor Cyan
Write-Host "GitHub会在1-2分钟内自动更新网站" -ForegroundColor Gray
Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
