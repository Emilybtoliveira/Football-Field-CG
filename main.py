from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy as np


""" camera_x = 0
camera_y = 2 #30
camera_z = 4 #30 """
camera_x = 0
camera_y = 110
camera_z = 110 
""" 
center_x = 20
center_y = 3
center_z = -100 """

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

goalsCounter1 = 0
goalsCounter2 = 0

posYBall = 0.7
posXBall = 0
posZBall = 0
angleRotation = 45

flagRotationBallX = 0
flagRotationBallY = 1
flagRotationBallZ = 0

textID2 = 0
textID = 0

day = True

#TODO fazer uma função para as texturas!

#======================== MODELAGEM =====================================
def drawField():
    global textID2, textID
    v1 = [ 40.0, 0.0, -20.0]
    v2 = [-40.0, 0.0, -20.0]
    v3 = [-40.0, 0.0,  20.0]
    v4 = [ 40.0, 0.0,  20.0]
    v5 = [ 40.0, 0.5,  20.0]
    v6 = [ 40.0, 0.5, -20.0]
    v7 = [-40.0, 0.5, -20.0]
    v8 = [-40.0, 0.5,  20.0]

    v9 = [100.0, 0.0, -100.0]
    v10 = [-100.0, 0.0, -100.0]
    v11 = [-100.0, 0.0,  100.0]
    v12 = [ 100.0, 0.0,  100.0]
    
    # parte externa ao campo
    glBindTexture(GL_TEXTURE_2D,textID2)
    glEnable(GL_TEXTURE_2D)
    
    glBegin(GL_QUADS) 
    glNormal3f(0,1,0)
    glColor3f(0.3,0.5,0)
    
    glVertex3fv(v9)
    glTexCoord2f(0, 1)
    glVertex3fv(v10)
    glTexCoord2f(0, 0)
    glVertex3fv(v11)
    glTexCoord2f(1,0)
    glVertex3fv(v12)
    glTexCoord2f(1, 1)
    
    glEnd()

    glDisable(GL_TEXTURE_2D)

    glBegin(GL_QUADS)  
    glNormal3f(0,1,0)
    glColor3f(0.54, 0.27, 0.07)
    glVertex3fv(v1)
    glVertex3fv(v2)
    glVertex3fv(v3)
    glVertex3fv(v4)
    glEnd()

    glBegin(GL_QUADS) 
    glNormal3f(0,1,0)
    glColor3f(0.54, 0.27, 0.07)
    glVertex3fv(v1)
    glVertex3fv(v4)
    glVertex3fv(v5)
    glVertex3fv(v6)
    glEnd()

    glBegin(GL_QUADS) 
    glNormal3f(0,1,0)
    glColor3f(0.54, 0.27, 0.07)
    glVertex3fv(v1)
    glVertex3fv(v2)
    glVertex3fv(v7)
    glVertex3fv(v6)
    glEnd()

    glBegin(GL_QUADS) 
    glNormal3f(0,1,0)
    glColor3f(0.54, 0.27, 0.07)
    glVertex3fv(v2)
    glVertex3fv(v3)
    glVertex3fv(v8)
    glVertex3fv(v7)
    glEnd()

    
    # glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS) 
    glNormal3f(0,1,0)
    glColor3f(0.54, 0.27, 0.07)
    glVertex3fv(v3)
    # glTexCoord2f(0, 1)
    glVertex3fv(v8)
    # glTexCoord2f(0, 0)
    glVertex3fv(v5)
    # glTexCoord2f(1, 0)
    glVertex3fv(v4)
    # glTexCoord2f(1, 1)
    glEnd()
    # glDisable(GL_TEXTURE_2D)


    glBindTexture(GL_TEXTURE_2D,textID)
    glEnable(GL_TEXTURE_2D)

    especularidade = [-1.0, -1.0, -1.0, 1.0]
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, especularidade)
    
    glBegin(GL_QUADS)     
    glNormal3f(0,1,0)
    glColor3f(0.0, 0.85, 0.0) #base do campo

    glVertex3fv(v5)
    glTexCoord2f(0, 1)
    glVertex3fv(v8)
    glTexCoord2f(0, 0)
    glVertex3fv(v7)
    glTexCoord2f(1, 0)
    glVertex3fv(v6)
    glTexCoord2f(1, 1)
    glEnd()  

    glDisable(GL_TEXTURE_2D)
    
    
def drawGoalpost(x_pos):
    glPushMatrix()

    glRotate(90, 1, 0, 0)
    glTranslate(x_pos, 0.5, -3.5)
    cylinder = gluNewQuadric()
    gluQuadricDrawStyle (cylinder, GLU_LINE)
    gluCylinder(cylinder, 0.15, 0.15, 3, 500, 500)
   
    glTranslate(0, -3.5, 0.0)
    cylinder = gluNewQuadric()
    gluQuadricDrawStyle (cylinder, GLU_LINE)
    gluCylinder(cylinder, 0.15, 0.15, 3, 100, 100)
    glPopMatrix()

    glPushMatrix()
    glRotate(180, 1, 0, 0)
    glTranslate(x_pos, -3.5, -0.6)
    cylinder = gluNewQuadric()
    gluQuadricDrawStyle (cylinder, GLU_LINE)
    gluCylinder(cylinder, 0.15, 0.15, 3.8, 100, 100)

    glPopMatrix()

def drawBall():
    global posYBall,posXBall, posZBall, angleRotation, flagRotationBallX, flagRotationBallY, flagRotationBallZ

    glFlush() # para apagar a primeira e add a segunda
    glColor3f(1.0, 1.0, 1.0)
   
    glPushMatrix()
    glTranslatef (posXBall, posYBall, posZBall)
   
    glRotatef(angleRotation, flagRotationBallX, flagRotationBallY, flagRotationBallZ)
    # o 1 é em qual eixo tem que ser feita a rotacao
    glutWireSphere (0.5, 20, 20)
   
    glPopMatrix()

def drawBleachStructure(y_translation = 0):     
    glPushMatrix()

    glColor3f(0.8, 0.8,0.8)    
    
    glRotate(-90, 1, 0, 0)   
    height = 1.5
    x_translation = 0.0
    glTranslate(0, y_translation, 0)

    for i in range(4):
        glTranslate(x_translation, 0, 0)

        cylinder = gluNewQuadric()
        gluQuadricDrawStyle (cylinder, GLU_LINE)
        gluCylinder(cylinder, 0.05, 0.05, height, 500, 500)

        height += 1.5
        x_translation -= 1.0

    
    glRotate(90, 0, 1, 0) 
    cylinder = gluNewQuadric()
    gluQuadricDrawStyle (cylinder, GLU_LINE)
    gluCylinder(cylinder, 0.05, 0.05, (x_translation*-1) + 2, 500, 500)     

    cylinder = gluNewQuadric()
    gluQuadricDrawStyle (cylinder, GLU_LINE)
    gluCylinder(cylinder, 0.05, 0.05, (x_translation*-1) + 2, 500, 500) 

    
    glPopMatrix()
    
def drawABleachSideRight():
    glTranslate(40,0,-45) # mudar isso aqui
    glRotate(-90, 0, 1, 0)
    lista = [-62,-18]    
    for i in range (2): #qnt
        glPushMatrix()
        drawBleachStructure(lista[i])
        glTranslate(0,-40,-40)
        glPopMatrix()
    

    glPushMatrix()
    glRotate(180, 0, 1, 0)  
    glTranslate(6,6.0,-62)
    cylinder = gluNewQuadric()
    gluQuadricDrawStyle (cylinder, GLU_LINE)
    gluCylinder(cylinder, 0.05, 0.05, 45, 500, 500) 
    glPopMatrix()

    
    glColor3f(0.0, 0.7,1.0)

    glPushMatrix()
    glTranslate(-0.5, 1.5, 40)
    glScalef(1.5, -0.5, 45.0) # mudando esse 80 ja vai ajudar nas coisas!
    glutSolidCube(1.0)  
    

    
    glTranslate(-1.0, -2.5, 0)
    glScalef(1.1, 1.0, 1)
    glutSolidCube(1.0)
    

    
    glTranslate(-1.1, -3.0, 0)
    glScalef(1.3, 1.0, 1.0)
    glutSolidCube(1.0)    
    
    glPopMatrix()

def drawABleachSideDown():
    
    glTranslate(25,0,40) # posicao de tudo
    glRotate(180, 0, 1, 0)  # fez rodar, só precisa manipular as

    for i in range (3):
        drawBleachStructure(-40*i)

    
    glPushMatrix()
    glRotate(180, 0, 1, 0)  # o que é
    glTranslate(6,6.0,-80) # movendo algo
    cylinder2 = gluNewQuadric()
    gluQuadricDrawStyle (cylinder2, GLU_LINE)
    gluCylinder(cylinder2, 0.05, 0.05, 80, 500, 500) 
    glPopMatrix()

    
    glColor3f(0.0, 0.7,1.0)

    glPushMatrix()
    glTranslate(-0.5, 1.5, 40) # move as bases
    glScalef(1.5, -0.5, 80.0)
    glutSolidCube(1.0)  
    
    glTranslate(-1.0, -2.5, 0)
    glScalef(1.5, 1.0, 1.0)
    glutSolidCube(1.0)

    glTranslate(-1.1, -3.0, 0)
    glScalef(1.3, 1.0, 1.0)
    glutSolidCube(1.0)   
    glPopMatrix()
    
def drawABleachSideUp():
    # 55,0,-60
    glTranslate(-30,0,-40) # posicao de tudo
    # glRotate(180, 0, 1, 0)  # fez rodar, só precisa manipular as

    for i in range (3):
        drawBleachStructure(-40*i)

    
    glPushMatrix()
    glRotate(180, 0, 1, 0)  # o que é
    glTranslate(6,6.0,-80) # movendo algo
    cylinder2 = gluNewQuadric()
    gluQuadricDrawStyle (cylinder2, GLU_LINE)
    gluCylinder(cylinder2, 0.05, 0.05, 80, 500, 500) 
    glPopMatrix()

    
    glColor3f(0.0, 0.7,1.0)
    specular = [0.5, 0.5, 0.5, 1.0]
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    #glMaterialf(GL_FRONT, GL_SHININESS, 128)

    glPushMatrix()
    glTranslate(-0.5, 1.5, 40) # move as bases
    glScalef(1.5, -0.5, 80.0)
    glutSolidCube(1.0)  
    
    glTranslate(-1.0, -2.5, 0)
    glScalef(1.5, 1.0, 1.0)
    glutSolidCube(1.0)

    glTranslate(-1.1, -3.0, 0)
    glScalef(1.3, 1.0, 1.0)
    glutSolidCube(1.0)   
    glPopMatrix()

def drawABleachSideLeft():
    glTranslate(-40,0,45) # mudar isso aqui
    glRotate(90, 0, 1, 0)
    lista = [-62,-18]    
    for i in range (2): #qnt
        glPushMatrix()
        drawBleachStructure(lista[i])
        glTranslate(0,-40,-40)
        glPopMatrix()
    

    glPushMatrix()
    glRotate(180, 0, 1, 0)  
    glTranslate(6,6.0,-62)
    cylinder = gluNewQuadric()
    gluQuadricDrawStyle (cylinder, GLU_LINE)
    gluCylinder(cylinder, 0.05, 0.05, 45, 500, 500) 
    glPopMatrix()

    
    glColor3f(0.0, 0.7,1.0)

    glPushMatrix()
    glTranslate(-0.5, 1.5, 40)
    glScalef(1.5, -0.5, 45.0) # mudando esse 80 ja vai ajudar nas coisas!
    glutSolidCube(1.0)  
    

    
    glTranslate(-1.0, -2.5, 0)
    glScalef(1.1, 1.0, 1)
    glutSolidCube(1.0)
    

    
    glTranslate(-1.1, -3.0, 0)
    glScalef(1.3, 1.0, 1.0)
    glutSolidCube(1.0)    
    
    glPopMatrix()
 
def drawBleachers():
    # Laterais
    glPushMatrix()
    drawABleachSideRight() # lateral
    glPopMatrix()

    glPushMatrix()
    drawABleachSideUp()
    
    glPopMatrix()

    glPushMatrix()
    drawABleachSideDown()
    glPopMatrix()
    # Fundos do campo

    glPushMatrix()
    drawABleachSideLeft()
    glPopMatrix()

    #TODO diminuir as arquibancadas e girar elas!
    # TODO resolver o posicionamento!

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

def circleSymmetry(xoffset, zoffset, x, z):
    glVertex3f(xoffset+x, 0.5, zoffset+z);
    glVertex3f(xoffset-x, 0.5, zoffset+z);
    glVertex3f(xoffset+x, 0.5, zoffset-z);
    glVertex3f(xoffset-x, 0.5, zoffset-z);
    glVertex3f(xoffset+z, 0.5, zoffset+x);
    glVertex3f(xoffset-z, 0.5, zoffset+x);
    glVertex3f(xoffset+z, 0.5, zoffset-x);
    glVertex3f(xoffset-z, 0.5, zoffset-x);

#======================== BRESENHAM =====================================
#fonte do algoritmo: https://www.geeksforgeeks.org/bresenhams-circle-drawing-algorithm/
def bresenhamFieldCircle(r):
    x = 0
    z = r
    d = 3 - 2 * r

    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    
    #glVertex3f (x, y, 0)
    circleSymmetry(0, -1.5, x, z)

    while x < z:
        if (d < 0): 
            d += (4 * x) + 0.06
            x += 0.01
        else:
            d += 4 * (x - z) + 0.010
            x += 0.01
            z -= 0.01        

        circleSymmetry(0, -1.5, x, z)         
    glEnd()

def bresenhamFieldHalfCircle(r, xoffset, zoffset):
    x = 0
    z = r
    d = 3 - 2 * r

    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(xoffset+x, 0.5, zoffset+z)
    glVertex3f(xoffset-x, 0.5, zoffset+z)

    while x < z:
        if (d < 0): 
            d += (4 * x) + 0.06
            x += 0.01
        else:
            d += 4 * (x - z) + 0.010
            x += 0.01
            z -= 0.01        
    
        glVertex3f(xoffset+x, 0.5, zoffset+z)
        glVertex3f(xoffset-x, 0.5, zoffset+z)   
    glEnd()

def drawFieldLines():
    bresenhamFieldLines(-33.0, 0.5, 33.0, 0.5, 15.0, 15.0, "H")
    bresenhamFieldLines(-33.0, 0.5, 33.0, 0.5, -17.8, -17.8, "H")
    bresenhamFieldLines(-33.0, 0.5, 33.0, 0.5, 15.0, -17.8, "V")
    bresenhamFieldLines(33.0, 0.5, 33.0, 0.5, 15.0, -17.8, "V")
    bresenhamFieldLines(0, 0.5, 0, 0.5, 15.0, -17.8, "V")
    
    #LEFT SIDE
    bresenhamFieldLines(-30.5, 0.5, -32.0, 0.5, 1.0, -3.5, "V")
    bresenhamFieldLines(-33.0, 0.5, -30.5, 0.5, -3.5, -3.5, "H")
    bresenhamFieldLines(-33.0, 0.5, -30.5, 0.5, 1.0, -3.5, "H")

    bresenhamFieldLines(-27.5, 0.5, 29.0, 0.5, 4.0, -6.5, "V")
    bresenhamFieldLines(-33.0, 0.5, -27.5, 0.5, -6.5, -7.5, "H")
    bresenhamFieldLines(-33.0, 0.5, -27.5, 0.5, 4.0, -7.5, "H")

    #RIGHT SIDE
    bresenhamFieldLines(30.5, 0.5, 32.0, 0.5, 1.0, -3.5, "V")
    bresenhamFieldLines(30.5, 0.5, 33.0, 0.5, -3.5, -3.5, "H")
    bresenhamFieldLines(30.5, 0.5, 33.0, 0.5, 1.0, -3.5, "H")

    bresenhamFieldLines(27.5, 0.5, -32.0, 0.5, 4.0, -6.5, "V")
    bresenhamFieldLines(27.5, 0.5, 33.0, 0.5, -6.5, -7.5, "H")
    bresenhamFieldLines(27.5, 0.5, 33.0, 0.5, 4.0, -7.5, "H")

    bresenhamFieldCircle(2.5)
    glRotate(90,0,1,0)
    bresenhamFieldHalfCircle(2.5, 1, -29.2)
    glRotate(180,0,1,0)
    bresenhamFieldHalfCircle(2.5, -1.0, -29.2)

#======================== PLACAR E GOL =====================================
def textScore(x, y, color, text):
    glColor3fv(color)
    glWindowPos2f(x, y)
    glutBitmapString(GLUT_BITMAP_TIMES_ROMAN_24, text.encode('ascii'))

def displayScores():
    #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    textScore(100, 100, (1, 0, 0), str(goalsCounter1))
    textScore(150, 100, (1, 0, 0), "x")
    textScore(200, 100, (1, 0, 0), str(goalsCounter2))
    #glutSwapBuffers()
    #glutPostRedisplay()

def gol():

    # Atualizar os contadores e chamar essa função para redesenhar!
    glFlush()
    displayScores()

def checkSideLimits():
    # mudar isso aqui!
    if posZBall>=17.5 or posZBall<=-17.5:
        # retornar pro centro
        returnBallCenter()    

def returnBallCenter():
    global posYBall,posXBall,posZBall,angleRotation, flagRotationBallX, flagRotationBallY, flagRotationBallZ

    posYBall = 0.7
    posXBall = 0
    posZBall = 0
    angleRotation = 45

    flagRotationBallX = 0   
    flagRotationBallY = 1
    flagRotationBallZ = 0

def checkIfHitsBar():
    global posYBall,posXBall,posZBall
    # mudar aqui!
    if posXBall == -34 or posXBall == 34:
        return posZBall in [-1.5, -1.75,1.75, 2]

def checkGoalLineLimits(side):
    global goalsCounter1, goalsCounter2, posXBall

    
    if checkIfHitsBar():
        if side == "left":
            posXBall+=0.25
        else:
            posXBall-=0.25
        
    # mudar isso aqui
    if posXBall>=33.5:
        if posZBall<2.5 and posZBall>-1.5:
            goalsCounter1+=1
            print("GOL")

        returnBallCenter()
        
    # mudar isso aqui
    elif posXBall<=-33.5:

        if posZBall<2.5 and posZBall>-1.5:
            goalsCounter2+=1
            print("GOL")

        returnBallCenter()      
  
#======================== CAMERA E MOVIMENTAÇÃO  =====================================
def makeMovements(direction):
    global posZBall, angleRotation, flagRotationBallZ, flagRotationBallX, flagRotationBallY, posZBall, posXBall, posYBall
    
    if direction == "up":
        posZBall-=0.25
        #print(f"PosZ {posZBall}")
        flagRotationBallX = 0
        flagRotationBallY=0
        flagRotationBallZ=1
        angleRotation+=90

    elif direction == "down":
        posZBall+=0.25
        #print(f"PosZ {posZBall}")
        flagRotationBallX = 0
        flagRotationBallY=0
        flagRotationBallZ=1
        angleRotation-=90
    elif direction == "left":
        posXBall-=0.25
       # print(f"PosX {posXBall}")
        flagRotationBallZ= 0
        flagRotationBallY=0
        flagRotationBallX=1
        angleRotation-=90
        
    elif direction == "right":
        posXBall+=0.25
        #print(f"PosX {posXBall}")
        flagRotationBallZ = 0
        flagRotationBallY=0
        flagRotationBallX=1
        angleRotation+=90

def move_camera():
    glMatrixMode(GL_MODELVIEW) 
    glLoadIdentity()
    gluLookAt(camera_x, camera_y, camera_z,
              center_x, center_y, center_z,
              lookat_x, lookat_y, lookat_z)

def keyboard_handler(key, x, y):
    global camera_x, camera_y, camera_z, center_x, center_y, center_z, lookat_x, lookat_y, lookat_z, drawing_rotation, rotation_x_flag, rotation_y_flag, last_y_drawing_rotation, last_x_drawing_rotation, last_axis_used, posYBall, posXBall, posZBall, day
    print(key)
    if key == b'w': 
        camera_y += 1
        center_y += 1

    elif key == b's':
        camera_y -= 1
        center_y -= 1

    elif key == b'a': 
        camera_x -= 1
        center_x -= 1

    elif key == b'd':
        camera_x += 1
        center_x += 1

    elif key == b'q': 
        camera_z -= 1
        center_z -= 1

    elif key == b'e':
        camera_z += 1
        center_z += 1

    elif key == b'm':
        #lookat_y -= 1 * 1

        if last_axis_used == "x":
            last_x_drawing_rotation = drawing_rotation
            drawing_rotation = last_y_drawing_rotation

        drawing_rotation -= 1
        rotation_x_flag = 0
        rotation_y_flag = 1
        last_axis_used = "y"

    elif key == b'b':
       # lookat_x += 1 * 0.1
        if last_axis_used == "x":
            last_x_drawing_rotation = drawing_rotation
            drawing_rotation = last_y_drawing_rotation
        drawing_rotation += 1
        rotation_x_flag = 0
        rotation_y_flag = 1
        last_axis_used = "y"


    elif key == b'n':
       # lookat_x += 1 * 0.1
        if last_axis_used == "y":
            last_y_drawing_rotation = drawing_rotation
            drawing_rotation = last_x_drawing_rotation
        drawing_rotation -= 1
        rotation_x_flag = 1
        rotation_y_flag = 0
        last_axis_used = "x"
    
    elif key == b'j':
       # lookat_x += 1 * 0.1
        if last_axis_used == "y":
            last_y_drawing_rotation = drawing_rotation
            drawing_rotation = last_x_drawing_rotation  
        drawing_rotation += 1
        rotation_x_flag = 1
        rotation_y_flag = 0
        last_axis_used = "x"
    
    elif key == b'l':
        if day:
            day = False
        else:
            day = True


    elif key == GLUT_KEY_UP:
       # lookat_x += MOVE_UNIT * 0.1
        makeMovements("up")
        
        checkSideLimits()
        
        
    elif key == GLUT_KEY_LEFT:
       # lookat_x += MOVE_UNIT * 0.1
       # Rotacao eixo X
        makeMovements("left")
        checkGoalLineLimits("left")
        
        
    elif key == GLUT_KEY_DOWN:
       # lookat_x += MOVE_UNIT * 0.1
       # Rotacionar no eixo Z
        makeMovements("down")
        checkSideLimits()
        
        
    elif key == GLUT_KEY_RIGHT:
        makeMovements("right")
        checkGoalLineLimits("right")
        
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


#======================== FUNÇÕES GERAIS  =====================================
def display():
    ilumination()

    global textID2, textID
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Clear color and depth buffer
    #print(drawing_rotation, rotation_x_flag, rotation_y_flag, 0)
    glRotate(drawing_rotation, rotation_x_flag, rotation_y_flag, 0)
    glMatrixMode(GL_MODELVIEW) 

    drawField()    

    drawBall()

    glTranslate(0, 0, 1.4)
    drawGoalpost(33.2)
    drawGoalpost(-33.2)

    displayScores()

    drawFieldLines()
    
    drawBleachers()

    glutSwapBuffers()
    

def textura1(source):
    img = Image.open(source)
    img_data = np.array(list(img.getdata()), np.int8)
    textID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D,textID)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return textID

def textura2(source):
    img = Image.open(source)
    img_data = np.array(list(img.getdata()), np.int8)
    textID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D,textID)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    return textID


def ilumination():   
    global textID 
    if day:
        globalAmb = [1.0, 1.0, 1.0, 1.0]
        light_color = [1.0, 1.0, 1.0, 1.0]
        glClearColor(0.0, 0.5, 1.0, 1.0)    
        textID = textura1("gramados/day_gramado.jpg")
    else:
        globalAmb = [0.2, 0.2, 0.2, 1.0]
        light_color = [0.0, 0.0, 0.1, 1.0]
        glClearColor(0.0, 0.0, 0.1, 1.0)    
        textID = textura1("gramados/night_gramado.jpg")

    
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, globalAmb)
    
    posVector = [0.0, 0.0, 20.0]
    dirVector = [0.0, 0, -1.0]
        
    glLightfv (GL_LIGHT1, GL_POSITION, posVector)
    glLightfv (GL_LIGHT1, GL_SPOT_DIRECTION, dirVector)
    glLightf (GL_LIGHT1, GL_SPOT_CUTOFF, 30)
    glLightfv (GL_LIGHT1, GL_DIFFUSE, light_color)
    #glLightfv (GL_LIGHT1, GL_SPECULAR, light_color)
    #glLightfv (GL_LIGHT1, GL_AMBIENT, color);
 
    """especularidade = [1.0, 1.0, 1.0, 1.0]
    glMaterialfv(GL_FRONT, GL_SPECULAR, especularidade)
    glMaterialf(GL_FRONT, GL_SHININESS, 2.0) """    
    
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT1)
   # glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    #glShadeModel(GL_FLAT)
    #glEnable(GL_CULL_FACE)

def init():
    global textID2, textID 
    glClearColor(0.0, 0.5, 1.0, 1.0)    


    glMatrixMode(GL_MODELVIEW) 
    gluLookAt (camera_x, camera_y, camera_z,center_x, center_y, center_z,lookat_x, lookat_y, lookat_z)
    
     
  
    glMatrixMode(GL_PROJECTION)
    #glFrustum(-3.0, 3.0, 3.0, -3.0, 5.0, 15.0)
    gluPerspective(45, 640/640, 0.1, 400.0)
    glMatrixMode(GL_MODELVIEW)     
    glEnable(GL_DEPTH_TEST)


glutInit()
glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB)
glutInitWindowPosition(400, 300)
glutInitWindowSize(900, 600)  
glutCreateWindow("Football Field Simulator")
init() 
#ilumination()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard_handler)
glutSpecialFunc(keyboard_handler)

glutMainLoop()