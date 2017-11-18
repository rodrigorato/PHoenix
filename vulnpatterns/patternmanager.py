from vulnpatterns import patternhandler
from collections import defaultdict


class PatternManager:
    def __init__(self):
        self._patterns = patternhandler.load_patterns()
        self._sinks_to_patterns = defaultdict(list)
        self._sinks = self.filter_sinks()

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

    """
        @param a list of sinks that we're interested in
        @return a dict that maps sinks to patterns
    """
    def get_sinks_to_patterns_dict(self, sinks):
        sinks_to_patterns_dict = defaultdict(list)

        for sink in sinks:
            sinks_to_patterns_dict[sink].append(self._sinks_to_patterns[sink])

        return sinks_to_patterns_dict

    def test():
        for pattern in get_patterns():
            print(pattern.get_vulnerability_name())
            print(pattern.get_entry_points())
            print(pattern.get_sanitization_functions())
            print(pattern.get_sinks(), "\n")
