import argparse
from classes import PackageManager

def main():
    parser = argparse.ArgumentParser(description="Package Manager for repositories")
    parser.add_argument("command", choices=["install", "update", "uninstall", "list"], nargs="?")
    parser.add_argument("repo_name", nargs="?")
    parser.add_argument("--custom_path", help="Specify custom path for repository installation")

    args = parser.parse_args()

    package_manager = PackageManager()

    if args.command == "install":
        repo_name = args.repo_name or input("Введите имя репозитория: ")
        custom_path = args.custom_path or input("Введите кастомный путь (оставьте пустым для использования домашней директории): ")
        package_manager.install(repo_name, custom_path)

    elif args.command == "update":
        repo_name = args.repo_name or input("Введите имя репозитория: ")
        package_manager.update(repo_name)

    elif args.command == "uninstall":
        repo_name = args.repo_name or input("Введите имя репозитория: ")
        package_manager.uninstall(repo_name)

    elif args.command == "list":
        package_manager.list()

if __name__ == "__main__":
    main()
