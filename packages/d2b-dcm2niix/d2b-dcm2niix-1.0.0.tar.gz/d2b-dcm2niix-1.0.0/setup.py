# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['d2b_dcm2niix']
install_requires = \
['d2b>=1.0.0,<2.0.0']

entry_points = \
{'d2b': ['dcm2niix = d2b_dcm2niix']}

setup_kwargs = {
    'name': 'd2b-dcm2niix',
    'version': '1.0.0',
    'description': 'Dcm2niix plugin for the d2b package',
    'long_description': "# d2b-dcm2niix\n\nDcm2niix plugin for the d2b package\n\n[![PyPI Version](https://img.shields.io/pypi/v/d2b-dcm2niix.svg)](https://pypi.org/project/d2b-dcm2niix/)\n\n## Installation\n\n```bash\npip install d2b-dcm2niix\n```\n\n## Usage\n\nAfter installation the `d2b run` command should have additional `dcm2niix`-specific flags:\n\n```text\n$ d2b run --help\nusage: d2b run [-h] -c CONFIG_FILE -p PARTICIPANT -o OUT_DIR [-s SESSION] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--no-dcm2niix | --dcm2niix | --force-dcm2niix] in_dir [in_dir ...]\n\nOrganize data in the BIDS format\n\npositional arguments:\n  in_dir                Directory(ies) containing files to organize\n\nrequired arguments:\n  -c CONFIG_FILE, --config CONFIG_FILE\n                        JSON configuration file (see example/config.json)\n  -p PARTICIPANT, --participant PARTICIPANT\n                        Participant ID\n  -o OUT_DIR, --out-dir OUT_DIR\n                        Output BIDS directory\n  --no-dcm2niix         Don't run dcm2niix on the input directories. (This is the default)\n  --dcm2niix            Run dcm2niix on each of the input directories before organization code executes. dcm2niix execution will be skipped for directories for which converted results from a previous run are found.\n  --force-dcm2niix      Run dcm2niix on each of the input directories before organization code executes. Previous dcm2niix results will be overwritten\n\noptional arguments:\n  -s SESSION, --session SESSION\n                        Session ID\n  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}\n                        Set logging level\n```\n\nSpecifically, the following new (mutually exclusive) options are available:\n\n- `--no-dcm2niix`: This is the default behaviour (i.e. the behaviour of the `d2b run` command if none of the dcm2niix flags are set)\n\n- `--dcm2niix`: This will try to run `dcm2niix` on (copies of) each of the input directories prior to proceeding with BIDS-ification. **NOTE:** If any NIfTI files are found from a previous `d2b run --dcm2niix ...` run, then dcm2niix will not be invoked on that (copy of that) specific input directory.\n\n- `--force-dcm2niix`: This will run `dcm2niix` on (copies of) each of the input directories _always_, regardless of files from previous `d2b run` runs.\n\nAlso, there should be a new subcommand `d2b dcm2niix` available:\n\n```text\n$ d2b dcm2niix --help\nusage: d2b dcm2niix [-h] in_dir [in_dir ...] out_dir\n\nRun dcm2niix with the options used by d2b\n\npositional arguments:\n  in_dir      DICOM directory(ies)\n  out_dir     Output BIDS directory\n\noptional arguments:\n  -h, --help  show this help message and exit\n```\n\nThis command is the equivalent of `dcm2bids`'s `dcm2bids_helper` command. In particular it's serves as a way to run dcm2niix in the exact same way that `d2b run --[force-]dcm2niix` would run the command (i.e. potentially useful to see what the resulting sidecars/filenames would look like).\n",
    'author': 'Andrew Ross',
    'author_email': 'andrew.ross.mail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/d2b-dev/d2b-dcm2niix',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
