#!/usr/bin/python3
"""Live-only, user-scoped language, keyboard and country selection."""
import json
import os
from pathlib import Path
import subprocess
import tkinter as tk
from tkinter import ttk

LANGUAGES = {'English': 'en_US.UTF-8', 'हिन्दी (Hindi)': 'hi_IN.UTF-8'}
KEYBOARDS = {'English (US)': ('us', ''), 'English (India)': ('in', 'eng'),
             'Hindi (India, Bolnagri)': ('in', 'bolnagri')}
COUNTRIES = {'India': 'Asia/Kolkata', 'United States': 'America/New_York',
             'United Kingdom': 'Europe/London', 'Other (UTC)': 'Etc/UTC'}
CONFIG = Path.home() / '.config' / 'jatayu' / 'live-choices.json'

def main():
    root=tk.Tk()
    root.title('JatayuOS · First flight')
    root.configure(bg='#101c37')
    root.geometry('600x390')
    root.resizable(False,False)
    stage=tk.IntVar(value=0)
    selected=[tk.StringVar(value=next(iter(m))) for m in (LANGUAGES,KEYBOARDS,COUNTRIES)]
    page=ttk.Frame(root,padding=32)
    page.pack(expand=True,fill='both',padx=22,pady=22)
    heading=ttk.Label(page,font=('Sans',22,'bold'))
    heading.pack(anchor='w',pady=(0,10))
    info=ttk.Label(page,wraplength=460)
    info.pack(anchor='w',pady=(0,20))
    combo=ttk.Combobox(page,state='readonly',width=32)
    combo.pack(anchor='w')
    status=ttk.Label(page,wraplength=480)
    status.pack(anchor='w',pady=18)
    def show():
        i=stage.get()
        heading.config(text=['Welcome · Language','Keyboard layout','Your country'][i])
        info.config(text=['Choose the language for this live session.',
                          'Choose the keyboard layout you will type with.',
                          'Choose your country for the live session time zone.'][i])
        combo.config(values=list((LANGUAGES,KEYBOARDS,COUNTRIES)[i]))
        combo.set(selected[i].get())
        next_button.config(text='Start desktop' if i==2 else 'Next')
        status.config(text='Step %d of 3' % (i+1))
    def advance():
        i=stage.get(); selected[i].set(combo.get())
        if i<2:
            stage.set(i+1); show(); return
        locale=LANGUAGES[selected[0].get()]
        layout, variant=KEYBOARDS[selected[1].get()]
        zone=COUNTRIES[selected[2].get()]
        available=subprocess.run(['locale','-a'],capture_output=True,text=True,check=False).stdout.lower().replace('-','')
        if locale.lower().replace('-','') in available:
            os.environ['LANG']=locale
            os.environ['LANGUAGE']=locale.split('_')[0]
        else:
            os.environ['LANG']='C.UTF-8'
            # Language packs must be included in the ISO for full translations.
        os.environ['TZ']=zone
        subprocess.run(['setxkbmap', '-layout', layout, '-variant', variant], check=False)
        CONFIG.parent.mkdir(parents=True,exist_ok=True)
        CONFIG.write_text(json.dumps({'locale':locale,'keyboard':layout,'keyboard_variant':variant,'country':selected[2].get(),
                                      'timezone':zone,'locale_available':locale.lower().replace('-','') in available}),encoding='utf-8')
        root.destroy()
    next_button=ttk.Button(page,text='Next',command=advance)
    next_button.pack(anchor='e',side='bottom')
    show()
    root.protocol('WM_DELETE_WINDOW',lambda: None)
    root.mainloop()
