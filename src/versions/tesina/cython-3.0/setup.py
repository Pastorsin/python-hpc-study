from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

ext_modules = [
    Extension(
        "cynbody",
        ["cynbody.pyx"],
        extra_compile_args=[
            "-O3",
            "-march=native",
            "-ffast-math",
            "-qopenmp",
        ],
        extra_link_args=["-qopenmp"],
    )
]

setup(
    name="cynbody",
    cmdclass={"build_ext": build_ext},
    ext_modules=cythonize(ext_modules, language_level="3"),
)
