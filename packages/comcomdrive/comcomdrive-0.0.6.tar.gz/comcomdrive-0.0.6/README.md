# How to use comcomdrive

Comcomdrive is package which enables to use google drive in Ainize workspace.

## Prerequisite

Google desktop client credential is required and sholud be located '~/.comcomdrive'

## Installation

```
$ pip3 install comcomdrive
```

## Usage

### Command-line interface(cli)

1. Login

Start google authentication in console, and generate token.json file to '~/.comcomdrive' path.

```
$ comcomdrive login
```

2. Search

Receive keyword by prompt, and return list(id, and name) of file the name of which contains keyword.

```
$ comcomdrive search
```

### Authentication class

```
from comcomdrive import auth

auth.Auth().login()
```

### Search class

```
from comcomdrive import search

search.Search().list_all_files()
search.Search().search_keyword('file_keyword')
```

### Transfer class

```
from comcomdrive import transfer

# upload file to root folder
transfer.Transfer().upload_file('src_file')

# create new dest folder and upload file to the folder
transfer.Transfer().upload_file('src_file', 'dest')

# download file or folder with id
transfer.Transfer().download_file('1j-MBEcJr8RHblsQPitI33mI5cPI-CgZ9')
```
