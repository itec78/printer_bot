import importlib.util
import logging
import os

logger = logging.getLogger(__name__)


def load_plugins(plugins_dir):
	"""Import every plugins/<name>/*.py plugin and index it by its COMMANDS aliases."""
	plugins = {}
	for dirname in sorted(os.listdir(plugins_dir)):
		plugin_dir = os.path.join(plugins_dir, dirname)
		if dirname.startswith("_") or not os.path.isdir(plugin_dir):
			continue

		pyfiles = [f for f in sorted(os.listdir(plugin_dir)) if f.endswith(".py") and not f.startswith("_")]
		if not pyfiles:
			logger.warning(f"Plugin folder '{dirname}' has no .py file, skipping")
			continue

		# Prefer a file matching the folder name, otherwise accept a single unambiguous file
		fname = f"{dirname}.py" if f"{dirname}.py" in pyfiles else None
		if fname is None:
			if len(pyfiles) > 1:
				logger.warning(f"Plugin folder '{dirname}' has multiple .py files ({', '.join(pyfiles)}) and none matches the folder name, skipping")
				continue
			fname = pyfiles[0]

		fpath = os.path.join(plugin_dir, fname)
		modname = f"plugins.{dirname}"
		spec = importlib.util.spec_from_file_location(modname, fpath)
		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)
		for cmd in getattr(module, "COMMANDS", []):
			cmd = cmd.lower()
			if cmd in plugins:
				logger.warning(f"Command '{cmd}' from plugin '{dirname}' overrides plugin '{plugins[cmd].NAME}'")
			plugins[cmd] = module
	return plugins
