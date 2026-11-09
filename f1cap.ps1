param([int]$Vk = 0x70, [int]$Times = 3, [int]$Gap = 70, [string]$Out = "D:\001wyh\newrf\tools\dumps\f1.png", [int]$Wait = 600)
Add-Type @"
using System;using System.Runtime.InteropServices;using System.Drawing;
public class F1Cap {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint p);
  [DllImport("user32.dll")] public static extern bool AttachThreadInput(uint a, uint b, bool f);
  [DllImport("user32.dll")] public static extern void keybd_event(byte k, byte s, uint f, IntPtr e);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  public struct RECT { public int L, T, R, B; }
  public static void Focus(IntPtr h) {
    IntPtr fg = GetForegroundWindow();
    uint pid = 0; GetWindowThreadProcessId(fg, out pid);
    uint tid = (uint)System.Diagnostics.Process.GetCurrentProcess().Threads[0].Id;
    AttachThreadInput(tid, pid, true); ShowWindow(h, 9); SetForegroundWindow(h); AttachThreadInput(tid, pid, false);
  }
  public static void Key(byte vk, int times, int gap) {
    for (int i = 0; i < times; i++) {
      keybd_event(vk, (byte)0, 0, IntPtr.Zero);
      System.Threading.Thread.Sleep(gap);
      keybd_event(vk, (byte)0, 2, IntPtr.Zero);
      System.Threading.Thread.Sleep(gap);
    }
  }
  public static void Shot(IntPtr h, string path) {
    RECT r; GetWindowRect(h, out r);
    int w = r.R - r.L, ht = r.B - r.T;
    Bitmap bmp = new Bitmap(w, ht);
    using (Graphics g = Graphics.FromImage(bmp)) {
      IntPtr dc = g.GetHdc(); PrintWindow(h, dc, 2); g.ReleaseHdc(dc);
    }
    bmp.Save(path, System.Drawing.Imaging.ImageFormat.Png); bmp.Dispose();
  }
}
"@ -ReferencedAssemblies System.Drawing
$p = Get-Process -Name RocketFoundry | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
$h = [IntPtr]([int64]$p.MainWindowHandle)
[F1Cap]::Focus($h)
Start-Sleep -Milliseconds 400
[F1Cap]::Key([byte]$Vk, $Times, $Gap)
Start-Sleep -Milliseconds $Wait
[F1Cap]::Shot($h, $Out)
"sent vk=$Vk times=$Times"
