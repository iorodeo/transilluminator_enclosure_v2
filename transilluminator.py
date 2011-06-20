import scipy
from py2scad import *

class Transilluminator(Basic_Enclosure):

    def __init__(self,params):
        self.params = params

    def make(self):
        self.__make_holder_and_cover()
        super(Transilluminator,self).make()
        self.__make_custom_holes()

    def get_filter_holder_projection(self):
        return Projection(self.filter_holder)

    def get_cover_plate_projection(self):
        return Projection(self.cover_plate)

    def  __make_custom_holes(self): 
        hole_list = []

        filter_location = self.params['filter_location']
        holder_thickness = self.params['filter_holder_thickness']
        inner_x, inner_y, inner_z = self.params['inner_dimensions']

        # Add square hole to top
        hole = {
                'panel' : 'top',
                'type'  : 'square',
                'location': filter_location, 
                'size': (65,65),
                }
        hole_list.append(hole)

        # Add square hole to filter holder
        hole = { 
                'panel' : 'filter_holder',
                'type' :  'square',
                'location' : filter_location,
                'size':  (70,70),
                }
        hole_list.append(hole)

        # Add hole for power connector 
        hole = {
                'panel': 'left',
                'type':  'square',
                'location': (0,0),
                'size':  (26.9, 27.6)
                }
        hole_list.append(hole)

        # Add mounting holes for power connector
        # 5-40 threaded.
        for i in (-1,1):
            hole  = {
                    'panel' : 'left',
                    'type':  'round', 
                    'location' : (i*36.8/2.0, 0),
                    'size'  : 0.104*INCH2MM 
                    }
            hole_list.append(hole)

        # Make vent holes for bottom
        gap = 4*0.25*INCH2MM
        vent_hole_diam = 0.25*INCH2MM
        N = int(inner_x/(4*vent_hole_diam))
        x_pos = scipy.linspace(-inner_x/2+gap, inner_x/2-gap,N)
        y_pos = [-inner_y/4.0, inner_y/4.0]
        for x in x_pos:
            for y in y_pos:
                hole = {
                        'panel'    : 'bottom', 
                        'type'     :  'round',
                        'location' : (x,y),
                        'size'     : vent_hole_diam,
                        }
                hole_list.append(hole)

        # Make mount holes for UV lamp
        # 8-32
        lamp_mount_spacing = 142.0
        lamp_mount_offset = 0.5*INCH2MM
        lamp_mount_diam =0.136*INCH2MM   
        for x in (-0.5*lamp_mount_spacing, 0.5*lamp_mount_spacing):
            hole = {
                    'panel'     : 'bottom', 
                    'type'      : 'round',
                    'location'  : (x-lamp_mount_offset,0),
                    'size'      : lamp_mount_diam, 
                    }
            hole_list.append(hole)

        self.add_holes(hole_list, cut_depth=2*holder_thickness)
        

    def __make_holder_and_cover(self):
        """
        Create copy of top for filter holder
        """
        inner_x, inner_y, inner_z = self.params['inner_dimensions']
        wall_thickness = self.params['wall_thickness']
        holder_thickness = self.params['filter_holder_thickness']
        top_x_overhang = self.params['top_x_overhang']
        top_y_overhang = self.params['top_y_overhang']
        lid_radius = self.params['lid_radius']

        # Get dimensions of top panel
        top_x = inner_x + 2.0*(wall_thickness + top_x_overhang)
        top_y = inner_y + 2.0*(wall_thickness + top_y_overhang)
        top_z = holder_thickness
        self.top_x, self.top_y = top_x, top_y
        top_size = top_x, top_y, top_z
            
        # Create filter holder 
        holder_params = {'size' : top_size, 'radius' : lid_radius, 'slots' : []}
        holder_maker = Plate_W_Slots(holder_params)
        self.filter_holder = holder_maker.make()

        # Create cover plate
        top_size  = top_x, top_y, self.params['cover_thickness']
        cover_params = {'size' : top_size, 'radius' : lid_radius, 'slots' : []}
        cover_maker = Plate_W_Slots(cover_params)
        self.cover_plate = cover_maker.make()

        # Add holes for standoffs
        standoff_diameter = self.params['standoff_diameter']
        standoff_offset = self.params['standoff_offset']
        standoff_hole_diameter = self.params['standoff_hole_diameter']

        hole_list = []
        self.standoff_xy_pos = []
        self.standoff_list = []
        for i in (-1,1):
            for j in (-1,1):
                # Create holes for standoffs
                x = i*(0.5*inner_x - 0.5*standoff_diameter - standoff_offset)
                y = j*(0.5*inner_y - 0.5*standoff_diameter - standoff_offset)
                self.standoff_xy_pos.append((x,y))
                hole = { 
                        'panel'     : 'filter_holder', 
                        'type'      : 'round',
                        'location'  : (x,y), 
                        'size'      : standoff_hole_diameter,
                        }
                hole_list.append(hole)
                hole = { 
                        'panel'     : 'cover_plate', 
                        'type'      : 'round',
                        'location'  : (x,y), 
                        'size'      : standoff_hole_diameter,
                        }
                hole_list.append(hole)

        self.add_holes(hole_list,cut_depth=2*holder_thickness)


    def get_assembly(self, **kwargs):
        assembly_options = {
                'explode'            : (0,0,0),
                'show_filter_holder' : True,
                'show_cover_plate'   : True,
                }
        assembly_options.update(kwargs)
        explode = assembly_options['explode']
        explode_x, explode_y, explode_z = explode

        parts_list = super(Transilluminator,self).get_assembly(**kwargs)

        inner_x, inner_y, inner_z = self.params['inner_dimensions']
        wall_thickness = self.params['wall_thickness']
        holder_thickness = self.params['filter_holder_thickness']
        cover_thickness = self.params['cover_thickness']
        
        # Translate top and bottom into assembled positions
        top_z_shift = 0.5*inner_z + 0.5*wall_thickness + explode_z
        filter_z_shift = top_z_shift + 0.5*holder_thickness + 0.5*wall_thickness + explode_z
        filter_holder = Translate(self.filter_holder, v=(0.0,0.0,filter_z_shift))
        filter_holder = Color(filter_holder,rgba=(1,0,0,1))

        # Translate cover plate into  positon
        cover_z_shift = filter_z_shift + 0.5*cover_thickness + 0.5*wall_thickness 
        cover_plate = Translate(self.cover_plate, v=(0,0,cover_z_shift+explode_z))
        cover_plate = Color(cover_plate,rgba=(0,0,1,0.5))

        if assembly_options['show_filter_holder'] == True:
            parts_list.append(filter_holder)
        if assembly_options['show_cover_plate'] == True:
            parts_list.append(cover_plate)

        return parts_list

