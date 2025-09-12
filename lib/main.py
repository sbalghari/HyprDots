from core.installer import HyprDotsInstaller
from core.uninstaller import HyprDotsUninstaller
from core.updater import HyprDotsUpdater
from cli.arg_parser import ArgumentParser
from cli.commands import Commands

def main():
    # Main components
    installer = HyprDotsInstaller(dry_run=False)
    uninstaller = HyprDotsUninstaller(dry_run=False)
    updater = HyprDotsUpdater(dry_run=False)
    
    # cli
    parser = ArgumentParser.create_parser()
    args = parser.parse_args()

    if args.install:
        Commands.handle_install(installer)
    elif args.remove:
        Commands.handle_uninstall(uninstaller)
    elif args.update:
        Commands.handle_update(updater)
    elif args.check_update:
        Commands.handle_check_update(updater)
    else:
        Commands.handle_no_command(parser)

if __name__ == "__main__":
    main()