from vulnpatterns import patternhandler
from collections import defaultdict


class PatternManager:
    def __init__(self):
        self._patterns = patternhandler.load_patterns()
        self._unique_patterns_list = []
        self._sinks_to_patterns = defaultdict(list)
        self._sinks = self.filter_sinks()
        self._sanitizations = self.filter_sanitizations()
        self._sanits_to_patterns = defaultdict(list)

        for pattern in self._patterns:
            for entry_point in pattern.get_entry_points():
                if entry_point not in self._unique_patterns_list:
                    self._unique_patterns_list.append(entry_point)


    """
        @return a list of all sinks without a repeated one
    """
    def filter_sinks(self):
        sinks = []

        """
            For each sink in each pattern:
              - Add it to the sinks list
              - Add it to the _sinks_to_patterns dictionary, building it here
        """
        for pattern in self._patterns:
            for sink in pattern.get_sinks():

                # Assumes there are no repeated patterns
                self._sinks_to_patterns[sink].append(pattern)

                # Checks if sink is already in the list
                if sink not in sinks:
                    sinks.append(sink)

        return sinks

    """
        @return a list of all sinks without a repeated one
    """
    def filter_sanitizations(self):
        sanitizations = []

        """
            For each sanitization in each pattern:
              - Add it to the sanitization list
              - Add it to the _sanitizations_to_patterns dictionary, building it here
        """
        for pattern in self.get_patterns():
            for sanitization in pattern.get_sanitization_functions():

                # Checks if sanitization is already in the list
                if sanitization not in sanitizations:
                    sanitizations.append(sanitization)

        return sanitizations

    def get_all_sinks(self):
        return self._sinks

    def get_patterns(self):
        return self._patterns

    def get_unique_patterns_list(self):
        return self._unique_patterns_list


    """
        @param a list of sinks that we're interested in
        @return a dict that maps sinks to patterns
    """
    def get_sinks_to_patterns_dict(self, sinks):
        sinks_to_patterns_dict = defaultdict(list)

        for sink in sinks:
            sinks_to_patterns_dict[sink].append(self._sinks_to_patterns[sink])

        return sinks_to_patterns_dict

    def get_sanitizations_to_patterns_dict(self, sanits):
        sanits_to_patterns_dict = defaultdict(list)

        patterns = self.get_unique_patterns_list()

        for sanit in sanits:
            sanits_to_patterns_dict[sanit].append(self._sanits_to_patterns[sanit])

        return sanits_to_patterns_dict

    """
        @return a dict that maps sinks to patterns
    """
    def get_sinks_to_patterns(self):
        sinks_to_patterns = defaultdict(list)

        for sink in self._sinks:
            for pattern in self._patterns:
                if sink in pattern.get_sinks():
                    sinks_to_patterns[sink].append(pattern)

        return sinks_to_patterns

    """
        @param a list of sinks that we're interested in
        @return a dict that maps sinks to patterns
    """
    def get_sanitizations_to_patterns(self):
        sanitizations_to_patterns = defaultdict(list)

        for sanitization in self._sanitizations:
            for pattern in self.get_patterns():
                if sanitization in pattern.get_sanitization_functions():
                    sanitizations_to_patterns[sanitization].append(pattern)

        return sanitizations_to_patterns
