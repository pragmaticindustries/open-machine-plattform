Architecture of the platform
=========================================

The OMAP Backend is built on top of `Django <https://www.djangoproject.com/>`_ which is written in `Python <https://www.python.org/>`_.
Django calls itself the Framework for *perfectionists with deadlines* and this is one reason why we consider it a good choice.
On the other hand, besides all C-based languages python is widely adopted in the industry and thus a machine manufacturers may already have a team capable of writing Python.

The general structure at the moment is a `modular monolith <https://www.jrebel.com/blog/what-is-a-modular-monolith>`_ but there are REST APIs for nearly every operation so that it could also be extended with containers.
We have chosen this approach as it leads to a (in our opinion) reasonable tradeoff between modularity and operational complexity.
The modules are basically `django-apps <https://docs.djangoproject.com/en/4.0/ref/applications/>`_ but extended via a module system (TODO: Module System).

Currently, we only barely use javascript on the frontend and mostly rely on server-side rendering. Here, we follow the philosophy from the `Ruby on Rails <https://rubyonrails.org/>`_ Team.
They developed the `Hotwire Stack <https://hotwired.dev/>`_ as alternative to frontend frameworks like vue.js.
Although such an addition could be coming in the future.
Currently most javascript used is organized as `Stimulus.js <https://stimulus.hotwired.dev/>`_ Controllers.

Communication from Machines (or more general Edge Devices) is done via `MQTT <https://mqtt.org/>`_ but an AMQP Adapter is planned in the future.
A separate MQTT Process is running as bridge and can handle incoming MQTT messages.
We have our own pluggable MQTT Handler system to allow other Apps to bring further messaging handlers.
