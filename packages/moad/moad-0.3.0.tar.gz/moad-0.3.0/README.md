# moad: Mix Open Api Documents

[![PyPI - License](https://img.shields.io/pypi/l/moad)](https://pypi.org/project/moad/)
[![PyPI](https://img.shields.io/pypi/v/moad)](https://pypi.org/project/moad/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/moad)

Tool to Mix Open Api Docs. You can copy components from other openapi docs. 
The tool was initially written to share objects between openapi docs if there is a requirement for the docs to be in a single file.

You can place the following comments in one openapi doc:
```yaml
# moad-mixin:begin:other.yml:components/schemas
# moad-mixin:end
```

moad will scan the file and attempt to replace the text between `begin` and `end` with the content of the schemas of file `test2.yml`

Usage:
```bash
python -m pip install moat
python -m moat

```

Cou can only select certain elements from a path
```yaml
# moad-mixin:begin:other.yml:components/schemas>address,user
# moad-mixin:end

```