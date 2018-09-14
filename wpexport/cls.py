import os
import json
import logging
import git
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods.posts import GetPosts
import pypandoc

class WPExport(object):
    """docstring for wpexport."""

    PARAMETER = {
        'wp_url': {'help': 'The root url to yout Wordpress'},
        'wp_user': {'help': 'The Wordpress user'},
        'wp_pw': {'help': 'The password of the Wordpress user'},
        'folder': {'help': 'The locale folder for the files'},
        'git_url': {'help': 'The url of the repo in GitHub'},
        'git_user': {'help': 'The GitHub user'},
        'git_email': {'help': 'The GitHub user email'},
        'git_folder': {'help': 'A sube folder for the post'},
    }

    '''This map the text format to his file extension. All pasible formats:
    beamer, commonmark, context, docbook, docbook5, dokuwiki, dzslides, epub,
    epub3, fb2, haddock, html, html5, icml, man, mediawiki, native, ,
    opendocument, opml, org, revealjs, rtf, s5,
    slideous, slidy, tei, texinfo, textile, zimwiki
    '''
    FORMAT_EXT = {
        'asciidoc': 'txt',
        'markdown': 'md',
        'markdown_github': 'md',
        'markdown_mmd': 'md',
        'markdown_phpextra': 'md',
        'markdown_strict': 'md',
        'rst': 'rst',
        'plain': 'txt',
        'json': 'json',
        'docx': 'docx',
        'latex': 'tex',
        'odt': 'odt',
    }

    FORMATS = [ name for name in FORMAT_EXT ]

    DEFAULT_CONFIG = os.path.join(os.path.expanduser('~'), '.wpexport.conf')

    def __init__(self, **kwargs):
        self.logger = logging.getLogger('wpexport')
        self.param = {}
        for name in self.PARAMETER:
            self.param[name] = None

        self.setup(**kwargs)

    def setup(self, **kwargs):
        for name in self.PARAMETER:
            if name in kwargs and kwargs[name]:
                self.param[name] = kwargs[name]

        if 'folder' in kwargs and kwargs['folder']:
            self.param['folder'] = os.path.abspath(kwargs['folder'])

        if 'format' in kwargs:
            self.param['format'] = kwargs['format']

        if 'wp_url' in kwargs and kwargs['wp_url']:
            self.param['wp_url'] = kwargs['wp_url'] + 'xmlrpc.php'

    @property
    def file_extension(self):
        return self.FORMAT_EXT[self.param['format']]

    @property
    def check(self):
        return True

    def cli(self):
        '''Display a dialog to input all parameters'''
        for name, info in self.PARAMETER.items():
            print(info['help'])
            value = input('[ {} ] : '.format(name))
            if value: self.param[name] = value
            print()

    def save(self, filename):
        if self.param:
            with open(filename, 'w') as outfile:
                json.dump(self.param, outfile)

    def load(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        self.setup(**data)

    def export(self, folder):
        files = []
        wp = Client(self.param['wp_url'], self.param['wp_user'], self.param['wp_pw'])
        for post in wp.call(GetPosts({'post_status': 'publish'})):

            html_filename = os.path.join(folder, post.slug + '.html')
            export_filename = os.path.join(folder, '{}.{}'.format(post.slug, self.file_extension) )
            files.append(export_filename)

            with open(html_filename, 'w', encoding="utf-8") as f:
                f.write('<h1>{}</h1>'.format(post.title))
                f.write(post.content)
            pypandoc.convert_file(html_filename, self.param['format'], outputfile=export_filename)

            os.remove(html_filename)
            self.logger.info('create file: ' +export_filename)

        return files

    def get_repo(self):
        if os.path.exists(self.param['folder']):
            repo = git.Repo(self.param['folder'])
        else:
            os.makedirs(self.param['folder'])
            repo = git.Repo.clone_from(self.param['git_url'], self.param['folder'], branch='master')

        repo.remotes.origin.fetch()
        repo.remotes.origin.pull()
        return repo

    def backup(self):
        self.logger.info('setup repo folder')
        repo = self.get_repo()

        if self.param['git_folder']:
            folder = os.path.join(self.param['folder'], self.param['git_folder'])

            if not os.path.exists(folder):
                logger.info('create post folder')
                os.makedirs(post_folder)
        else:
            folder = self.param['folder']

        files = self.export(folder)

        self.logger.info('upload to GitHub')
        repo.index.add(files)
        author = git.Actor(self.param['git_user'], self.param['git_email'])
        repo.index.commit('update posts', author=author)

        info = repo.remotes.origin.push()[0]
        self.logger.info('push flags: ' + str(info.flags))
