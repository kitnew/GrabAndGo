import os

current_dir = os.getcwd()

print(f"Текущая рабочая директория: {current_dir}")

script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Папка скрипта: {script_dir}")