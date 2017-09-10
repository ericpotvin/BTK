""" Severity Module
"""


class Severity(object):
    """ Severity Class
    """

    HIGH = "good"
    MEDIUM = "ok"
    LOW = "low"

    LOWER_BOUND = 50
    HIGHER_BOUND = 90

    @staticmethod
    def get_color(ratio):
        """ Get the color for a ratio
            :param ratio: The ratio
            :return: string
        """
        if ratio >= Severity.HIGHER_BOUND:
            return Severity.HIGH
        if ratio >= Severity.LOWER_BOUND:
            return Severity.MEDIUM
        return Severity.LOW
