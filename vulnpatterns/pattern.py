class Pattern:
    def __init__(self, name, entry, san, sinks):
        self._name = name
        self._entry_points = entry
        self._sanitization_functions = san
        self._sinks = sinks

    def get_vulnerability_name(self):
        return self._name

    def get_entry_points(self):
        return self._entry_points

    def get_sanitization_functions(self):
        return self._sanitization_functions

    def get_sinks(self):
        return self._sinks

