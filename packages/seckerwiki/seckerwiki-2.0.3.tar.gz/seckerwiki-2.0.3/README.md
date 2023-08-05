# Seckerwiki Scripts

This package is a CLI that helps me manage my markdown-based [Foam](https://foambubble.github.io/) workspace, or my "Personal Wiki".
I store everything in my wiki, from journal entries to uni notes.

## Installation

Version `1.x` had requirements for extra dependencies to get the lecture-to-markdown converter working properly. Since I no longer go to uni, I don't need those scripts anymore, so the installation is as simple as:

```
pip3 install seckerwiki
```

Once installed, run this command in the root of your wiki repo:

```
seckerwiki setup
```

## Commands

### Setup

This command does a couple of things:

- Creates a `config.yml` file in `~/.config/seckerwiki`, which is used to configure some things in the repo.
- Creates a `credentials` file in `~/.config/seckerwiki/`, which stores secrets.

Edit the credentials file to add a secret passsword used for decrypting your Journal (see below).

### log 

Alias for git log, with some pretty graph options.


### commit 

does a git commit, generating a commit message. If there are a number of staged files, the commit header shows the top level folders instead.

Args:

- `-y`: skip verification and commit

### sync

perform a `git pull` then `git push`

### journal

I use my wiki to store encrypted journal entries.

Run `wiki journal` to generate a new empty journal entry in the journal folder specified in the settings. `wiki journal --encrypt` replaces all the `.md` files with `.md.asc` files, encrypting the files with a symmetric key specified in the settings. `wiki journal --decrypt [path]` decrypts a file and prints it to stdout.
