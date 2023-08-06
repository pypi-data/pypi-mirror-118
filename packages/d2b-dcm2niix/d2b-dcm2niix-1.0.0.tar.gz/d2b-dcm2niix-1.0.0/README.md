# d2b-dcm2niix

Dcm2niix plugin for the d2b package

[![PyPI Version](https://img.shields.io/pypi/v/d2b-dcm2niix.svg)](https://pypi.org/project/d2b-dcm2niix/)

## Installation

```bash
pip install d2b-dcm2niix
```

## Usage

After installation the `d2b run` command should have additional `dcm2niix`-specific flags:

```text
$ d2b run --help
usage: d2b run [-h] -c CONFIG_FILE -p PARTICIPANT -o OUT_DIR [-s SESSION] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--no-dcm2niix | --dcm2niix | --force-dcm2niix] in_dir [in_dir ...]

Organize data in the BIDS format

positional arguments:
  in_dir                Directory(ies) containing files to organize

required arguments:
  -c CONFIG_FILE, --config CONFIG_FILE
                        JSON configuration file (see example/config.json)
  -p PARTICIPANT, --participant PARTICIPANT
                        Participant ID
  -o OUT_DIR, --out-dir OUT_DIR
                        Output BIDS directory
  --no-dcm2niix         Don't run dcm2niix on the input directories. (This is the default)
  --dcm2niix            Run dcm2niix on each of the input directories before organization code executes. dcm2niix execution will be skipped for directories for which converted results from a previous run are found.
  --force-dcm2niix      Run dcm2niix on each of the input directories before organization code executes. Previous dcm2niix results will be overwritten

optional arguments:
  -s SESSION, --session SESSION
                        Session ID
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set logging level
```

Specifically, the following new (mutually exclusive) options are available:

- `--no-dcm2niix`: This is the default behaviour (i.e. the behaviour of the `d2b run` command if none of the dcm2niix flags are set)

- `--dcm2niix`: This will try to run `dcm2niix` on (copies of) each of the input directories prior to proceeding with BIDS-ification. **NOTE:** If any NIfTI files are found from a previous `d2b run --dcm2niix ...` run, then dcm2niix will not be invoked on that (copy of that) specific input directory.

- `--force-dcm2niix`: This will run `dcm2niix` on (copies of) each of the input directories _always_, regardless of files from previous `d2b run` runs.

Also, there should be a new subcommand `d2b dcm2niix` available:

```text
$ d2b dcm2niix --help
usage: d2b dcm2niix [-h] in_dir [in_dir ...] out_dir

Run dcm2niix with the options used by d2b

positional arguments:
  in_dir      DICOM directory(ies)
  out_dir     Output BIDS directory

optional arguments:
  -h, --help  show this help message and exit
```

This command is the equivalent of `dcm2bids`'s `dcm2bids_helper` command. In particular it's serves as a way to run dcm2niix in the exact same way that `d2b run --[force-]dcm2niix` would run the command (i.e. potentially useful to see what the resulting sidecars/filenames would look like).
