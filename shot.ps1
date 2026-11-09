Add-Type -AssemblyName System.Drawing
$src = @'
using System;
using System.Runtime.InteropServices;
public class PW {
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern IntPtr GetWindowDC(IntPtr h);
  public struct RECT { public int L, T, R, B; }
}
'@
Add-Type -TypeDefinition $src
$p = Get-Process -Name RocketFoundry | Select-Object -First 1
$h = $p.MainWindowHandle
$r = New-Object PW+RECT
[PW]::GetWindowRect($h, [ref]$r) | Out-Null
$w = $r.R - $r.L
$hh = $r.B - $r.T
"window ${w}x${hh}"
$bmp = New-Object System.Drawing.Bitmap($w, $hh)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$hdc = $g.GetHdc()
$ok = [PW]::PrintWindow($h, $hdc, 2)
$g.ReleaseHdc($hdc)
$g.Dispose()
"printwindow=" + $ok
$bmp.Save("D:\001wyh\newrf\tools\shot_win.png", [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()
"saved " + (Get-Item -LiteralPath "D:\001wyh\newrf\tools\shot_win.png").Length
