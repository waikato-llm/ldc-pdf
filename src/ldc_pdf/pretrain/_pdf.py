import argparse
from typing import Iterable, List, Union

from pypdf import PdfReader
from simple_range import Range, ALL

from ldc.core import LOGGING_WARN, domain_suffix
from ldc.base_io import locate_files
from ldc.pretrain import PretrainData, PretrainReader


class PdfPretrainReader(PretrainReader):
    """
    Extracts text from PDF files to use for pretraining.
    """

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 page_range: str = None, invert: bool = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARN):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param page_range: the range of pages to read, None for all
        :type page_range: str
        :param invert: whether to invert the page range matching (ie discard)
        :type invert: bool
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.source_list = source_list
        self.page_range = page_range
        self.invert = invert
        self._inputs = None
        self._current_input = None

    def name(self) -> str:
        """
        Returns the name of the reader, used as command-line name.

        :return: the name
        :rtype: str
        """
        return "from-pdf-" + domain_suffix(self)

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Extracts text from PDF files to use for pretraining."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the PDF file(s) to read; glob syntax is supported", required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the data files to use", required=False, nargs="*")
        parser.add_argument("-p", "--page_range", metavar="RANGE", type=str, default=ALL, help="The range of pages to read; " + Range.help(), required=False)
        parser.add_argument("-V", "--invert", action="store_true", help="Whether to invert the page range, i.e., discard rather than keep.", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.source = ns.input
        self.source_list = ns.input_list
        self.page_range = ns.page_range
        self.invert = ns.invert

    def initialize(self):
        """
        Initializes the reading, e.g., for opening files or databases.
        """
        super().initialize()
        self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True)
        if self.page_range is None:
            self.page_range = "first-last"

    def read(self) -> Iterable[PretrainData]:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable[PretrainData]
        """
        self.finalize()

        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input
        self.logger().info("Reading from: " + str(self.session.current_input))
        reader = PdfReader(self.session.current_input)
        page_range = Range(self.page_range, len(reader.pages))
        pages = set(page_range.indices())

        for i in range(len(reader.pages)):
            if (self.invert and (i in pages)) or (not self.invert and (i not in pages)):
                continue

            page = reader.pages[i]
            text = page.extract_text()

            meta = dict()
            meta["file"] = self.session.current_input
            meta["page"] = i

            yield PretrainData(
                content=text,
                meta=meta,
            )

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._inputs) == 0

    def finalize(self):
        """
        Finishes the reading, e.g., for closing files or databases.
        """
        if self._current_input is not None:
            super().finalize()
            self._current_input = None
