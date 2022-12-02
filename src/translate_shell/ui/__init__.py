"""Define common functions shared by CLI and REPL."""
import atexit
import json
import logging
import os
from argparse import Namespace, _StoreAction
from pathlib import Path
from types import ModuleType
from typing import Callable

from .. import APPDIRS, CONFIG_FILE, CONFIG_PATH, HISTORY_FILE, HISTORY_PATH
from ..__main__ import get_parser
from ..config import Configuration
from ..external import readline
from ..external.rich import traceback
from ..external.rich.logging import RichHandler
from ..translate import translate
from ..translators import TRANSLATORS, get_dummy
from ..utils.speakers import get_speaker
from ..utils.youdaozhiyun import get_youdaozhiyun_app_info

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
    APPDIRS.user_data_path.mkdir(parents=True, exist_ok=True)
    HISTORY_PATH.touch(exist_ok=True)
    atexit.register(readline.write_history_file, HISTORY_FILE)  # type: ignore
    readline.read_history_file(HISTORY_FILE)
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
        logger.info(CONFIG_FILE + "is not found!")
        return config
    namespace = {}
    try:
        exec(configure_code, namespace, namespace)  # nosec: B102
    except Exception as e:
        logger.error(e)
        logger.warning("Ignore " + CONFIG_FILE)
        return config
    configure = namespace.get("configure")
    if not isinstance(configure, Callable):
        return config
    try:
        new_config = configure()
    except Exception as e:
        logger.error(e)
        logger.warning("Ignore configuration of " + CONFIG_FILE)
        return config
    if not isinstance(new_config, Configuration):
        logger.error("configuration of " + CONFIG_FILE + "is not legal!")
        return config
    return new_config


def init(args: Namespace) -> Namespace:
    """Init args.

    Because ``langdetect`` and many online translators use ``zh-cn`` not
    ``zh_CN``, we need preprocess. We must ignore ``--help``, ``--version``,
    and other arguments which cannot be customized.

    :param args:
    :type args: Namespace
    """
    if args.config:
        config_path = Path(args.config)
    else:
        config_path = CONFIG_PATH
    config = init_config(config_path)
    for action in get_parser()._get_optional_actions():
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
    args.last_text = ""
    logging.root.level += 10 * (args.quiet - args.verbose)

    global get_speaker, get_youdaozhiyun_app_info
    get_speaker = args.get_speaker
    get_youdaozhiyun_app_info = args.get_youdaozhiyun_app_info
    return args


def process(args: Namespace) -> tuple[str, str]:
    """Process.

    :param args:
    :type args: Namespace
    :rtype: tuple[str, str]
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
        args.last_text is None,
    )
    if text == "" or text == args.last_text:
        return text, ""
    target_lang = args.target_lang
    if target_lang == "auto":
        target_lang = os.getenv("LANG", "zh_CN.UTF-8").split(".")[0]
        if target_lang not in ["zh_CN", "zh_TW"]:
            target_lang = target_lang.split("_")[0]
    target_lang = target_lang.lower().replace("_", "-")
    source_lang = args.source_lang.lower().replace("_", "-")
    translators = [
        TRANSLATORS.get(translator, get_dummy(translator))
        for translator in args.translators.split(",")
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
    return text, rst
