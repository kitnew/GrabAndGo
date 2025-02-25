import os
import yaml
import importlib
import sys

def load_templates():
    """Загружает все шаблоны из папки config/templates."""
    templates = []
    for file in os.listdir('/home/nikitachernysh/Projects/GrabAndGo/config/templates'):
        if file.endswith('.yaml'):
            with open(os.path.join('/home/nikitachernysh/Projects/GrabAndGo/config/templates', file), 'r') as f:
                templates.append(yaml.safe_load(f))
    return templates

def get_template_for_url(url):
    """Возвращает подходящий шаблон для указанного URL."""
    domain = url.split("/")[2]
    templates = load_templates()
    for template in templates:
        if template['domain'] in domain:
            return template
    raise ValueError(f"No template found for domain: {domain}")

def get_instructions_for_url(url):
    """Загружает соответствующие инструкции для данного URL."""
    domain = url.split("/")[2].split(".")[-2]  # Получаем домен

    # Добавляем путь к конфигурационному каталогу в sys.path
    config_path = os.path.join(os.path.dirname(__file__), '../../config/instructions')
    sys.path.append(config_path)

    try:
        # Загружаем инструкцию для домена
        module = importlib.import_module(domain)  # Импортируем инструкцию по имени домена
        return module
    except ModuleNotFoundError:
        raise ValueError(f"No instructions found for domain: {domain}")

def parse_url(url, is_post=False):
    """Главная функция для парсинга, которая адаптирует сайт и его шаблон."""
    domain = "https://" + url.split("/")[2]  # Получаем домен
    template = get_template_for_url(url)  # Получаем шаблон
    instructions = get_instructions_for_url(url)  # Получаем инструкции

    if not is_post:
        # Если это папка, используем инструкцию для папки
        media = instructions.parse_folder(url, domain, template['selectors'])
    else:
        # Если это пост, используем инструкцию для поста
        media = instructions.parse_post(url, template['selectors'])

    return media