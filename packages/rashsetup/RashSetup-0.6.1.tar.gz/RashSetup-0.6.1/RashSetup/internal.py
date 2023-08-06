import importlib
import sys
import subprocess
import sqlite3
import pathlib
import shutil
import logging
import typing

import RashSetup as RashSetup

from .crawlers import *

__all__ = ["ModuleManager", "DBManager"]

__all__.extend(ALL)


class ModulePathManager:
    def __init__(self):
        self.mod = pathlib.Path(__file__).parent / "__RashModules__"
        self.mod.mkdir(exist_ok=True)

        _ = self.mod / "__init__.py"
        None if _.exists() else _.write_text("")

    def check_module(self, name, path=None):
        path = path if path else self.mod
        return all(
            (
                (path / name).exists(),
                (path / name / "__init__.py").exists(),
                (path / name / "settings.json").exists(),
            )
        )

    def uninstall_module(self, name):
        shutil.rmtree(self.mod / name)

    def gen_path(self, name, create=True):
        mod = self.mod / name
        mod.mkdir(exist_ok=True) if create else None
        return self.mod / name

    def settings(self, module):
        return SettingsParser(self.gen_path(module) / "settings.json", True)


class DBManager(ModulePathManager):
    def __init__(self):
        super().__init__()
        self.sql = self.mod.parent / "__RashSQL__.sql"
        self.connector = sqlite3.connect(
            self.mod / "__RashModules__.db", check_same_thread=False
        )

        self.__start()

    def cursor(self):
        return self.connector.cursor()

    def __start(self):
        temp = self.cursor()
        temp.executescript(self.sql.read_text())
        self.connector.commit()

    def sql_code(self, code, *args) -> tuple:
        return self.execute_one_line(
            *self.execute_one_line(
                "SELECT SQL, Empty FROM Sql WHERE Hash = ?", False, code
            ),
            *args
        )

    def execute_one_line(self, script, all_=False, *args):
        temp = self.cursor()
        temp.execute(script, args)

        return temp.fetchall() if all_ else temp.fetchone()

    def commit(self):
        self.connector.commit()

    def close(self):
        self.connector.close()

    def downloaded(self, name, hosted, version, readme):
        print(self.sql_code(10, name, hosted, version, readme), "#$")
        self.commit()

    def update_settings(self, name, version, readme=None):
        self.sql_code(8, version, name)
        self.sql_code(9, readme, name) if readme else None

        self.commit()


class HeavyModuleManager(DBManager):
    def download(self, name: str, url: typing.Optional[str] = None, _=None):
        url = url if url else self.sql_code(3, name)[0]
        path = str(self.gen_path(name))

        setup = RawSetup(RepoSetup, url, path)
        setup.process.start()
        setup.process.join()

        return setup.parse()

    def grab_readme(self, url):
        setup = RawSetup(READMESetup, url)
        setup.process.start()
        setup.process.join()

        status, result = setup.parse()

        if not status:
            return ""

        return result

    def check_for_update(self, *args, **_):
        pass

    def update_settings(self, settings: SettingsParser, *_) -> None:
        return super().update_settings(
            settings.name(), settings.version(), settings.readme()
        )


class ModuleManager(HeavyModuleManager):
    def __init__(self):
        super().__init__()

    def check(self):
        for module in self.sql_code(1):
            module: str = module[0]

            if self.check_module(module):
                continue

            yield module


class RashRawSetup(ModuleManager):
    def __init__(self):
        super().__init__()
        self.root = format_root()

        self.start()

    def setup(self, module):
        self.root.info("Downloading Missing Module %s", module)

        # downloads Modules
        status, result = self.download(module)
        assert status, result

        # exacts settings
        settings = self.settings(module)

        # installs requires
        assert settings.install_required()

        # downloads readme part
        temp = self.grab_readme(settings.readme())
        settings.update_readme(temp) if temp else None

        # updates to database
        self.root.debug("Downloaded %s, updating details to database", module)
        self.update_settings(settings)

    def block(self):
        # informs failure
        self.root.critical(
            "Failed to start Rash because of the above exception. Please try again."
        )
        self.root.info(
            "If you find this unreasonable, please raise an issue at: https://github.com/RahulARanger/RashSetup"
        )

        # blocks
        while True:
            pass

    def start(self):
        self.root.info("Starting RashSetup!")

        # Downloads if missing
        passed = True
        for module in self.check():
            try:
                self.setup(module)
            except Exception as _:
                self.root.exception("Failed to Download %s", module, exc_info=True)
                passed = False
                break

        None if passed else self.block()


class RawRashSetup(DBManager):
    def __init__(self, exe=None):
        super().__init__()

        self.logger = format_root()
        self.logger.info("Scanning Modules")

        self.start(exe)

    def python(self):
        possible = pathlib.Path(sys.executable).parent.parent / "Scripts"

        temp = None

        for p in possible.iterdir():
            if p.stem == "python":
                temp = p
                break

            temp = p if p.stem == "python3" else None

        self.logger.info("redirecting to %s", temp) if temp else self.logger.critical("python not found %s", temp)
        return temp

    def check(self):
        for module in self.sql_code(1):
            if not self.check_module(module[0]):
                return True

        return False

    def start(self, exe):
        if self.check():
            self.fetch(exe)

        skip_code = """
import RashSetup.__RashModules__.Rash.Start as Rash
setup = Rash.Start()
sys.exit(0)
        """

        subprocess.Popen([
            exe if exe else self.python(), "-c", skip_code
        ])

    def fetch(self, exe):
        self.logger.info("Some Modules are missing, Downloading them")

        skip_code = """
import RashSetup.internal as Setup
setup = Setup.RashRawSetup()
        """

        try:
            subprocess.run([
                exe if exe else self.python(), "-c", skip_code
            ], check=True)
        except Exception as _:
            self.logger.exception("Failed to Download Rash Modules", exc_info=True)
            while True:
                pass
