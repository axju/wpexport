import os
import argparse
from wpexport import WPExport

def main():
    parser = argparse.ArgumentParser(description='Wordpress to GitHub')
    parser.add_argument('--setup', default=False, action='store_true',  help='Create the config file')
    parser.add_argument('--config', type=str, default=WPExport.DEFAULT_CONFIG, help='The config file.')
    parser.add_argument('--local', type=str, help='Export the post to a local folder')
    parser.add_argument('--format', choices=WPExport.FORMATS, default='markdown_github', help='The format')

    for name, info in WPExport.PARAMETER.items():
        parser.add_argument('--'+name, type=str, help=info['help'])

    args = parser.parse_args()
    app = WPExport()

    if args.setup:
        app.cli()
        app.save(args.config)
        exit()

    # load config if exists
    if os.path.exists(args.config): app.load(args.config)

    # load the param from the command line. It ovverid the other parameters
    app.setup(**vars(args))

    # check the parameters
    if not app.check:
        parser.print_help()

    # if the output is set, only export to the folder
    if args.local:
        if os.path.exists(args.local):
            app.export(args.local)
        else:
            print('folder not exists')
        exit()

    # create the backup
    app.backup()


if __name__ == '__main__':
    main()
