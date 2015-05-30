Homebrew and Cask for Alfred
=========

Easily control [Homebrew](http://brew.sh) and [Cask](http://caskroom.io/) with [Alfred](http://www.alfredapp.com).

![Homebrew & Cask for Alfred Screenshot](https://raw.github.com/fniephaus/alfred-homebrew/master/screenshot.gif)


## Features

- Script filters ```brew``` and ```casks``` with support for the following commands:
    - ```doctor```, ```info```, ```install```, ```list```, ```search```, ```uninstall```, ```update``` and ```upgrade```
- Background cache refresh


## Configuration

If you installed homebrew-cask and you can changed where the applications will be installed by adding a line like this to your `.bash_profile` or `.zshenv`:

```shell
# Specify your defaults in this environment variable
export HOMEBREW_CASK_OPTS="--appdir=/Applications --caskroom=/usr/local/Caskroom"
```

## Credits

This workflow uses [Github Octicons](https://github.com/github/octicons/) and [alfred-workflow](https://github.com/deanishe/alfred-workflow).
