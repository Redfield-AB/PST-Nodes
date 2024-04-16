
![pst_header](./.static/pst_header.svg)

<p align="center"> 
Personal Storage Table Extension for Knime
</p>


<p align="center">
    <a href="">
        <img alt="GitHub release" src="https://img.shields.io/badge/Python-%3E%3D3.9-green">
     </a>
    <a href="https://github.com/Redfield-AB/PST-Nodes/actions/workflows/unit_tests.yml" target="_blank">
        <img src="https://github.com/Redfield-AB/PST-Nodes/actions/workflows/unit_tests.yml/badge.svg" alt="lint">
    </a>
</p>



## Installation:

You can currently install the extension through the zipped update site. Once you've downloaded and unzipped the folder, follow these steps to access the extension:

- Add the unzipped folder to KNIME AP as a Software Site in File → Preferences → Install/Update → Available Software Sites

- Go to Install KNIME Extensions and search for `personal storage table `

<video width="820" height="440" controls>
    <source src="./.static/pst demo.mov" type="video/mp4">
</video>

![](./.static/pst%20demo.mov)

## Devlopement 🚀

🚨 Please read the [guidelines for contributing](./CONTRIBUTING.md) 


It is recommended to have Python 3.9+

First clone this repo, then navigate to the folder `PST-Nodes`:

```
$ git clone https://github.com/Redfield-AB/PST-Nodes.git

$ cd PST-Nodes
```
Switch to the dev branch by running the following command:

```
$ git checkout dev
```
Make sure that the dev branch is up-to-date by running the following command:

```
$ git pull
```
Create your feature/ bugfix branch off of dev branch. Check [guidelines for contributing](./CONTRIBUTING.md) for branches naming conventions.

```
$ git checkout -m `your_branch_name`
```

Create a conda/Python environment containing the [knime-python-base](https://anaconda.org/knime/knime-python-base) metapackage, together with the node development API [knime-extension](https://anaconda.org/knime/knime-extension).

```
$ conda create -n my_python_env python=3.9 knime-python-base=5.2 knime-extension=5.2 -c knime -c conda-forge
```

Install requirments

```
$ pip install -r requirments.txt
```

Update the [config.yml](./config.yml) as described [here](https://docs.knime.com/latest/pure_python_node_extensions_guide/index.html#tutorial-writing-first-py-node)