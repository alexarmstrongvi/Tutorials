# Julia Tutorial
================

# Installation
`brew install julia`

# Environment/Package management
* Resources
    * [Official Docs](https://pkgdocs.julialang.org/)
    * [Towards Data Science](https://towardsdatascience.com/how-to-setup-project-environments-in-julia-ec8ae73afe9c)

Julia has a built-in package manager for creating projects (same as python viritual env?).
However, it doesn't appear that you can easily create viritual envs for a specific julia version.

For a new env
```bash
julia> ]
pkg> generate my_env
pkg> activate my_env
pkg> status
pkg> add cool_package
pkg> remove pacakge_i_dont_want
pkg> <backspace> or <ctrl> + c
```

To start up julia in an environment
`>> julia --project=path/to/project_dir


# Running in Jupyter Notebook
* Create a conda env with the correct version of python and jupyter notebook
    * What is the latest version that is compatible with IJulia?

# Things to look into
* REPLs
    * Julia REPL
    * Pkg REPL
    * Shell REPL

# Resources
* [Style guide](https://docs.julialang.org/en/v1/manual/style-guide/)
