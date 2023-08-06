# jlmc

Generate documentation cards for code in JupyterLab.

## Requirements

* JupyterLab >= 3.0


## Installation
```bash
pip install jlmodelcards
```


## Development Installation
There are two versions of this extension, each supporting v2 and v3 of JupyterLab.


Create a `conda` environment if you do not have an environment already.
```bash
conda create -n [environment-name] --override-channels --strict-channel-priority -c conda-forge -c anaconda jupyterlab cookiecutter nodejs git
```
Activate the environment.
```bash
conda activate [environment-name]
```

Since there is only one python dependeny, there is no `environment.yml` file. You can install the `jupyterlab` package.
```bash
# for JupyterLab 3.x 
conda install -c conda-forge jupyterlab
```

If you want to install the previou version of Jupyterlab.
```bash
# for JupyterLab 2.x 
conda install -c conda-forge jupyterlab=2
```

Once you install `jupyterlab`, you can access `jlpm` which is JupyterLab's pinned version of [yarn](https://yarnpkg.com/).
```bash
# Install dependencies
jlpm install
```

You can install the extension without building as well.
```bash
jupyter labextension install . --no-build
```

You can watch the source directory and run JupyterLab in watch mode to watch for changes in the extension's source and automatically rebuild the extension and application.

```bash
# Watch the source directory in another terminal tab
jlpm watch
# Run jupyterlab in watch mode in one terminal tab
jupyter lab --watch
```

Once you make any changes to the code, you can rebuild the extension.
```bash
jlpm run build
```

