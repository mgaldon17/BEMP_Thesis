class Tally:

    def __init__(self, number, list_vals, list_errors):
        self.number = number
        self.list_vals = list_vals
        self.list_errors = list_errors

    def set_list_errors(self, rel_error):
        self.list_errors.append(rel_error)

    def set_list_vals(self, val):
        self.list_vals.append(val)

    def get_list_vals(self):
        return self.list_vals

    def get_list_errors(self):
        return self.list_errors

    def get_number(self):
        return self.number
