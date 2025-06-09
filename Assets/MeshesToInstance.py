import unreal

def convert_selected_to_instanced():
    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    selected_actors = actor_subsystem.get_selected_level_actors()

    static_mesh_actors = [
        actor for actor in selected_actors
        if actor.get_class().get_name() == "StaticMeshActor"
    ]

    if len(static_mesh_actors) < 2:
        unreal.log_error("Select at least 2 StaticMeshActors.")
        return

    static_mesh = static_mesh_actors[0].static_mesh_component.static_mesh
    if not static_mesh:
        unreal.log_error("Selected actors have no StaticMesh assigned.")
        return

    for actor in static_mesh_actors:
        if actor.static_mesh_component.static_mesh != static_mesh:
            unreal.log_error("Not all selected actors share the same Static Mesh.")
            return

    materials = static_mesh_actors[0].static_mesh_component.get_materials()

    location = static_mesh_actors[0].get_actor_location()
    rotation = static_mesh_actors[0].get_actor_rotation()

    new_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Actor, location, rotation)
    new_actor.set_actor_label(f"ISM_{static_mesh.get_name()}")

    ism_component = unreal.InstancedStaticMeshComponent(outer=new_actor, name="GeneratedISM")
    ism_component.set_editor_property("static_mesh", static_mesh)
    ism_component.set_editor_property("mobility", unreal.ComponentMobility.STATIC)

    for i, mat in enumerate(materials):
        ism_component.set_material(i, mat)

    new_actor.set_editor_property("root_component", ism_component)

    added = 0
    for actor in static_mesh_actors:
        transform = actor.get_actor_transform()
        if ism_component.add_instance(transform) != -1:
            added += 1
        else:
            unreal.log_warning(f"Failed to add instance from {actor.get_name()}")

    for actor in static_mesh_actors:
        actor_subsystem.destroy_actor(actor)

    unreal.log(f"[✓] Created ISM actor with {added} instances of {static_mesh.get_name()}")

# Запуск
convert_selected_to_instanced()
