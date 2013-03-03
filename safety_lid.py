from py2scad import *

class SafetyLid(object):

    def __init__(self,params):
        self.params = params
        self.make_top()
        self.make_front_and_back()
        self.make_left_and_right()
        self.make_hinge_mount()

    def make_top(self):
        size  = (self.params['x_dim'], self.params['y_dim'], self.params['thickness'])
        self.top = Cube(size=size)

    def make_front_and_back(self):
        size = (self.params['x_dim'], self.params['z_dim'], self.params['thickness'])
        side = Cube(size=size)
        self.back_side = side
        self.front_side = side

    def make_left_and_right(self):
        x = self.params['y_dim'] - 2*self.params['thickness']
        y = self.params['z_dim']
        z = self.params['thickness']
        size = x,y,z
        side = Cube(size=size)
        self.left_side = side
        self.right_side = side

    def make_hinge_mount(self):
        h = 2.0*self.params['thickness']
        r = 0.5*self.params['hinge_hole_diam']
        hole_cyl = Cylinder(h=h,r1=r,r2=r)
        x_shift = 0.5*self.params['hinge_hole_sep']
        hole0 = Translate(hole_cyl,v=(x_shift, 0, 0))
        hole1 = Translate(hole_cyl,v=(-x_shift,0,0))
        hole_template = Union([hole0, hole1])
        x_shift = 0.5*self.params['hinge_spacing']
        hole_template0 = Translate(hole_template,v=(x_shift,0,0))
        hole_template1 = Translate(hole_template,v=(-x_shift,0,0))
        y_shift = -0.5*self.params['z_dim'] + self.params['hinge_hole_z']
        hole_template0 = Translate(hole_template0,v=(0,y_shift,0))
        hole_template1 = Translate(hole_template1,v=(0,y_shift,0))
        self.left_side = Difference([self.left_side, hole_template0, hole_template1])

    def get_layout(self):
        parts_list = []

        y_shift = 0.5*self.params['y_dim'] + 0.5*self.params['z_dim'] + 2*self.params['thickness']
        front_side = Translate(self.front_side, v=(0,y_shift,0))
        parts_list.append(front_side)

        back_side = Translate(self.back_side,v=(0,-y_shift,0))
        parts_list.append(back_side)

        left_side = Rotate(self.left_side,a=90,v=(0,0,1))
        x_shift = 0.5*self.params['x_dim'] + 0.5*self.params['z_dim'] + 2*self.params['thickness']
        left_side = Translate(left_side,v=(x_shift, 0, 0 ))
        parts_list.append(left_side)

        right_side = Rotate(self.right_side,a=90,v=(0,0,1))
        right_side = Translate(right_side,v=(-x_shift, 0, 0))
        parts_list.append(right_side)

        parts_list.append(self.top)
        parts_list = [Projection(part,cut=False) for part in parts_list]

        return parts_list


    def get_assembly(self):
        parts_list = []
        top = self.top
        parts_list.append(top)

        z_shift = -0.5*self.params['z_dim'] - 0.5*self.params['thickness']
        # Add form and back sides
        back_side = self.back_side
        back_side = Rotate(back_side, a=90, v=(-1,0,0))
        back_side = Rotate(back_side, a=180, v=(0,0,1))
        y_shift = 0.5*self.params['y_dim'] - 0.5*self.params['thickness']
        back_side = Translate(back_side, v=(0, y_shift, z_shift))
        back_side = Color(back_side, rgba=(1,0,0,1))
        parts_list.append(back_side)

        front_side = self.front_side
        front_side = Rotate(front_side, a=90, v=(-1,0,0))
        y_shift = -0.5*self.params['y_dim'] + 0.5*self.params['thickness']
        front_side = Translate(front_side, v=(0, y_shift, z_shift))
        front_side = Color(front_side, rgba=(1,0,0,1))
        parts_list.append(front_side)

        ## Add left and right sides
        left_side = self.left_side
        left_side = Rotate(left_side,a=90,v=(1,0,0))
        left_side = Rotate(left_side,a=90,v=(0,0,-1))
        x_shift = -0.5*self.params['x_dim'] + 0.5*self.params['thickness']
        left_side = Translate(left_side,v=(x_shift, 0, z_shift))
        left_side = Color(left_side,rgba=(0,0,1,1))
        parts_list.append(left_side)

        right_side = self.right_side
        right_side = Rotate(right_side,a=90,v=(1,0,0))
        right_side = Rotate(right_side,a=90,v=(0,0,1))
        x_shift = +0.5*self.params['x_dim'] - 0.5*self.params['thickness']
        right_side = Translate(right_side,v=(x_shift, 0, z_shift))
        right_side = Color(right_side,rgba=(0,0,1,1))
        parts_list.append(right_side)

        return parts_list



# -----------------------------------------------------------------------------
if __name__ == '__main__':
    params = {
            'x_dim'           : 4.0*INCH2MM, 
            'y_dim'           : 4.0*INCH2MM,  
            'z_dim'           : 0.84*INCH2MM,
            'thickness'       : 3,
            'hinge_hole_sep'  : 14.8,
            'hinge_hole_diam' : 0.14*INCH2MM,
            'hinge_spacing'   : 2.0*INCH2MM,
            'hinge_hole_z'    : 10,
            }

    lid = SafetyLid(params=params)

    prog_assem = SCAD_Prog()
    prog_assem.fn = 50
    prog_assem.add(lid.get_assembly())
    prog_assem.write('safety_lid_assembly.scad')

    #prog_layout = SCAD_Prog()
    #prog_layout.fn = 50
    #prog_layout.add(lid.get_layout())
    #prog_layout.write('safety_lid_layout.scad')
