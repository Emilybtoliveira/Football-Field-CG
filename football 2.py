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

goalsCounter1 = 0
goalsCounter2 = 0

posYBall = 2.7
posXBall = 0
posZBall = 0
angleRotation = 45

flagRotationBallX = 0
flagRotationBallY = 1
flagRotationBallZ = 0

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
    global posYBall,posXBall, posZBall, angleRotation, flagRotationBallX, flagRotationBallY, flagRotationBallZ

    glFlush() # para apagar a primeira e add a segunda
    glColor3f(1.0, 1.0, 1.0)
   # glLoadIdentity()
    glPushMatrix()
    glTranslatef (posXBall, posYBall, posZBall)
    #glTranslatef (0.5, 0.0, 0.0)
    glRotatef(angleRotation, flagRotationBallX, flagRotationBallY, flagRotationBallZ)
    # o 1 é em qual eixo tem que ser feita a rotacao
    # TODO 
    glutWireSphere (0.5, 10, 10)
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

# GOAL / SCORES

def textScore(x, y, color, text):
    glColor3fv(color)
    glWindowPos2f(x, y)
    glutBitmapString(GLUT_BITMAP_TIMES_ROMAN_24, text.encode('ascii'))

def displayScores():
    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    textScore(100, 100, (1, 0, 0), str(goalsCounter1))
    textScore(150, 100, (1, 0, 0), "x")
    textScore(200, 100, (1, 0, 0), str(goalsCounter2))
    # glutSwapBuffers()
    # glutPostRedisplay()

def gol():

    # Atualizar os contadores e chamar essa função para redesenhar!
    glFlush()
    displayScores()



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
    displayScores()

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


def checkSideLimits():
    if posZBall>=4.25 or posZBall<=-4.25:
        # retornar pro centro
        returnBallCenter()
        

def returnBallCenter():
    global posYBall,posXBall,posZBall,angleRotation, flagRotationBallX, flagRotationBallY, flagRotationBallZ

    posYBall = 2.7
    posXBall = 0
    posZBall = 0
    angleRotation = 45

    flagRotationBallX = 0   
    flagRotationBallY = 1
    flagRotationBallZ = 0

def checkIfHitsBar():
    #codigo aqui para ver se vai bater na trave
    # se bater, impedir de andar!
    pass

def checkGoalLineLimits():
    global goalsCounter1, goalsCounter2
    # checar se a pos é menor que as traves e maior que a linha de fundo
    
    if posXBall>=9.25:
        # trocar placar de 1
        goalsCounter1+=1
        print("GOL")
        # gol()
        returnBallCenter()
       
    elif posXBall<=-9.5:
        # Gol, trocar placar de 2 e voltar pro meio
        goalsCounter2+=1
        print("GOL")
        # gol()
        returnBallCenter()


def makeMovements(direction):
    global posZBall, angleRotation, flagRotationBallZ, flagRotationBallX, flagRotationBallY, posZBall, posXBall, posYBall
    
    if direction == "up":
        posZBall-=0.25
        print(posZBall)
        flagRotationBallX = 0
        flagRotationBallY=0
        flagRotationBallZ=1
        angleRotation+=90

    elif direction == "down":
        posZBall+=0.25
        flagRotationBallX = 0
        flagRotationBallY=0
        flagRotationBallZ=1
        angleRotation-=90
    elif direction == "left":
        posXBall-=0.25
        print(posXBall)
        flagRotationBallZ= 0
        flagRotationBallY=0
        flagRotationBallX=1
        angleRotation-=90
        
    elif direction == "right":
        posXBall+=0.25
        flagRotationBallZ = 0
        flagRotationBallY=0
        flagRotationBallX=1
        angleRotation+=90

def keyboard_handler(key, x, y):
    global camera_x, camera_y, camera_z, center_x, center_y, center_z, lookat_x, lookat_y, lookat_z, drawing_rotation, rotation_x_flag, rotation_y_flag, last_y_drawing_rotation, last_x_drawing_rotation, last_axis_used, goalsCounter1, goalsCounter2, posXBall, posYBall,posZBall, angleRotation, flagRotationBallX, flagRotationBallY, flagRotationBallZ

    # TODO checar os limites, e dentro dos limites se é gol
    # TODO se a bola passar da linha de fundo, checar se foi goi
    # TODO se a bola passar da linha lateral, reiniciar ela para o meio do campo
# TODO separar em funcoes
# TODO fazer rotacao
    
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

    elif key == GLUT_KEY_UP:
       # lookat_x += MOVE_UNIT * 0.1
        makeMovements("up")
        checkSideLimits()
        
        
    elif key == GLUT_KEY_LEFT:
       # lookat_x += MOVE_UNIT * 0.1
       # Rotacao eixo X
        makeMovements("left")
        checkGoalLineLimits()
        
        
    elif key == GLUT_KEY_DOWN:
       # lookat_x += MOVE_UNIT * 0.1
       # Rotacionar no eixo Z
        makeMovements("down")
        checkSideLimits()
        
        
    elif key == GLUT_KEY_RIGHT:
        makeMovements("right")
        checkGoalLineLimits()
        
        # Rotacionar no eixo X
       # lookat_x += MOVE_UNIT * 0.1
        
    elif key == b'0':
        # TODO definir limite de cima
        posYBall+=0.25
       # lookat_x += MOVE_UNIT * 0.1
        
    elif key == b'1':
        newYPos = posYBall-0.25
        if newYPos>=0:
            posYBall-=0.25
       # lookat_x += MOVE_UNIT * 0.1
        

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
glutSpecialFunc(keyboard_handler);

glutMainLoop()