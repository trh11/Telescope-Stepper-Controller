int stepPin = 13;                           //sets pin 13 as the stepper logic pin
int dirPin = 12;                            //sets pin 12 as the direction pin
int m1Pin = 11;                             //sets pin 11 as the M1 microstepping pin
int m0Pin = 10;                             //sets pin 10 as the M0 microstepping pin
int count = 0;
int qrt = 0;

void setup()
{  
 Serial.begin(9600);                        //begins serial conection to computer over USB
 pinMode(stepPin, OUTPUT);                  //sets the stepper logic pin STEP as an output
 pinMode(dirPin, OUTPUT);                   //sets the direction pin DIR as an output
 pinMode(m1Pin, OUTPUT);                    //sets the M1 microstepping pin as an output
 pinMode(m0Pin, OUTPUT);                    //sets the M0 microstepping pin an output
}

void loop()
  { 
  while (Serial.available() > 0) {          //looks for a serial signal from USB
    int set = Serial.parseInt();            //selects the first byte for direction and microstepping (dir, m1, m0)
    int steps = Serial.parseInt();          //selects the second byte for number of steps
    int freq = Serial.parseInt();           //selects the third byte for the frequency of stepper logic
    constrain(freq, 1, 10000);              //prevents a divide by zer0 situation for frequency
    int halt = bitRead(set, 7);             //reads bit7 for the HALT bit from set
    int slew = bitRead(set, 6);
    int dir = bitRead(set, 2);              //reads bit2 for DIR
    int m1 = bitRead(set, 1);               //reads bit1 for M1
    int m0 = bitRead(set, 0);               //reads bit0 for M0
    if (slew == 1)
    {
      int max = 1;
      for (int n = 0; n <= max-1; n++)
      {
        max++;
        if (Serial.available() > 0)
        {
          int check = Serial.read();
          if (check == 32)
            break;
        }
        digitalWrite(stepPin, HIGH);          //writes STEPS logic high 
        delay(500/freq);                      //holds high for one half period = (1 second)/(2 freq)
        digitalWrite(stepPin, LOW);           //writes STEPS logic low
        delay(500/freq);                      //holds low for one half period = (1 second)/(2 freq) 
      }
    }
    if (halt == 1)                          //if the HALT flag is up prevents stop button misuse
    {
      Serial.print(0);
      Serial.flush();                       //flushes the serial buffer.  
      delay(10);                            //delays 1.5 seconds to prevent serial confusion from rapid button presses
      break;                                //resumes looking for a SEND signal
    }
    if (Serial.available() > 0)             //if any activity     
      {
        int check = Serial.read();          //looks for any button presses after parsing signal
        if (check >= 127)                   //if halt flag is up 
        {
          Serial.write(0);
          Serial.flush();                   //flushes the serial buffer. 
          delay(1500);                      //delays 1.5 seconds to prevent serial confusion from rapid button presses         
          break;                            //resumes looking for a SEND signal
        }
        if (check = 64)
        {
          Serial.print(count);
          Serial.flush();
          delay(10);
          break;  
        }
      }
    if (dir == 1)                           //if set = x1xx
    {
      digitalWrite(dirPin, HIGH);           //writes DIR high (cw)
    }
    else                                    //if set = x0xx
    {
      digitalWrite(dirPin,LOW);             //writes DIR low (cw)
    }
    if (m1 == 1)                            //if set = xx1x
    {
      digitalWrite(m1Pin, HIGH);            //writes M1 high
    }
    else                                    //if set = xx0x
    {
      digitalWrite(m1Pin,LOW);              //writes M1 low
    }
    if (m0 == 1)                            //if set = xxx1
    {
      digitalWrite(m0Pin, HIGH);            //writes M0 high
    }
    else                                    //if set = xxx0
    {
      digitalWrite(m0Pin,LOW);              //writes M0 low
    }
    for (int n = 0; n <= steps-1; n++)     //initiates loop for "steps" number of periods
    {
      if (Serial.available() > 0)           //if any activity     
      {
        int check = Serial.read();
        if (check >= 127)    
        {
          Serial.print(n); 
          delay(2000);                       //delays .1 seconds to prevent serial confusion from rapid button presses          
          //Serial.flush();
          break;                            //resumes looking for a SEND signal
        }
        else
        {
        Serial.flush();
        }
      }
      digitalWrite(stepPin, HIGH);          //writes STEPS logic high 
      delay(500/freq);                      //holds high for one half period = (1 second)/ (2 freq)
      digitalWrite(stepPin, LOW);           //writes STEPS logic low
      delay(500/freq);                      //holds low for one half period = (1 second)/ (2 freq) 
      if (n == steps-1)
      {
        Serial.flush();
        delay(100);
        Serial.print(n + 1);
      }
    }
  }
}
