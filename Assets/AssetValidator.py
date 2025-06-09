import unreal
import json
import os

# --- Загрузка конфигурации ---
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

with open(CONFIG_PATH, "r") as f:
    CONFIG = json.load(f)

ASSET_PATH = CONFIG.get("asset_path", "/Game/")
ALLOWED_LIGHTMAP_RES = tuple(CONFIG.get("allowed_lightmap_resolution", [32, 512]))
NAMING_RULES = CONFIG.get("naming_rules", {"StaticMesh": "SM_"})
VERBOSE = CONFIG.get("verbose", False)

# --- Лог ---
def log(msg, force=False):
    if VERBOSE or force:
        unreal.log(msg)

# --- UV каналов ---
def get_num_uv_channels(mesh):
    try:
        lods = mesh.get_editor_property("lods")
        if not lods or len(lods) == 0:
            return 0
        build_settings = lods[0].get_editor_property("build_settings")
        generate_lightmap_uvs = build_settings.get_editor_property("generate_lightmap_uvs")
        return 2 if generate_lightmap_uvs else 1
    except Exception:
        return 0

# --- Коллизия ---
def has_valid_collision(mesh):
    try:
        body_setup = mesh.get_editor_property("body_setup")
        return body_setup is not None
    except:
        return False

# --- Lightmap Res ---
def get_lightmap_resolution(mesh):
    try:
        lods = mesh.get_editor_property("lods")
        if not lods or len(lods) == 0:
            return 0
        return lods[0].get_editor_property("light_map_resolution")
    except:
        return 0

# --- Валидация ---
def validate_static_mesh(asset_data):
    asset_name = str(asset_data.asset_name)
    asset = asset_data.get_asset()
    issues = []

    log(f"Validating asset: {asset_name}")

    # Нейминг
    expected_prefix = NAMING_RULES.get("StaticMesh", "")
    if not asset_name.startswith(expected_prefix):
        issues.append("Bad naming (should start with SM_)")
    else:
        log("✓ Naming OK")

    # LODs
    lods_count = asset.get_num_lods()
    log(f"LOD count: {lods_count}")
    if lods_count < 2:
        issues.append("No LODs")
    else:
        log("✓ LODs OK")

    # Коллизия
    if not has_valid_collision(asset):
        issues.append("No collision")
    else:
        log("✓ Collision OK")

    # UV каналы
    uv_channels = get_num_uv_channels(asset)
    log(f"UV channels: {uv_channels}")
    if uv_channels < 2:
        issues.append("Less than 2 UV channels (likely no UV2 for Lightmap)")
    else:
        log("✓ UV channels OK")

    # Lightmap resolution
    res = get_lightmap_resolution(asset)
    log(f"Lightmap resolution: {res}")
    if res < ALLOWED_LIGHTMAP_RES[0] or res > ALLOWED_LIGHTMAP_RES[1]:
        issues.append(f"Lightmap resolution out of bounds: {res}")
    else:
        log("✓ Lightmap resolution OK")

    return issues

# --- Основной проход ---
def run_validator():
    log("=== Starting Asset Validation ===", force=True)

    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = asset_registry.get_assets_by_path(ASSET_PATH, recursive=True)

    for asset_data in assets:
        asset_class = asset_data.asset_class_path.asset_name

        if asset_class == "StaticMesh":
            issues = validate_static_mesh(asset_data)
            asset_path = str(asset_data.package_name)

            if issues:
                log(f"[!] {asset_path}:", force=True)
                for issue in issues:
                    log(f"    - {issue}", force=True)
            else:
                log(f"[OK] {asset_path}", force=True)

    log("=== Validation Complete ===", force=True)

# --- Запуск ---
run_validator()
