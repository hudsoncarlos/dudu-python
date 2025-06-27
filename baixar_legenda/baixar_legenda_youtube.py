import subprocess
import os

output_path = os.path.expanduser("~/Downloads/%(title)s.%(ext)s")

def baixar_legenda():
    url = input("Digite a URL do vídeo do YouTube: ").strip()
    idioma = input("Digite o código do idioma da legenda (ex: pt, en): ").strip()

    comando = [
        "yt-dlp",
        "--write-auto-subs",        # Usa legendas automáticas (você pode mudar para --write-subs se preferir as enviadas)
        "--sub-lang", idioma,
        "--output", output_path,
        "--skip-download",
        url
    ]

    # comando = [
    #     "yt-dlp",
    #     "--write-auto-subs",        # Usa legendas automáticas (você pode mudar para --write-subs se preferir as enviadas)
    #     "--sub-lang", idioma,
    #     "--output", output_path,
    #     "--convert-subs", "srt",
    #     "--skip-download",
    #     url
    # ]

    print("\n📥 Baixando legenda...\n")
    try:
        subprocess.run(comando, check=True)
        print("\n✅ Legenda baixada com sucesso!")
    except subprocess.CalledProcessError:
        print("\n❌ Ocorreu um erro ao baixar a legenda.")

if __name__ == "__main__":
    baixar_legenda()
