param([int]$X, [int]$Y)
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W32 {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, int dx, int dy, int c, int e);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int n);
}
"@
$p = Get-Process -Name RocketFoundry -ErrorAction Stop | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
if ($null -eq $p) { throw "no RocketFoundry window" }
$h = [IntPtr]([int64]$p.MainWindowHandle)
[W32]::ShowWindow($h, 9) | Out-Null
[W32]::SetForegroundWindow($h) | Out-Null
Start-Sleep -Milliseconds 400
[W32]::SetCursorPos($X, $Y) | Out-Null
Start-Sleep -Milliseconds 200
[W32]::mouse_event(0x0002, 0, 0, 0, 0)
Start-Sleep -Milliseconds 120
[W32]::mouse_event(0x0004, 0, 0, 0, 0)
"clicked $X,$Y"
