Web VPython 3.2

################### basic parameters
L = 4
g = 9.81

scene.userzoom = True
scene.userspin = True
scene.userpan = True
mode = 0

mBall= 0.25
vBall = vector(0, 0, 0)

mBullet = 0.002
vBullet = vector(100, 0, 0)
vBulletStart = 100
bulletShot = True
bulletFirstShot = True

theta = pi/2
omega = 0

frameRate = 50000
dt = 1/frameRate


transitionY = 2

arrow(pos=vector(0,0,0), axis=vector(5,0,0), color=color.red, shaftwidth=0.1)
arrow(pos=vector(0,0,0), axis=vector(0,5,0), color=color.green, shaftwidth=0.1)
arrow(pos=vector(0,0,0), axis=vector(0,0,5), color=color.blue, shaftwidth=0.1)


ball = sphere(pos=vector(L*cos(theta),transitionY-L*sin(theta),0), radius = 0.5, color = color.orange)
rod = cylinder(pos=vec(0, transitionY, 0), axis=vec(cos(theta), -sin(theta), 0), color=color.orange, radius = 0.05, length = L)

gr = graph(align='right', title="<b> Energy of Pendulum vs Time<b>", ytitle="Energy [J]", xtitle="Time [s]", xmin=0,ymin=0)
my_curve = gcurve(color=color.red, label="Kinetic Energy")
my_curve2 = gcurve(color=color.blue, label="Potential Energy")


### ALL THE BINDS

def massBallChange(s):
    global mBall
    mBall = s.value
    ball_text.text = f"{mBall:.3f} kg"

def massBulletChange(s):
    global mBullet
    mBullet = s.value
    mass_text.text = f"{mBullet:.3f} kg"

def speedBulletChange(s):
    global vBullet
    vBullet = vector(s.value,0,0)
    speed_text.text = f"{s.value:.1f} m/s"


def lenChange(s):
    if(mode==0):
        global L
        L = s.value
        length_text.text = f"{s.value:.1f} m"


def my_action(b):
    global mode
    if(b.text == "2D"):
        mode = 1
    else:
        mode = 0

# 2. Create the button
button(bind=my_action, text="1D", pos=scene.caption_anchor)
button(bind=my_action, text="2D", pos=scene.caption_anchor)


### BULLET MASS !!
scene.append_to_caption("\n\nBullet Mass: ")
mass_text = wtext(text=f"{mBullet:.3f} kg")

slider_mass_bullet = slider( bind=massBulletChange, min=0,max=0.1,value=mBullet, length=250, step=.001)

### BALL MASS !!
scene.append_to_caption("\n\nBall Mass: ")
ball_text = wtext(text=f"{mBall:.3f} kg")

slider_mass_ball = slider( bind=massBallChange, min=0, max=50, value=mBall, length=250)

### BULLET START VEL.
scene.append_to_caption("\n\nBullet Speed: ")

speed_text = wtext(text=f"{vBullet.x:.3f} m/s")

slider_bullet_speed = slider( bind=speedBulletChange, min=50, max=1000, value=vBullet.x, length=250, step=50)

### LENGTH FOR PENDULUM
scene.append_to_caption("\n\nPendulum Length: ")

length_text = wtext(text=f"{L:.3f} m")

slider_length = slider( bind=lenChange, min=0, max=10, value=L, length=250, step=.5)


sleep(2)
t=0
while True:
    ### sliders on display  
    rate(frameRate)
    if(bulletShot):
        if(bulletFirstShot):
            omega = getNewSpeed(vBall, mBall, vBullet, mBullet)
            bulletFirstShot = False
        alpha = g*cos(theta)/L
        omega += alpha*dt
        theta += omega*dt
        ball.pos.x = L*cos(theta)
        ball.pos.y = transitionY-L*sin(theta)
        rod.rotate(angle=omega, axis=vector(cos(theta), -sin(theta), 0))
        
        my_curve.plot(t, (mBall+mBullet)*(L*omega)*(L*omega)/2) # kinetic energy
        my_curve2.plot(t, (mBullet)*vBulletStart*vBulletStart/2-(mBall+mBullet)*(L*omega)*(L*omega)/2) # potential energy
        t += dt

def getNewSpeed(ballVelocity, ballMass, bulletVelocity, bulletMass):
    newMomentum = calculate2DMomentum(ballVelocity, ballMass, bulletVelocity, bulletMass)
    totalMass = ballMass + bulletMass
    return (newMomentum/totalMass)

def calculate2DMomentum(ballVelocity, ballMass, bulletVelocity, bulletMass):
    momentumX = calculate1DMomentum(ballVelocity.x, ballMass, bulletVelocity.x, bulletMass)
    momentumZ = calculate1DMomentum(ballVelocity.z, ballMass, bulletVelocity.x, bulletMass)
    return (sqrt(momentumX ** 2 + momentumZ ** 2))
    
    
def calculate1DMomentum(ballSpeed, ballMass, bulletSpeed, bulletMass):
    return(ballSpeed*ballMass + bulletSpeed*bulletMass)
