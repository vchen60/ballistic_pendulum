Web VPython 3.2
from vpython import *

################### basic parameters
L = 2
g = 9.81

scene.align = 'left'
scene.width = 400
scene.height = 280
scene.center=vec(0,2.5,0)
scene.userzoom = True
scene.userspin = True
scene.userpan = True
mode = 0

mBall= 1
vBall = vector(0, 0, 0)

mBullet = 0.002
vBullet = vector(1000, 0, 0)
vBulletStart = 1000
bulletShot = True
bulletFirstShot = True

theta = pi/2
omega = 0
frameRate = 10000
dt = 1/frameRate

transitionY = L/2

x=arrow(pos=vector(0,0,0), axis=vector(5,0,0), color=color.red, shaftwidth=0.1)
label(pos=x.pos + x.axis, text='x', xoffset=20, height=16)

y=arrow(pos=vector(0,0,0), axis=vector(0,0,5), color=color.blue, shaftwidth=0.1)
label(pos=y.pos + y.axis, text='y', yoffset=20, height=16)

z=arrow(pos=vector(0,0,0), axis=vector(0,5,0), color=color.green, shaftwidth=0.1)
label(pos=z.pos + z.axis, text='z', zoffset=20, height=16)

ball = sphere(pos=vector(L*cos(theta),transitionY-L*sin(theta)+L/2,0), radius = 0.25, color = color.orange)
rod = cylinder(pos=vec(0, transitionY+L/2, 0), axis=ball.pos-vec(0, transitionY+L/2, 0), color=color.orange, radius = 0.03, length = L)

gr = graph(align='left', title="<b> Energy of Pendulum vs Time<b>", ytitle="Energy [J]", xtitle="Time [s]", xmin=0,ymin=0, width=400, height=280)
my_curve = gcurve(color=color.red, label="Kinetic Energy")
my_curve2 = gcurve(color=color.blue, label="Potential Energy")


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
#    global length_label
#    global length_text
#    global slider_length
    if(mode==0):
        global L
        L = s.value
        length_text.text = f"{s.value:.1f} m"
        update_transitionY(s)
        rod.pos.y = transitionY+L/2
        rod.length = L
        rod.axis = ball.pos - vec(0, transitionY+L/2, 0)
    else:
        length_label.text = "Angle of Bullet to (+) x-axis: "
        L = s.value()
        length_text.text = f"{s.value:.1f} degrees"
        ## fix transition?
##change bullet angle to allow 0 to 180

def my_action(b):
    theta = pi/2
    omega = 0
    global mode
    if(b.text == "2D"):
        mode = 1
        length_label.text = "Angle of Bullet to x-z plane: "
        length_text.text = f"{L:.3f} degrees"
        slider_length.delete()
        L = 90
        slider_length.visible = True
        slider_length = slider( bind=lenChange, min=45, max=135, value=L, length=250, step=5)
    else:
        mode = 0
        length_label.text = "Pendulum Length: "
        length_text.text = f"{L:.3f} m"
        L = 4
        slider_length.delete()
        slider_length.visible = True
        slider_length = slider( bind=lenChange, min=0.5, max=10, value=L, length=250, step=.5)
    print("Switching to the following number of degrees of freedom:", mode+1)

def update_transitionY(b):
    if(mode ==0):
        global transitionY
        transitionY = b.value/2

# 2. Create the button
button(bind=my_action, text="1D", pos=scene.caption_anchor)
button(bind=my_action, text="2D", pos=scene.caption_anchor)

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

running = False

def main_loop(b):
    global running
    if(b.text=='START'):
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
            

scene.append_to_caption("\n\n")
button(bind=main_loop, text="START", pos=scene.caption_anchor)
button(bind=main_loop, text="STOP", pos=scene.caption_anchor)

scene.append_to_caption("\n\n\n\n\n\n")

t=0        
while True:
    rate(frameRate)
    if(running):
        if(mode==0):
            ### sliders on display  
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
            sleep(5) #fix to be correct
    # if not running, put smth here
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
