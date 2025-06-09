import unreal

# --- Настройки ---
ASSET_PATH = "/Game/"  # Папка, в которой валидируем ассеты
ALLOWED_LIGHTMAP_RES = (32, 512)
NAMING_RULES = {
    "StaticMesh": "SM_",
}

# --- Хелпер логов ---
def log(msg):
    unreal.log(msg)

# --- Проверка количества UV каналов (LOD0) ---
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

# --- Валидация StaticMesh ассета ---
def validate_static_mesh(asset_data):
    asset_name = str(asset_data.asset_name)
    asset = asset_data.get_asset()
    issues = []

    # Нейминг
    if not asset_name.startswith(NAMING_RULES["StaticMesh"]):
        issues.append("Bad naming (should start with SM_)")

    # LOD'ы
    if asset.get_num_lods() < 2:
        issues.append("No LODs")

    # Коллизия
    try:
        has_collision = asset.get_editor_property("has_collision")
        if not has_collision:
            issues.append("No collision")
    except Exception as e:
        issues.append(f"Collision check failed: {e}")

    # UV2
    try:
        uv_channels = get_num_uv_channels(asset)
        if uv_channels < 2:
            issues.append("Less than 2 UV channels (likely no UV2 for Lightmap)")
    except Exception as e:
        issues.append(f"UV channel check failed: {e}")

    # Lightmap resolution
    try:
        res = asset.light_map_resolution
        if res < ALLOWED_LIGHTMAP_RES[0] or res > ALLOWED_LIGHTMAP_RES[1]:
            issues.append(f"Lightmap resolution out of bounds: {res}")
    except Exception as e:
        issues.append(f"Lightmap resolution check failed: {e}")

    return issues

# --- Основной запуск ---
def run_validator():
    log("=== Starting Asset Validation ===")

    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = asset_registry.get_assets_by_path(ASSET_PATH, recursive=True)

    for asset_data in assets:
        asset_class = asset_data.asset_class_path.asset_name

        if asset_class == "StaticMesh":
            issues = validate_static_mesh(asset_data)
            asset_path = str(asset_data.package_name)

            if issues:
                log(f"[!] {asset_path}:")
                for issue in issues:
                    log(f"    - {issue}")
            else:
                log(f"[OK] {asset_path}")

    log("=== Validation Complete ===")

# --- Запуск ---
run_validator()
