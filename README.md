# Python HPC

Optimizaciones incrementales de N-Body (*all-pairs*) con el fin de evaluar y comparar las prestaciones de los traductores de Python en el ámbito de HPC. Este trabajo ha servido como base para las siguientes publicaciones:

- **Springer** - [Performance Comparison of Python Translators for a Multi-threaded CPU-bound Application](https://link.springer.com/chapter/10.1007/978-3-031-05903-2_2)
```
@InProceedings{10.1007/978-3-031-05903-2_2,
  author="Milla, Andr{\'e}s
  and Rucci, Enzo",
  editor="Pesado, Patricia
  and Gil, Gustavo",
  title="Performance Comparison of Python Translators for a Multi-threaded CPU-Bound Application",
  booktitle="Computer Science -- CACIC 2021",
  year="2022",
  publisher="Springer International Publishing",
  address="Cham",
  pages="21--38",
  abstract="Currently, Python is one of the most widely used languages in various application areas. However, it has limitations when it comes to optimizing and parallelizing applications due to the nature of its official CPython interpreter, especially for CPU-bound applications. To solve this problem, several alternative translators have emerged, each with a different approach and its own cost-performance ratio. Due to the absence of comparative studies, we have carried out a performance comparison of these translators using N-Body as a case study (a well-known problem with high computational demand). The results obtained show that CPython and PyPy presented poor performance due to their limitations when it comes to parallelizing algorithms; while Numba and Cython achieved significantly higher performance, proving to be viable options to speed up numerical algorithms.",
  isbn="978-3-031-05903-2"
}

```
- **Tesina de grado** - [Un Estudio Comparativo entre Traductores de Python para Aplicaciones Paralelas de Memoria Compartida](http://sedici.unlp.edu.ar/handle/10915/133463)
  - [Presentación](https://docs.google.com/presentation/d/12FppMCOUSMPD140URRJLe8UJ6pOpUX1LFrOkLnjcz9g/edit?usp=sharing)
```
@phdthesis{milla2022estudio,
  title={Un estudio comparativo entre traductores de Python para aplicaciones paralelas de memoria compartida},
  author={Milla, Andr{\'e}s},
  year={2022},
  school={Universidad Nacional de La Plata}
}
```
- **PyConAr 2021** - [Acelerando aplicaciones paralelas en Python: Numba vs. Cython](https://eventos.python.org.ar/events/pyconar2021/activity/448/)
```
@misc{milla_rucci_pycon,
  address = {PyCon 2021},
  type = {Conferencia},
  title = {Acelerando aplicaciones paralelas en {Python}: {Numba} vs. {Cython}},
  url = {https://eventos.python.org.ar/events/pyconar2021/activity/448/},
  author={Milla, Andr{\'e}s and Rucci, Enzo},
  month = oct,
  year = {2021},
}
```
- **CACIC 2021** - [Acelerando código científico en Python usando Numba](http://sedici.unlp.edu.ar/handle/10915/126012)
```
@inproceedings{milla_rucci_cacic,
  title={Acelerando c{\'o}digo cient{\'\i}fico en Python usando Numba},
  author={Milla, Andr{\'e}s and Rucci, Enzo},
  booktitle={XXVII Congreso Argentino de Ciencias de la Computaci{\'o}n (CACIC 2021)},
  year={2021}
}
```

## Organización

El código fuente se encuentra en el directorio `src`, el cual contiene los siguientes subdirectorios:

- `versions`: Contiene el código fuente de cada versión probada.
- `benchmarker`: Script para realizar los benchmarks.
- `test`: Tests de las versiones desarrolladas.
- `core`: Utilidades comunes a los módulos.


## Contribución

### Requisitos

| Paquete     | Versión     |
| ----------- | ----------- |
| Python      | 3.8.10      |
| PyPy        | 7.3.1       |
| Cython      | 0.29.22     |
| Pip         | 21.0.1      |
| Virtualenv  | 20.0.17     |


En entornos basados en Debian se pueden instalar con el siguiente comando:

```apt-get install python3 python3-pip cython pypy3 virtualenv```

### Ejecución

1. Instalar las dependencias:

   ```make install```

2. Configurar los parámetros del benchmark en el archivo `config.toml` y ejecutar:

   ```make benchmark```

Los resultados podrán verse en el directorio `benchmarks`.

- *Nota*: En caso de no disponer el compilador ICC, se puede optar por otro a través del `Makefile`.

## Contacto

- [andressmilla@gmail.com](mailto:andressmilla@gmail.com)
- [erucci@lidi.info.unlp.edu.ar](mailto:erucci@lidi.info.unlp.edu.ar)
