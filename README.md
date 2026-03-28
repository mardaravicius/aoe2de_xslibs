# aoe2de_xslibs

Python-authored XS libraries for Age of Empires II: DE.

This project depends on `aoe2de_xs_converter` via GitHub instead of a
machine-specific filesystem path. That makes installs portable across
computers as long as Git can access the repository.

For local development on both repos at once, install the converter first and
then install this project without re-resolving dependencies:

```bash
pip install -e ~/PyCharmProjects/aoe2de_xs_converter
pip install -e ~/PyCharmProjects/aoe2de_xslibs --no-deps
```

For reproducible releases, replace the `@main` Git dependency with a tag or
commit pin after you create converter releases.
