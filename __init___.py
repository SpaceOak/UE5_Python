import sys, os

plugin_dir = os.path.dirname(__file__)
if plugin_dir not in sys.path:
    sys.path.append(plugin_dir)

# Р”РѕР±Р°РІР»РµРЅРёРµ РІСЃРµС… РїРѕРґРїР°РїРѕРє (СЃР°Р±РјРѕРґСѓР»РµР№)
for name in os.listdir(plugin_dir):
    full_path = os.path.join(plugin_dir, name)
    if os.path.isdir(full_path) and not name.startswith("__"):
        if full_path not in sys.path:
            sys.path.append(full_path)