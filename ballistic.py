Web VPython 3.2
L = 4
g = 9.81

scene.userspin = True

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


sleep(2)
t=0
while True:
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


