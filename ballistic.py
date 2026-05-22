Web VPython 3.2
L = 4
mBall= 0.25
theta = pi/4
g = 9.81
frameRate = 50000
dt = 1/frameRate
omega = 1
transitionY = 2

ball = sphere(pos=vector(L*cos(theta),transitionY-L*sin(theta),0), radius = 0.5, color = color.orange)
rod = cylinder(pos=vec(0, transitionY, 0), axis=vec(cos(theta), -sin(theta), 0), color=color.orange, radius = 0.05, length = L)
while True:
    rate(frameRate)
    alpha = g*cos(theta)/L
    omega += alpha*dt
    theta += omega*dt
    ball.pos.x = L*cos(theta)
    ball.pos.y = transitionY-L*sin(theta)
    rod.rotate(angle=omega, axis=vector(cos(theta), -sin(theta), 0))

def calculate2DMomentum(ballVelocity, ballMass, bulletVelocity, bulletMass):
    
def calculate1DMomentum(ballSpeed, ballMass, bulletSpeed, bulletMass):
    return(ballSpeed * ballMass + bulletSpeed + bulletMass)

