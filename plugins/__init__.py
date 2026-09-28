import importlib.util
import os


def load_plugins(plugins_dir):
	"""Import every plugins/<name>/<name>.py plugin and index it by its COMMANDS aliases."""
	plugins = {}
	for dirname in sorted(os.listdir(plugins_dir)):
		plugin_dir = os.path.join(plugins_dir, dirname)
		fpath = os.path.join(plugin_dir, f"{dirname}.py")
		if dirname.startswith("_") or not os.path.isfile(fpath):
			continue
		modname = f"plugins.{dirname}"
		spec = importlib.util.spec_from_file_location(modname, fpath)
		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)
		for cmd in getattr(module, "COMMANDS", []):
			plugins[cmd.lower()] = module
	return plugins
