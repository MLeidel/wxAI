#
# wxAI.py
# wxPython GUI with OpenAI API`
#
import os
import iniproc
import markdown
import webbrowser
import wx
from openai import OpenAI

intro = '''
Welcome to wxAI

This is connected to the OpenAI API, so you must have a registered key
from OpenAI which you will setup in your computer's environment.
Then edit the "openai" value in your "options.ini" file
located in wxAI's directory.

https://beta.openai.com/signup

Open the README.html file, located in the app's directory, for
other details on using wxAI.

'''

opts = [] # loading options from the options.ini file into a list
opts = iniproc.read("options.ini",'openai',     # 0
                                   'model',     # 1
                                   'fontsz1',   # 2
                                   'fontsz2',   # 3
                                   'role',      # 4
                                   'log')       # 5

class MyFrame(wx.Frame):
    def __init__(self, parent, title="wxAI V1.0 OpenAI " + opts[1]):
        super(MyFrame, self).__init__(parent, title=title, size=(600, 550))

        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(5, 5)

        # ----------------------------
        # First Text Widget (text1) the Prompt area
        # ----------------------------
        # This TextCtrl will expand horizontally but not vertically
        self.text1 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        sizer.Add(
            self.text1,
            pos=(0, 0),          # Position at row 0, column 0
            span=(1, 4),         # Span of 1 row and 2 columns
            flag=wx.EXPAND       # Allow horizontal expansion
        )
        sizer.SetItemMinSize(self.text1, self.text1.GetSize().GetWidth(), 125)  # Set minimum height
        self.text1.Bind(wx.EVT_KEY_DOWN, self.on_key_down_hotkeys)
        self.text1.SetToolTip("Enter Prompt in this field")
        self.text1.SetFocus()

        # ----------------------------
        # Second Text Widget (text2) the response area
        # ----------------------------
        # This TextCtrl will expand both horizontally and vertically
        self.text2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)  # wx.TE_DONTWRAP
        sizer.Add(
            self.text2,
            pos=(1, 0),          # Position at row 1, column 0
            span=(1, 4),         # Span of 1 row and 2 columns
            flag=wx.EXPAND       # Allow both horizontal and vertical expansion
        )
        self.text2.Bind(wx.EVT_KEY_DOWN, self.on_key_down_hotkeys)
        self.text2.SetValue(intro)

        # ----------------------------
        # Clear Button
        # ----------------------------
        clear_btn = wx.Button(panel, label="Clear")
        sizer.Add(
            clear_btn,
            pos=(2, 0),          # Position at row 2, column 0
            span=(1, 1),         # Span of 1 row and 1 column
            flag=wx.EXPAND | wx.ALL, # Align to bottom-right
            border=5  # behaves like a "margin"
        )
        # Bind the close button event to the handler
        clear_btn.Bind(wx.EVT_BUTTON, self.on_clear)
        clear_btn.SetToolTip("Erase query and response text")

        # ----------------------------
        # Export Button
        # ----------------------------
        export_btn = wx.Button(panel, label="Export")
        sizer.Add(
            export_btn,
            pos=(2, 1),          # Position at row 2, column 0
            span=(1, 1),         # Span of 1 row and 1 column
            flag=wx.EXPAND | wx.ALL, # Align to bottom-right
            border=5  # behaves like a "margin"
        )
        # Bind the close button event to the handler
        export_btn.Bind(wx.EVT_BUTTON, self.on_export)
        export_btn.SetToolTip("Open response in web browser")

        # ----------------------------
        # Submit Button
        # ----------------------------
        submit_btn = wx.Button(panel, label="Submit")
        sizer.Add(
            submit_btn,
            pos=(2, 2),          # Position at row 2, column 0
            span=(1, 1),         # Span of 1 row and 1 column
            flag=wx.EXPAND | wx.ALL, # Align to bottom-right
            border=5  # behaves like a "margin"
        )
        submit_btn.SetToolTip(f"Submit prompt to {opts[1]} (Ctrl-G)")
        submit_btn.Bind(wx.EVT_BUTTON, self.on_submit)

        # ----------------------------
        # Close Button
        # ----------------------------
        close_btn = wx.Button(panel, label="Close")
        sizer.Add(
            close_btn,
            pos=(2, 3),          # Position at row 2, column 0
            span=(1, 1),         # Span of 1 row and 1 column
            flag=wx.EXPAND | wx.ALL, # Align to bottom-right
            border=5  # behaves like a "margin"
        )
        # Bind the close button event to the handler
        close_btn.Bind(wx.EVT_BUTTON, self.on_close)
        close_btn.SetToolTip("Ctrl-Q")


        # ----------------------------
        # Configure Growable Columns and Rows
        # ----------------------------
        sizer.AddGrowableCol(0, 1)    # Column 0 for Submit button & response area grows horizontally
        sizer.AddGrowableCol(1, 1)    # Clear button grows horizontally
        sizer.AddGrowableCol(2, 1)    # Export button grows horizontally
        sizer.AddGrowableCol(3, 1)    # Close button grows horizontally
        sizer.AddGrowableRow(1, 1)    # Prompt area ROW grows vertically

        panel.SetSizer(sizer)

        #----------------------------
        # set window metrics from winfo file
        # ----------------------------
        if os.path.isfile("winfo"):
            with open("winfo", "r", encoding='utf-8') as fin:
                winfo = fin.read()
            p = winfo.split("|")
            x, y, w, h = int(p[0]), int(p[1]), int(p[2]), int(p[3])
            position = wx.Point(x, y)
            self.SetPosition(position)
            self.SetSize(wx.Size(w, h))

        #----------------------------
        # SET CUSTOM FONTS
        # https://docs.wxpython.org/wx.FontInfo.html#wx-fontinfo
        # https://docs.wxpython.org/wx.FontFamily.enumeration.html#wx-fontfamily
        custom_font1 = wx.Font( wx.FontInfo(int(opts[2])).Family(wx.FONTFAMILY_MODERN) )  # monospace
        self.text1.SetFont(custom_font1)
        custom_font2 = wx.Font( wx.FontInfo(int(opts[3])).Family(wx.FONTFAMILY_TELETYPE) )
        self.text2.SetFont(custom_font2)

        self.Show()


    # ----------------------------
    #   Event handlers follow
    # ----------------------------

    def on_close(self, event):
        ''' Event handler for the Close button.'''
        # save Window metrics
        pos = self.GetPosition()
        x, y = str(pos[0]), str(pos[1])
        size = self.GetSize()
        w, h = str(size[0]), str(size[1])
        with open("winfo", "w") as fout:
            fout.write(x + "|" + y + "|" + w + "|" + h)
        self.Close()


    def on_clear(self, event):
        ''' Event handler for the Clear button.'''
        dlg = wx.MessageDialog(
            self,
            "Do you want to clear PROMPT and RESPONSE areas?",  # content
            "Confirm Clear",  # title
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
        )
        result = dlg.ShowModal()
        dlg.Destroy()

        if result == wx.ID_YES:
            self.text1.SetValue("")
            self.text2.SetValue("")


    def on_export(self, event):
        ''' convert MD file to HTML file and open in default browser '''
        mdtext = self.text2.GetValue()
        htmlText = markdown.markdown(mdtext, extensions=['tables', 'fenced_code'])
        htmlFile = "exported.html"
        # open in default browser
        with open(htmlFile, 'w', encoding='utf-8') as file:
            file.write(htmlText)
        webbrowser.open(htmlFile)


    def on_submit(self, event):
        ''' Event handler for Submit button (Ctrl-G). '''
        self.text2.SetValue("Processing ...")
        wx.Yield()
        query = self.text1.GetValue()
        aitext = self.gptCode(opts[0], opts[1], query)
        if aitext == "":
            self.text2.SetValue("")
            self.text1.SetValue("")
            return
        self.text2.SetValue(aitext)
        if opts[5].lower() == "true":
            with open("log.md", "w", encoding='utf-8') as fout:
                fout.write("\n==================================================\n\n")
                fout.write(aitext)


    def gptCode(self, key: str, model: str, query: str) -> str:
        ''' method to access OpenAI chat.completions API '''
        try:
            client = OpenAI(
            api_key = os.environ.get(key)  # openai API
        )
        except Exception as e:
            wx.MessageBox(str(e), 'Info', wx.OK | wx.ICON_ERROR)
            return ""

        try:
            response = client.chat.completions.create(
              model=model,
              messages=[{"role": "user", "content": opts[4]},
                  {"role": "user", "content" : query.strip()}
              ]
            )
            output = response.choices[0].message.content
            return output
        except Exception as e:
            wx.MessageBox(str(e), 'Info', wx.OK | wx.ICON_ERROR)
            return ""


    def on_key_down_hotkeys(self, event):
        ''' Set up HotKeys for the App '''
        keycode = event.GetKeyCode()
        modifiers = event.GetModifiers()

        # Check if Ctrl is pressed and the key is 'G'
        if modifiers == wx.MOD_CONTROL and keycode == ord('G'):
            self.on_submit(event)
        else:
            event.Skip()  # Ensure other key events are processed
        # Check if Ctrl is pressed and the key is 'Q'
        if modifiers == wx.MOD_CONTROL and keycode == ord('Q'):
            self.on_close(event)
        else:
            event.Skip()  # Ensure other key events are processed


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None)
        self.SetTopWindow(frame)
        return True

if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()