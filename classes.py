import os
import requests
from settings import Settings
from exceptions import RepoNotInstalledError, NoConfigFileError

class PackageManager:
    def __init__(self):
        self._settings = Settings()
        self.repos = self._settings.get("repos")

    def install(self, repo_name, custom_path=None):
        if repo_name not in self.repos:
            self.repos[repo_name] = RepoManager(repo_name, custom_path)
        self.repos[repo_name].install()

    def update(self, repo_name):
        if repo_name in self.repos:
            self.repos[repo_name].update()
        else:
            raise RepoNotInstalledError

    def uninstall(self, repo_name):
        if repo_name in self.repos:
            self.repos[repo_name].uninstall()
            del self.repos[repo_name]
        else:
            raise RepoNotInstalledError

    def list(self):
        print("Установленные репозитории:")
        for repo_name in self.repos:
            print(f"- {repo_name}")

        # Сохраняем обновленные данные в settings.json
        self._settings.save({"repos": self.repos})

class RepoManager:
    def __init__(self, repo_name, custom_path=None):
        self.repo_name = repo_name
        self.owner = "HamletSargsyan"
        self.repo_url = f"https://api.github.com/repos/{self.owner}/{repo_name}/releases/latest"
        self.config_file = ".rmconfig"
        self.base_path = os.path.expanduser("~/repos") if custom_path is None else custom_path

    def install(self):
        if not self._check_config_file():
            raise NoConfigFileError

        release_info = self._get_latest_release()
        if release_info:
            download_url = release_info['zipball_url']
            response = requests.get(download_url)
            zip_file_path = os.path.join(self.base_path, f"{self.repo_name}_latest.zip")
            
            with open(zip_file_path, 'wb') as zip_file:
                zip_file.write(response.content)
                
            print(f"{self.repo_name} успешно установлен в {self.base_path}.")

    def update(self):
        if not self._check_config_file():
            raise NoConfigFileError

        self.uninstall()
        self.install()
        print(f"{self.repo_name} успешно обновлен.")

    def uninstall(self):
        zip_file_path = os.path.join(self.base_path, f"{self.repo_name}_latest.zip")
        if os.path.exists(zip_file_path):
            os.remove(zip_file_path)
            print(f"{self.repo_name} успешно удален.")
        else:
            print(f"{self.repo_name} не найден.")

    def _get_latest_release(self):
        response = requests.get(self.repo_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Не удалось получить информацию о последнем релизе {self.repo_name}.")

    def _check_config_file(self) -> bool:
        config_file_url = f"https://raw.githubusercontent.com/{self.owner}/{self.repo_name}/main/{self.config_file}"
        response = requests.get(config_file_url)

        if response.status_code == 200:
            config_file_path = os.path.join(self.base_path, self.repo_name, self.config_file)
            os.makedirs(os.path.dirname(config_file_path), exist_ok=True)
            
            with open(config_file_path, 'wb') as config_file:
                config_file.write(response.content)
            return True
        else:
            return False
