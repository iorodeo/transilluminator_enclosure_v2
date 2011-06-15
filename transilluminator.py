from py2scad import *

class Transilluminator(Basic_Enclosure):

    def __init__(self,params):
        self.params = params

    def make(self):
        self.__make_filter_holder()
        super(Transilluminator,self).make()
        self.__make_filter_holes()

    def  __make_filter_holes(self): 
        hole_list = []

        filter_location = self.params['filter_location']
        holder_thickness = self.params['filter_holder_thickness']
        # Add square hole to top
        hole = {
                'panel' : 'top',
                'type'  : 'square',
                'location': filter_location, 
                'size': (65,65),
                }
        hole_list.append(hole)
        hole = { 
                'panel' : 'filter_holder',
                'type' :  'square',
                'location' : filter_location,
                'size':  (70,70),
                }
        hole_list.append(hole)
        self.add_holes(hole_list, cut_depth=2*holder_thickness)


    def __make_filter_holder(self):
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

        self.add_holes(hole_list,cut_depth=2*holder_thickness)

    def get_assembly(self, **kwargs):
        explode = kwargs['explode']

        parts_list = super(Transilluminator,self).get_assembly(**kwargs)

        # Translate filter holder into position
        inner_x, inner_y, inner_z = self.params['inner_dimensions']
        wall_thickness = self.params['wall_thickness']
        holder_thickness = self.params['filter_holder_thickness']
        
        explode_x, explode_y, explode_z = explode

        # Translate top and bottom into assembled positions
        top_z_shift = 0.5*inner_z + 0.5*wall_thickness + explode_z
        filter_z_shift = top_z_shift + 0.5*holder_thickness + 0.5*wall_thickness + explode_z
        filter_holder = Translate(self.filter_holder, v=(0.0,0.0,filter_z_shift))
        filter_holder = Color(filter_holder,rgba=(1,0,0,1))
        parts_list.append(filter_holder)

        return parts_list

