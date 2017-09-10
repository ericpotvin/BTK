""" Report Module
"""
import os

from Code import Code
from constants import DATA_BASE, CC_BASE
from File import File
from Folder import Folder
from HTML import HTML
from Statistics import Statistics


class Report(object):
    """ Class for report generation
    """

    ROOT_PATH = "root/"

    def __init__(self):
        """ Constructor
        """
        self.script_base = ""
        self.files = []

    def handle_files(self):
        """ Process files
            :return: None
        """
        if not self.files:
            return

        total_lines = 0
        covered_lines = 0
        dirs = {}

        for file_ in self.files:
            Statistics.calculate(file_)

            dir_name = os.path.dirname(file_.path)
            if dir_name not in dirs:
                dirs[dir_name] = Folder(dir_name)
            dirs[dir_name].add_file(file_)

        for dir_ in dirs.values():
            total_lines = total_lines + dir_.total_lines
            covered_lines = covered_lines + dir_.covered_lines

        open_file = open(
            os.path.join(
                CC_BASE,
                HTML.INDEX_FILE + HTML.FILE_EXT), "w"
        )

        root_link = HTML.get_link(CC_BASE, HTML.LINK_ROOT, "")

        open_file.write(HTML.get_header(root_link, HTML.TABLE_HEADER))

        for dir_ in dirs.values():
            path = os.path.join(
                self.ROOT_PATH,
                dir_.name[1:], HTML.INDEX_FILE + HTML.FILE_EXT
            ).replace('//', '/')

            last_pos = dir_.name.rfind("/")

            open_file.write(
                HTML.get_line(
                    path,
                    dir_.name[last_pos + 1:],
                    dir_.total_lines,
                    dir_.covered_lines
                )
            )

        open_file.write(HTML.get_footer(total_lines, covered_lines))
        open_file.close()

        for dir_ in dirs.values():

            path = (CC_BASE + "/" + self.ROOT_PATH + dir_.name)\
                .replace('//', '/')

            if not os.path.exists(path):
                os.makedirs(path)

            open_file = open(
                os.path.join(path, HTML.INDEX_FILE + HTML.FILE_EXT),
                "w"
            )

            open_file.write(
                HTML.get_header(root_link + dir_.basename, HTML.TABLE_HEADER)
            )

            for file_ in dir_.files:
                open_file.write(
                    HTML.get_line(
                        file_.basename + HTML.FILE_EXT,
                        file_.basename,
                        file_.total_lines,
                        file_.covered_lines
                    )
                )

            open_file.write(
                HTML.get_footer(dir_.total_lines, dir_.covered_lines)
            )
            open_file.close()

        for file_ in self.files:
            self.handle_file(file_)

    def handle_file(self, file_name):
        """ Handle a file
            :param file_name: The filename to process
            :return: None
        """
        dir_name = os.path.dirname(file_name.path)
        basename = os.path.basename(file_name.path)
        path = CC_BASE + self.ROOT_PATH + "/" + os.path.abspath(dir_name)
        path = path.replace('//', '/')

        if not os.path.exists(path):
            os.makedirs(path)

        open_file = open(os.path.join(path, basename + HTML.FILE_EXT), "w")

        source_data = File.read_file(self.script_base + file_name.path)

        last_pos = dir_name.rfind("/")

        html_link = HTML.get_link(CC_BASE, "root", "") + \
            HTML.get_link(path, dir_name[last_pos + 1:], basename)

        open_file.write(HTML.get_header(html_link, HTML.SRC_PREFIX))

        processing_line = 1
        previous_line_is_continued = False

        for line in source_data.splitlines():
            line = line.decode("utf-8")
            line = line.replace("&", "&amp;")
            line = line.replace(">", "&gt;")
            line = line.replace("<", "&lt;")
            line = line.replace('"', '&quot;')

            line_covered = processing_line in file_name.lines and \
                Code.line_is_code(line) or \
                processing_line > 1 and \
                previous_line_is_continued

            if line_covered:
                span_class = "covered"
            elif Code.line_is_code(line):
                span_class = "not_covered"
            else:
                span_class = "not_code"

            line_to_save = HTML.get_html(HTML.LINE_SOURCE) % (
                processing_line,
                span_class,
                line
            )

            open_file.write(line_to_save)

            previous_line_is_continued = True if line.endswith("\\") else False
            processing_line = processing_line + 1

        open_file.write(
            HTML.get_html(HTML.SRC_SUFFIX)
            +
            HTML.get_footer(
                file_name.total_lines, file_name.covered_lines, False
            )
        )

    def generate(self):
        """ Generate the report
            :return: None
        """

        if not os.path.exists(CC_BASE):
            os.makedirs(CC_BASE)

        for root, _, files in os.walk(DATA_BASE, topdown=False):

            for name in files:
                path = os.path.join(root, name)

                if not os.path.exists(path):
                    print ("Could not load %s, skipping" % path)
                    continue

                file_ = File.load(path, self.script_base)
                self.files.append(file_)

        self.handle_files()
