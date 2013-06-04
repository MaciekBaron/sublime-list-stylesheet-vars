# List stylesheet variables
Simple [Sublime 2/3](http://www.sublimetext.com/) plugin for listing stylesheet preprocessor variables used in a file.

Supported preprocessors:
 - [LESS](http://lesscss.org/)
 - [SASS/SCSS](http://sass-lang.com/)
 - [Stylus](http://learnboost.github.io/stylus/)

The default hotkey is <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>L</kbd> (or <kbd>Ctrl</kbd>+<kbd>Shift</kbd>
+<kbd>L</kbd> on Linux to avoid conflicts with the lock screen hotkey).

It displays a list of variables used in your current file allowing you to insert a selected one
directly into your code. It also supports `@import`ed files so you can use variables defined in
external files. This can be disabled in settings.

Note that the plugin automatically ignores anything which looks like a vendor prefixed statement (e.g.
`@-webkit-keyframes`) and reserved words (e.g. `@media`, `@import` etc.)

![Screenshot](http://i41.tinypic.com/eajivq.png)

Please note that the plugin currently does not understand variable scope and therefore will display all
the occurances of a variable.

## Installation
Execute the following command in your Sublime Packages folder: `git clone git://github.com/MaciekBaron/sublime-list-stylesheet-vars.git List\ Stylesheet\ Variables`

I will prepare a plugin to Package Manager after additional testing

## Configuration
The settings file has currently two options:

 - `readImported` (default: `true`) - decides whether the plugin should attempt to read imported files
 - `readAllViews` (default: `false`) - decides whether the plugin should attempt to read all opened files

Currently if the plugin checks all opened files, it will only check for imported files in the currently
selected file.

