# wxAI
## Desktop Front-End for OpenAI Query

![wxAI](images/wxAI_1.png "wxAI")

wxAI is similar to [GptGUI](https://github.com/MLeidel/GptGUI "Git Website").

wxAI is written in Python3 with wxPython producing a GTK GUI
on Linux and a true _light_ theme look on Windows.

wxAI has fewer options than GptGUI and the `options.ini` file must be edited manually.

At this time this is what an `options.ini` might contain:

        # wsAI.py
        openai=GPTKEY
        model=o1-mini
        role=you are a helpful coding assistant
        log=on
        fontsz1=10
        fontsz2=12

The **Export** button converts the markdown response to HTML and presents it in the
system default browser. 

The other functions are self explanatory.

Python3 must be installed along with these modules:

        markdown
        wx
        openai

To run:

      $ python3 wxAI.py
    
---

## Environment Variables

### [Linux](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/ "How To") [Windows](https://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10/ "How To")



