from sisifo.namespaces import common


def _load_plugins():
    # Import here to avoid polluting "namespaces" module.
    import importlib
    import pkgutil

    for _, full_name, _ in pkgutil.iter_modules():
        if full_name.startswith("sisifo_"):
            _, name = full_name.split("_")
            globals()[name] = importlib.import_module(full_name)


_load_plugins()
