param(
  [string]$Text = "test",
  [int]$ClickX = -1,
  [int]$ClickY = -1,
  [string]$Shot = ""
)
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W32c {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, int dx, int dy, int c, int e);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int n);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
  public struct RECT { public int L, T, R, B; }
}
"@
$p = Get-Process -Name RocketFoundry -ErrorAction Stop | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
$h = [IntPtr]([int64]$p.MainWindowHandle)
[W32c]::ShowWindow($h, 9) | Out-Null
[W32c]::SetForegroundWindow($h) | Out-Null
Start-Sleep -Milliseconds 400
$r = New-Object W32c+RECT
[W32c]::GetWindowRect($h, [ref]$r) | Out-Null
if ($ClickX -ge 0) {
  [W32c]::SetCursorPos($r.L + $ClickX, $r.T + $ClickY) | Out-Null
  Start-Sleep -Milliseconds 200
  [W32c]::mouse_event(0x0002, 0, 0, 0, 0)
  Start-Sleep -Milliseconds 100
  [W32c]::mouse_event(0x0004, 0, 0, 0, 0)
  Start-Sleep -Milliseconds 400
}
[System.Windows.Forms.SendKeys]::SendWait($Text)
Start-Sleep -Milliseconds 700
if ($Shot -ne "") {
  $w = $r.R - $r.L; $hh = $r.B - $r.T
  $bmp = New-Object System.Drawing.Bitmap($w, $hh)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $hdc = $g.GetHdc()
  [W32c]::PrintWindow($h, $hdc, 2) | Out-Null
  $g.ReleaseHdc($hdc); $g.Dispose()
  $bmp.Save($Shot, [System.Drawing.Imaging.ImageFormat]::Png)
  $bmp.Dispose()
}
"typed $Text; rect $($r.L),$($r.T)"
