import sublime, sublime_plugin, os, re

class StyleSheetSetup:
    def __init__(self, extensions, regex, partials=None, index=None):
        if partials is None:
            self.partials = False
        else:
            self.partials = partials

        if index is None:
            self.index = False
        else:
            self.index = index

        self.extensions = extensions
        self.regex = regex

class ListStylesheetVariables(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings('stylevariables.sublime-settings')

        handle_imports = settings.get("readImported")
        read_all_views = settings.get("readAllViews")

        # Define setups
        less_setup = StyleSheetSetup((b'.less', b'.lessimport'), "(@[^\s\\]]*)\s*: *(.*);")
        sass_setup = StyleSheetSetup((b'.sass', b'.scss'), "^\s*(\$[^\s\\]{}]*)\s*: *([^;\n]*);?", True) # Last argument True because using partials
        stylus_setup = StyleSheetSetup((b'.styl',), "^\s*([^\s\\]\[]*) *= *([^;\n]*)", False, True)
        sass_erb_setup = StyleSheetSetup((b'.scss.erb', b'.sass.erb'), "^\s*(\$[^\s\\]{}]*)\s*: <?%?=? *([^;\n]*);? [\%>]?", True)

        # Add all setups to the setup tuple
        setups = (less_setup, sass_setup, stylus_setup, sass_erb_setup)

        chosen_setup = None

        self.edit = edit
        fn = self.view.file_name().encode("utf_8")

        for setup in setups:
            for ext in setup.extensions:
                if fn.endswith(ext):
                    chosen_setup = setup

        if chosen_setup == None:
            return

        # Handle imports
        imports = []
        imported_vars = []

        compiled_regex = re.compile(chosen_setup.regex, re.MULTILINE)

        if handle_imports:
            self.view.find_all("@import [\"|\'](.*)[\"|\']", 0, "$1", imports)

            file_dir = os.path.dirname(fn).decode("utf-8")

            for i, filename in enumerate(imports):
                has_extension = False
                for ext in chosen_setup.extensions:
                    if filename.endswith(ext.decode("utf-8")):
                        has_extension = True

                if has_extension == False:
                    # We need to try and find the right extension
                    for ext in chosen_setup.extensions:
                        ext = ext.decode("utf-8")
                        if os.path.isfile(os.path.normpath(file_dir + '/' + filename + ext)):
                            filename += ext
                            break
                        if chosen_setup.partials:
                            fn_split = os.path.split(filename)
                            partial_filename = fn_split[0] + "/_" + fn_split[1]
                            if os.path.isfile(os.path.normpath(file_dir + partial_filename + ext)):
                                filename = "_" + filename + ext
                                break
                        if chosen_setup.index and os.path.isfile(os.path.normpath(file_dir + "/" + filename + "/index" + ext)):
                            filename += "/index" + ext
                try:
                    f = open(os.path.normpath(file_dir + '/' + filename), 'r')
                    contents = f.read()
                    f.close()

                    m = re.findall(compiled_regex, contents)
                    imported_vars = imported_vars + m
                except:
                    print('Could not load file ' + filename)

            # Convert a list of tuples to a list of lists
            imported_vars = [list(item) for item in imported_vars]

        self.variables = []

        vars_from_views = []

        if read_all_views:
            for view in self.view.window().views():
                viewfn = self.view.file_name().encode("utf-8")
                compatible_view = False

                for ext in chosen_setup.extensions:
                    if viewfn.endswith(ext):
                        viewvars = []
                        view.find_all(chosen_setup.regex, 0, "$1|$2", viewvars)
                        vars_from_views += viewvars
                        break;
        else:
            self.view.find_all(chosen_setup.regex, 0, "$1|$2", self.variables)



        self.variables += vars_from_views
        self.variables = list(set(self.variables))
        for i, val in enumerate(self.variables):
            self.variables[i] = val.split("|")
        self.variables = imported_vars + self.variables
        self.variables.sort()
        self.view.window().show_quick_panel(self.variables, self.insert_variable, sublime.MONOSPACE_FONT)

    def insert_variable(self, choice):
        if choice == -1:
            return
        self.view.run_command('insert_text', {'string': self.variables[choice][0]})

class InsertText(sublime_plugin.TextCommand):
    def run(self, edit, string=''):
        for selection in self.view.sel():
            self.view.insert(edit, selection.begin(), string)
