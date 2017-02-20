# conan-libuv

[Conan](http://conan.io) C++ dependency definition for the [LibUV](http://libuv.org) asynchronous I/O framework.

`conaninfo.txt` usage:

```Ini
[requires]
LibUV/1.9.1@cloudwall/stable

[generators]
cmake
```

`conaninfo.py` usage:

```python
generators = "cmake"

def config_options(self):
    self.requires.add("LibUV/1.9.1@cloudwall/stable")
```