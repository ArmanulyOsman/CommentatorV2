from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': [],  # Укажи зависимости вручную при необходимости
    'includes': [],  # Например: ['requests', 'numpy']
    'iconfile': None  # сюда можно добавить .icns файл
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
