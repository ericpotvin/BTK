""" Code module
"""
import re


class Code(object):
    """ Code class
    """

    # noinspection Annotator
    RE_FUNCTION = re.compile(
        r"^(function[\t ]+)*[A-Z_]+[\w]*[\t ]*\([\t ]*\)$", re.IGNORECASE
    )
    # noinspection Annotator
    RE_RESERVED = re.compile(
        r"^({|}|else|then|fi|done|esac|do|;;)$", re.IGNORECASE
    )

    @staticmethod
    def line_is_code(line):
        """ Check if the current line is code
            :param line: The line
            :return: boolean
        """
        tmp = line.strip()

        if tmp == "" or tmp.startswith('#'):
            return False

        if tmp.startswith("function") or Code.RE_FUNCTION.match(tmp):
            return False

        if Code.RE_RESERVED.match(tmp):
            return False

        return True
