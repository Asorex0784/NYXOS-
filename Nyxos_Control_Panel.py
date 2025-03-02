import os
import time
import sys
import subprocess
import logging
import hashlib
import importlib

# ANSI renk kodları
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_BLUE = "\033[34m"
COLOR_MAGENTA = "\033[35m"
COLOR_CYAN = "\033[36m"
COLOR_WHITE = "\033[37m"
COLOR_BOLD = "\033[1m"

def slow_type(text, color=COLOR_MAGENTA, speed=0.03):
    """Renkli ve yavaş yazı efekti"""
    print(color, end='')
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print(COLOR_RESET, end='')

def draw_box(width, lines, border_color=COLOR_MAGENTA):
    """Geliştirilmiş kutu çizme fonksiyonu"""
    # Üst kenar
    print(border_color + '┌' + '─'*(width-2) + '┐' + COLOR_RESET)
    
    # İçerik
    for line in lines:
        print(border_color + '│' + COLOR_RESET + ' ' + line.ljust(width-4) + ' ' + border_color + '│' + COLOR_RESET)
    
    # Alt kenar
    print(border_color + '└' + '─'*(width-2) + '┘' + COLOR_RESET)

def list_files(directory):
    """Dosya listeleme"""
    try:
        return "\n".join(os.listdir(directory))
    except Exception as e:
        return f"Hata: {str(e)}"

def write_file(directory, filename, content):
    """Dosya yazma"""
    try:
        file_path = os.path.join(directory, filename + ".txt")
        with open(file_path, "w") as file:
            file.write(content)
        return f"{file_path} başarıyla oluşturuldu."
    except Exception as e:
        return f"Hata: {str(e)}"

def delete_file(directory, filename):
    """Dosya silme"""
    try:
        file_path = os.path.join(directory, filename + ".txt")
        if os.path.exists(file_path):
            os.remove(file_path)
            return f"{file_path} silindi."
        return "Dosya bulunamadı."
    except Exception as e:
        return f"Hata: {str(e)}"

def ping_ip(ip):
    """Ping at"""
    try:
        result = subprocess.run(['ping', '-c', '4', ip], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Hata: {str(e)}"

def check_permissions(directory):
    """Güvenlik taraması"""
    try:
        insecure_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if os.stat(file_path).st_mode & 0o777 == 0o777:  # Herkese açık dosyalar
                    insecure_files.append(file_path)
        return "\n".join(insecure_files) if insecure_files else "Güvenli: Herkese açık dosya bulunamadı."
    except Exception as e:
        return f"Hata: {str(e)}"

def log_action(action):
    """Günlük kaydı"""
    try:
        logging.basicConfig(filename='panel.log', level=logging.INFO, format='%(asctime)s - %(message)s')
        logging.info(action)
        return "İşlem günlüğe kaydedildi."
    except Exception as e:
        return f"Hata: {str(e)}"

def hash_password(password):
    """Şifre hashleme"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_account(username, password):
    """Hesap oluşturma"""
    try:
        with open("accounts.txt", "a") as file:
            file.write(f"{username}:{hash_password(password)}\n")
        return "Hesap başarıyla oluşturuldu."
    except Exception as e:
        return f"Hata: {str(e)}"

def login(username, password):
    """Hesaba giriş yapma"""
    try:
        with open("accounts.txt", "r") as file:
            for line in file:
                stored_username, stored_password = line.strip().split(":")
                if username == stored_username and hash_password(password) == stored_password:
                    return "Giriş başarılı!"
        return "Giriş başarısız!"
    except Exception as e:
        return f"Hata: {str(e)}"

def delete_account(username, password):
    """Hesap silme"""
    try:
        with open("accounts.txt", "r") as file:
            lines = file.readlines()
        with open("accounts.txt", "w") as file:
            deleted = False
            for line in lines:
                stored_username, stored_password = line.strip().split(":")
                if username == stored_username and hash_password(password) == stored_password:
                    deleted = True
                else:
                    file.write(line)
            return "Hesap başarıyla silindi." if deleted else "Hesap bulunamadı veya şifre yanlış."
    except Exception as e:
        return f"Hata: {str(e)}"

def delete_all_accounts():
    """Tüm hesapları silme"""
    try:
        with open("accounts.txt", "w") as file:
            file.write("")
        return "Tüm hesaplar başarıyla silindi."
    except Exception as e:
        return f"Hata: {str(e)}"

def add_ip(ip):
    """IP ekleme"""
    try:
        with open("ips.txt", "a") as file:
            file.write(f"{ip}\n")
        return f"{ip} başarıyla eklendi."
    except Exception as e:
        return f"Hata: {str(e)}"

def list_ips():
    """Kayıtlı IP'leri listeleme"""
    try:
        with open("ips.txt", "r") as file:
            ips = file.readlines()
        return "Kayıtlı IP'ler:\n" + "".join(ips) if ips else "Kayıtlı IP bulunamadı."
    except FileNotFoundError:
        return "Kayıtlı IP bulunamadı."
    except Exception as e:
        return f"Hata: {str(e)}"

def delete_ip(ip):
    """IP silme"""
    try:
        with open("ips.txt", "r") as file:
            lines = file.readlines()
        with open("ips.txt", "w") as file:
            deleted = False
            for line in lines:
                if line.strip() != ip:
                    file.write(line)
                else:
                    deleted = True
            return f"{ip} başarıyla silindi." if deleted else "IP bulunamadı."
    except FileNotFoundError:
        return "Kayıtlı IP bulunamadı."
    except Exception as e:
        return f"Hata: {str(e)}"

def add_plugin(plugin_name):
    """Eklenti ekleme"""
    try:
        with open("plugins.txt", "a") as file:
            file.write(f"{plugin_name}\n")
        return f"{plugin_name} başarıyla eklendi."
    except Exception as e:
        return f"Hata: {str(e)}"

def list_plugins():
    """Eklentileri listeleme"""
    try:
        with open("plugins.txt", "r") as file:
            plugins = file.readlines()
        return "Eklentiler:\n" + "".join(plugins) if plugins else "Eklenti bulunamadı."
    except FileNotFoundError:
        return "Eklenti bulunamadı."
    except Exception as e:
        return f"Hata: {str(e)}"

def delete_plugin(plugin_name):
    """Eklenti silme"""
    try:
        with open("plugins.txt", "r") as file:
            lines = file.readlines()
        with open("plugins.txt", "w") as file:
            deleted = False
            for line in lines:
                if line.strip() != plugin_name:
                    file.write(line)
                else:
                    deleted = True
            return f"{plugin_name} başarıyla silindi." if deleted else "Eklenti bulunamadı."
    except FileNotFoundError:
        return "Eklenti bulunamadı."
    except Exception as e:
        return f"Hata: {str(e)}"

def main():
    menu_items = [
        ("Dosya İşlemleri", [
            ("Dosya Yaz", "Belirtilen dizine dosya yazma işlemi."),
            ("Dosya Sil", "Belirtilen dizinden dosya silme işlemi.")
        ]),
        ("Ağ Taraması", [
            ("Ağ Taraması Yap", "Belirtilen IP'ye ping atma işlemi."),
            ("IP Ekle", "Yeni bir IP ekleme işlemi."),
            ("Kayıtlı IP'leri Göster", "Kayıtlı IP'leri listeleme işlemi."),
            ("IP Sil", "Kayıtlı bir IP'yi silme işlemi.")
        ]),
        ("Güvenlik Taraması", "Güvenlik açıkları taranıyor..."),
        ("Kullanıcı Hesaplarını Yönet", [
            ("Hesap Oluştur", "Yeni bir hesap oluşturma işlemi."),
            ("Hesaba Giriş Yap", "Varolan bir hesaba giriş yapma işlemi."),
            ("Hesap Sil", "Varolan bir hesabı silme işlemi."),
            ("Hesapları Sil", "Tüm hesapları silme işlemi.")
        ]),
        ("Eklenti Yönetimi", [
            ("Eklenti Ekle", "Yeni bir eklenti ekleme işlemi."),
            ("Eklentileri Listele", "Kayıtlı eklentileri listeleme işlemi."),
            ("Eklenti Sil", "Kayıtlı bir eklentiyi silme işlemi.")
        ]),
        ("Çıkış", "Sistem kapatılıyor...")
    ]
    
    selected = 0
    sub_selected = 0
    in_sub_menu = False
    message = []
    panel_width = 60
    exit_flag = False

    while not exit_flag:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Başlık
        print(COLOR_MAGENTA + COLOR_BOLD + "\n" + "┌" + "─"*(panel_width-2) + "┐")
        print("│" + " NYXOS SYSTEM CONTROL PANEL ".center(panel_width-2, '░') + "│")
        print("└" + "─"*(panel_width-2) + "┘" + COLOR_RESET)
        
        # Menü
        menu_lines = []
        if in_sub_menu:
            # Alt menüyü göster
            for i, (sub_title, _) in enumerate(menu_items[selected][1]):
                prefix = COLOR_GREEN + "➤ " if i == sub_selected else "  "
                menu_lines.append(prefix + COLOR_WHITE + sub_title.ljust(panel_width-6) + COLOR_RESET)
        else:
            # Ana menüyü göster
            for i, (title, _) in enumerate(menu_items):
                prefix = COLOR_GREEN + "➤ " if i == selected else "  "
                menu_lines.append(prefix + COLOR_WHITE + title.ljust(panel_width-6) + COLOR_RESET)
        
        draw_box(panel_width, menu_lines, COLOR_MAGENTA)
        
        # Bilgi Paneli
        print(COLOR_MAGENTA + '┌' + '─'*(panel_width-2) + '┐' + COLOR_RESET)
        print(COLOR_MAGENTA + '│' + COLOR_RESET + ' ', end='')
        if message:
            print(message[0].ljust(panel_width-4), end='')
        else:
            print("Lütfen bir işlem seçiniz...".ljust(panel_width-4), end='')
        print(' ' + COLOR_MAGENTA + '│' + COLOR_RESET)
        print(COLOR_MAGENTA + '└' + '─'*(panel_width-2) + '┘' + COLOR_RESET)
        
        # Kullanıcı girişi (Pydroid 3 uyumlu)
        try:
            key = input("Seçiniz: ").strip().lower()
        except EOFError:
            print(COLOR_RED + "\nÇıkış yapılıyor..." + COLOR_RESET)
            break
        
        if key == 'w':
            if in_sub_menu:
                if sub_selected > 0:
                    sub_selected -= 1
                else:
                    sub_selected = len(menu_items[selected][1]) - 1  # En üste dön
            else:
                if selected > 0:
                    selected -= 1
                else:
                    selected = len(menu_items) - 1  # En üste dön
            message = []
        elif key == 's':
            if in_sub_menu:
                if sub_selected < len(menu_items[selected][1]) - 1:
                    sub_selected += 1
                else:
                    sub_selected = 0  # En üste dön
            else:
                if selected < len(menu_items) - 1:
                    selected += 1
                else:
                    selected = 0  # En üste dön
            message = []
        elif key == 'a':
            if in_sub_menu:
                in_sub_menu = False
            message = []
        elif key == 'd':
            if not in_sub_menu and isinstance(menu_items[selected][1], list):
                in_sub_menu = True
                sub_selected = 0  # Alt menüye girince ilk seçenek seçili olsun
            message = []
        elif key == 'q':
            if in_sub_menu:
                in_sub_menu = False  # Alt menüden çık
            else:
                exit_flag = True  # Sistemden çık
                print(COLOR_RED + "\nÇıkış yapılıyor..." + COLOR_RESET)
                time.sleep(1)
                continue
            message = []
        elif key == '':
            if in_sub_menu:
                if selected == 0:  # Dosya İşlemleri
                    if sub_selected == 0:  # Dosya Yaz
                        directory = input("Dizin yolunu girin: ")
                        filename = input("Dosya adını girin: ")
                        content = input("Dosya içeriğini girin: ")
                        message = [write_file(directory, filename, content)]
                    elif sub_selected == 1:  # Dosya Sil
                        directory = input("Dizin yolunu girin: ")
                        filename = input("Dosya adını girin: ")
                        message = [delete_file(directory, filename)]
                elif selected == 1:  # Ağ Taraması
                    if sub_selected == 0:  # Ağ Taraması Yap
                        ip = input("Ping atılacak IP: ")
                        message = [ping_ip(ip)]
                    elif sub_selected == 1:  # IP Ekle
                        ip = input("Eklemek istediğiniz IP: ")
                        message = [add_ip(ip)]
                    elif sub_selected == 2:  # Kayıtlı IP'leri Göster
                        message = [list_ips()]
                    elif sub_selected == 3:  # IP Sil
                        ip = input("Silmek istediğiniz IP: ")
                        message = [delete_ip(ip)]
                elif selected == 3:  # Kullanıcı Hesaplarını Yönet
                    if sub_selected == 0:  # Hesap Oluştur
                        username = input("Kullanıcı adı: ")
                        password = input("Şifre: ")
                        message = [create_account(username, password)]
                    elif sub_selected == 1:  # Hesaba Giriş Yap
                        username = input("Kullanıcı adı: ")
                        password = input("Şifre: ")
                        message = [login(username, password)]
                    elif sub_selected == 2:  # Hesap Sil
                        username = input("Kullanıcı adı: ")
                        password = input("Şifre: ")
                        message = [delete_account(username, password)]
                    elif sub_selected == 3:  # Hesapları Sil
                        message = [delete_all_accounts()]
                elif selected == 4:  # Eklenti Yönetimi
                    if sub_selected == 0:  # Eklenti Ekle
                        plugin_name = input("Eklenti adı: ")
                        message = [add_plugin(plugin_name)]
                    elif sub_selected == 1:  # Eklentileri Listele
                        message = [list_plugins()]
                    elif sub_selected == 2:  # Eklenti Sil
                        plugin_name = input("Silmek istediğiniz eklenti: ")
                        message = [delete_plugin(plugin_name)]
                slow_type("\n" + "»"*20 + " İşlem Başlatılıyor " + "«"*20 + "\n", COLOR_MAGENTA)
                time.sleep(1)
            else:
                if selected == len(menu_items) - 1:
                    exit_flag = True
                    print(COLOR_RED + "\nÇıkış yapılıyor..." + COLOR_RESET)
                    time.sleep(1)
                    continue
                elif isinstance(menu_items[selected][1], list):
                    in_sub_menu = True
                    sub_selected = 0  # Alt menüye girince ilk seçenek seçili olsun
                else:
                    _, msg = menu_items[selected]
                    if selected == 2:  # Güvenlik Taraması
                        directory = input("Taranacak dizin: ")
                        message = [check_permissions(directory)]
                    else:
                        message = [msg]
                    slow_type("\n" + "»"*20 + " İşlem Başlatılıyor " + "«"*20 + "\n", COLOR_MAGENTA)
                    time.sleep(1)

if __name__ == "__main__":
    main()