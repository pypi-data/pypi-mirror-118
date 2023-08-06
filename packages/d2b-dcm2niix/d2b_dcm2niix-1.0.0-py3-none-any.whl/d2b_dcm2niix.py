from __future__ import annotations

import argparse
import logging
import re
import subprocess
from pathlib import Path
from typing import Any
from typing import TYPE_CHECKING

from d2b.hookspecs import hookimpl

if TYPE_CHECKING:
    from d2b.d2b import D2B


__version__ = "1.0.0"

OPTIONS = {"-b": "y", "-ba": "y", "-z": "y", "-f": "%3s_%f_%p_%t"}


class CLI_OPTIONS:
    no = "no"
    run = "run"
    force = "force"


class Dcm2niix:
    def __init__(
        self,
        dcm_dir: str | Path,
        nii_dir: str | Path,
        options: dict[str, Any] = None,
        subprocess_run_kwargs: dict[str, Any] = None,
    ):
        self.dcm_dir = Path(dcm_dir)
        self.nii_dir = Path(nii_dir)
        self.options = options or OPTIONS
        self.subprocess_run_kwargs = subprocess_run_kwargs or {
            "check": True,
            "capture_output": True,
            "text": True,
        }

        self.completed_process: subprocess.CompletedProcess

    @staticmethod
    def help() -> str:
        return subprocess.run(("dcm2niix",), capture_output=True, text=True).stdout

    @classmethod
    def version(cls) -> str:
        help_text = cls.help()
        match = re.search(r"v\d+\.\d+\.\d+", help_text, re.MULTILINE)
        if match is None:
            raise ValueError(
                "Could not find executable 'dcm2niix'. "
                "Is it installed and on your PATH?",
            )
        return match.group(0)

    def run(self):
        cmd = (
            "dcm2niix",
            *sum(([str(k), str(v)] for k, v in self.options.items()), []),
            "-o",
            str(self.nii_dir),
            str(self.dcm_dir),
        )
        self.completed_process = subprocess.run(cmd, **self.subprocess_run_kwargs)


@hookimpl
def register_commands(subparsers: argparse._SubParsersAction):
    create_dcm2niix_parser(subparsers)


def create_dcm2niix_parser(subparsers: argparse._SubParsersAction | None):
    description = "Run dcm2niix with the options used by d2b"
    if subparsers is None:
        _parser = argparse.ArgumentParser(description=description)
    else:
        _parser = subparsers.add_parser("dcm2niix", description=description)

    _parser.add_argument("in_dir", type=Path, nargs="+", help="DICOM directory(ies)")
    _parser.add_argument(
        "out_dir",
        type=Path,
        help="Output BIDS directory",
    )

    _parser.set_defaults(handler=handler)

    return _parser


def handler(args: argparse.Namespace):
    in_dirs: list[Path] = args.in_dir
    out_dir: Path = args.out_dir

    for in_dir in in_dirs:
        app = Dcm2niix(dcm_dir=in_dir, nii_dir=out_dir)
        app.run()

    print("Example in:")
    print(out_dir)


@hookimpl
def prepare_run_parser(
    optional: argparse._ArgumentGroup,
):
    dcm2niix_group = optional.add_mutually_exclusive_group()
    dcm2niix_group.add_argument(
        "--no-dcm2niix",
        dest="dcm2niix",
        action="store_const",
        const=CLI_OPTIONS.no,
        default=CLI_OPTIONS.no,
        help="Don't run dcm2niix on the input directories. (This is the default)",
    )
    dcm2niix_group.add_argument(
        "--dcm2niix",
        dest="dcm2niix",
        action="store_const",
        const=CLI_OPTIONS.run,
        help="Run dcm2niix on each of the input directories before "
        "organization code executes. dcm2niix execution will be skipped for "
        "directories for which converted results from a previous run are found.",
    )
    dcm2niix_group.add_argument(
        "--force-dcm2niix",
        dest="dcm2niix",
        action="store_const",
        const=CLI_OPTIONS.force,
        help="Run dcm2niix on each of the input directories before "
        "organization code executes. Previous dcm2niix results will be "
        "overwritten",
    )


@hookimpl
def pre_run_logs(logger: logging.Logger):
    logger.info(f"d2b-dcm2niix:version: {__version__}")
    logger.info(f"dcm2niix:version: {Dcm2niix.version()}")


@hookimpl(tryfirst=True)
def collect_files(
    d2b_dir: Path,
    options: dict[str, Any],
    d2b: D2B,
) -> list[Path] | None:
    if options["dcm2niix"] == CLI_OPTIONS.no:
        # if we don't have the --[force-]dcm2niix flag set on the command line
        return

    dcm_dirs = list(fp for fp in d2b_dir.rglob("*folder*") if fp.is_dir())
    files: list[Path] = []
    for dcm_dir in dcm_dirs:
        nii_dir = dcm_dir / "nii"
        nii_dir.mkdir(exist_ok=True, parents=True)

        prev_results = len(list(nii_dir.rglob("*.nii.gz"))) > 0
        is_not_force = options["dcm2niix"] != CLI_OPTIONS.force
        if prev_results and is_not_force:
            d2b.logger.warning(
                f"❗ Found converted nii files in directory [{nii_dir}]. "
                "Skipping dcm2niix. Run with --force-dcm2niix to overwrite.",
            )
            continue

        m = f"Running dcm2niix on directory [{dcm_dir}], writing outputs to [{nii_dir}]"
        d2b.logger.info(m)
        d2n = Dcm2niix(dcm_dir=dcm_dir, nii_dir=nii_dir)
        d2n.run()
        files.extend(nii_dir.rglob("*.json"))

    return files
