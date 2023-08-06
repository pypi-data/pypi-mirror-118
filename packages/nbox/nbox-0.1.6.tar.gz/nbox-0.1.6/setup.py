# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nbox', 'nbox.framework']

package_data = \
{'': ['*']}

install_requires = \
['randomname==0.1.3', 'rich==10.7.0']

setup_kwargs = {
    'name': 'nbox',
    'version': '0.1.6',
    'description': 'ML Inference 🥶',
    'long_description': '# Nbox\n\nA library that makes using a host of models provided by the opensource community a lot more easier. \n\n> The entire purpose of this package is to make inference chill.\n\n```\npip install nbox\n```\n\n## Usage\n\n```python\nimport nbox\n\n# As all these models come from the popular frameworks you use such as \n# torchvision, efficient_pytorch or hf.transformers\nmodel = nbox.load("torchvision/mobilenetv2", pretrained = True)\n\n# nbox makes inference the priority so you can use it\n# pass it a list for batch inference \nout_single = model(\'cat.jpg\')\nout = model([Image.open(\'cat.jpg\'), np.array(Image.open(\'cat.jpg\'))])\ntuple(out.shape) == (2, 1000)\n\n# deploy the model to a managed kubernetes cluster on NimbleBox.ai\nurl_endpoint, nbx_api_key = model.deploy()\n\n# or load a cloud infer model and use seamlessly\nmodel = nbox.load(\n  model_key_or_url = url_endpoint,\n  nbx_api_key = nbx_api_key,\n  category = "image"\n)\n\n# Deja-Vu!\nout_single = model(\'cat.jpg\')\nout = model([Image.open(\'cat.jpg\'), np.array(Image.open(\'cat.jpg\'))])\ntuple(out.shape) == (2, 1000)\n```\n\n## Things for Repo\n\n- Using [`poetry`](https://python-poetry.org/) for proper package management as @cshubhamrao says.\n  - Add new packages with `poetry add <name>`. Do not add `torch`, `tensorflow` and others, useless burden to manage those.\n  - When pushing to pypi just do `poetry build && poetry publish` this manages all the things around\n- Install `pytest` and then run `pytest tests/ -v`.\n- Using `black` for formatting, VSCode to the moon.\n\n# License\n\nThe code in thist repo is licensed as [BSD 3-Clause](./LICENSE). Please check for individual repositories for licenses. Here are some of them:\n\n### Requirements\n\n- [`rich`](https://github.com/willmcgugan/rich/blob/master/LICENSE)\n\n### Model Sources\n\n99% of the credit for `nbox` goes to the amazing people behind these projects:\n\n- [`torch`](https://github.com/pytorch/pytorch/blob/master/LICENSE)\n- [`transformers`](https://github.com/huggingface/transformers/blob/master/LICENSE)\n- [`efficientnet-pytorch`](https://github.com/lukemelas/EfficientNet-PyTorch/blob/master/LICENSE)\n',
    'author': 'Yash Bonde',
    'author_email': 'bonde.yash97@gmail.com',
    'maintainer': 'Yash Bonde',
    'maintainer_email': 'bonde.yash97@gmail.com',
    'url': 'https://docs.nimblebox.ai/nbox/python-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
