"""
Creates an enclosure
"""
from transilluminator import Transilluminator
from py2scad import *

#style = 'small'
#style = 'asymmetric' 
style = 'large'

# Inside dimensions
x,y,z = 7.25*INCH2MM, 4.25*INCH2MM, 2.0*INCH2MM       

dy_for_imager = 0.539*INCH2MM   # for Gilberts design


if style == 'small':
    filter_y_loc = 0
elif style == 'asymmetric':
    y += dy_for_imager
    filter_y_loc = 0.5*dy_for_imager
elif style == 'large':
    y += 2*dy_for_imager
    filter_y_loc = 0
else:
    raise ValueError, 'unknown style {0}'.format(style)

 
fn = 70

params = {
        'inner_dimensions'              : (x,y,z), 
        'wall_thickness'                : 3.0, 
        'lid_radius'                    : 0.25*INCH2MM,  
        'top_x_overhang'                : 0.15*INCH2MM,
        'top_y_overhang'                : 0.15*INCH2MM,
        'bottom_x_overhang'             : 0.15*INCH2MM,
        'bottom_y_overhang'             : 0.15*INCH2MM, 
        'lid2front_tabs'                : (0.2,0.5,0.8),
        'lid2side_tabs'                 : (0.25, 0.75),
        'side2side_tabs'                : (0.5,),
        'lid2front_tab_width'           : 0.75*INCH2MM,
        'lid2side_tab_width'            : 0.75*INCH2MM, 
        'side2side_tab_width'           : 0.5*INCH2MM,
        'tab_depth_adjust'              : -0.6,
        'standoff_diameter'             : 0.25*INCH2MM,
        'standoff_offset'               : 0.05*INCH2MM,
        'standoff_hole_diameter'        : 0.116*INCH2MM, 
        'filter_holder_thickness'       : 6.0,
        'filter_location'               : (1.25*INCH2MM - 0.325*INCH2MM,filter_y_loc),  
        'cover_thickness'               : 3.0,
        'mask_thickness'                : 1.5,
        'hole_list'                     : [],
        'window_size'                   : 'large',
        'small_window_size'             : [65, 65],
        'small_filter_size'             : [70,70],
        'large_window_size'             : [75, 75],
        'large_filter_size'             : [82.6, 82.6],
        'lamp_mount_spacing'            : 142.0,
        'lamp_mount_offset'             : 0.5*INCH2MM,
        'lamp_mount_diam'               : 0.136*INCH2MM,   
        'power_jack_location'           : (-2.5*INCH2MM, 0),
        'power_jack_panel'              : 'front',
        'power_jack_hole_size'          : (26.9, 27.6),
        'power_jack_mount_hole_size'    : 0.104*INCH2MM,
        'power_jack_mount_hole_offset'  : 36.8/2.0,
        'power_jack_extender_thickness' : 6.0,
        'power_extender_hole_size'      : 0.136*INCH2MM,
        'include_vent_holes'            : False,

        }


enclosure = Transilluminator(params)
enclosure.make()

part_assembly = enclosure.get_assembly(
    explode=(0,0,15),
    show_top=True,
    show_left=False,
    show_right=False,
    show_filter_holder=True,
    show_bottom=False,
    show_cover_plate=False
    )

part_projection = enclosure.get_projection()
part_cover_plate = enclosure.get_cover_plate_projection()
part_filter_holder = enclosure.get_filter_holder_projection()
part_mask_plate = enclosure.get_mask_plate_projection()

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

prog_mask_plate = SCAD_Prog()
prog_mask_plate.fn = fn
prog_mask_plate.add(part_mask_plate)
prog_mask_plate.write('mask_plate_projection.scad')

prog_filter_holder = SCAD_Prog()
prog_filter_holder.fn = fn
prog_filter_holder.add(part_filter_holder)
prog_filter_holder.write('filter_holder_projection.scad')

prog_extender = SCAD_Prog()
prog_extender.fn = fn
prog_extender.add(Projection(enclosure.power_extender))
prog_extender.write('power_extender.scad')




