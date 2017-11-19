from vulnpatterns import patternhandler
from collections import defaultdict


class PatternManager:
    def __init__(self):
        self._patterns = patternhandler.load_patterns()
        self._sinks_to_patterns = defaultdict(list)
        self._sinks = self.filter_sinks()
        self._unique_patterns_list = []
        self._sanits_to_patterns = defaultdict(list)

        for pattern in self._patterns:
            for entry_point in pattern._entry_points:
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

        for sanit in sanits:
            sanits_to_patterns_dict[sanit].append(self._sanits_to_patterns[sanit])

        return sanits_to_patterns_dict

    def test():
        for pattern in get_patterns():
            print(pattern.get_vulnerability_name())
            print(pattern.get_entry_points())
            print(pattern.get_sanitization_functions())
            print(pattern.get_sinks(), "\n")
