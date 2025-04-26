import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Copy Text Between Triple Back-Ticks')
        self.panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # Text control for input
        self.text_control = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_PROCESS_TAB)
        self.vbox.Add(self.text_control, 1, wx.EXPAND | wx.ALL, 10)

        # Button to copy text
        self.copy_button = wx.Button(self.panel, label='Copy Between Back-Ticks')
        self.copy_button.Bind(wx.EVT_BUTTON, self.on_copy)
        self.vbox.Add(self.copy_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.panel.SetSizer(self.vbox)

    def on_copy(self, event):
        text = self.text_control.GetValue()
        lines = text.splitlines()
        result = []
        in_backticks = False

        for line in lines:
            if line.startswith('```'):
                if in_backticks:
                    break
                else:
                    in_backticks = True
                    continue
            else:
                if in_backticks:
                    result.append(line)  # Collect lines within the back-ticked region

        # Join selected text and put it to the clipboard
        if result:
            clipboard_text = '\n'.join(result)
            self.set_clipboard(clipboard_text)
            wx.MessageBox('Copied to clipboard:', clipboard_text)
        else:
            wx.MessageBox('No text found between triple back-ticks.')

    def set_clipboard(self, text):
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(text))
            wx.TheClipboard.Close()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
