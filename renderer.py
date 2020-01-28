
import tkinter,math

class Window():
    def __init__(self,dimensions_xy=(1280,720),position_xy=(0,0)):
        self.dimensions_xy = (int(dimensions_xy[0]),int(dimensions_xy[1]))
        position_xy = (int(position_xy[0]),int(position_xy[1]))
        # instantiates root (the window)
        self.root = tkinter.Tk()
        self.root.geometry(str(self.dimensions_xy[0])+"x"+str(self.dimensions_xy[1])+"+"+str(position_xy[0])+"+"+str(position_xy[1]))
        # instantiates the canvas (the drawable area)
        self.canvas = tkinter.Canvas(self.root,width=self.dimensions_xy[0],height=self.dimensions_xy[1],bg="white")
        self.canvas.pack()
        
    def set_colour_rectangle(self,rectangle_id,fill_colour,outline_colour=None):
        if outline_colour==None:
            outline_colour=fill_colour
        attributes = {"fill":fill_colour,
                   "outline":outline_colour}
        self.canvas.itemconfigure(rectangle_id, attributes)
        
    def move_rectangle(self,rectangle_id,diff_xy):
        (diff_x, diff_y) = diff_xy
        self.canvas.move(rectangle_id,diff_x,diff_y)
    
    def create_rectangle(self,position_xy,dimensions_xy,fill_colour,outline_colour=None):
        attributes = {}
        (x1,y1)=position_xy
        (x2,y2)=add(position_xy,dimensions_xy)
        rectangle_id = self.canvas.create_rectangle(x1,y1,x2,y2,attributes)
        self.set_colour_rectangle(rectangle_id,fill_colour,outline_colour)
        return rectangle_id
        
    def update(self):
        self.root.update()
        
    def close(self):
        self.root.destroy()
        
    def get_pixel_xy(self, portion_of_xy):
        return (int(portion_of_xy[0]*self.dimensions_xy[0]),int(portion_of_xy[1]*self.dimensions_xy[1]))
        
class Bitmap():
    def __init__(self,window,portion_dimensions_xy=(1,1),resolution_xy=(128,72),portion_position_xy=(0,0),initial_colour="white"):
        self.window = window
        dimensions_xy = self.window.get_pixel_xy(portion_dimensions_xy)
        resolution_xy = (int(resolution_xy[0]),int(resolution_xy[1]))
        self.portion_position_xy = portion_position_xy
        # instantiates the pixels and ensures that subpixels (if present) are accounted for
        self.pixels = []
        avg_pixel_dimensions_xy = (dimensions_xy[0]/resolution_xy[0],dimensions_xy[1]/resolution_xy[1])
        sum_pixel_dimensions_xy = (0,0)
        current_pixel_dimensions_xy = (0,0)
        for row in range(0,resolution_xy[1]):
            pixel_row = []
            if sum_pixel_dimensions_xy[1]<=row*avg_pixel_dimensions_xy[1]:
                current_pixel_dimensions_xy = (current_pixel_dimensions_xy[0],math.ceil(avg_pixel_dimensions_xy[1]))
            else:
                current_pixel_dimensions_xy = (current_pixel_dimensions_xy[0],math.floor(avg_pixel_dimensions_xy[1]))
            for col in range(0,resolution_xy[0]):
                if sum_pixel_dimensions_xy[0]<=col*avg_pixel_dimensions_xy[0]:
                    current_pixel_dimensions_xy = (math.ceil(avg_pixel_dimensions_xy[0]),current_pixel_dimensions_xy[1])
                else:
                    current_pixel_dimensions_xy = (math.floor(avg_pixel_dimensions_xy[0]),current_pixel_dimensions_xy[1])
                pixel_row.append(self.Pixel(self,(sum_pixel_dimensions_xy),(current_pixel_dimensions_xy),initial_colour))
                sum_pixel_dimensions_xy = (sum_pixel_dimensions_xy[0]+current_pixel_dimensions_xy[0],sum_pixel_dimensions_xy[1])
            sum_pixel_dimensions_xy = (0,sum_pixel_dimensions_xy[1]+current_pixel_dimensions_xy[1])
            self.pixels.append(pixel_row)
                
    def get_pixels(self):
        return self.pixels
    
    def create_pixel(self,position_xy,dimensions_xy,colour):
        pixel_position_xy = self.window.get_pixel_xy(self.portion_position_xy)
        absolute_position_xy = add(position_xy,pixel_position_xy)
        return self.window.create_rectangle(absolute_position_xy,dimensions_xy,colour)
    
    def recolour_pixel(self,rectangle_id,colour):
        self.window.set_colour_rectangle(rectangle_id,colour)
        
    def relocate_pixel(self,rectangle_id,diff_xy):
        self.window.move_rectangle(rectangle_id,diff_xy)
    
    def move_by(self,portion_diff_xy):
        old_xy = self.window.get_pixel_xy(self.portion_position_xy)
        self.portion_position_xy = add(self.portion_position_xy,portion_diff_xy)
        new_xy = self.window.get_pixel_xy(self.portion_position_xy)
        pixel_diff_xy = add(new_xy,negative(old_xy))
        self.move_by_pixels(pixel_diff_xy)
        
    def move_to(self,new_portion_position_xy):
        old_xy = self.window.get_pixel_xy(self.portion_position_xy)
        self.portion_position_xy = new_portion_position_xy
        new_xy = self.window.get_pixel_xy(self.portion_position_xy)
        pixel_diff_xy = add(new_xy,negative(old_xy))
        self.move_by_pixels(pixel_diff_xy)
    
    def move_by_pixels(self,pixel_diff_xy):
        for row_of_pixels in self.pixels:
            for pixel in row_of_pixels:
                pixel.move_by(pixel_diff_xy)
    
        

    class Pixel():
        def __init__(self,bitmap,position_xy,dimensions_xy,colour="white"):
            self.bitmap = bitmap
            self.position_xy=position_xy
            self.dimensions_xy=dimensions_xy
            self.colour = colour
            self.rectangle_id = self.bitmap.create_pixel(self.position_xy,self.dimensions_xy,self.colour)
            
        def set_colour(self,colour):
            self.colour = colour
            self.bitmap.recolour_pixel(self.rectangle_id,self.colour)
        
        def move_by(self,diff_xy):
            self.position_xy=add(self.position_xy,diff_xy)
            self.bitmap.relocate_pixel(self.rectangle_id,diff_xy)

        
def add(tuple_a,tuple_b):
    resulting_tuple = []
    for i in range(0,len(tuple_a)):
        resulting_tuple.append(tuple_a[i]+tuple_b[i])
    return resulting_tuple

def negative(tuple_a):
    resulting_tuple = []
    for i in range(0,len(tuple_a)):
        resulting_tuple.append(-1*tuple_a[i])
    return resulting_tuple
