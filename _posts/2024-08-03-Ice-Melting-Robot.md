---
title: Ice Melting Robot
description: Group project where we built a robot that can detect, approach, collect, and melt ice to store in an underside container
date: 2024-08-03 09:33:00 +0800
pin: false
---

## Robot Code

```cpp
#include <AFMotor.h>
#include <Servo.h>
AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);
Servo servo1;
Servo servo2;
Servo servo3;
int top_servo_pos;
int side_servo_pos1;
int side_servo_pos2;
int trig1 = A3;
int echo1 = A5;
int trig2 = A2;
int echo2 = A1;
int temp = A0;
int center = 90; // the position of the top servo motor such that it is facing directly forwards atop the robot
int initial_position = 1;
float top_distance1;
float top_distance2;
float inside_distance;
float time1;
float time2;
float change;
bool rotation = true;
bool thermometer = false;
bool cold = false;
bool heater = false;

void setup()
{
  motor1.setSpeed(70); // set initial speed of the motor & stop
  motor1.run(RELEASE);
  motor2.setSpeed(70); // set initial speed of the motor & stop
  motor2.run(RELEASE);
  motor3.setSpeed(70); // set initial speed of the motor & stop
  motor3.run(RELEASE);
  motor4.setSpeed(70); // set initial speed of the motor & stop
  motor4.run(RELEASE);
  servo1.attach(10);
  servo2.attach(9);
  servo3.attach(2);
  pinMode(A0, INPUT); // input for temperature sensor
  pinMode(A4, OUTPUT); // output for heating elements
  pinMode(trig1, OUTPUT);
  pinMode(echo1, INPUT);
  pinMode(trig2, OUTPUT);
  pinMode(echo2, INPUT);
  Serial.begin(9600);
}

void loop()
{
  if (rotation && initial_position > 0) // initially fix the side servo motors at their starting position
  {
    servo1.write(20);
    initial_position -= 1;
  }

  if (rotation) // continuously rotate top servo motor with top distance sensor
  {
    motor1.run(FORWARD); // turn on motor
    motor2.run(FORWARD); // turn on motor
    motor3.run(FORWARD); // turn on motor
    motor4.run(FORWARD); // turn on motor
    for (top_servo_pos = center; top_servo_pos >= center-30; top_servo_pos -= 1) // sweeps position of top servo motor from centered to left 30 degrees
    {
      servo3.write(top_servo_pos);

      digitalWrite(trig1, LOW); // gather distance readings of top distance sensor while top servo rotates side to side
      delayMicroseconds(2);
      digitalWrite(trig1, HIGH);
      delayMicroseconds(10);
      digitalWrite(trig1, LOW);
      
      time1 = pulseIn(echo1, HIGH);
      top_distance1 = time1/148.1;

      digitalWrite(trig1, LOW);
      delayMicroseconds(2);
      digitalWrite(trig1, HIGH);
      delayMicroseconds(10);
      digitalWrite(trig1, LOW);
      
      time1 = pulseIn(echo1, HIGH);
      top_distance2 = time1/148.1;
      Serial.println(change);
      
      change = abs(top_distance2 - top_distance1); // determine the change in distance reading
    }
    for (top_servo_pos = center-30; top_servo_pos <= center+30; top_servo_pos += 1) // sweeps position of top servo motor from left 30 degrees to right 30 degrees
    {
      servo3.write(top_servo_pos);

      digitalWrite(trig1, LOW); // gather distance readings of top distance sensor while top servo rotates side to side
      delayMicroseconds(2);
      digitalWrite(trig1, HIGH);
      delayMicroseconds(10);
      digitalWrite(trig1, LOW);
      
      time1 = pulseIn(echo1, HIGH);
      top_distance1 = time1/148.1;

      digitalWrite(trig1, LOW);
      delayMicroseconds(2);
      digitalWrite(trig1, HIGH);
      delayMicroseconds(10);
      digitalWrite(trig1, LOW);
      
      time1 = pulseIn(echo1, HIGH);
      top_distance2 = time1/148.1;
      
      change = abs(top_distance2 - top_distance1); // determine the change in distance reading
      Serial.println(change);
    }
    for (top_servo_pos = center+30; top_servo_pos >= center; top_servo_pos -= 1) // sweeps position of top servo motor from right 30 degrees to centered
    {
      servo3.write(top_servo_pos);

      digitalWrite(trig1, LOW); // gather distance readings of top distance sensor while top servo rotates side to side
      delayMicroseconds(2);
      digitalWrite(trig1, HIGH);
      delayMicroseconds(10);
      digitalWrite(trig1, LOW);
      
      time1 = pulseIn(echo1, HIGH);
      top_distance1 = time1/148.1;

      digitalWrite(trig1, LOW);
      delayMicroseconds(2);
      digitalWrite(trig1, HIGH);
      delayMicroseconds(10);
      digitalWrite(trig1, LOW);
      
      time1 = pulseIn(echo1, HIGH);
      top_distance2 = time1/148.1;
      
      change = abs(top_distance2 - top_distance1); // determine the change in distance reading
      Serial.println(change);
    }
  }

  if (change > .5) // detect the presence of an object; if change in distance reading surpasses .5 inches, an object is in the path
  {
    Serial.println("DETECTED!");
    motor1.run(RELEASE); // turn off motor
    motor2.run(RELEASE); // turn off motor
    motor3.run(RELEASE); // turn off motor
    motor4.run(RELEASE); // turn off motor
    for (side_servo_pos1 = 20; side_servo_pos1 <= 180; side_servo_pos1 += 1) // sweeps position of side servo motors from 20 to 180 degrees, closing the hadith
    {
      servo1.write(side_servo_pos1);
      servo2.write(180-side_servo_pos1);
      delay(25);
    }
  }
  
  if (thermometer)
  {
    int reading = analogRead(temp);
    
    float voltage = reading * 5.0; // convert reading to voltage
    voltage /= 1024.0;

    float temperatureC = (voltage - 0.5) * 100 ;
    Serial.print(temperatureC);
    Serial.print("\xC2\xB0"); // degree symbol
    Serial.println(" C"); // converts to Celsius

    float temperatureF = (temperatureC * 9.0 / 5.0) + 32.0;
    Serial.print(temperatureF);
    Serial.print("\xC2\xB0"); // degree symbol
    Serial.println(" F"); // converts to Fahrenheit

    if (temperatureF < 72) // detect if temperature of robot interior reaches below room temperature
    {
      cold = true;
    }
    
    delay(500); // wait a half-second
  }
  
  if (cold) // initiate heating if ice is in the robot interior
  {
    heater = true;
  }

  if (heater)
  {
    digitalWrite(A4, HIGH); // start the heating elements

    digitalWrite(trig2, LOW); // gather distance reading for inside distance sensor
    delayMicroseconds(2);
    digitalWrite(trig2, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig2, LOW);
    
    time2 = pulseIn(echo2, HIGH);
    inside_distance = time2/148.1;

    if (inside_distance >= 7) // if the ice has completely melted inside the robot and entered into the bottom container, the distance reading will be >= the distance to the hatch
    {
      heater = false; // turn off the heaters once the ice has completely melted
    }
  }
}
```
{: file='Ice_Melting_Robot.ino'}
<div style="text-align: center; font-size: smaller; color: #555;">
C++ code in Arduino IDE, incorporates object detection and semi-autonomous movement
</div>

## Circuit Diagram

![Desktop View](/assets/img/MeltingRobot/CircuitDiagram.png){: width="972" height="589" }
_Circuit diagram of all wiring, integrating Arduino Uno, ultrasonic distance sensors, servo motors, DC motors, and wheels_

## Robot Photos

![Desktop View](/assets/img/MeltingRobot/IceMeltingRobot1.jpg){: width="972" height="589" }
_All wiring to the Arduino UNO mounted on the top of the robot chassis_

![Desktop View](/assets/img/MeltingRobot/IceMeltingRobot2.jpg){: width="972" height="589" }
_Front side of the robot with the scooping bucket_

![Desktop View](/assets/img/MeltingRobot/IceMeltingRobot3.jpg){: width="972" height="589" }
_Interior of the robot chassis with the heating elements mounted on the side_

## Robot Demo

{% include embed/youtube.html id='RLdY105ML2s' %}
_Test video of robot successfully locating and loading object_
