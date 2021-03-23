import renderer as renderer
import time

print("\nstarting test")

wait_time = 1/4
position_a = (1/4,1/4)
position_b = (1/4,1/4)
movement_a = (1/4,1/4)
dimensions_a = (1/4,1/4)

print(" - testing: creating window")

window_dimensions = (1280,720)
window_position = (200,100)
window = renderer.Window(window_dimensions,window_position)
window.update()
time.sleep(wait_time)


print(" - testing: rectangle objects")

rectangle = renderer.Rectangle(window,position_a,dimensions_a,"blue")
window.update()
time.sleep(wait_time)
rectangle.set_colour("green")
window.update()
time.sleep(wait_time)
rectangle.move_by(movement_a)
window.update()
time.sleep(wait_time)
rectangle.move_to(position_b)
window.update()
time.sleep(wait_time)
window.remove(rectangle)
window.update()
time.sleep(wait_time)

print(" - testing: oval objects")

oval = renderer.Oval(window,position_a,dimensions_a,"red")
window.update()
time.sleep(wait_time)
oval.set_colour("green")
window.update()
time.sleep(wait_time)
oval.move_by(movement_a)
window.update()
time.sleep(wait_time)
oval.move_to(position_b)
window.update()
time.sleep(wait_time)
window.remove(oval)
window.update()
time.sleep(wait_time)

print(" - testing: bitmap objects")

bitmap_resolution = (128,72)
bitmap = renderer.Bitmap(window,position_a,bitmap_resolution,dimensions_a)
pixels = bitmap.get_pixels()
for row in range(bitmap_resolution[1]):
    for col in range(bitmap_resolution[0]):
        if col%3==0:
            pixels[row][col].set_colour("red")
        elif col%3==1:
            pixels[row][col].set_colour("blue")
        else:
            pixels[row][col].set_colour("green")
window.update()
time.sleep(wait_time)
pixels = bitmap.get_pixels()
for row in range(bitmap_resolution[1]):
    for col in range(bitmap_resolution[0]):
        if col%3==0:
            pixels[row][col].set_colour("magenta")
        elif col%3==1:
            pixels[row][col].set_colour("black")
        else:
            pixels[row][col].set_colour("yellow")
window.update()
time.sleep(wait_time)
bitmap.move_by(movement_a)
window.update()
time.sleep(wait_time)
bitmap.move_to(position_b)
window.update()
time.sleep(wait_time)
window.remove(bitmap)
window.update()
time.sleep(wait_time)

print(" - testing: text objects")

text_content = "original text"
typeface = "arial"
size = 10
style = "normal"
colour = "black"
text = renderer.Text(window,position_a,text_content,typeface,size,style,colour)
window.update()
time.sleep(wait_time)
text.set_text("new text")
text.set_colour("red")
window.update()
time.sleep(wait_time)
text.set_typeface("helvetica")
text.set_size(20)
text.set_style("italic")
window.update()
time.sleep(wait_time)
text.move_by(movement_a)
window.update()
time.sleep(wait_time)
text.move_to(position_b)
window.update()
time.sleep(wait_time)
window.remove(text)
window.update()
time.sleep(wait_time)

print(" - testing: closing window")

window.close()
time.sleep(wait_time)

print("finished test\n")



