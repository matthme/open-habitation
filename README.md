# EcoHabitasOpen

This is a project started at the [Energy Data Hackdays 2021](https://energydatahackdays.ch/). Please see our [project page](https://hack.opendata.ch/project/779) for background.

## Service

This repository contains a minimal backend service API based on the [Falcon](http://falconframework.org/) framework, [Pandas DataPackage Reader](https://github.com/rgieseke/pandas-datapackage-reader), and the [Falcon plugin](https://github.com/alysivji/falcon-apispec) for [apispec](https://apispec.readthedocs.io/en/latest/index.html).

Install the [Poetry](https://python-poetry.org/) dependency manager, then:

```
poetry install
poetry shell
python api.py
```

At this point you should see the message "Serving on port..."

Test the API using a REST client such as [RESTer](https://github.com/frigus02/RESTer) with queries such as:

http://localhost:8000/bldg

## License

This package is licensed by its maintainers under the MIT License.

If you intended to use these data in a public or commercial product, please
check the data sources themselves for any specific restrictions.