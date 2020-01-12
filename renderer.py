
import tkinter,time,math

class Window():
    def __init__(self,dimensions_xy=(1280,720),resolution_xy=(128,72),position_xy=(0,0),initial_colour="white"):
        self.resolution_xy=resolution_xy
        # instantiates root (the window)
        self.root = tkinter.Tk()
        self.root.geometry(str(dimensions_xy[0])+"x"+str(dimensions_xy[1])+"+"+str(position_xy[0])+"+"+str(position_xy[1]))
        # instantiates the canvas (the drawable area)
        self.canvas = tkinter.Canvas(self.root,width=dimensions_xy[0],height=dimensions_xy[1])
        self.canvas.pack()
        # instantiates the pixels and ensures that subpixels (if present) are accounted for
        self.pixels = []
        avg_pixel_dimensions_xy = (dimensions_xy[0]/resolution_xy[0],dimensions_xy[1]/resolution_xy[1])
        sum_pixel_dimensions_xy = (0,0)
        current_pixel_dimensions_xy = (0,0)
        for row in range(0,resolution_xy[1]):
            pixel_row = []
            if sum_pixel_dimensions_xy[1]<=row*avg_pixel_dimensions_xy[1]:
                pixel_dimensions_xy = (pixel_dimensions_xy[0],math.ceil(avg_pixel_dimensions_xy[1]))
            else:
                pixel_dimensions_xy = (pixel_dimensions_xy[0],math.floor(avg_pixel_dimensions_xy[1]))
            for col in range(0,resolution_xy[0]):
                if sum_pixel_dimensions_xy[0]<=col*avg_pixel_dimensions_xy[0]:
                    pixel_dimensions_xy = (math.ceil(avg_pixel_dimensions_xy[0]),pixel_dimensions_xy[1])
                else:
                    pixel_dimensions_xy = (math.floor(avg_pixel_dimensions_xy[0]),pixel_dimensions_xy[1])
                pixel_row.append(Pixel(self,(sum_pixel_dimensions_xy),(pixel_dimensions_xy),initial_colour))
                sum_pixel_dimensions_xy = (sum_pixel_dimensions_xy[0]+pixel_dimensions_xy[0],sum_pixel_dimensions_xy[1])
            sum_pixel_dimensions_xy = (0,sum_pixel_dimensions_xy[1]+pixel_dimensions_xy[1])
            self.pixels.append(pixel_row)
                
    def get_pixels(self):
        return self.pixels
        
    def update(self):
        self.root.update()
        
    def close(self):
        self.root.destroy()
    
    def create_pixel(self,position_xy,dimensions_xy,colour):
        attributes = {"fill":colour,
                   "outline":colour}
        (x1,y1)=position_xy
        (x2,y2)=(position_xy[0]+dimensions_xy[0],position_xy[1]+dimensions_xy[1])
        return self.canvas.create_rectangle(x1,y1,x2,y2,attributes)
    
    def recolour_pixel(self,rectangle_id,colour):
        attributes = {"fill":colour,
                   "outline":colour}
        self.canvas.itemconfigure(rectangle_id, attributes)

class Pixel():
    def __init__(self,window,position_xy,dimensions_xy,colour="white"):
        self.window = window
        self.position_xy=position_xy
        self.dimensions_xy=dimensions_xy
        self.colour = colour
        self.rectangle_id = self.window.create_pixel(self.position_xy,self.dimensions_xy,self.colour)
        
    def set_colour(self,colour):
        self.colour = colour
        self.window.recolour_pixel(self.rectangle_id, self.colour)

        

#test
px = 1280
py = 720
spx = 128
spy = 72
w = Window((px,py),(spx,spy),(100,100))
t=w.get_pixels()

w.update()
for row in range(spy):
    for col in range(1,2):
        t[row][col].set_colour("red")
        w.update()
for row in range(spy): 
    for col in range(3,4):
        t[row][col].set_colour("blue")
        w.update()
for row in range(spy):
    for col in range(5,6):
        t[row][col].set_colour("green")
        w.update()
time.sleep(1)
