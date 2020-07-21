#Cristopher jose Rodolfo Barrios Solis
#lab2

import struct
def char(c):
		return struct.pack('=c', c.encode('ascii'))

def word(c):
	return struct.pack('=h', c)
	
def dword(c):
	return struct.pack('=l', c)

def normalizeColorArray(colors_array):
    return [round(i*255) for i in colors_array]

def color(r,g,b):
	return bytes([b, g, r])

class Render(object):
    def __init__(self):
        self.framebuffer = []
        self.width = 520
        self.height = 300
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_width = 520
        self.viewport_height = 300
        self.glClear()

    def glInit(self):
        return "Generando...\n"

    def glClear(self):
        self.framebuffer = [
            [color(0,0,0) for x in range(self.width)] 
            for y in range(self.height)
        ]

    def glCreateWindow(self, width, height):
        self.height = height
        self.width = width

    def glClearColor(self, r=1, g=1, b=1):
        normalized = normalizeColorArray([r,g,b])
        clearColor = color(normalized[0], normalized[1], normalized[2])

        self.framebuffer = [
            [clearColor for x in range(self.width)] for y in range(self.height)
        ]

    def glColor(self, r=0, g=0, b=0):
        normalized = normalizeColorArray([r,g,b])
        self.color = color(normalized[0], normalized[1], normalized[2])

    def glViewport(self, x, y, width, height):
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_height = height
        self.viewport_width = width

    def point(self, x, y):
        self.framebuffer[y][x] = self.color

    def glVertex(self, x, y):
        final_x = round((x+1) * (self.viewport_width/2) + self.viewport_x)
        final_y = round((y+1) * (self.viewport_height/2) + self.viewport_y)
        self.point(final_x, final_y)


    def glCord(self, value, is_vertical):
        real_coordinate = ((value+1) * (self.viewport_height/2) + self.viewport_y) if is_vertical else ((value+1) * (self.viewport_width/2) + self.viewport_x)
        return round(real_coordinate)

    def glLine(self, x0, y0, x1, y1) :
        x0 = self.glCord(x0, False)
        x1 = self.glCord(x1, False)
        y0 = self.glCord(y0, True)
        y1 = self.glCord(y1, True)

        steep = abs(y1 - y0) > abs(x1 - x0)

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0 
        y = y0
        threshold =  dx

        for x in range(x0, x1):
            self.point(y, x) if steep else self.point(x, y)
            
            offset += 2*dy

            if offset >= threshold:
                y += -1 if y0 > y1 else 1
                threshold += 2*dx
                

    def glFinish(self, filename='out.bmp'):
        f = open(filename, 'bw')

        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])

        f.close()


bitmap = Render()

print(bitmap.glInit())

bitmap.glCreateWindow(600, 600)
bitmap.glViewport(90, 200, 420 , 200) 

bitmap.glClear()
bitmap.glClearColor(0, 0, 0)
bitmap.glColor(0.15, 0.255, 0) 

#linea 1
bitmap.glLine(-0.75, -1, 0.25, 1)
#linea 2
bitmap.glLine(0.25, -1, 0.25, 1)
#linea 3
bitmap.glLine(-0.75, -1, 0.25, -1)

bitmap.glFinish()