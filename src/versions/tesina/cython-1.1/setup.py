from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

ext_modules = [
    Extension(
        "cynbody",
        ["cynbody.pyx"],
        extra_compile_args=["-O3", "-xCORE-AVX512", "-qopt-zmm-usage=high"],
    )
]

setup(
    name="cynbody",
    cmdclass={"build_ext": build_ext},
    ext_modules=cythonize(ext_modules, language_level="3"),
)
