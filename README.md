# wpexport
This small python package backup your Wordpress post to GitHub/locale. It
convert the html to Markdown with pypandoc. For the api interaction, I uses the
two packages gitpython and python-wordpress-xmlrpc. So you have to install this
dependence, if you wand to install it from source.

## quick start
Install:
```bash
pip install wpexport
```
It uses pandoc. You may have to install it manually.
```bash
sudo apt install pandoc
```
More information https://pandoc.org/installing.html

Set up your settings:
```bash
python -m wpexport --setup
```
After you have input all the parameters, they will be save in the file
~.wpexport.conf. Notice your passwords are also in this file.

Now you are ready to have some fun.
```bash
wpexport
```

## command line arguments
This command export all your post to the GitHub repo. If you didn't like the
config file, you can pass the parameter throw the terminal. Use the name of the
parameter as the command option. The command option will always override the
config file. For axample you cann uses the config file for all parametes exclude
the password. And then pass the password throw the command line.
```bash
wpexport --wp_pw 1234
```

## the config file
You can also uses another config file. For the setup as well as the backup
function.
```bash
wpexport --config "/path/to/your/config.json"
```
The config file is a basic json file. You can look into it and change the
values, if you like.

## only local export
If you didn't like GitHub, only export it to your local machine.
```bash
wpexport --output "/path/to/your/export"
```

## how does it work?
Coming soon.

## development
Clone repo:
```bash
git clone https://github.com/axju/wpexport.git
```
Create virtual environment and update dev-tools:
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade wheel pip setuptools twine
```
Install wpexport:
```bash
pip install -e .
```

Publish the packages:
```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```
