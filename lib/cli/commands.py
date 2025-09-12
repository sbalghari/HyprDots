import sys


class Commands:
    @staticmethod
    def handle_install(installer) -> None:
        installer.install()

    @staticmethod
    def handle_uninstall(uninstaller) -> None:
        uninstaller.uninstall()

    @staticmethod
    def handle_update(updater) -> None:
        updater.update()

    @staticmethod
    def handle_check_update(updater) -> None:
        updater.check_update()

    @staticmethod
    def handle_no_command(parser) -> None:
        parser.print_help()
        sys.exit(0)
