param([int]$X,[int]$Y,[int]$Ticks)
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class SC {
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x,int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f,int dx,int dy,int c,int e);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h, IntPtr a, int x,int y,int cx,int cy,uint f);
}
"@
$p = Get-Process -Name RocketFoundry | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
$h = [IntPtr]([int64]$p.MainWindowHandle)
[SC]::SetWindowPos($h, [IntPtr](-1), 0,0,0,0, 0x0043) | Out-Null
[SC]::SetForegroundWindow($h) | Out-Null
Start-Sleep -Milliseconds 500
[SC]::SetCursorPos($X,$Y) | Out-Null
Start-Sleep -Milliseconds 200
for ($i=0; $i -lt $Ticks; $i++) {
  [SC]::mouse_event(0x0800, 0, 0, -120, 0)
  Start-Sleep -Milliseconds 120
}
Start-Sleep -Milliseconds 300
[SC]::SetWindowPos($h, [IntPtr](-2), 0,0,0,0, 0x0043) | Out-Null
"scrolled"