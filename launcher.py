import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import os
import subprocess
import time
import shutil
import tempfile
import stat
from io import BytesIO
import sys

# URLs do GitHub
VERSION_URL = "https://raw.githubusercontent.com/GRIDSTUDIOOFC/projeto-manhattan/main/version.txt"
EXE_URL = "https://raw.githubusercontent.com/GRIDSTUDIOOFC/projeto-manhattan/main/launcher.exe"

def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar a imagem da URL '{url}': {e}")
    except Exception as e:
        print(f"Erro ao processar a imagem baixada de '{url}': {e}")
    return None

def check_for_updates(current_version):
    try:
        response = requests.get(VERSION_URL)
        response.raise_for_status()
        latest_version = response.text.strip()
        if latest_version != current_version:
            print(f"Nova versão disponível: {latest_version}")
            return latest_version
        else:
            print("Você já está na versão mais recente.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao verificar atualizações: {e}")
        return None

def download_new_exe():
    try:
        response = requests.get(EXE_URL, stream=True)
        response.raise_for_status()
        temp_path = os.path.join(tempfile.gettempdir(), "launcher_new.exe")
        with open(temp_path, 'wb') as new_exe:
            shutil.copyfileobj(response.raw, new_exe)
        print("Novo launcher baixado com sucesso.")
        return temp_path
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar nova versão do launcher: {e}")
        return None

def replace_exe(new_exe_path):
    try:
        # Fechar o launcher atual
        current_exe = sys.argv[0]
        # Esperar um pouco para garantir que o processo esteja realmente encerrado
        time.sleep(2)

        # Substituir o executável antigo pelo novo
        temp_path = os.path.join(tempfile.gettempdir(), "launcher_temp.exe")
        shutil.move(new_exe_path, temp_path)
        os.rename(temp_path, current_exe)

        print("Executável substituído com sucesso.")
        
        # Reexecutar o novo executável
        subprocess.Popen([current_exe])
        sys.exit()
    except Exception as e:
        print(f"Erro ao substituir o executável: {e}")

def update_launcher():
    current_version = "1.2"  # Versão atual do launcher
    new_version = check_for_updates(current_version)
    
    if new_version:
        new_exe_path = download_new_exe()
        if new_exe_path:
            replace_exe(new_exe_path)

def show_animation():
    root = tk.Tk()
    root.title("PixelWave")

    # Definir o ícone da janela
    icon_url = "https://raw.githubusercontent.com/GRIDSTUDIOOFC/projeto-manhattan/main/images/ICONE.ico"
    try:
        icon_data = requests.get(icon_url).content
        icon_image = Image.open(BytesIO(icon_data)).resize((32, 32))  # Ícone de 32x32 pixels
        root.iconphoto(False, ImageTk.PhotoImage(icon_image))
    except Exception as e:
        print(f"Ícone não encontrado ou erro ao baixar o ícone: {e}")

    # Centralizar o launcher na tela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 800
    window_height = 600
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
    root.resizable(False, False)

    # Baixar a imagem de fundo do GitHub
    background_url = "https://raw.githubusercontent.com/GRIDSTUDIOOFC/projeto-manhattan/main/images/BACKGROUND.jpg"
    background_image = download_image(background_url)
    if background_image:
        root.background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(root, image=root.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Frame central para os slides
    frame_width = 655
    frame_height = 350
    frame_x = (window_width - frame_width) // 2
    frame_y = (window_height - frame_height) // 2

    main_frame = tk.Frame(root, width=frame_width, height=frame_height, bg="white")
    main_frame.place(x=frame_x, y=frame_y)

    # Adicionar a apresentação de slides
    canvas = tk.Canvas(main_frame, width=frame_width, height=frame_height, bg="white")
    canvas.pack()

    # URLs das imagens desejadas do GitHub
    image_urls = [
        "https://raw.githubusercontent.com/GRIDSTUDIOOFC/projeto-manhattan/main/images/FOTO-1.jpg",
        "https://raw.githubusercontent.com/GRIDSTUDIOOFC/projeto-manhattan/main/images/FOTO-2.jpg",
        "https://raw.githubusercontent.com/GRIDSTUDIOOFC/projeto-manhattan/main/images/FOTO-3.jpg",
        "https://raw.githubusercontent.com/GRIDSTUDIOOFC/projeto-manhattan/main/images/FOTO-4.jpg",
        "https://raw.githubusercontent.com/GRIDSTUDIOOFC/projeto-manhattan/main/images/FOTO-5.jpg",
        "https://raw.githubusercontent.com/GRIDSTUDIOOFC/projeto-manhattan/main/images/FOTO-6.jpg",
        "https://raw.githubusercontent.com/GRIDSTUDIOOFC/projeto-manhattan/main/images/FOTO-7.jpg",
    ]

    image_list = []
    for url in image_urls:
        img_data = download_image(url)
        if img_data:
            image = ImageTk.PhotoImage(img_data)
            image_list.append(image)
        else:
            print(f"Falha ao baixar a imagem da URL '{url}'. Verifique a URL fornecida.")

    current_image = 0

    def update_image():
        nonlocal current_image
        if current_image < len(image_list):
            canvas.delete("all")
            canvas.create_image(frame_width // 2, frame_height // 2, image=image_list[current_image])
            current_image = (current_image + 1) % len(image_list)
            root.after(5000, update_image)  # Troca de imagem a cada 5 segundos
        else:
            print("Todas as imagens foram exibidas.")

    update_image()

    # Frame para a seleção da versão
    selection_frame = tk.Frame(root, bg="white", padx=4, pady=4, bd=0)
    selection_frame.place(x=10, y=window_height - 60, anchor=tk.W)

    # Título para a seleção, com fonte menor
    tk.Label(selection_frame, text="Versão:", bg="white", font=("Arial", 8)).pack(side=tk.LEFT, padx=5)

    # Combobox menor e mais integrada ao design
    script_version = tk.StringVar(value="versao1")
    version_combobox = ttk.Combobox(selection_frame, textvariable=script_version, values=["Versão 1", "DEMO"], state="readonly", width=10, font=("Arial", 8))
    version_combobox.pack(side=tk.LEFT)

    # Botão START
    start_button = tk.Button(root, text="START", command=lambda: start_loading(root, script_version), bg="white", fg="black", font=("Arial", 12, "bold"), width=8, height=1)
    start_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)  # Ajuste a posição Y

    # Botão de atualização
    update_button = tk.Button(root, text="Verificar Atualizações", command=update_launcher)
    update_button.place(relx=0.9, rely=0.9, anchor=tk.CENTER)  # Colocado abaixo do botão START


    root.mainloop()

def start_loading(root, script_version):
    # Remover a destruição do botão START
    start_button = root.children['!button']

    progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate", length=655, style="Custom.Horizontal.TProgressbar")
    progress_bar.place(relx=0.5, rely=0.9, anchor=tk.CENTER, y=-30)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Custom.Horizontal.TProgressbar", troughcolor='blue', background='blue')

    total_steps = 97
    step_duration = 10

    def update_progress(step):
        progress_bar['value'] = step
        root.update_idletasks()
        if step < total_steps:
            root.after(step_duration, update_progress, step + 1)
        else:
            root.after(500, lambda: progress_bar.destroy())
            # Execute the selected script here instead of showing a new window
            main(script_version.get().lower().replace("versão 1", "versao1"))

    update_progress(0)

def main(script_version):
    if script_version == "versao1":
        script_url = "https://raw.githubusercontent.com/GRIDSTUDIOOFC/projeto-manhattan/main/scripts/SCRIPT.jsx"
    elif script_version == "demo":
        script_url = "https://raw.githubusercontent.com/GRIDSTUDIOOFC/projeto-manhattan/main/scripts/SCRIPT-DEMO.jsx"
    else:
        print("Versão do script desconhecida.")
        return

    temp_dir = tempfile.mkdtemp()
    local_path = os.path.join(temp_dir, "meu_script_ofuscado.jsx")

    def download_file_from_github(url, dest_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(dest_path, 'wb') as file:
                file.write(response.content)
            os.chmod(dest_path, stat.S_IRUSR | stat.S_IWUSR)
            print("Script baixado com sucesso.")
        else:
            print("Falha ao baixar o script.")
            exit(1)

    download_file_from_github(script_url, local_path)

    photoshop_paths = [
        r'C:\Program Files\Adobe\Adobe Photoshop 2024\Photoshop.exe',
        r'C:\Program Files\Adobe\Adobe Photoshop (Beta)\Photoshop.exe'
    ]

    def run_photoshop_script(paths, script_path):
        for path in paths:
            if os.path.exists(path):
                try:
                    subprocess.run([path, '-r', script_path], check=True)
                    print("Script executado com sucesso no Photoshop.")
                    return True
                except subprocess.CalledProcessError as e:
                    print(f"Falha ao executar o script no Photoshop: {e}")
        print("Nenhum caminho válido para o Photoshop encontrado.")
        return False

    def remove_file_with_retries(file_path, retries=5, delay=2):
        for attempt in range(retries):
            try:
                os.remove(file_path)
                print("Script removido com sucesso.")
                return True
            except Exception as e:
                print(f"Falha ao remover o script (tentativa {attempt + 1}/{retries}): {e}")
                time.sleep(delay)
        print("Não foi possível remover o script após várias tentativas.")
        return False

    success = run_photoshop_script(photoshop_paths, local_path)
    
    if not remove_file_with_retries(local_path):
        print("O arquivo ainda existe após várias tentativas.")

    try:
        shutil.rmtree(temp_dir)
        print("Pasta temporária removida com sucesso.")
    except Exception as e:
        print(f"Falha ao remover a pasta temporária: {e}")

    if os.path.exists(local_path):
        print("O arquivo ainda existe. Verificação final falhou.")
    else:
        print("O arquivo foi removido corretamente na verificação final.")
    
    print("O script foi executado e removido com sucesso.")

if __name__ == "__main__":
    show_animation()