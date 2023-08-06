import logging
import os
from typing import Dict, List, Any
import argparse


__all__ = ["add_options", "apply_options"]


logger = logging.getLogger(__name__)


def add_options(parser: argparse.ArgumentParser) -> None:
    """
    Add options to parser.
    """
    parser.add_argument(
        "opts",
        help="modify config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )


def apply_options(config: Dict[str, Any], args: argparse.Namespace) -> None:
    """
    Update config using opts.
    """
    try:
        from yacs.config import CfgNode as CN
    except ImportError as e:
        logger.error("`apply_options` requiring yacs(version==0.1.8), "
                     "but not installed.")
        raise e
    opts = args.opts
    config_CN = CN(config)
    if opts is not None and len(opts) > 0:
        config_CN.merge_from_list(opts)
    config.update(config_CN)
