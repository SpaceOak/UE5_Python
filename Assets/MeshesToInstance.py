import unreal

def log(msg):
    unreal.log(msg)

def convert_selected_to_instanced():
    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    selected_actors = actor_subsystem.get_selected_level_actors()

    static_mesh_actors = [
        actor for actor in selected_actors
        if actor.get_class().get_name() == "StaticMeshActor"
    ]

    if len(static_mesh_actors) < 2:
        log("Select at least 2 StaticMeshActors to combine.")
        return

    mesh_ref = static_mesh_actors[0].static_mesh_component.static_mesh
    for actor in static_mesh_actors:
        if actor.static_mesh_component.static_mesh != mesh_ref:
            log("[!] Not all selected actors share the same Static Mesh.")
            return

    location = static_mesh_actors[0].get_actor_location()
    rotation = static_mesh_actors[0].get_actor_rotation()

    # Спавним StaticMeshActor
    new_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, location, rotation)

    # Отключаем видимость StaticMeshComponent
    smc = new_actor.static_mesh_component
    smc.set_visibility(False, True)
    smc.set_editor_property("hidden_in_game", True)
    smc.set_editor_property("mobility", unreal.ComponentMobility.STATIC)

    # Создаём InstancedStaticMeshComponent
    ism_component = unreal.InstancedStaticMeshComponent(outer=new_actor)
    ism_component.set_editor_property("static_mesh", mesh_ref)

    # Назначаем как RootComponent
    new_actor.set_editor_property("root_component", ism_component)

    # Добавляем инстансы
    for actor in static_mesh_actors:
        transform = actor.get_actor_transform()
        ism_component.add_instance(transform)

    new_actor.set_actor_label(f"ISM_{mesh_ref.get_name()}")

    for actor in static_mesh_actors:
        unreal.EditorLevelLibrary.destroy_actor(actor)

    log(f"[✓] Created ISM actor with {len(static_mesh_actors)} instances of {mesh_ref.get_name()}")

# --- Запуск ---
convert_selected_to_instanced()
