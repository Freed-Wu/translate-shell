"""Define common functions shared by CLI and REPL."""
import atexit
import json
import logging
import os
import signal
from argparse import Namespace, _StoreAction
from pathlib import Path
from threading import get_ident, main_thread
from types import ModuleType
from typing import Callable

from .. import CONFIG_FILE, HISTORY_FILE
from ..__main__ import get_parser
from ..config import Configuration
from ..external import readline
from ..external.rich import traceback
from ..external.rich.logging import RichHandler
from ..translate import translate
from ..translators import TRANSLATORS, get_dummy
from ..translators.online.youdaozhiyun import YoudaozhiyunTranslator
from ..translators.speaker import Speaker

traceback.install()
logging.basicConfig(
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],
)

logger = logging.getLogger(__name__)


def init_readline() -> ModuleType:
    """Init readline.

    :rtype: ModuleType
    """
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.touch(exist_ok=True)
    atexit.register(readline.write_history_file, HISTORY_FILE)  # type: ignore
    readline.read_history_file(HISTORY_FILE)
    readline.set_completer_delims(" ")
    return readline


def init_config(path: Path) -> Configuration:
    """Read config file.

    :param path:
    :type path: Path
    :rtype: Configuration
    """
    config = Configuration()
    try:
        configure_code = path.read_text()
    except FileNotFoundError:
        logger.info(str(CONFIG_FILE) + "is not found!")
        return config
    namespace = {}
    try:
        # skipcq: PYL-W0122
        exec(configure_code, namespace, namespace)  # nosec: B102
    except Exception as e:  # skipcq: PYL-W0703
        logger.error(e)
        logger.warning("Ignore " + str(CONFIG_FILE))
        return config
    configure = namespace.get("configure")
    if not isinstance(configure, Callable):
        return config
    try:
        new_config = configure()
    except Exception as e:  # skipcq: PYL-W0703
        logger.error(e)
        logger.warning("Ignore configuration() of " + str(CONFIG_FILE))
        return config
    if not isinstance(new_config, Configuration):
        logger.error(
            "configuration() of " + str(CONFIG_FILE) + "is not legal!"
        )
        return config
    return new_config


def init(args: Namespace) -> None:
    """Init args.

    Because ``langdetect`` and many online translators use ``zh-cn`` not
    ``zh_CN``, we need preprocess. We must ignore ``--help``, ``--version``,
    and other arguments which cannot be customized.

    :param args:
    :type args: Namespace
    :rtype: None
    """
    if args.config:
        config_file = Path(args.config)
    else:
        config_file = CONFIG_FILE
    config = init_config(config_file)
    for action in get_parser()._get_optional_actions():  # skipcq: PYL-W0212
        if (
            not isinstance(action, _StoreAction)
            or getattr(args, action.dest) != action.default
        ):
            continue
        value = getattr(config, action.dest, None)
        if isinstance(value, str):
            setattr(args, action.dest, value)
    for attr in config.__all__:
        value = getattr(config, attr, None)
        if value is not None:
            setattr(args, attr, value)
    args.text = " ".join(args.text)
    _readline = init_readline()
    _readline.set_completer(args.complete)
    if args.text:
        _readline.add_history(args.text)
    args.last_text = ""
    logging.root.level += 10 * (args.quiet - args.verbose)
    # override default functions
    YoudaozhiyunTranslator.get_youdaozhiyun_app_info = (
        args.get_youdaozhiyun_app_info
    )
    Speaker.get_speaker = args.get_speaker


def is_sub_thread() -> bool:
    """Judge if current thread is a subthread.

    :rtype: bool
    """
    return main_thread().ident != get_ident()


def process(args: Namespace, is_repl: bool = False) -> None:
    """Process.

    :param args:
    :type args: Namespace
    :param is_repl: If the input is REPL's stdin, it is ``True``.
    :type is_repl: bool
    :rtype: None
    """
    (
        text,
        args.target_lang,
        args.source_lang,
        args.translators,
    ) = args.process_input(
        args.text,
        args.target_lang,
        args.source_lang,
        args.translators,
        is_repl,
    )
    if text == "" or (not is_repl and text == args.last_text):
        return
    target_lang = args.target_lang
    if target_lang == "auto":
        target_lang = os.getenv("LANG", "zh_CN.UTF-8").split(".")[0]
        if target_lang not in ["zh_CN", "zh_TW"]:
            target_lang = target_lang.split("_")[0]
    target_lang = target_lang.lower().replace("_", "-")
    source_lang = args.source_lang.lower().replace("_", "-")
    translator_names = filter(
        len, map(lambda x: x.strip(), args.translators.split(","))
    )
    translators = [
        TRANSLATORS.get(translator, get_dummy(translator))
        for translator in translator_names
    ]
    translation = translate(
        text,
        target_lang,
        source_lang,
        translators,
    )
    if args.format == "json":
        rst = json.dumps(vars(translation))
    elif args.format == "yaml":
        from ..external import yaml

        rst = yaml.dump(vars(translation))
    else:
        rst = args.process_output(translation)
        if rst and args.notification and is_sub_thread():
            args.notify(rst)
    if rst:
        if is_sub_thread():
            os.kill(os.getpid(), signal.SIGINT)
            args.last_text = text
            print(
                args.get_prompt(
                    args.text,
                    args.target_lang,
                    args.source_lang,
                    args.translators,
                )
            )
        # must be after print prompt
        print(rst)
