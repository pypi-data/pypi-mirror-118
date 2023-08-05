from typing import Dict, Any, List

from krong.task import Task
from krong.tasks.tagger.modules.korean_analyzer import KoreanAnalyzer
from krong.tasks.tagger.usages import USAGE_EN, USAGE_KO

# use global variable to prevent duplicated loading
_DECOMPOSITION_KOREAN_ANALYZER = None
_NON_DECOMPOSITION_KOREAN_ANALYZER = None


class Tagger(Task):
    f"""
    {USAGE_EN}

    Args:
        decomposition (bool): use decomposition mode
    """

    def __init__(self, decomposition: bool = False):
        self.decomposition = decomposition
        global _DECOMPOSITION_KOREAN_ANALYZER
        global _NON_DECOMPOSITION_KOREAN_ANALYZER

        if self.decomposition is True:
            if not _DECOMPOSITION_KOREAN_ANALYZER:
                _DECOMPOSITION_KOREAN_ANALYZER = KoreanAnalyzer(
                    decompound_mode="DISCARD",
                    infl_decompound_mode="DISCARD",
                )
            self.analyzer = _DECOMPOSITION_KOREAN_ANALYZER
        else:
            if not _NON_DECOMPOSITION_KOREAN_ANALYZER:
                _NON_DECOMPOSITION_KOREAN_ANALYZER = KoreanAnalyzer(
                    decompound_mode="NONE",
                    infl_decompound_mode="NONE",
                )
            self.analyzer = _NON_DECOMPOSITION_KOREAN_ANALYZER

    def __call__(self, sequence: str):
        out = self.analyzer.do_analysis(sequence)
        return [_ for _ in zip(out["termAtt"], out["posTagAtt"])]

    @staticmethod
    def usage() -> Dict[str, str]:
        return {
            "en": USAGE_EN,
            "ko": USAGE_KO,
        }
