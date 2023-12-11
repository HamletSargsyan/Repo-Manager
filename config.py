from inquirer.themes import Default, term

class Theme(Default):
    def __init__(self):
        super().__init__()
        self.List.selection_color = term.green