from typing import Literal
from rich import print

def alert(message: str, level: Literal['log', 'warning', 'error', 'success'] = 'log', enter: bool = True):
    match level:
        case 'log':
            print(f'[bright_white]{message}[/bright_white]')
        case 'warning':
            print(f'[bright_yellow]{message}[/bright_yellow]')
        case 'error':
            print(f'[bright_red]{message}[/bright_red]')
        case 'success':
            print(f'[bright_green]{message}[/bright_green]')
        case _:
            print(f'[bright_white]{message}[/bright_white]')

    if enter:
        input("Нажмите ENTER, чтобы продолжить...")
