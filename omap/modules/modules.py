"""
This is a very first draft idea of a module system.

The general idea is to NOT use Djangos ``django.setup()`` which inherently uses the ENV Variable to find the path
to a settings.py and loads it.

Instead we use the ``settings.configure()`` method INSTEAD of ``django.setup()`` where you can pass in arbitrary settings.

From my understanding ``django.setup()`` BASICALLY does nothing else than to load the settings.py (from the ENV variable)
and then calls configure with all (ALL CAPS) Variables from the settings.py file.
"""
import importlib
import inspect
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Optional, List, Set, Union, Iterable

logger = logging.getLogger("modules")

MODULE_LOCATIONS = ["omap.modules.omap_module_registry"]

_modules = []


def modules():
    return _modules


class ModuleConfig:
    pass


class OmapModule(object):
    """
    Very simple implementation of all properties of a "Module"
    """

    def __init__(
        self,
        module_name,
        module_version,
        django_apps,
        module_dependencies: Optional[List[str]] = None,
        settings_entries: Optional[Dict] = None,
        constance_config: Optional[Dict] = None,
        pip_dependencies=None,
    ) -> None:
        self.module_name = module_name
        self.module_version = module_version
        self.django_apps = django_apps
        self.module_dependencies = module_dependencies
        self.settings_entries = settings_entries
        self.constance_config = constance_config
        self.pip_dependencies = pip_dependencies


BASE_DIR = Path(__file__).resolve().parent.parent


def collect_registry(module_locations: List[str]):
    module_configs = {}

    for module in module_locations:
        logger.debug(f"Checking module {module}")
        m = importlib.import_module(module)

        module_definitions = []

        for a, b in inspect.getmembers(m):
            if inspect.isclass(b) and inspect.getmodule(b) == m:
                if issubclass(b, ModuleConfig):
                    logger.debug(f"Adding class {b} to module definitions")
                    module_definitions.append(b)

        if len(module_definitions) == 0:
            logger.warning(f"No module definition found in module {module}")
            continue

        for definition in module_definitions:
            logger.debug(
                f"We found definition {definition.__name__} in module {module}"
            )

            # Get all necessary attributes
            attributes = {
                "module_name": None,
                "module_version": None,
                "django_apps": None,
                "pip_dependencies": [],
                "module_dependencies": [],
                "settings_entries": {},
                "constance_config": {},
            }

            module_dict = {}
            for attr_name, default in attributes.items():
                if not hasattr(definition, attr_name):
                    if default is not None:
                        module_dict[attr_name] = default
                        continue
                    else:
                        raise RuntimeError(f"Missing required attribute {attr_name}")
                module_dict[attr_name] = getattr(definition, attr_name)

            logger.debug(f"Module Dict: {module_dict}")

            if module_dict["module_name"] in module_configs:
                raise RuntimeError(
                    f"Duplicate Module Name found: {module_dict['name']}"
                )

            # Create Portal Module class from it
            module_configs[module_dict["module_name"]] = OmapModule(**module_dict)

    return module_configs


# This is a draft for a registr.
# In a real world scenario this would be loaded from some manifest or cfg files or something?!
modules_registry = collect_registry(MODULE_LOCATIONS)


def resolve(modules: Union[str, List[str]]) -> Iterable[OmapModule]:
    """
    This method takes one or more module names and looks up the modules in the registry above.
    Then it checks if the modules have dependencies on other moduels and if so, adds them to the "context" as well.

    It finally returns a complete list of all modules that have to be loaded
    OR
    ends with an exception
    """
    unresolved = [modules] if isinstance(modules, str) else modules
    if len(unresolved) == 0:
        raise AssertionError("No module given to load, terminating!")
    resolved = []
    # resolve until all are resolved
    while len(unresolved) > 0:
        module_name = unresolved.pop()
        logging.info(f"Checking resolution for {module_name}")
        if module_name in resolved:
            unresolved.remove(module_name)
            continue
        logging.info(f"Resolving {module_name}")
        module: OmapModule = modules_registry.get(module_name)
        if not module:
            raise RuntimeError(f"Unresolvable Module {module_name}")
        resolved.append(module)
        if module.module_dependencies:
            logging.info(f"Found dependencies: {module.module_dependencies}")
            unresolved.extend(module.module_dependencies)

    logging.info(
        f"Modules to load: {[m.module_name + ':' + m.module_version for m in resolved]}"
    )

    return resolved


def install_modules(modules: Iterable[OmapModule]):
    def install(package):
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    logging.info("Check if there are module dependencies to install...")
    for module in modules:
        module: OmapModule
        logging.info(f"Checking Module {module.module_name}:{module.module_version}")
        if module.pip_dependencies:
            logging.info(
                f"Module {module.module_name}:{module.module_version} has dependencies"
            )
            for package in module.pip_dependencies:
                logging.info(f"Start Installation of package {package}")
                try:
                    install(package)
                    logging.info(f"Successfully installed {package}")
                except Exception:
                    raise ModuleNotFoundError(
                        f"Unable to install package {package} for Module {module.module_name}:{module.module_version}"
                    )
            logging.info(
                f"Successfully installed all dependencies for {module.module_name}:{module.module_version}"
            )


def configure_modules():
    """
    This is the central hook.
    It loads the name(s) of the Modules to load from the env variable OMAP_MODULES,
    resolves them and then configures django accordingly.
    So this is a somewhat "improved" version of the ``django.setup()`` function but serves the same purpose
    """

    # Add them to the "installed" modules

    logging.basicConfig(level="INFO")
    # Manipulate classpath
    sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
    sys.path.insert(0, os.path.join(BASE_DIR, "packages/portal_theme"))

    modules = get_resolved_modules()

    global _modules
    _modules = modules.copy()

    apps: Set = set()
    additional_settings = {}
    constance_config = {}

    # Install modules
    install_modules(modules)

    for module in modules:
        module: OmapModule
        apps.update(module.django_apps)
        if module.settings_entries:
            additional_settings.update(module.settings_entries)
        if module.constance_config:
            constance_config.update(module.constance_config)

    from django.conf import settings

    # merge constnace configs, if there are multiple ones
    if "CONSTANCE_CONFIG" in additional_settings:
        constance_config.update(additional_settings["CONSTANCE_CONFIG"])
        del additional_settings["CONSTANCE_CONFIG"]

    base_settings = {}
    if os.getenv("DJANGO_SETTINGS_MODULE"):
        # We can use a base settings file
        mod = importlib.import_module(os.getenv("DJANGO_SETTINGS_MODULE"))
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)
                base_settings[setting] = setting_value

    # We have to be careful with the merge especially with INSTALLED_APPS
    merged_apps = (
        base_settings.get("INSTALLED_APPS", [])
        + additional_settings.get("INSTALLED_APPS", [])
        + list(apps)
    )
    # Same goes with CONSTANCE Config
    merged_constance = {**base_settings.get("CONSTANCE_CONFIG", {}), **constance_config}

    merged = base_settings.copy()
    merged.update(additional_settings)

    # Handle special cases
    merged.update({"INSTALLED_APPS": merged_apps})
    merged.update({"CONSTANCE_CONFIG": merged_constance})

    # TEST for dynamic urls
    merged.update({"ROOT_URLCONF": "omap.modules.module_urls"})

    settings.configure(**merged)

    # Now modify the INSTALLED_APPS for all apps that contain a urls.py file
    # TODO do this after the apps are ready
    # from django.apps import apps as django_apps
    #
    # for app in django_apps.get_app_configs():
    #     if not hasattr(app, "url_prefix"):
    #         urls_path = app.module.__name__ + ".urls"
    #         try:
    #             mod = importlib.import_module(urls_path)
    #         except ModuleNotFoundError:
    #             logging.debug(f"No url module found under {urls_path}", exc_info=True)
    #             continue
    #         # We can/should add it
    #         setattr(app, "url_prefix", app.name)


def get_resolved_modules(module_names=None):
    if module_names:
        modules = module_names
    else:
        # Read from ENV Variable
        modules = os.getenv("OMAP_MODULES")

    if not modules:
        # TODO do we need this?
        # raise RuntimeError(
        #     "No Modules given, please set the module to env varibale OMAP_MODULES"
        # )
        return []
    module_list = modules.split(",")
    modules = resolve(module_list)
    return modules
