import argparse
import copy
import fnmatch
import re
from pathlib import Path
from typing import Dict, Iterator, List

import requests
import urllib3

# (c) gruber. Liberal Regex Pattern for Web URLs. https://gist.github.com/gruber/8891611
URL_REGEX = r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"  # noqa

# terminal colors
T_GREY = "\033[90m"
T_RED = "\033[91m"
T_GREEN = "\033[92m"
T_END = "\033[0m"


class TestResult:
    def __init__(self, url: str, code: int = 0, skip: bool = False, error: str = None):
        self.url = url
        self.code = code
        self.skip = skip
        self.error = error

    @property
    def ok(self) -> bool:
        return not self.error and 200 <= self.code < 300

    def __str__(self):
        cache = f" {T_GREY}[cached result]{T_END}" if self.skip else ""

        if self.error:
            status = f"{T_RED}{'ERROR':>5}{T_END}"
        elif 200 <= self.code < 300:
            status = f"{T_GREEN}{'OK':>5}{T_END}"
        else:
            status = f"{T_RED}{'FAIL':>5}{T_END}"

        if self.error:
            return f"{status} {self.error} - {self.url}{cache}"

        return f"{status} {self.code} - {self.url}{cache}"

    def as_skipped(self):
        obj = copy.copy(self)
        obj.skip = True
        return obj


class LinkChecker:
    def __init__(
        self,
        root: Path,
        include: str,
        regex: str,
        skip_ssl: bool = False,
        only_fails: bool = False,
    ):
        self.root = root.resolve()
        self.include = include
        self.regex = re.compile(regex)
        self.skip_ssl = skip_ssl
        self.only_fails = only_fails

        self._test_results: Dict[TestResult] = {}

        if self.skip_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # select the 1st group, if groups have been used in the
        # regex, otherwise, get the full match (the 0th group)
        self._regex_group = 1 if self.regex.groups > 0 else 0

    def check(self):
        all_urls = self._get_all_urls()
        for file, urls in all_urls.items():
            printed_prolog = False

            for url in urls:
                result = self._test_url(url)

                if not self.only_fails or not result.ok:
                    if not printed_prolog:
                        print(file)
                        printed_prolog = True

                    print(result)

            if printed_prolog:
                print()

    def _get_all_urls(self) -> Dict[Path, List[str]]:
        """
        Get a dictionary that maps filenames to a list of URLs to test
        """
        result = {}

        for file in self._iter_files():
            urls = list(self._iter_urls(file))
            if len(urls) > 0:
                result[file] = urls

        return result

    def _iter_files(self) -> Iterator[Path]:
        """
        Crawl all files in `root`, recursively, that match the `include` pattern
        """
        for file in self.root.glob("**/*"):
            if file.is_file() and fnmatch.fnmatch(file.name, self.include):
                yield file

    def _iter_urls(self, file: Path) -> Iterator[str]:
        """
        Crawl all links in `file` that match the `regex` pattern
        """
        with open(file, encoding="utf-8") as f:
            for line in f:
                for match in re.finditer(self.regex, line):
                    url = match.group(self._regex_group)
                    yield url

    def _test_url(self, url: str) -> TestResult:
        if url in self._test_results:
            # return the existing result with skip flag set
            return self._test_results[url].as_skipped()

        test_result = None

        try:
            url_canonical = LinkChecker._ensure_schema(url)
            resp = requests.head(
                url_canonical, allow_redirects=True, verify=not self.skip_ssl
            )
            test_result = TestResult(url=url, code=resp.status_code)
        except (requests.RequestException, urllib3.exceptions.HTTPError) as e:
            test_result = TestResult(url=url, error=str(e))

        self._test_results[url] = test_result
        return test_result

    @staticmethod
    def _ensure_schema(url: str) -> str:
        if not re.match(r"^https?://", url):
            return "http://" + url
        return url


def main():
    parser = argparse.ArgumentParser(description="Check for dead links in all files")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Directory in which we recursively check matching files (default: '.' - current directory)",
    )
    parser.add_argument(
        "--include",
        "-i",
        type=str,
        default="*.*",
        help="A glob pattern that files have to match (default: '*.*' - everything)",
    )
    parser.add_argument(
        "--regex",
        "-r",
        type=str,
        default=URL_REGEX,
        help="Regex to extract URLs with group syntax support (default: https://gist.github.com/gruber/8891611)",
    )
    parser.add_argument(
        "--skip-ssl",
        action="store_true",
        help="Do not verify the SSL certificate when performing requests",
    )
    parser.add_argument(
        "--only-fails",
        action="store_true",
        help="Only output failed requests",
    )

    args = parser.parse_args()
    print(f"arguments {vars(args)}")
    print()

    lc = LinkChecker(**vars(args))
    lc.check()


if __name__ == "__main__":
    main()
