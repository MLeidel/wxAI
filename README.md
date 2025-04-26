# wxAI
## Desktop Front-End for OpenAI Query

_see **wxGAI** for Google Gemini_

![wxAI](images/wxAI_1.png "wxAI")

wxAI is similar to [GptGUI](https://github.com/MLeidel/GptGUI "Git Website").

You will need an OpenAI api-key to use this program.

wxAI is written in Python3 with wxPython producing a GTK GUI
on Linux and a true _light_ theme look on Windows.

wxAI has fewer options than GptGUI and the `options.ini` file must be edited manually.

At this time this is what an `options.ini` might contain:

        # wxAI.py
        openai=GPTKEY
        model=o1-mini
        role=you are a helpful coding assistant
        log=on
        fontsz1=10
        fontsz2=12

The **Export** button converts the markdown response to HTML and presents it in the
system default browser. 

The other function buttons are self explanatory.

---

## Hot Keys

        Ctrl-H     This help message
        Ctrl-F     Find text
        Ctrl-N     Find next
        Ctrl-Q     Quit App
        Ctrl-G     Execute AI request
        Alt-Ctrl-C
                   Copy Code in Markup
---

wxAI requires these other python3 modules:

        markdown
        wx
        openai

To run:

      $ python3 wxAI.py
    
---

## Environment Variables

### [Linux](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/ "How To") [Windows](https://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10/ "How To")



