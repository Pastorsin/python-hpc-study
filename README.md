# Python HPC

Optimizaciones incrementales de N-Body (*all-pairs*) con el fin de evaluar y comparar las prestaciones de los traductores de Python en el ámbito de HPC. Este trabajo ha servido como base para las siguientes publicaciones:

- **CACIC 2021** - [Acelerando código científico en Python usando Numba](http://sedici.unlp.edu.ar/handle/10915/126012)
```
@inproceedings{milla_rucci_cacic,
  title={Acelerando c{\'o}digo cient{\'\i}fico en Python usando Numba},
  author={Milla, Andr{\'e}s and Rucci, Enzo},
  booktitle={XXVII Congreso Argentino de Ciencias de la Computaci{\'o}n (CACIC 2021)},
  year={2021}
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
- **Tesina de grado** - Un Estudio Comparativo entre Traductores de Python para Aplicaciones Paralelas de Memoria Compartida (*en proceso*)
  - [Presentación](https://docs.google.com/presentation/d/12FppMCOUSMPD140URRJLe8UJ6pOpUX1LFrOkLnjcz9g/edit?usp=sharing)

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
