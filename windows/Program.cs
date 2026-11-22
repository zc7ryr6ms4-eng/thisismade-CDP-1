namespace Thisismade;

static class Program
{
    public const string AppName = "Thisismade CD Player";
    public const string Version = "1.0.0";

    [STAThread]
    static void Main(string[] args)
    {
        using var mutex = new Mutex(true, "Thisismade.CDPlayer.SingleInstance", out bool first);
        if (!first)
        {
            if (args.Length > 0) Native.SendToRunning(AppName, args);
            else Native.SendToRunning(AppName, Array.Empty<string>());
            return;
        }
        ApplicationConfiguration.Initialize();
        Application.Run(new MainForm(args));
    }
}
