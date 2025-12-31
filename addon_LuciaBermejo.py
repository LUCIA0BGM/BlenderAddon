bl_info = {
    "name" : "Herramientas de Lucia (Pro UI)",
    "blender" : (4, 0, 0),
    "category" : "Object / Mesh",
    "version" : (2, 9, 0),
    "author" : "Lucia Bermejo",
    "description" : "Toolkit completo. Pie Menu con estados visuales (Disabled)."
}

import bpy
import bmesh

# =========================================================================
# 1. SISTEMA DE DATOS
# =========================================================================

def init_props():
    bpy.types.Scene.lucia_tris_total = bpy.props.IntProperty(default=0)
    bpy.types.Scene.lucia_tris_idx   = bpy.props.IntProperty(default=0)
    bpy.types.Scene.lucia_ngons_total = bpy.props.IntProperty(default=0)
    bpy.types.Scene.lucia_ngons_idx   = bpy.props.IntProperty(default=0)
    
    bpy.types.Scene.lucia_source_obj = bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Fuente",
        description="Objeto del que copiaremos el material"
    )

def update_statistics(context):
    obj = context.active_object
    if not obj or obj.mode != 'EDIT':
        return

    bm = bmesh.from_edit_mesh(obj.data)
    tris_list = []
    ngons_list = []
    
    for f in bm.faces:
        v_len = len(f.verts)
        if v_len == 3: tris_list.append(f)
        elif v_len > 4: ngons_list.append(f)
            
    context.scene.lucia_tris_total = len(tris_list)
    context.scene.lucia_ngons_total = len(ngons_list)

    active = bm.faces.active
    
    if active in tris_list:
        context.scene.lucia_tris_idx = tris_list.index(active) + 1
    else:
        context.scene.lucia_tris_idx = 0
        
    if active in ngons_list:
        context.scene.lucia_ngons_idx = ngons_list.index(active) + 1
    else:
        context.scene.lucia_ngons_idx = 0

# =========================================================================
# 2. PANEL LATERAL
# =========================================================================

class LUCIA_PT_MainPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_lucia_tools"
    bl_label = "Herramientas de Artista"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Lucia Tools"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # --- Origen ---
        layout.label(text="Gestión:", icon="PREFERENCES")
        layout.operator("object.origin_to_world", text="Origen al Mundo", icon="EMPTY_DATA")
        
        # --- Materiales ---
        layout.separator()
        box_mat = layout.box()
        box_mat.label(text="Copiar Materiales:", icon="MATERIAL")
        row = box_mat.row()
        row.prop(scene, "lucia_source_obj", text="Fuente")
        row = box_mat.row()
        row.scale_y = 1.2
        if scene.lucia_source_obj:
            row.enabled = True
        else:
            row.enabled = False
        row.operator("object.link_picked_material", text="Aplicar a Selección", icon="PASTEDOWN")

        # --- Modelado ---
        layout.separator()
        layout.label(text="Modelado:", icon="EDITMODE_HLT")
        box = layout.box()
        box.label(text="Make Planar:", icon="MOD_DATA_TRANSFER")
        row = box.row(align=True)
        row.operator("mesh.make_planar_x", text="X")
        row.operator("mesh.make_planar_y", text="Y")
        row.operator("mesh.make_planar_z", text="Z")
        
        box.label(text="Loops Paralelos:", icon="MESH_GRID")
        row = box.row(align=True)
        sub = row.row(align=True)
        sub.scale_x = 1.2
        sub.operator("mesh.select_parallel_shrink", text="- Contraer", icon="REMOVE")
        sub.operator("mesh.select_parallel_grow", text="+ Expandir", icon="ADD")
        
        # --- Auditoría ---
        layout.separator()
        layout.label(text="Auditoría Topología:", icon="ERROR")
        layout.operator("mesh.force_update_stats", text="(Re)Calcular Datos", icon="FILE_REFRESH")

        # Tris
        box = layout.box()
        box.label(text="Triángulos:", icon="MESH_DATA")
        row = box.row(); split = row.split(factor=0.4) 
        split.operator("mesh.select_tris", text="Sel. Todos")
        split.label(text=f" Total: {scene.lucia_tris_total}")
        row = box.row(); split = row.split(factor=0.4) 
        op_focus = split.operator("mesh.navigate_error", text="Focus", icon="VIEWZOOM")
        op_focus.mode = 'TRI'; op_focus.direction = 0 
        row_nav = split.row(align=True); row_nav.alignment = 'LEFT'
        op_p = row_nav.operator("mesh.navigate_error", text="", icon="TRIA_LEFT"); op_p.mode='TRI'; op_p.direction=-1 
        idx = scene.lucia_tris_idx
        row_nav.label(text=f" Activo: {idx} " if idx > 0 else " Activo: - ")
        op_n = row_nav.operator("mesh.navigate_error", text="", icon="TRIA_RIGHT"); op_n.mode='TRI'; op_n.direction=1

        # N-Gons
        box = layout.box()
        box.label(text="N-Gons:", icon="MOD_BEVEL")
        row = box.row(); split = row.split(factor=0.4)
        split.operator("mesh.select_ngons", text="Sel. Todos")
        split.label(text=f" Total: {scene.lucia_ngons_total}")
        row = box.row(); split = row.split(factor=0.4)
        op_focus = split.operator("mesh.navigate_error", text="Focus", icon="VIEWZOOM")
        op_focus.mode = 'NGON'; op_focus.direction = 0
        row_nav = split.row(align=True); row_nav.alignment = 'LEFT'
        op_p = row_nav.operator("mesh.navigate_error", text="", icon="TRIA_LEFT"); op_p.mode='NGON'; op_p.direction=-1 
        idx = scene.lucia_ngons_idx
        row_nav.label(text=f" Activo: {idx} " if idx > 0 else " Activo: - ")
        op_n = row_nav.operator("mesh.navigate_error", text="", icon="TRIA_RIGHT"); op_n.mode='NGON'; op_n.direction=1

# =========================================================================
# 3. PIE MENU (DISEÑO GHOST)
# =========================================================================

class LUCIA_MT_PieMenu(bpy.types.Menu):
    bl_label = "Lucia Tools Pie"
    bl_idname = "LUCIA_MT_pie_menu"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        
        is_edit = (context.active_object and context.active_object.mode == 'EDIT')
        
        # Función auxiliar para dibujar botones grises si no es Edit Mode
        def draw_ghost(slot, op_id, txt, ico, props=None):
            if is_edit:
                # Botón Normal
                op = pie.operator(op_id, text=txt, icon=ico)
            else:
                # Botón Desactivado (Dentro de una columna disabled)
                col = pie.column()
                col.enabled = False
                op = col.operator(op_id, text=txt, icon=ico)
            
            # Asignar propiedades si existen
            if props and op:
                for attr, val in props.items():
                    setattr(op, attr, val)

        # 1. IZQUIERDA (WEST) - Siempre activo
        pie.operator("object.origin_to_world", icon="EMPTY_DATA")
        
        # 2. DERECHA (EAST) - Siempre activo (aunque poll lo deshabilite si no es obj mode)
        pie.operator("object.link_picked_material", icon="PASTEDOWN")
        
        # 3. ABAJO (SOUTH) - Select NGons (Ghost en Obj)
        draw_ghost(pie, "mesh.select_ngons", "Sel. All NGons", "MOD_BEVEL")

        # 4. ARRIBA (NORTH) - Select Tris (Ghost en Obj)
        draw_ghost(pie, "mesh.select_tris", "Sel. All Tris", "MESH_DATA")

        # --- SLOTS DIAGONALES ---
        
        # 5. NO (Top-Left) -> Prev Tri
        draw_ghost(pie, "mesh.navigate_error", "Prev Tri", "TRIA_LEFT", {'mode':'TRI', 'direction':-1})
        
        # 6. NE (Top-Right) -> Next Tri
        draw_ghost(pie, "mesh.navigate_error", "Next Tri", "TRIA_RIGHT", {'mode':'TRI', 'direction':1})
        
        # 7. SO (Bottom-Left) -> Prev Ngon
        draw_ghost(pie, "mesh.navigate_error", "Prev Ngon", "TRIA_LEFT", {'mode':'NGON', 'direction':-1})
        
        # 8. SE (Bottom-Right) -> Next Ngon
        draw_ghost(pie, "mesh.navigate_error", "Next Ngon", "TRIA_RIGHT", {'mode':'NGON', 'direction':1})

# =========================================================================
# 4. OPERADORES
# =========================================================================

class OBJECT_OT_LinkPickedMaterial(bpy.types.Operator):
    bl_idname = "object.link_picked_material"
    bl_label = "Copiar Material desde Fuente"
    bl_description = "Copia el material del objeto seleccionado en el panel a la selección actual"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        source_obj = context.scene.lucia_source_obj
        selected_objs = context.selected_objects
        if not source_obj:
            self.report({'ERROR'}, "¡Selecciona primero un objeto origen en el panel!"); return {'CANCELLED'}
        if not source_obj.active_material:
            self.report({'WARNING'}, f"El objeto '{source_obj.name}' no tiene ningún material."); return {'CANCELLED'}
        target_mat = source_obj.active_material
        count = 0
        for obj in selected_objs:
            if obj != source_obj and obj.type == 'MESH':
                if not obj.data.materials: obj.data.materials.append(target_mat)
                else: obj.active_material_index = 0; obj.active_material = target_mat
                count += 1
        self.report({'INFO'}, f"Material '{target_mat.name}' copiado a {count} objetos."); return {'FINISHED'}

class MESH_OT_ForceUpdate(bpy.types.Operator):
    bl_idname = "mesh.force_update_stats"; bl_label = "Actualizar Estadísticas"; bl_options = {'REGISTER', 'UNDO'} 
    @classmethod
    def poll(cls, context): return context.active_object and context.active_object.mode == 'EDIT'
    def execute(self, context): update_statistics(context); return {'FINISHED'}

class MESH_OT_NavigateError(bpy.types.Operator):
    bl_idname = "mesh.navigate_error"; bl_label = "Navegar"; bl_options = {'REGISTER', 'UNDO'}
    mode: bpy.props.StringProperty()
    direction: bpy.props.IntProperty()
    
    # MODIFICADO: Poll permite Object Mode para que se dibuje en el Pie (pero disabled)
    @classmethod
    def poll(cls, context): 
        return context.active_object and context.active_object.type == 'MESH'
        
    def execute(self, context):
        # SEGURIDAD: Si no es Edit Mode, cancelamos
        if context.active_object.mode != 'EDIT':
            self.report({'WARNING'}, "Debes estar en Edit Mode")
            return {'CANCELLED'}

        obj = context.active_object; bm = bmesh.from_edit_mesh(obj.data)
        target_faces = []
        for f in bm.faces:
            if self.mode == 'TRI' and len(f.verts) == 3: target_faces.append(f)
            elif self.mode == 'NGON' and len(f.verts) > 4: target_faces.append(f)
        if not target_faces: self.report({'WARNING'}, "No hay elementos."); return {'CANCELLED'}
        current_index = -1
        if bm.faces.active in target_faces: current_index = target_faces.index(bm.faces.active)
        if current_index == -1: new_index = 0
        else: new_index = (current_index + self.direction) % len(target_faces)
        target_face = target_faces[new_index]
        bpy.ops.mesh.select_all(action='DESELECT')
        target_face.select = True; bm.faces.active = target_face
        bmesh.update_edit_mesh(obj.data); bpy.ops.view3d.view_selected(use_all_regions=False)
        update_statistics(context)
        return {'FINISHED'}

class SELECT_NGONS(bpy.types.Operator):
    bl_idname = "mesh.select_ngons"; bl_label = "Sel N-Gons"; bl_options = {'REGISTER', 'UNDO'}
    
    # MODIFICADO: Poll permite Object Mode
    @classmethod
    def poll(cls, c): 
        return c.active_object and c.active_object.type == 'MESH'
        
    def execute(self, c):
        if c.active_object.mode != 'EDIT':
            self.report({'WARNING'}, "Debes estar en Edit Mode")
            return {'CANCELLED'}

        bm = bmesh.from_edit_mesh(c.active_object.data)
        for v in bm.verts: v.select=False
        for e in bm.edges: e.select=False
        for f in bm.faces: f.select = (len(f.verts) > 4)
        bmesh.update_edit_mesh(c.active_object.data); update_statistics(c); return {'FINISHED'}

class SELECT_TRIS(bpy.types.Operator):
    bl_idname = "mesh.select_tris"; bl_label = "Sel Tris"; bl_options = {'REGISTER', 'UNDO'}
    
    # MODIFICADO: Poll permite Object Mode
    @classmethod
    def poll(cls, c): 
        return c.active_object and c.active_object.type == 'MESH'
        
    def execute(self, c):
        if c.active_object.mode != 'EDIT':
            self.report({'WARNING'}, "Debes estar en Edit Mode")
            return {'CANCELLED'}

        bm = bmesh.from_edit_mesh(c.active_object.data)
        for v in bm.verts: v.select=False
        for e in bm.edges: e.select=False
        for f in bm.faces: f.select = (len(f.verts) == 3)
        bmesh.update_edit_mesh(c.active_object.data); update_statistics(c); return {'FINISHED'}

class ORIGIN_TO_WORLD(bpy.types.Operator):
    bl_idname = "object.origin_to_world"; bl_label = "Origen"; bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, c):
        o=c.active_object; curs=c.scene.cursor.location.copy(); c.scene.cursor.location=(0,0,0)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR'); c.scene.cursor.location=curs; return {'FINISHED'}

def mp(o,a): 
    bm=bmesh.from_edit_mesh(o.data); s=[v for v in bm.verts if v.select]
    if s: 
        val=getattr(o.matrix_world@s[0].co,a); inv=o.matrix_world.inverted()
        for v in s: g=o.matrix_world@v.co; setattr(g,a,val); v.co=inv@g
        bmesh.update_edit_mesh(o.data)

class MPX(bpy.types.Operator):
    bl_idname = "mesh.make_planar_x"
    bl_label = "X"
    bl_options = {'REGISTER', 'UNDO'}
    @classmethod
    def poll(cls, c): return c.active_object and c.active_object.mode == 'EDIT'
    def execute(self, c): mp(c.active_object, 'x'); return {'FINISHED'}

class MPY(bpy.types.Operator):
    bl_idname = "mesh.make_planar_y"
    bl_label = "Y"
    bl_options = {'REGISTER', 'UNDO'}
    @classmethod
    def poll(cls, c): return c.active_object and c.active_object.mode == 'EDIT'
    def execute(self, c): mp(c.active_object, 'y'); return {'FINISHED'}

class MPZ(bpy.types.Operator):
    bl_idname = "mesh.make_planar_z"
    bl_label = "Z"
    bl_options = {'REGISTER', 'UNDO'}
    @classmethod
    def poll(cls, c): return c.active_object and c.active_object.mode == 'EDIT'
    def execute(self, c): mp(c.active_object, 'z'); return {'FINISHED'}

def get_p(e):
    p=[];
    for f in e.link_faces:
        if len(f.verts)==4:
            for oe in f.edges:
                if not set(e.verts)&set(oe.verts): p.append(oe)
    return p

class LOOP_G(bpy.types.Operator):
    bl_idname = "mesh.select_parallel_grow"
    bl_label = "Expandir"
    bl_options = {'REGISTER', 'UNDO'}
    @classmethod
    def poll(cls, c): return c.active_object and c.active_object.mode == 'EDIT'
    def execute(self, c):
        bm=bmesh.from_edit_mesh(c.active_object.data); s=[e for e in bm.edges if e.select]; a=set()
        for e in s: 
            for x in get_p(e): a.add(x)
        for x in a: x.select=True
        bmesh.update_edit_mesh(c.active_object.data); bpy.ops.mesh.loop_multi_select(ring=False); return{'FINISHED'}

class LOOP_S(bpy.types.Operator):
    bl_idname = "mesh.select_parallel_shrink"
    bl_label = "Contraer"
    bl_options = {'REGISTER', 'UNDO'}
    @classmethod
    def poll(cls, c): return c.active_object and c.active_object.mode == 'EDIT'
    def execute(self, c):
        bm=bmesh.from_edit_mesh(c.active_object.data); s=[e for e in bm.edges if e.select]; r=set()
        for e in s:
            if sum(1 for x in get_p(e) if x.select)<2: r.add(e)
        for x in r: x.select=False
        bmesh.update_edit_mesh(c.active_object.data); return{'FINISHED'}

# =========================================================================
# REGISTRO
# =========================================================================

classes = [
    ORIGIN_TO_WORLD, MPX, MPY, MPZ, LOOP_G, LOOP_S,
    OBJECT_OT_LinkPickedMaterial, SELECT_NGONS, SELECT_TRIS,
    MESH_OT_NavigateError, MESH_OT_ForceUpdate,
    LUCIA_PT_MainPanel, LUCIA_MT_PieMenu
]

addon_keymaps = []

def register():
    init_props()
    for c in classes: bpy.utils.register_class(c)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS', shift=True)
        kmi.properties.name = "LUCIA_MT_pie_menu"
        addon_keymaps.append((km, kmi))

def unregister():
    for c in reversed(classes): bpy.utils.unregister_class(c)
    for km, kmi in addon_keymaps: km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    del bpy.types.Scene.lucia_tris_total; del bpy.types.Scene.lucia_tris_idx
    del bpy.types.Scene.lucia_ngons_total; del bpy.types.Scene.lucia_ngons_idx
    del bpy.types.Scene.lucia_source_obj

if __name__ == "__main__":
    register()