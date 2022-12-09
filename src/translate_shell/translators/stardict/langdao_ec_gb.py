"""langdao-ec-gb"""
import re

from ...translate import translate
from .. import TRANSLATION

RE_EXPLAIN = re.compile(r"\w+\.")


def parse_tokens(tokens: list[str], res: TRANSLATION) -> TRANSLATION:
    """Parse tokens.

    :param tokens:
    :type tokens: list[str]
    :param res:
    :type res: TRANSLATION
    :rtype: TRANSLATION
    """
    explains = {}
    details = {}
    for i, token in enumerate(tokens, 1):
        if token.startswith("*["):
            res["phonetic"] = tokens[0].lstrip("*[").rstrip("]")
        elif token.startswith("【"):
            k, _, v = token.partition(" ")
            explains[k.lstrip("【").rstrip("】")] = v
        elif RE_EXPLAIN.match(token):
            k, _, v = token.partition(" ")
            explains[k] = v
        elif token.startswith("相关词组:"):
            phrases = list(map(lambda x: x.strip(), tokens[i + 1 :]))
            paraphrases = []
            for phrase in phrases:
                paraphrase = translate(
                    phrase, "zh-cn", "en", ["stardict"]
                ).results[0]["paraphrase"]
                paraphrases += [paraphrase]
            details["相关词组"] = dict(zip(phrases, paraphrases))
            break
    res["explains"] = explains
    res["details"] = details
    if res["explains"] == {}:
        res["paraphrase"] = tokens[0]
    return res
