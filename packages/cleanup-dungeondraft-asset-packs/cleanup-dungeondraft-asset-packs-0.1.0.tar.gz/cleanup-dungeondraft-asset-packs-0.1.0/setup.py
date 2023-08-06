# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cleanup_dungeondraft_asset_packs']
entry_points = \
{'console_scripts': ['cleanup-dungeondraft-asset-packs = '
                     'cleanup_dungeondraft_asset_packs:main']}

setup_kwargs = {
    'name': 'cleanup-dungeondraft-asset-packs',
    'version': '0.1.0',
    'description': 'CLI tool to clean up Dungeondraft asset packs',
    'long_description': '`cleanup-dungeondraft-asset-packs` is a CLI tool to cleanup Dungeondraft asset packs.\n\nI noticed that some asset packs from [CartographyAssets](https://cartographyassets.com) would register entries in the [Dungeondraft](https://dungeondraft.net) tag list that are associated with an empty asset list. This made the asset discovery process quite painful. \n\n![Emptry tag entry](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/cleaning-up-dungeondraft-tag-list/empty-assets.webp)\n\nI wrote that CLI tool to automate the process of cleaning up these empty tag entries, in order to keep the tag list as clean as possible.\n ',
    'author': 'Balthazar Rouberol',
    'author_email': 'br@imap.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brouberol/cleanup-dungeondraft-asset-packs',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
