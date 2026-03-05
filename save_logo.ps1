# Quick Logo Saver for Staten Island Website
# chmod a+x save_logo.ps1 OR just run: .\save_logo.ps1

Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host "   Staten Island Logo Quick Saver" -ForegroundColor Green
Write-Host "===========================================================" -ForegroundColor Cyan
Write-Host ""

$destinationPath = "static\images\logo.jpg"
$destinationDir = "static\images"

# Ensure directory exists
if (-Not (Test-Path $destinationDir)) {
    New-Item -ItemType Directory -Path $destinationDir -Force | Out-Null
    Write-Host "✓ Created directory: $destinationDir" -ForegroundColor Green
}

Write-Host "METHOD 1: From Clipboard (FASTEST)" -ForegroundColor Yellow
Write-Host "          Right-click your logo → Copy Image" -ForegroundColor Gray
Write-Host "          Then press ENTER" -ForegroundColor Gray
Write-Host ""
Write-Host "METHOD 2: Enter file path" -ForegroundColor Yellow
Write-Host "          Type/paste the full path to your logo" -ForegroundColor Gray
Write-Host ""
Write-Host "METHOD 3: Drag & Drop" -ForegroundColor Yellow
Write-Host "          Drag your logo file here and press ENTER" -ForegroundColor Gray
Write-Host ""
Write-Host "Choice (1/2/3 or full file path): " -NoNewline -ForegroundColor Cyan

$input = Read-Host

if ($input -eq "1" -or $input -eq "") {
    # Try clipboard
    Write-Host "`nAttempting to get image from clipboard..." -ForegroundColor Cyan
    try {
        Add-Type -Assembly System.Windows.Forms
        Add-Type -Assembly System.Drawing
        $img = [Windows.Forms.Clipboard]::GetImage()
        
        if ($img) {
            $img.Save($destinationPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
            Write-Host "✅ SUCCESS! Logo saved from clipboard!" -ForegroundColor Green
            Get-Item $destinationPath | Format-List Name, Length, LastWriteTime
        } else {
            Write-Host "❌ No image found in clipboard" -ForegroundColor Red
            Write-Host "   Please right-click your logo and select 'Copy Image' first" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ Error accessing clipboard: $_" -ForegroundColor Red
    }
} elseif ($input -eq "2") {
    Write-Host "Enter the full path to your logo file: " -NoNewline
    $sourcePath = Read-Host
    $sourcePath = $sourcePath.Trim('"').Trim("'")
    
    if (Test-Path $sourcePath) {
        Copy-Item $sourcePath $destinationPath -Force
        Write-Host "✅ Logo copied successfully!" -ForegroundColor Green
        Get-Item $destinationPath | Format-List Name, Length, LastWriteTime
    } else {
        Write-Host "❌ File not found: $sourcePath" -ForegroundColor Red
    }
} elseif ($input -eq "3") {
    Write-Host "Drag your logo file here and press ENTER: " -NoNewline
    $sourcePath = Read-Host
    $sourcePath = $sourcePath.Trim('"').Trim("'")
    
    if (Test-Path $sourcePath) {
        Copy-Item $sourcePath $destinationPath -Force
        Write-Host "✅ Logo copied successfully!" -ForegroundColor Green
        Get-Item $destinationPath | Format-List Name, Length, LastWriteTime
    } else {
        Write-Host "❌ File not found: $sourcePath" -ForegroundColor Red
    }
} elseif (Test-Path $input.Trim('"').Trim("'")) {
    # User provided a direct path
    $sourcePath = $input.Trim('"').Trim("'")
    Copy-Item $sourcePath $destinationPath -Force
    Write-Host "✅ Logo copied successfully!" -ForegroundColor Green
    Get-Item $destinationPath | Format-List Name, Length, LastWriteTime
} else {
    Write-Host "❌ Invalid choice or file not found" -ForegroundColor Red
}

Write-Host "`n===========================================================" -ForegroundColor Cyan
Write-Host " Restart your Flask server to see the logo on all pages!" -ForegroundColor Green
Write-Host "===========================================================`n" -ForegroundColor Cyan
