param(
  [int]$X = -1,
  [int]$Y = -1,
  [int]$Delay = 900,
  [string]$Shot = "",
  [switch]$Key,
  [string]$KeyName = "",
  [int]$Wheel = 0
)
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W32b {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, int dx, int dy, int c, int e);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int n);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
  [DllImport("user32.dll")] public static extern void keybd_event(byte k, byte s, uint f, IntPtr e);
  public struct RECT { public int L, T, R, B; }
}
"@
$p = Get-Process -Name RocketFoundry -ErrorAction Stop | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
if ($null -eq $p) { throw "no RocketFoundry window" }
$h = [IntPtr]([int64]$p.MainWindowHandle)
[W32b]::ShowWindow($h, 9) | Out-Null
[W32b]::SetForegroundWindow($h) | Out-Null
Start-Sleep -Milliseconds 350
$r = New-Object W32b+RECT
[W32b]::GetWindowRect($h, [ref]$r) | Out-Null
if ($X -ge 0 -and $Y -ge 0) {
  [W32b]::SetCursorPos($r.L + $X, $r.T + $Y) | Out-Null
  Start-Sleep -Milliseconds 180
  [W32b]::mouse_event(0x0002, 0, 0, 0, 0)
  Start-Sleep -Milliseconds 100
  [W32b]::mouse_event(0x0004, 0, 0, 0, 0)
  "clicked win($X,$Y) -> screen($($r.L + $X),$($r.T + $Y))"
} elseif ($Key) {
  $vk = [byte][char]$KeyName
  [W32b]::keybd_event($vk, 0, 0, [IntPtr]::Zero)
  Start-Sleep -Milliseconds 80
  [W32b]::keybd_event($vk, 0, 2, [IntPtr]::Zero)
  "pressed $KeyName"
}
Start-Sleep -Milliseconds $Delay
if ($Wheel -ne 0) {
  $n = [Math]::Abs($Wheel)
  $dir = if ($Wheel -gt 0) { 120 } else { -120 }
  for ($i = 0; $i -lt $n; $i++) {
    [W32b]::mouse_event(0x0800, 0, 0, $dir, 0)
    Start-Sleep -Milliseconds 70
  }
  Start-Sleep -Milliseconds 900
}
if ($Shot -ne "") {
  $w = $r.R - $r.L; $hh = $r.B - $r.T
  $bmp = New-Object System.Drawing.Bitmap($w, $hh)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $hdc = $g.GetHdc()
  [W32b]::PrintWindow($h, $hdc, 2) | Out-Null
  $g.ReleaseHdc($hdc)
  $g.Dispose()
  $bmp.Save($Shot, [System.Drawing.Imaging.ImageFormat]::Png)
  $bmp.Dispose()
  Start-Sleep -Milliseconds 5600
  $src = Join-Path $env:APPDATA "Godot\app_userdata\Rocket Foundry\zh_dump.txt"
  $dst = [IO.Path]::ChangeExtension($Shot, ".txt")
  if (Test-Path -LiteralPath $src) { Copy-Item -LiteralPath $src -Destination $dst -Force }
  "shot $Shot ($w x $hh)"
}
