param([string]$Out = "D:\001wyh\newrf\tools\dumps\cap.png", [int]$Wait = 900)
Add-Type @"
using System;using System.Runtime.InteropServices;using System.Drawing;
public class Cap {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint p);
  [DllImport("user32.dll")] public static extern bool AttachThreadInput(uint a, uint b, bool f);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  public struct RECT { public int L, T, R, B; }
  public static void Focus(IntPtr h) {
    IntPtr fg = GetForegroundWindow();
    uint pid = 0; GetWindowThreadProcessId(fg, out pid);
    AttachThreadInput((uint)System.Diagnostics.Process.GetCurrentProcess().Threads[0].Id, pid, true);
    ShowWindow(h, 9);
    SetForegroundWindow(h);
    AttachThreadInput((uint)System.Diagnostics.Process.GetCurrentProcess().Threads[0].Id, pid, false);
  }
  public static void Shot(IntPtr h, string path) {
    RECT r; GetWindowRect(h, out r);
    int w = r.R - r.L, ht = r.B - r.T;
    Bitmap bmp = new Bitmap(w, ht);
    using (Graphics g = Graphics.FromImage(bmp)) {
      IntPtr dc = g.GetHdc();
      PrintWindow(h, dc, 2);
      g.ReleaseHdc(dc);
    }
    bmp.Save(path, System.Drawing.Imaging.ImageFormat.Png);
    bmp.Dispose();
  }
}
"@ -ReferencedAssemblies System.Drawing
$p = Get-Process -Name RocketFoundry | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
$h = [IntPtr]([int64]$p.MainWindowHandle)
[Cap]::Focus($h)
Start-Sleep -Milliseconds $Wait
[Cap]::Shot($h, $Out)
"cap " + $Out
