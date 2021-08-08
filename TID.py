from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from os import system
from sys import platform 
from math import ceil
from pynput import keyboard
from io import BytesIO
import win32clipboard


dim = (1920, 1080)
padx = 100
pady = 100
fonts = {'C64 Pro' : 'C64_Pro_Mono-STYLE.ttf', 'TT2020 Base' : 'TT2020Base-Regular.ttf', 'Average Mono' : 'AverageMono.ttf',
        'Consolas' : 'Consolas.ttf', 'Adobe Source Code Scans' : 'SourceCodePro-Regular.ttf',
        'Liberation Mono' : 'LiberationMono-Regular.ttf', 'Times New Roman' : 'times.ttf', 
        'Comic Sans MS' : 'ComicSansMS3.ttf', 'Papyrus' : 'PAPYRUS.TTF'}

v_anchor = {'center' : 'mm', 'left' : 'mm'}
dfont = 'Liberation Mono'
dfsize = 40
dwrap = 30

def mkI():
    with open('text.txt', 'r') as file:
        try: 
            ptwrap = int(twrap.get())
            if ptwrap < 0:
                print("wrap length too small")
                ptwrap = dwrap
        except: 
            ptwrap = dwrap
            print('invalid wrap length')
        t = ''
        for line in file:
            t = t+line
        t = t.strip()
        if ptwrap:
            nt = ''
            i = 0
            for w in t.split(' '):
                if w.find('\n') == -1:
                    i += len(w) + 1
                else: 
                    i = 0
                if i >= ptwrap:
                    nt = nt + '\n' + w + ' '
                    i = len(w)+1
                else: 
                    nt = nt + w + ' '
                
            t = nt.strip()
        i = Image.new("RGB", dim, (0, 0, 0))
        i_d = ImageDraw.Draw(i)
       
        try: 
            pfsize = int(fsize.get())
            if pfsize < 1:
                print('font size too small')
                pfsize = dfsize
        except:
            pfsize = dfsize
            print('font size invalid')
        f = ImageFont.truetype('fonts/'+fonts[s_font.get()], pfsize)
        t_dim = i_d.textbbox((0, 0), t, font = f, anchor = v_anchor[v_align.get()], align =
                v_align.get())
        t_dim = (int(t_dim[2] - t_dim[0]), int(t_dim[3] - t_dim[1]))
        print(t_dim)
        t_dim = (t_dim[0]+padx, t_dim[1]+pady)
        
        i = Image.new("RGB", (t_dim[0], t_dim[1]), (0, 0, 0))
        i_d = ImageDraw.Draw(i)
        i_d.text((t_dim[0]//2, t_dim[1]//2), t, font = f, fill = (255, 255, 255), anchor =
                v_anchor[v_align.get()], align = v_align.get())

        i.save('code.png')
        if platform == 'linux':
            try: 
                system('xclip -selection clipboard -target image/png -i code.png')
            except: 
                print('.. -. ... - .- .-.. .-.. / -..- -.-. .-.. .. .--. / ... - ..- .--. .. -.. .-.-.-')
        elif platform == 'win32':
            output = BytesIO()
            i.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()
		
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
        else: 
            print("-.-- --- ..- .----. .-. . / -. --- - / .-. ..- -. -. .. -. --. / .-- .. -. -..\
            --- .-- ... / --- .-. / .-.. .. -. ..- -..- / .-.. --- .-.. .-.-.-")

        if i_show.get():
            i.show()
pk = {keyboard.Key.shift : False}
def on_press(key):
    pk[key] = True
    sp = pk[keyboard.Key.shift]
    if key == keyboard.Key.f12 and sp:
        mkI()
def on_release(key):
    pk[key] = False


root = tk.Tk()
frame1 = tk.Frame(root)
s_font = tk.StringVar(value = dfont)
v_align = tk.StringVar(value = 'center')
i_show = tk.BooleanVar(value = False)
fsize = tk.StringVar(value = f"{dfsize}")
twrap = tk.StringVar(value = f"{dwrap}")

b1 = tk.Button(frame1, text = 'generate', command = mkI)
r1 = []
i = 0
for x, y in fonts.items():
    i += 1
    r1.append(tk.Radiobutton(frame1, text = x, variable = s_font, value = x))

r2 = []
i = 0
for x, y in v_anchor.items():
    i += 1
    r2.append(tk.Radiobutton(frame1, text = x, variable = v_align, value = x))
c1 = tk.Checkbutton(frame1, text = 'print', variable = i_show, offvalue = False, onvalue = True)
l1 = tk.Label(frame1, text = 'font size')
e1 = tk.Entry(frame1, textvariable = fsize, exportselection = 0, width = 5)
l2 = tk.Label(frame1, text = 'text wrap')
e2 = tk.Entry(frame1, textvariable = twrap, exportselection = 0, width = 5)

def main():
    root.title("- . -..- - / - --- / .. -- .- --. .")
    root.geometry("300x350")
    frame1.place(anchor = 'center', relx = 0.5, rely = 0.5)
    i = 0
    for rb in r1:
        rb.grid(row = i, column = 0, sticky = 'w', padx = 10, pady = 2)
        i += 1
    i = 0
    for rb in r2:
        rb.grid(row = i, column = 1, sticky = 'w', padx = 10, pady = 2)
        i += 1
    c1.grid(row = len(r2)+1, column = 1, sticky = 'w', padx = 10, pady = 2)
    l1.grid(row = len(r2)+2, column = 1, sticky = 's')
    e1.grid(row = len(r2)+3, column = 1, sticky = 'n')
    l2.grid(row = len(r2)+4, column = 1, sticky = 's')
    e2.grid(row = len(r2)+5, column = 1, sticky = 'n')
    b1.grid(row = 100, column = 0, columnspan = 100)

    listener = keyboard.Listener(on_press = on_press, on_release = on_release)
    listener.start()

    root.mainloop()

main()
