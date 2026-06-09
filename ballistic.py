Web VPython 3.2
from vpython import *

## DO NOT CHANGE

scene.align = 'left'
scene.width = 400
scene.height = 280
scene.center=vec(0,2.5,0)
running = False

frameRate = 10000
dt = 1/frameRate
t=0

bulletShot = True
bulletFirstShot = True

################### basic parameters
L = 2
bulletAngle = 90
g = 9.81

a = vec(0, -g, 0)
mode = 0

mBall= 1
vBall = vector(0, 0, 0)

mBullet = 0.002
vBullet = vector(1000, 0, 0)
vBulletStart = 1000

theta = pi/2
omega = 0

transitionY = L/2
pivot = vector(0, transitionY+L/2, 0)
pBall = pivot + vector(1,-sqrt(L**2-1),0)

gr = graph(align='left', title="<b> Energy of Pendulum vs Time<b>", ytitle="Energy [J]", xtitle="Time [s]", xmin=0,ymin=0, width=400, height=280)
my_curve = gcurve(graph = gr, color=color.red, label="Kinetic Energy")
my_curve2 = gcurve(graph = gr, color=color.blue, label="Potential Energy")

##### AXES

x=arrow(pos=vector(0,0,0), axis=vector(5,0,0), color=color.red, shaftwidth=0.1)
label(pos=x.pos + x.axis, text='x', xoffset=20, height=16)

y=arrow(pos=vector(0,0,0), axis=vector(0,0,5), color=color.blue, shaftwidth=0.1)
label(pos=y.pos + y.axis, text='y', yoffset=20, height=16)

z=arrow(pos=vector(0,0,0), axis=vector(0,5,0), color=color.green, shaftwidth=0.1)
label(pos=z.pos + z.axis, text='z', zoffset=20, height=16)

##########

ball = sphere(pos=vector(L*cos(theta),-L*sin(theta)+L,0), radius = 0.25, color = color.orange)
rod = cylinder(pos=vec(0, transitionY+L/2, 0), axis=ball.pos-vec(0, transitionY+L/2, 0), color=color.orange, radius = 0.03, length = L)

### ALL THE BINDS

def massBallChange(s):
    global mBall
    global ball
    mBall = s.value
    ball_text.text = f"{mBall:.3f} kg"
    ball.radius = 0.25 * (s.value**(1/3))

def massBulletChange(s):
    global mBullet
    mBullet = s.value
    mass_text.text = f"{mBullet:.3f} kg"

def speedBulletChange(s):
    global vBullet
    vBullet = vector(s.value,0,0)
    speed_text.text = f"{s.value:.1f} m/s"

def lenChange(s):
    global mode
    global L
    global transitionY
    global slider_length
    global bulletAngle
    if mode == 0:
        L = s.value
        length_text.text = f"{s.value:.1f} m"
        update_transitionY(s)
        rod.pos.y = transitionY + L/2
        rod.length = L
        rod.axis = ball.pos - vec(0, transitionY + L/2, 0)
    else:
        bulletAngle = s.value
        angleRad = bulletAngle * pi / 180
        vBall = vector(vBulletStart * cos(angleRad), 0, vBulletStart * sin(angleRad))
        length_text.text = f"{s.value:.1f} degrees"


def my_action(b):
    theta = pi/2
    omega = 0
    global mode
    global L
    global bulletAngle
    global slider_length
    global pBall
    global vBall
    global mBall
    global transitionY
    global printlag
    
    global t = 0
    if(b.text == "2D"):
        mode = 1
        length_label.text = "Angle of Bullet to x-z plane: "
        slider_length.delete()
        bulletAngle = 90
        slider_length = slider( bind=lenChange, min=0, max=180, value=bulletAngle, length=250, step=5)
        length_text.text = f"{bulletAngle:.1f} degrees"
        pivot = vector(0, transitionY, 0)
        mBall= 0.25
        pBall = pivot + vector(1,-sqrt(L**2-1),0)
        angleRad = bulletAngle * pi / 180
        vBullet = vector(vBulletStart * cos(angleRad), 0, vBulletStart * sin(angleRad))
        vBall = vector(0, 0, 10)
    else:
        mode = 0
        length_label.text = "Pendulum Length: "
        L = 2
        slider_length.delete()
        slider_length = slider( bind=lenChange, min=0.5, max=10, value=L, length=250, step=.5)
        length_text.text = f"{L:.1f} m"
        
    printlag.delete()
    printlag = wtext(text="\n\n\n\n\n\n")
    
    reset()
    main_loop(b)

def reset():
    global ball
    global rod
    global running = False
    global a = vec(0, -g, 0)
    global t = 0
    
    global L = 2
    global bulletAngle = 90
    global g = 9.81
    
    global mBall = 1
    global vBall = vector(0, 0, 0)
    
    global mBullet = 0.002
    global vBullet = vector(1000, 0, 0)
    global vBulletStart = 1000
    global bulletAngle = 90
    
    global theta = pi/2
    global omega = 0
    
    global transitionY = 1
    global pivot = vector(0, transitionY, 0)
    global pBall = pivot + vector(1,-sqrt(2**2-1),0)
    
    global my_curve
    global my_curve2
    my_curve.data = []
    my_curve2.data = []
    
    ball.pos = vector(L*cos(theta), -L*sin(theta) + L, 0)
    ball.radius = 0.25 * (mBall**(1/3))
    rod.pos = vec(0, transitionY + L/2, 0)
    rod.length = L
    rod.axis = ball.pos - vec(0, transitionY + L/2, 0)

def update_transitionY(b):
    if(mode ==0):
        global transitionY
        transitionY = b.value/2

# 2. Create the buttons
button(bind=my_action, text="1D", pos=scene.caption_anchor)
button(bind=my_action, text="2D", pos=scene.caption_anchor)


scene.append_to_caption("\n\n")
button(bind=main_loop, text="START", pos=scene.caption_anchor)
button(bind=main_loop, text="STOP", pos=scene.caption_anchor)
button(bind=main_loop, text="RESET", pos=scene.caption_anchor)

### BULLET MASS !!
scene.append_to_caption("\n\nBullet Mass: ")
mass_text = wtext(text=f"{mBullet:.3f} kg")
slider_mass_bullet = slider( bind=massBulletChange, min=0.001,max=0.1,value=mBullet, length=250, step=.001)

### BALL MASS !!
scene.append_to_caption("\n\nBall Mass: ")
ball_text = wtext(text=f"{mBall:.2f} kg")
slider_mass_ball = slider( bind=massBallChange, min=0.5, max=20, value=mBall, length=250, step = .5)

### BULLET START VEL.
scene.append_to_caption("\n\nBullet Speed: ")
speed_text = wtext(text=f"{vBullet.x:.1f} m/s")
slider_bullet_speed = slider( bind=speedBulletChange, min=50, max=10000, value=vBullet.x, length=250, step=50)

### LENGTH FOR PENDULUM
scene.append_to_caption("\n\n")
length_label = wtext(text="Pendulum Length: ")
length_text = wtext(text=f"{L:.1f} m")
slider_length = slider( bind=lenChange, min=0.1, max=5, value=L, length=250, step=.1)


def main_loop(b):
    global running
    global gr
    global printlag
    global t
    if(b.text=='START'):
        printlag.delete()
        printlag = wtext(text="\n\n\n\n\n\n")
        gr.delete()
        gr = graph(align='left', title="<b> Energy of Pendulum vs Time<b>", ytitle="Energy [J]", xtitle="Time [s]", xmin=0,ymin=0, width=400, height=280)
        slider_length.disabled = True
        slider_bullet_speed.disabled = True
        slider_mass_ball.disabled = True
        slider_mass_bullet.disabled = True
        running = True
    else:
        slider_length.disabled = False
        slider_bullet_speed.disabled = False
        slider_mass_ball.disabled = False
        slider_mass_bullet.disabled = False
        running = False
        if(b.text=='RESET'):
            reset()
            t=0
            



printlag = wtext(text="\n\n\n\n\n\n")      
while True:
    rate(frameRate)
    if(running):
        if(mode==0):
            rate(frameRate)
            if(bulletShot):
                if(bulletFirstShot):
                    omega = getNewSpeed(vBall, mBall, vBullet, mBullet) /L
                    bulletFirstShot = False
                alpha = g*cos(theta)/L
                omega += alpha*dt
                theta += omega*dt
                ball.pos.x = L*cos(theta)
                ball.pos.y = transitionY-L*sin(theta)+L/2
                rod.pos.y = transitionY+L/2
                rod.length = L
                rod.axis = ball.pos - vec(0, transitionY+L/2, 0)
                
                my_curve.plot(t, (mBall+mBullet)*(L*omega)*(L*omega)/2) # kinetic energy
                my_curve2.plot(t, (mBullet+mBall)*g*(L-L*sin(theta))) # potential energy
                t += dt
        else:
            rate(frameRate)

            if(bulletShot):
                if(bulletFirstShot):
                    vBall = (mBall*vBall + mBullet*vBullet)/(mBall+mBullet)
                    bulletFirstShot = False

                a = vector(0,-g,0)

                r = pBall - pivot
                rHat = norm(r)

                aRadial = dot(a,rHat)*rHat
                aTangent = a - aRadial

                vBall += aTangent*dt

                vRadial = dot(vBall,rHat)*rHat
                vBall -= vRadial

                pBall += vBall*dt

                r = pBall - pivot
                rHat = norm(r)
                pBall = pivot + L*rHat

                ball.pos = pBall
                rod.pos = pivot
                rod.axis = pBall - pivot

                KE = 0.5*(mBall+mBullet)*mag(vBall)**2
                PE = (mBall+mBullet)*g*(pBall.y - (pivot.y - L)) ## find correction factor since PE != 0

                my_curve.plot(t, KE)
                my_curve2.plot(t, PE)

                t += dt

def getNewSpeed(ballVelocity, ballMass, bulletVelocity, bulletMass):
    newMomentum = calculate2DMomentum(ballVelocity, ballMass, bulletVelocity, bulletMass)
    totalMass = ballMass + bulletMass
    return (newMomentum/totalMass)

def calculate2DMomentum(ballVelocity, ballMass, bulletVelocity, bulletMass):
    momentumX = calculate1DMomentum(ballVelocity.x, ballMass, bulletVelocity.x, bulletMass)
    momentumZ = calculate1DMomentum(ballVelocity.z, ballMass, bulletVelocity.z, bulletMass)
    return (sqrt(momentumX ** 2 + momentumZ ** 2))
    
def calculate1DMomentum(ballSpeed, ballMass, bulletSpeed, bulletMass):
    return(ballSpeed*ballMass + bulletSpeed*bulletMass)
