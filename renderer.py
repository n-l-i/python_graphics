
import tkinter
import math

# constants
class OBJ_TYPE(object):
    __slots__ = ()
    RECTANGLE = "rectangle"
    OVAL = "oval"
    TEXT = "text"
OBJ_TYPE = OBJ_TYPE()
    

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
        
    def set_element_attributes(self,element,attributes):
        if isinstance(element,int):
            element_id = element
        else:
            element_id = element.get_id()
        self.canvas.itemconfigure(element_id,attributes)
        
    def move_element(self,element,diff_xy):
        if isinstance(element,Bitmap):
            pixels = element.get_pixels()
            for row_of_pixels in pixels:
                for pixel in row_of_pixels:
                    self.move_element(pixel,diff_xy)
            return
        (diff_x,diff_y) = diff_xy
        element_id = element.get_id()
        self.canvas.move(element_id,diff_x,diff_y)
    
    def create_element(self,obj_type,position_xy,dimensions_xy):
        attributes = {}
        (x1,y1)=position_xy
        (x2,y2)=add(position_xy,dimensions_xy)
        if obj_type == OBJ_TYPE.RECTANGLE:
            element_id = self.canvas.create_rectangle(x1,y1,x2,y2,attributes)
        elif obj_type == OBJ_TYPE.OVAL:
            element_id = self.canvas.create_oval(x1,y1,x2,y2,attributes)
        elif obj_type == OBJ_TYPE.TEXT:
            element_id = self.canvas.create_text(x1,y1,attributes)
        else:
            raise Exception("Tried to create element of undefined type: "+str(obj_type))
        return element_id
        
    def update(self):
        self.root.update()
        
    def close(self):
        self.root.destroy()
        
    def portion_to_pixel_xy(self,portion_of_xy):
        return (int(portion_of_xy[0]*self.dimensions_xy[0]),int(portion_of_xy[1]*self.dimensions_xy[1]))

    def remove(self,element):
        if isinstance(element,Rectangle):
            self.remove(element.element)
            return
        if isinstance(element,Oval):
            self.remove(element.element)
            return
        if isinstance(element,Text):
            self.remove(element.element)
            return
        if isinstance(element,Bitmap):
            pixels = element.get_pixels()
            for row_of_pixels in pixels:
                for pixel in row_of_pixels:
                    self.remove(pixel)
            return
        element_id = element.get_id()
        self.canvas.delete(element_id)
        
        
class Element():
    def __init__(self,obj_type,window,portion_position_xy=(0,0),portion_dimensions_xy=(1,1)):
        self.window = window
        self.portion_dimensions_xy = self.window.portion_to_pixel_xy(portion_dimensions_xy)
        self.portion_position_xy = portion_position_xy
        self.attributes = {}
        self.obj_type = obj_type
        self.element_id = self.create_element(obj_type,portion_position_xy,portion_dimensions_xy)
        
    def get_id(self):
        return self.element_id
        
    def create_element(self,obj_type,position_xy,dimensions_xy):
        absolute_position_xy = self.window.portion_to_pixel_xy(position_xy)
        absolute_dimensions_xy = self.window.portion_to_pixel_xy(dimensions_xy)
        return self.window.create_element(obj_type,absolute_position_xy,absolute_dimensions_xy)
    
    def set_colour(self,colour):
        self.attributes["fill"] = colour
        if self.obj_type != OBJ_TYPE.TEXT:
            self.attributes["outline"] = colour
        self.window.set_element_attributes(self.element_id,self.attributes)
    
    def set_text(self,text):
        self.attributes["text"] = text
        self.window.set_element_attributes(self.element_id,self.attributes)
    
    def set_font(self,font):
        self.attributes["font"] = font
        self.window.set_element_attributes(self.element_id,self.attributes)

    def move_by(self,portion_diff_xy):
        old_xy = self.window.portion_to_pixel_xy(self.portion_position_xy)
        self.portion_position_xy = add(self.portion_position_xy,portion_diff_xy)
        new_xy = self.window.portion_to_pixel_xy(self.portion_position_xy)
        pixel_diff_xy = add(new_xy,negative(old_xy))
        self.window.move_element(self,pixel_diff_xy)
        
    def move_to(self,new_portion_position_xy):
        old_xy = self.window.portion_to_pixel_xy(self.portion_position_xy)
        self.portion_position_xy = new_portion_position_xy
        new_xy = self.window.portion_to_pixel_xy(self.portion_position_xy)
        pixel_diff_xy = add(new_xy,negative(old_xy))
        self.window.move_element(self,pixel_diff_xy)


class Bitmap():
    def __init__(self,window,portion_dimensions_xy=(1,1),resolution_xy=(128,72),portion_position_xy=(0,0)):
        self.window = window
        dimensions_xy = self.window.portion_to_pixel_xy(portion_dimensions_xy)
        resolution_xy = (int(resolution_xy[0]),int(resolution_xy[1]))
        self.portion_position_xy = portion_position_xy
        self.init_pixels(dimensions_xy,resolution_xy)
        
    def init_pixels(self,dimensions_xy,resolution_xy):
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
                pixel_row.append(self.Pixel(self,(sum_pixel_dimensions_xy),(current_pixel_dimensions_xy),"white"))
                sum_pixel_dimensions_xy = (sum_pixel_dimensions_xy[0]+current_pixel_dimensions_xy[0],sum_pixel_dimensions_xy[1])
            sum_pixel_dimensions_xy = (0,sum_pixel_dimensions_xy[1]+current_pixel_dimensions_xy[1])
            self.pixels.append(pixel_row)
                
    def get_pixels(self):
        return self.pixels
    
    def create_pixel(self,position_xy,dimensions_xy,colour):
        pixel_position_xy = self.window.portion_to_pixel_xy(self.portion_position_xy)
        absolute_position_xy = add(position_xy,pixel_position_xy)
        return self.window.create_element(OBJ_TYPE.RECTANGLE,absolute_position_xy,dimensions_xy)
    
    def recolour_pixel(self,colour,pixel):
        attributes = pixel.get_attributes()
        attributes["fill"] = colour
        attributes["outline"] = colour
        self.window.set_element_attributes(pixel,attributes)
            
    def fill_colour(self,colour):
        for row_of_pixels in self.get_pixels():
            for pixel in row_of_pixels:
                self.recolour_pixel(colour,pixel)

    def move_by(self,portion_diff_xy):
        old_xy = self.window.portion_to_pixel_xy(self.portion_position_xy)
        self.portion_position_xy = add(self.portion_position_xy,portion_diff_xy)
        new_xy = self.window.portion_to_pixel_xy(self.portion_position_xy)
        pixel_diff_xy = add(new_xy,negative(old_xy))
        self.window.move_element(self,pixel_diff_xy)
        
    def move_to(self,new_portion_position_xy):
        old_xy = self.window.portion_to_pixel_xy(self.portion_position_xy)
        self.portion_position_xy = new_portion_position_xy
        new_xy = self.window.portion_to_pixel_xy(self.portion_position_xy)
        pixel_diff_xy = add(new_xy,negative(old_xy))
        self.window.move_element(self,pixel_diff_xy)
    
        
    class Pixel():
        def __init__(self,bitmap,position_xy,dimensions_xy,colour="black"):
            self.bitmap = bitmap
            self.position_xy=position_xy
            self.dimensions_xy=dimensions_xy
            self.colour = colour
            self.attributes = {}
            self.attributes["fill"] = colour
            self.attributes["outline"] = colour
            self.element_id = self.bitmap.create_pixel(self.position_xy,self.dimensions_xy,self.colour)
        
        def get_id(self):
            return self.element_id
        
        def get_attributes(self):
            return self.attributes
            
        def set_colour(self,colour):
            self.colour = colour
            self.attributes["fill"] = colour
            self.attributes["outline"] = colour
            self.bitmap.recolour_pixel(self.colour,self)
            
        
class Rectangle():
    def __init__(self,window,position_xy=(0,0),dimensions_xy=(1,1),colour="black"):
        self.element = Element(OBJ_TYPE.RECTANGLE,window,position_xy,dimensions_xy)
        self.set_colour(colour)
    
    def set_colour(self,colour):
        self.element.set_colour(colour)
    
    def move_by(self,portion_diff_xy):
        self.element.move_by(portion_diff_xy)
        
    def move_to(self,new_portion_position_xy):
        self.element.move_to(new_portion_position_xy)
        
        
class Oval():
    def __init__(self,window,position_xy=(0,0),dimensions_xy=(1,1),colour="black"):
        self.element = Element(OBJ_TYPE.OVAL,window,position_xy,dimensions_xy)
        self.set_colour(colour)
    
    def set_colour(self,colour):
        self.element.set_colour(colour)
    
    def move_by(self,portion_diff_xy):
        self.element.move_by(portion_diff_xy)
        
    def move_to(self,new_portion_position_xy):
        self.element.move_to(new_portion_position_xy)
        
class Text():
    def __init__(self,window,position_xy=(0,0),text="Default text.",typeface="arial",size=12,style="normal",colour="black"):
        self.element = Element(OBJ_TYPE.TEXT,window,position_xy,(1,1))
        self.text = text
        self.element.set_text(text)
        self.font = (typeface,size,style)
        self.element.set_font(self.font)
        self.set_colour(colour)
    
    def set_text(self,text):
        self.text = text
        self.element.set_text(text)
    
    def set_colour(self,colour):
        self.element.set_colour(colour)
    
    def set_typeface(self,typeface):
        self.font = (typeface,self.font[1],self.font[2])
        self.element.set_font(self.font)
        
    def set_size(self,size):
        self.font = (self.font[0],size,self.font[2])
        self.element.set_font(self.font)
        
    def set_style(self,style):
        self.font = (self.font[0],self.font[1],style)
        self.element.set_font(self.font)
    
    def move_by(self,portion_diff_xy):
        self.element.move_by(portion_diff_xy)
        
    def move_to(self,new_portion_position_xy):
        self.element.move_to(new_portion_position_xy)

        
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
