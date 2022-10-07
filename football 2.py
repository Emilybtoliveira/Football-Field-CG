from curses import KEY_UP
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

camera_x = 0
camera_y = 30
camera_z = 30

center_x = 0
center_y = 0
center_z = 0

lookat_x = 0
lookat_y = 1
lookat_z = 0

last_x_drawing_rotation = 0
last_y_drawing_rotation = 0
drawing_rotation = 0

last_axis_used = ""

rotation_x_flag = 0
rotation_y_flag = 0

MOVE_UNIT = 1
vel_unit = 1

def init():
    glClearColor(0.0, 0.1, 0.0, 1.0) 
    #glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW) 
    gluLookAt (camera_x, camera_y, camera_z,center_x, center_y, center_z,lookat_x, lookat_y, lookat_z)
    
    glMatrixMode(GL_PROJECTION)
    #glFrustum(-3.0, 3.0, 3.0, -3.0, 5.0, 15.0)
    gluPerspective(45, 640/640, 0.1, 80.0)
    glMatrixMode(GL_MODELVIEW)     
    

def drawField():
    v1 = [ 10.0, 0.0, -5.0]
    v2 = [-10.0, 0.0, -5.0]
    v3 = [-10.0, 0.0,  5.0]
    v4 = [ 10.0, 0.0,  5.0]
    v5 = [ 10.0, 2.0,  5.0]
    v6 = [ 10.0, 2.0, -5.0]
    v7 = [-10.0, 2.0, -5.0]
    v8 = [-10.0, 2.0,  5.0]

    glBegin(GL_QUADS)  
    glColor3f(0.0, 0.75, 0.0)
    glVertex3fv(v1)
    glVertex3fv(v2)
    glVertex3fv(v3)
    glVertex3fv(v4)

    glColor3f(0.0, 0.75, 0.0)
    glVertex3fv(v1)
    glVertex3fv(v4)
    glVertex3fv(v5)
    glVertex3fv(v6)

    glColor3f(0.0, 0.75, 0.0)
    glVertex3fv(v1)
    glVertex3fv(v2)
    glVertex3fv(v7)
    glVertex3fv(v6)

    glColor3f(0.0, 0.75, 0.0)
    glVertex3fv(v2)
    glVertex3fv(v3)
    glVertex3fv(v8)
    glVertex3fv(v7)

    glColor3f(0.0, 0.75, 0.0)
    glVertex3fv(v3)
    glVertex3fv(v8)
    glVertex3fv(v5)
    glVertex3fv(v4)

    glColor3f(0.0, 1.0, 0.0) #top
    glVertex3fv(v5)
    glVertex3fv(v8)
    glVertex3fv(v7)
    glVertex3fv(v6)
    glEnd()

def drawGoalpost(x_pos):
    glPushMatrix()
    glRotate(90, 1, 0, 0)
    glTranslate(x_pos, 0.5, -5.0)
    cylinder = gluNewQuadric()
    gluQuadricDrawStyle (cylinder, GLU_LINE)
    gluCylinder(cylinder, 0.4, 0.4, 3, 500, 500)
    """ glPopMatrix()

    glPushMatrix()
    glRotate(90, 1, 0, 0) """
    glTranslate(0, -3.5, 0.0)
    cylinder = gluNewQuadric()
    gluQuadricDrawStyle (cylinder, GLU_LINE)
    gluCylinder(cylinder, 0.4, 0.4, 3, 100, 100)
    glPopMatrix()

    glPushMatrix()
    glRotate(180, 1, 0, 0)
    glTranslate(x_pos, -5.0, -0.8)
    cylinder = gluNewQuadric()
    gluQuadricDrawStyle (cylinder, GLU_LINE)
    gluCylinder(cylinder, 0.4, 0.4, 4.0, 100, 100)
    glPopMatrix()

def drawBall():
    glColor3f(1.0, 1.0, 1.0)
   # glLoadIdentity()
    glPushMatrix()
    glTranslatef (0, 2.7, 0.0)
    #glTranslatef (0.5, 0.0, 0.0)
    glRotatef(45, 0, 1, 0)
    glutWireSphere (0.5, 20, 20)
   # glutSolidSphere(0.7, 8, 8)
    glPopMatrix()

def bresenhamFieldLines(x1, y1, x2, y2, z1, z2, direction):
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx 
    incE = 2 * dy 
    incNE = 2 * (dy - dx)
    x = x1
    y = y1
    z = z1

    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    
    glVertex3f (x, y, z)    
    if direction =="H":
        while x < x2:
            if d <= 0:
                d = d + incE
                x = x + 0.01
            else:
                d = d + incNE
                x = x + 0.01
                y = y + 0.01
            
            glVertex3f (x, y, z1)   
    elif direction == "V":
        while z > z2:
            if d <= 0:
                d = d + incE
                z = z - 0.01
            else:
                d = d + incNE
                z = z - 0.01
                #y = y + 0.01
            
            glVertex3f (x, y, z)  
    #glVertex3f (9.0, 2.0, 2.5)
    glEnd()

def bresenhamFieldCircle(r):
    x = 0
    y = r
    d = 1 - r

    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    
    glVertex3f (x, y, 0)  

    while x < r:
        if (d < 0): 
            d +=2 * x + 3
            x += 0.01
        else:
            d += 2 * (x - y) + 5
            x += 0.01
            #y -= 0.01        

        glVertex3f (x, y, 0)  
        glVertex3f (-x, y, 0)  
        glVertex3f (-x, -y, 0)  
        glVertex3f (x, -y, 0)
        print(x,y)

    #print(y, x)
         
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Clear color and depth buffer
    print(drawing_rotation, rotation_x_flag, rotation_y_flag, 0)
    glRotate(drawing_rotation, rotation_x_flag, rotation_y_flag, 0)
    glMatrixMode(GL_MODELVIEW) 

    drawField()    
    
    drawBall()

    glTranslate(0, 0, 1.4)
    drawGoalpost(8)
    drawGoalpost(-8)

    bresenhamFieldLines(-9.0, 2.0, 9.0, 2.0, 2.5, 2.5, "H")
    bresenhamFieldLines(-9.0, 2.0, 9.0, 2.0, -5.5, -5.5, "H")
    bresenhamFieldLines(-9.0, 2.0, 9.0, 2.0, 2.5, -5.5, "V")
    bresenhamFieldLines(9.0, 2.0, 9.0, 2.0, 2.5, -5.5, "V")
    bresenhamFieldLines(0, 2.0, 0, 2.0, 2.5, -5.5, "V")

    #bresenhamFieldCircle(1)

    glutSwapBuffers()

def move_camera():
    glMatrixMode(GL_MODELVIEW) 
    glLoadIdentity()
    gluLookAt(camera_x, camera_y, camera_z,
              center_x, center_y, center_z,
              lookat_x, lookat_y, lookat_z)
    print(f"posicao da camera: ({camera_x}, {camera_y}, {camera_z})")
    print(f"posicao do centro: ({center_x}, {center_y}, {center_z})")
    #glMatrixMode(GL_PROJECTION) 
    #glFrustum(-3.0, 3.0, 3.0, -3.0, 5.0, 15.0)
    #gluPerspective(45, 640/640, 0.1, 80.0)

def reshape(width, height): 
    pass

def keyboard_handler(key, x, y):
    global camera_x, camera_y, camera_z, center_x, center_y, center_z, lookat_x, lookat_y, lookat_z, drawing_rotation, rotation_x_flag, rotation_y_flag, last_y_drawing_rotation, last_x_drawing_rotation, last_axis_used
    
    if key == b'w': 
        camera_y += MOVE_UNIT * vel_unit
        center_y += MOVE_UNIT * vel_unit

    elif key == b's':
        camera_y -= MOVE_UNIT * vel_unit
        center_y -= MOVE_UNIT * vel_unit

    elif key == b'a': 
        camera_x -= MOVE_UNIT * vel_unit
        center_x -= MOVE_UNIT * vel_unit

    elif key == b'd':
        camera_x += MOVE_UNIT * vel_unit
        center_x += MOVE_UNIT * vel_unit

    elif key == b'q': 
        camera_z -= MOVE_UNIT * vel_unit
        center_z -= MOVE_UNIT * vel_unit

    elif key == b'e':
        camera_z += MOVE_UNIT * vel_unit
        center_z += MOVE_UNIT * vel_unit

    elif key == b'm':
        #lookat_y -= MOVE_UNIT * 1

        if last_axis_used == "x":
            last_x_drawing_rotation = drawing_rotation
            drawing_rotation = last_y_drawing_rotation

        drawing_rotation -= MOVE_UNIT
        rotation_x_flag = 0
        rotation_y_flag = 1
        last_axis_used = "y"

    elif key == b'b':
       # lookat_x += MOVE_UNIT * 0.1
        if last_axis_used == "x":
            last_x_drawing_rotation = drawing_rotation
            drawing_rotation = last_y_drawing_rotation
        drawing_rotation += MOVE_UNIT
        rotation_x_flag = 0
        rotation_y_flag = 1
        last_axis_used = "y"


    elif key == b'n':
       # lookat_x += MOVE_UNIT * 0.1
        if last_axis_used == "y":
            last_y_drawing_rotation = drawing_rotation
            drawing_rotation = last_x_drawing_rotation
        drawing_rotation -= MOVE_UNIT
        rotation_x_flag = 1
        rotation_y_flag = 0
        last_axis_used = "x"
    
    elif key == b'j':
       # lookat_x += MOVE_UNIT * 0.1
        if last_axis_used == "y":
            last_y_drawing_rotation = drawing_rotation
            drawing_rotation = last_x_drawing_rotation  
        drawing_rotation += MOVE_UNIT
        rotation_x_flag = 1
        rotation_y_flag = 0
        last_axis_used = "x"
    
    move_camera()
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowPosition(400, 300)
glutInitWindowSize(900, 600)  
glutCreateWindow("Football Field Simulator")
init() 
glutDisplayFunc(display)
#glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard_handler)

glutMainLoop()