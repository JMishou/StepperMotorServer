import RPi.GPIO as GPIO 	#import the gpio library
import time			#import the time library

GPIO.setmode(GPIO.BCM)		#sets the gpio to match the BCM number and not the physical pin number on the pin header
 
enable_pin = 18		#GPIO 18 is connected to 1,2 EN and 3,4 EN of the L293D chip physical pins 1 and 9
coil_A_1_pin = 4	#GPIO 4 is connected to 1A pin of the L293D chip physical pin 2
coil_A_2_pin = 17	#GPIO 17 is connected to 2A pin of the L293D chip physical pin 7
coil_B_1_pin = 23	#GPIO 23 is connected to 3A pin of the L293D chip physical pin 10
coil_B_2_pin = 24	#GPIO 24 is connected to 4A pin of the L293D chip physical pin 15
 
#Configure the gpio pins as outputs
GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

# The next two functions are the step sequencs.  They each take a delay and number of cycles.  
# Each cycle has 4 steps.  We are using the two coil method of driving a stepper motor.
# To learn how stepper motors work you may want to watch this video https://www.youtube.com/watch?v=bngx2dKl5jU

def forward(delay, cycles):  
  for i in range(0, cycles):  #loop through the number of cycles
    setStep(1, 0, 1, 0)       #Step #1 turn on coil A forward and B forward
    time.sleep(delay)         #delay before turning on the next step in the sequence.
    setStep(0, 1, 1, 0)       #Step #2 turn on coil A reverse and B forward
    time.sleep(delay)         #delay before turning on the next step in the sequence.
    setStep(0, 1, 0, 1)       #Step #2 turn on coil A reverse and B reverse
    time.sleep(delay)         #delay before turning on the next step in the sequence.
    setStep(1, 0, 0, 1)       #Step #2 turn on coil A forward and B reverse
    time.sleep(delay)
 
def backwards(delay, cycles):  
  for i in range(0, cycles):
    setStep(1, 0, 0, 1)
    time.sleep(delay)
    setStep(0, 1, 0, 1)
    time.sleep(delay)
    setStep(0, 1, 1, 0)
    time.sleep(delay)
    setStep(1, 0, 1, 0)
    time.sleep(delay)
  
def setStep(w1, w2, w3, w4):      #Function to turn on the corresponding gpio pins
  GPIO.output(coil_A_1_pin, w1)   #Set the outputs accordingly
  GPIO.output(coil_A_2_pin, w2)   #.
  GPIO.output(coil_B_1_pin, w3)   #.
  GPIO.output(coil_B_2_pin, w4)   #.
 
def stepperGo(direction, delay, cycles):  #Function to initate the stepper motor in motion
  GPIO.output(enable_pin, 1)  #Bring the enable pin high to turn on the L293D motor driver chip

  #Direction is handled as a boolean value 1 is forward 0 is reverse
  if direction:
    forward(delay,cycles)  #if forward turn the motor forwards
  else:
    backwards(delay,cycles)#if backwards turn the motor forwards

  setStep(0,0,0,0)  # when the motor is finished turn off all coils.

  GPIO.output(enable_pin, 0) #turn off the L293D chip


#Main code loop
while True:  #Infinite loop

    rpm = abs(int(raw_input("Speed (0-160 RPM)?")))  #Get RPM from user
    if rpm > 160:  #Max rpm is 160 if user input greater than 160 set it to 160 and display message.
       print ("Max 160 RPM... speed changed to 160 RPM")
       rpm = 160
    #delay = sec / step = 1 revolution / 200 steps * 60 sec / 1 minute * 1 minute / (RPM) revolutions
    #delay = 0.3 / RPM
    delay = 0.3 / RPM

    # get the # of revolutions from the user
    revolutions = abs(float(raw_input("how many revolutions?"))) 

    # there are 200 steps per revolution
    # each cycle is 4 steps => 50 cycles / revolution
    cycles = int(revolutions * 50) 

    #get the direction from the user
    direction = int(raw_input("Forward (1) or Backwards (0)? "))

    #since the user input for direction is 1 or 0 we need create a string
    #to add to the output.  If direction = 1 then dirstr = forward 
    #otherwise dirstr = backwards
    dirstr=""
    if direction:
      dirstr = "forward"
    else:
      dirstr = "backwards"

    #out put a message that states what the motor is doing.
    print ("{0} @ {1} RPM for {2} cycles".format(dirstr, rpm,cycles))

    #run the motor
    stepperGo(direction,delay,cycles)
    
    #repeat the loop


 
