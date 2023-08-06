# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['sphinxcontrib',
 'sphinxcontrib.needs_capri',
 'sphinxcontrib.needs_capri.service']

package_data = \
{'': ['*']}

install_requires = \
['sphinx-needs-extensions>=0.1.0,<0.2.0', 'sphinxcontrib-needs>=0.7,<0.8']

setup_kwargs = {
    'name': 'sphinx-needs-capri',
    'version': '0.1.0',
    'description': 'Synchronize codebeamer with Sphinx-Needs',
    'long_description': 'Sphinx-Needs-Capri\n==================\n\n.. image:: /docs/_static/sphinx_needs_codebeamer_logo.png\n   :align: center\n   :width: 50%\n\nThis `Sphinx <https://www.sphinx-doc.org/en/master/>`_ extension provides scripts and directives to synchronize\ndata between `codebeamer <https://codebeamer.com/>`_ from `Intland <https://intland.com/>`_ and the\nRequirement Engineering extension `Sphinx-Needs <https://sphinxcontrib-needs.readthedocs.io/en/latest/>`_ from\n`useblocks <https://useblocks.com>`_.\n\nLicense\n-------\nThis software is licensed under **BSL 1.1** and it can be used and distributed for free as long as it is not\nused for and inside commercial projects, products or documentations.\n\nA commercial license can be obtained by contacting the\n`useblocks team <mailto:mail@useblocks.com?subject=License for sphinx-needs-capri>`_.\n\nSee our `License file <https://raw.githubusercontent.com/useblocks/sphinx-needs-capri/main/LICENSE>`_\nfor details. Or take a look into the general `BSL FAQ <https://mariadb.com/bsl-faq-adopting/>`_.\n\nDevelopment\n-----------\n\nCodebeamer - Docker\n~~~~~~~~~~~~~~~~~~~\n\nTo start a codebeamer server local, you can use ``docker-compose up -d`` under ``/docker``.\nThis will download, create and run a codebeamer and a mysql container.\n\nAfter that open http://127.0.0.1:8080 in your browser and use the default codebeamer  user\n``bond`` with password ``007``.\n\nTo stop everything, run ``docker-compose down`` under ``/docker``.\n\nFor more information take a look into `Codebeamer\'s Docker documentation <https://codebeamer.com/cb/wiki/5562876>`_.\n\nLicense\n^^^^^^^\ncodebeamer gets executed with an evaluation license, which is valid for 7 days.\n\nIf you need a more suitable license, you can request one from the codebeamer support team: support@intland.com.\n\nThe support team will need your Host-ID, which should be by default ``LIN-02:42:AC:16:00:03`` for most docker\ninstallations. You can check this and other License details under: http://127.0.0.1:8080/sysadmin/configLicense.spr\n\nTo add your own license, create ``/docker/.env`` and add the following content::\n\n    # Your MAC Address\n    CB_MAC_ADDRESS=02:42:AC:16:00:03\n    CB_LICENSE=<license ...> ... </license>  #All in one line\n\n\nREST access\n^^^^^^^^^^^\nThe default user ``bond`` has already all needed privileges to access the codebeamer REST API under\n``http://127.0.0.1:8080/rest``.\n\nFor a quick test, execute ``curl --user bond:007 http://127.0.0.1:8080/rest/user/bond``.\n\nReturn value should be::\n\n    {\n      "uri" : "/user/1",\n      "name" : "bond",\n      "firstName" : "Default",\n      "lastName" : "System Administrator",\n      "dateFormat" : "MMM dd yyyy",\n      "status" : "Activated"\n    }\n\nThere is also a swagger-ui available to analyse the complete REST-API: http://127.0.0.1:8080/v3/swagger/editor.spr.\n\n\n\n\n\n\n',
    'author': 'team useblocks',
    'author_email': 'info@useblocks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/useblocks/sphinx-needs-capri',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
