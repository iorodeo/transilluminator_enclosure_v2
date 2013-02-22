"""
Creates an enclosure
"""
from transilluminator import Transilluminator
from py2scad import *

INCH2MM = 25.4

# Inside dimensions
x,y,z = 7.25*INCH2MM, 4.25*INCH2MM, 2.0*INCH2MM       # Smaller box for Gilberts design
# x,y,z = 8.5*INCH2MM, 4.5*INCH2MM, 2.5*INCH2MM       # Larger box
 
fn = 50

params = {
        'inner_dimensions'        : (x,y,z), 
        'wall_thickness'          : 3.0, 
        'lid_radius'              : 0.25*INCH2MM,  
        'top_x_overhang'          : 0.15*INCH2MM,
        'top_y_overhang'          : 0.15*INCH2MM,
        'bottom_x_overhang'       : 0.15*INCH2MM,
        'bottom_y_overhang'       : 0.15*INCH2MM, 
        'lid2front_tabs'          : (0.2,0.5,0.8),
        'lid2side_tabs'           : (0.25, 0.75),
        'side2side_tabs'          : (0.5,),
        'lid2front_tab_width'     : 0.75*INCH2MM,
        'lid2side_tab_width'      : 0.75*INCH2MM, 
        'side2side_tab_width'     : 0.5*INCH2MM,
        'tab_depth_adjust'        : -0.6,
        'standoff_diameter'       : 0.25*INCH2MM,
        'standoff_offset'         : 0.05*INCH2MM,
        'standoff_hole_diameter'  : 0.116*INCH2MM, 
        'filter_holder_thickness' : 6.0,
        'filter_location'         : (1.25*INCH2MM - 0.325*INCH2MM,0),  
        'cover_thickness'         : 3.0,
        'hole_list'               : [],
        'window_size'             : 'small',
        'small_window_size'       : [65, 65],
        'small_filter_size'       : [70,70],
        'large_window_size'       : [115, 100],
        'large_filter_size'       : [120, 105],
        'lamp_mount_spacing'      : 142.0,
        'lamp_mount_offset'       : 0.5*INCH2MM,
        'lamp_mount_diam'         : 0.136*INCH2MM,   
        'power_jack_location'     : (-2.5*INCH2MM, 0),
        'power_jack_panel'        : 'front',
        'include_vent_holes'      : False,

        }


enclosure = Transilluminator(params)
enclosure.make()

part_assembly = enclosure.get_assembly(
    explode=(0,0,5),
    show_top=True,
    show_left=True,
    show_right=True,
    show_filter_holder=True,
    show_bottom=True,
    show_cover_plate=False

    )
part_projection = enclosure.get_projection()
part_cover_plate = enclosure.get_cover_plate_projection()
part_filter_holder = enclosure.get_filter_holder_projection()

prog_assembly = SCAD_Prog()
prog_assembly.fn = fn 
prog_assembly.add(part_assembly)
prog_assembly.write('enclosure_assembly.scad')

prog_projection = SCAD_Prog()
prog_projection.fn = fn 
prog_projection.add(part_projection)
prog_projection.write('enclosure_projection.scad')

prog_cover_plate = SCAD_Prog()
prog_cover_plate.fn = fn
prog_cover_plate.add(part_cover_plate)
prog_cover_plate.write('cover_plate_projection.scad')

prog_filter_holder = SCAD_Prog()
prog_filter_holder.fn = fn
prog_filter_holder.add(part_filter_holder)
prog_filter_holder.write('filter_holder_projection.scad')




