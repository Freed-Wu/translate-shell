"""langdao-ce-gb"""
from ...translate import translate
from .. import TRANSLATION


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
    paraphrase = ""
    k = ""
    for i, token in enumerate(tokens):
        if token.startswith("【"):
            k, _, v = token.partition(" ")
            k = k.lstrip("【").rstrip("】")
            explains[k] = v
        elif token.startswith("相关词组:"):
            phrases = list(map(lambda x: x.strip(), tokens[i + 1 :]))
            paraphrases = []
            for phrase in phrases:
                paraphrase = translate(
                    phrase, "en", "zh-cn", ["stardict"]
                ).results[0]["paraphrase"]
                paraphrases += [paraphrase]
            details["相关词组"] = dict(zip(phrases, paraphrases))
            break
        elif k == "":
            if paraphrase == "":
                paraphrase = token
            else:
                paraphrase += "; " + token
        else:
            explains[k] += token
    res["paraphrase"] = paraphrase
    res["explains"] = explains
    res["details"] = details
    return res
