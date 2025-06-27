import tkinter as tk
from tkinter import messagebox
import subprocess

def baixar_legenda():
    url = entry_url.get().strip()
    idioma = entry_idioma.get().strip()
    auto = var_auto.get()

    if not url or not idioma:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
        return

    comando = [
        "yt-dlp",
        "--sub-lang", idioma,
        "--convert-subs", "srt",
        "--skip-download",
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
root.geometry("400x200")

# Campos
tk.Label(root, text="URL do Vídeo:").pack()
entry_url = tk.Entry(root, width=50)
entry_url.pack()

tk.Label(root, text="Idioma da Legenda (ex: pt, en):").pack()
entry_idioma = tk.Entry(root, width=10)
entry_idioma.pack()

var_auto = tk.BooleanVar()
tk.Checkbutton(root, text="Usar legenda automática (YouTube)", variable=var_auto).pack()

tk.Button(root, text="Baixar Legenda", command=baixar_legenda).pack(pady=10)

root.mainloop()
