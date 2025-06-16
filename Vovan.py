# -*- coding: utf-8 -*-

# VOVAN TOOLKIT v2.0 (Final Cut)
# Coded exclusively for Vladimir from Andrey.

import os
import platform
import socket
import secrets
import string
import time
import shutil
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.live import Live
from rich.spinner import Spinner

try:
    import psutil
    import requests
    from cryptography.fernet import Fernet
    import qrcode
    from PIL import Image
except ImportError:
    print("Ошибка: Необходимые библиотеки не найдены.")
    print("Пожалуйста, выполните команды установки, указанные на сайте.")
    exit()

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    clear_screen()
    console.print(Panel(f"[bold magenta]VOVAN TOOLKIT v2.0[/bold magenta]\n{title}", style="bold cyan", padding=(1, 2)))
    console.print()

def processing_status(text, delay):
    with console.status(f"[bold yellow]{text}", spinner="dots12") as status:
        time.sleep(delay)

def module_system_scanner():
    print_header("Модуль 1: System Scanner")
    processing_status("Анализ системных метрик...", 2)
    
    uname = platform.uname()
    table = Table(title="[bold green]Базовая информация о Системе[/bold green]", show_header=False, box=None)
    table.add_column("Параметр", style="cyan", no_wrap=True)
    table.add_column("Значение", style="white")
    table.add_row("Система", f"{uname.system} {uname.release}")
    table.add_row("Имя компьютера", uname.node)
    table.add_row("Процессор", uname.processor)
    console.print(Panel(table, border_style="green"))

    with Live(Spinner("bouncingBar", text="Считываю загрузку ЦП в реальном времени..."), refresh_per_second=10) as live:
        cpu_percs = psutil.cpu_percent(percpu=True, interval=1)
        time.sleep(1) # a little more time for effect
    cpu_table = Table(title="[bold green]Загрузка ЦП[/bold green]", box=None)
    cpu_table.add_column("Ядро", style="cyan")
    cpu_table.add_column("Загрузка", style="white")
    for i, percentage in enumerate(cpu_percs):
        cpu_table.add_row(f"Ядро {i+1}", f"{percentage}%")
    console.print(Panel(cpu_table, border_style="green"))
    
    mem = psutil.virtual_memory()
    mem_table = Table(title="[bold green]Оперативная память (RAM)[/bold green]", show_header=False, box=None)
    mem_table.add_column("Параметр", style="cyan")
    mem_table.add_column("Значение", style="white")
    mem_table.add_row("Всего", f"{mem.total / (1024**3):.2f} GB")
    mem_table.add_row("Используется", f"{mem.used / (1024**3):.2f} GB ({mem.percent}%)")
    console.print(Panel(mem_table, border_style="green"))
    
    Prompt.ask("\n[yellow]Нажмите Enter для возврата в меню...[/yellow]")

def module_qr_generator():
    print_header("Модуль 6: QR Code Generator")
    data = Prompt.ask("[cyan]Введите текст или ссылку для кодирования в QR[/cyan]")
    processing_status("Генерация изображения...", 1.5)
    
    try:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        filename = "qr_code.png"
        img.save(filename)
        console.print(Panel(f"[bold green]Успех! QR-код сохранен в файл [white]'{filename}'[/white] в этой же папке.[/bold green]", border_style="green"))
    except Exception as e:
        console.print(f"[red]Не удалось создать QR-код. Ошибка: {e}[/red]")
    Prompt.ask("\n[yellow]Нажмите Enter для возврата в меню...[/yellow]")

# ... (Остальные модули остаются такими же, как в предыдущей версии) ...
# Код для модулей 2, 3, 4, 5 (Network, File, Encryptor, Password) можно скопировать из предыдущего ответа
# Я вставлю их сюда для полноты картины.

def module_network_tools():
    # ... (код без изменений)
    while True:
        print_header("Модуль 2: Network Tools")
        choice = IntPrompt.ask(
            "[bold]Выберите инструмент:[/bold]\n"
            "1. Пинг хоста\n"
            "2. Информация об IP-адресе\n"
            "3. Узнать свой IP\n"
            "0. Назад в главное меню",
            choices=["1", "2", "3", "0"],
            show_choices=False
        )
        if choice == 1:
            host = Prompt.ask("[cyan]Введите адрес для пинга (напр. google.com)[/cyan]")
            clear_screen()
            console.print(f"Пингую {host}...")
            os.system(f"ping {host}")
            Prompt.ask("\n[yellow]Нажмите Enter для продолжения...[/yellow]")
        elif choice == 2:
            ip = Prompt.ask("[cyan]Введите IP-адрес для анализа[/cyan]")
            processing_status(f"Запрос информации для {ip}...", 1)
            try:
                response = requests.get(f"https://ipinfo.io/{ip}/json")
                response.raise_for_status()
                data = response.json()
                table = Table(title=f"Информация о {ip}", show_header=False)
                for key, value in data.items():
                    table.add_row(str(key).capitalize(), str(value))
                console.print(table)
            except Exception as e:
                console.print(f"[red]Ошибка: Не удалось получить информацию. {e}[/red]")
            Prompt.ask("\n[yellow]Нажмите Enter для продолжения...[/yellow]")
        elif choice == 3:
            processing_status("Определение адресов...", 1)
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
                s.close()
                public_ip = requests.get('https://api.ipify.org').text
                console.print(f"[green]Ваш локальный IP:[/green] [bold white]{local_ip}[/bold white]")
                console.print(f"[green]Ваш публичный IP:[/green] [bold white]{public_ip}[/bold white]")
            except Exception as e:
                console.print(f"[red]Не удалось определить IP. Проверьте подключение к сети. {e}[/red]")
            Prompt.ask("\n[yellow]Нажмите Enter для продолжения...[/yellow]")
        elif choice == 0:
            break

def module_file_manager():
    # ... (код без изменений)
    def sort_files(directory):
        EXT_MAP = {
            'Изображения': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
            'Документы': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx'],
            'Архивы': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'Музыка': ['.mp3', '.wav', '.ogg', '.flac'],
            'Видео': ['.mp4', '.avi', '.mkv', '.mov'],
        }
        with console.status("[bold yellow]Сортировка...", spinner="earth") as status:
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isfile(item_path):
                    file_ext = os.path.splitext(item)[1].lower()
                    moved = False
                    for folder, exts in EXT_MAP.items():
                        if file_ext in exts:
                            target_folder = os.path.join(directory, folder)
                            if not os.path.exists(target_folder):
                                os.makedirs(target_folder)
                            shutil.move(item_path, target_folder)
                            console.print(f"Перемещен [green]{item}[/green] -> [blue]{folder}[/blue]")
                            moved = True
                            break
            time.sleep(1)
        console.print("[bold green]Сортировка завершена![/bold green]")

    print_header("Модуль 3: File Manager Pro")
    path = Prompt.ask("[cyan]Введите путь к папке для сортировки (оставьте пустым для 'Загрузок')[/cyan]")
    if not path:
        path = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    if not os.path.isdir(path):
        console.print(f"[red]Ошибка: Папка '{path}' не найдена.[/red]")
    else:
        console.print(f"Выбрана папка: [bold yellow]{path}[/bold yellow]")
        if Prompt.ask("[bold red]Начать сортировку? Это действие необратимо.[/bold red] (y/n)").lower() == 'y':
            sort_files(path)
    Prompt.ask("\n[yellow]Нажмите Enter для возврата в меню...[/yellow]")

def module_data_encryptor():
    # ... (код без изменений)
    print_header("Модуль 4: Data Encryptor (алгоритм Fernet)")
    choice = IntPrompt.ask(
        "[bold]Выберите действие:[/bold]\n"
        "1. Сгенерировать новый ключ шифрования\n"
        "2. Зашифровать сообщение\n"
        "3. Расшифровать сообщение",
        choices=["1","2","3"], show_choices=False
    )
    if choice == 1:
        key = Fernet.generate_key()
        console.print(Panel(f"[bold]ВАШ НОВЫЙ КЛЮЧ:[/bold]\n{key.decode()}\n\n[red]Сохраните его в надежном месте! Без него данные не восстановить.[/red]", title="Ключ Сгенерирован", border_style="green"))
    elif choice == 2:
        key_str = Prompt.ask("[cyan]Вставьте ваш ключ шифрования[/cyan]")
        message = Prompt.ask("[cyan]Введите сообщение для шифрования[/cyan]")
        try:
            f = Fernet(key_str.encode())
            encrypted = f.encrypt(message.encode())
            console.print(Panel(f"[bold]ЗАШИФРОВАННОЕ СООБЩЕНИЕ:[/bold]\n{encrypted.decode()}", title="Готово", border_style="green"))
        except Exception:
            console.print("[red]Ошибка: Неверный ключ.[/red]")
    elif choice == 3:
        key_str = Prompt.ask("[cyan]Вставьте ваш ключ шифрования[/cyan]")
        encrypted_message = Prompt.ask("[cyan]Вставьте зашифрованное сообщение[/cyan]")
        try:
            f = Fernet(encrypted_message.encode())
            decrypted = f.decrypt(encrypted_message.encode())
            console.print(Panel(f"[bold]РАСШИФРОВАННОЕ СООБЩЕНИЕ:[/bold]\n{decrypted.decode()}", title="Готово", border_style="green"))
        except Exception:
            console.print("[red]Ошибка: Неверный ключ или поврежденные данные.[/red]")
    Prompt.ask("\n[yellow]Нажмите Enter для возврата в меню...[/yellow]")

def module_password_forge():
    # ... (код без изменений)
    print_header("Модуль 5: Password Forge")
    length = IntPrompt.ask("[cyan]Введите длину пароля[/cyan]", default=16)
    use_upper = Prompt.ask("[cyan]Включить заглавные буквы? (y/n)[/cyan]", default='y').lower() == 'y'
    use_digits = Prompt.ask("[cyan]Включить цифры? (y/n)[/cyan]", default='y').lower() == 'y'
    use_symbols = Prompt.ask("[cyan]Включить спецсимволы? (y/n)[/cyan]", default='y').lower() == 'y'

    alphabet = string.ascii_lowercase
    if use_upper: alphabet += string.ascii_uppercase
    if use_digits: alphabet += string.digits
    if use_symbols: alphabet += string.punctuation
    
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    console.print(Panel(f"[bold green]Сгенерированный пароль:[/bold green]\n\n[bold white on black] {password} [/bold white on black]", title="Готово", border_style="green"))
    Prompt.ask("\n[yellow]Нажмите Enter для возврата в меню...[/yellow]")

def main():
    clear_screen()
    console.print(Panel("""
[bold cyan]VOVAN TOOLKIT v2.0[/bold cyan]
[white]Загрузка завершена... Все модули в состоянии готовности.[/white]
[italic blue]Эксклюзивно для Владимира от Андрея.[/italic blue]
""", style="bold cyan", title="СИСТЕМА АКТИВНА"))
    
    while True:
        console.print("\n[bold]ГЛАВНОЕ МЕНЮ:[/bold]")
        choice = IntPrompt.ask(
            "1. System Scanner\n"
            "2. Network Tools\n"
            "3. File Manager Pro\n"
            "4. Data Encryptor\n"
            "5. Password Forge\n"
            "6. [bold magenta]QR Code Generator (NEW!)[/bold magenta]\n"
            "0. Выход",
            choices=["1", "2", "3", "4", "5", "6", "0"],
            show_choices=False
        )
        
        if choice == 1: module_system_scanner()
        elif choice == 2: module_network_tools()
        elif choice == 3: module_file_manager()
        elif choice == 4: module_data_encryptor()
        elif choice == 5: module_password_forge()
        elif choice == 6: module_qr_generator()
        elif choice == 0:
            console.print("[bold yellow]Завершение работы...[/bold yellow]")
            time.sleep(1)
            break
        
        clear_screen()
        console.print(Panel("[bold cyan]VOVAN TOOLKIT v2.0[/bold cyan]", style="bold cyan"))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Работа прервана пользователем. Аварийный выход.[/bold red]")