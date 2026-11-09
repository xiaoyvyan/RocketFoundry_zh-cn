param([int]$X,[int]$Y)
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class F32 {
  [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h, IntPtr after, int x, int y, int cx, int cy, uint f);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x,int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f,int dx,int dy,int c,int e);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h,int n);
}
"@
$p = Get-Process -Name RocketFoundry | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
$h = [IntPtr]([int64]$p.MainWindowHandle)
[F32]::ShowWindow($h,9) | Out-Null
[F32]::SetWindowPos($h, [IntPtr](-1), 0,0,0,0, 0x0043) | Out-Null   # HWND_TOPMOST + NOMOVE|NOSIZE|SHOWWINDOW
[F32]::SetForegroundWindow($h) | Out-Null
Start-Sleep -Milliseconds 700
[F32]::SetCursorPos($X,$Y) | Out-Null
Start-Sleep -Milliseconds 300
[F32]::mouse_event(0x0002,0,0,0,0); Start-Sleep -Milliseconds 90; [F32]::mouse_event(0x0004,0,0,0,0)
Start-Sleep -Milliseconds 400
[F32]::SetWindowPos($h, [IntPtr](-2), 0,0,0,0, 0x0043) | Out-Null   # HWND_NOTOPMOST
"fg=" + [F32]::GetForegroundWindow().ToInt64() + " win=" + $h.ToInt64()