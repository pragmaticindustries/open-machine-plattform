# Open Machinery Plattform (OMAP)

Welcome to the *Open MAchine Platform (OMAP*)!
The aim of *OMAP* is to make adoption of *industry 4.0* or *digitalization* easy to use and adoptable for companies of all sizes and of all roles.

Speaking of roles, we usually distinguish between **Machine Manufacturers**, i.e. Companies that build and sell *Machines* and **Machine Operators**, i.e. Companies that use *Machines* to produce whatever they produce.

The *OMAP* project aims especially at pushing the cooperation of all involved parties over machine data to build ecosystems that lead to a gain for all involved parties.

Documentation can be found on [readthedocs](https://omap.readthedocs.io/en/latest/).

## Start the OMAP

OMAP relies on a module system which extends Django Apps.
Just start it with the omap.py script (which is pretty similar to manage.py).

```
python omap.py runserver
```
or
```
./omap.py runserver
```

After this start it behaves exactly like a regular django project.
So migrations can e.g. be done via
```
./omap.py migrate
```
etc...

## Run Docker

To run the application in docker, run the following:
```
docker pull pragmaticindustriesgmbh/open-machine-platform
docker run -p 8000:8000 ragmaticindustriesgmbh/open-machine-platform
```
## Build Docker

If you want to build and run the docker image yourself, you can do so by running:
```
docker build -t pragmaticindustriesgmbh/open-machine-platform:latest . && docker run -p 8000:8000 pragmaticindustriesgmbh/open-machine-platform:latest
```
