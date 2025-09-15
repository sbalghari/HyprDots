from core.installer import SBDotsInstaller
from core.uninstaller import SBDotsUninstaller
from core.updater import SBDotsUpdater
from cli.arg_parser import ArgumentParser
from cli.commands import Commands

def main():
    # Main components
    installer = SBDotsInstaller(dry_run=False)
    uninstaller = SBDotsUninstaller(dry_run=False)
    updater = SBDotsUpdater(dry_run=False)
    
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