import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import os

def selecionar_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        var_pasta.set(pasta)

def baixar_legenda():
    url = entry_url.get().strip()
    idioma = entry_idioma.get().strip()
    auto = var_auto.get()
    pasta_destino = var_pasta.get().strip()

    if not url or not idioma or not pasta_destino:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos e selecione uma pasta.")
        return

    comando = [
        "yt-dlp",
        "--sub-lang", idioma,
        "--convert-subs", "srt",
        "--skip-download",
        "--output", os.path.join(pasta_destino, "%(title)s.%(ext)s"),
        url
    ]

    if auto:
        comando.insert(1, "--write-auto-subs")
    else:
        comando.insert(1, "--write-subs")

    try:
        subprocess.run(comando, check=True)
        messagebox.showinfo("Sucesso", "Legenda baixada com sucesso!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Erro", "Erro ao baixar a legenda.")

# GUI
root = tk.Tk()
root.title("Baixar Legendas do YouTube")
root.geometry("450x280")

# URL
tk.Label(root, text="URL do Vídeo:").pack()
entry_url = tk.Entry(root, width=60)
entry_url.pack()

# Idioma
tk.Label(root, text="Idioma da Legenda (ex: pt, en):").pack()v
entry_idioma = tk.Entry(root, width=10)
entry_idioma.pack()

# Legenda automática
var_auto = tk.BooleanVar()
tk.Checkbutton(root, text="Usar legenda automática (YouTube)", variable=var_auto).pack()

# Pasta destino
tk.Label(root, text="Pasta de destino:").pack()
var_pasta = tk.StringVar()
frame_pasta = tk.Frame(root)
entry_pasta = tk.Entry(frame_pasta, textvariable=var_pasta, width=40)
entry_pasta.pack(side=tk.LEFT, padx=(0, 5))
btn_pasta = tk.Button(frame_pasta, text="Selecionar", command=selecionar_pasta)
btn_pasta.pack(side=tk.LEFT)
frame_pasta.pack(pady=5)

# Botão baixar
tk.Button(root, text="Baixar Legenda", command=baixar_legenda).pack(pady=10)

root.mainloop()
