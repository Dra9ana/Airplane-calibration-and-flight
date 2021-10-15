const int touchPin = 2;
int touchVal = 0;

const int redPin = 3;
int redValue = 0;

const int greenPin = 11;
int greenValue = 0;

int ledVal = 0;
int ledPin = 0;

const int numCLK = 9;
const int numDIO = 8;

//ukljucene su biblioteke
#include <TM1637Display.h>
TM1637Display display(numCLK, numDIO);

#include <TimerOne.h>
//const int VCCPin = ;
const int xPin   = A0;
const int yPin   = A1;
const int zPin   = A2;
//const int GNDPin = A4;
int ax = 0;
int ax_ = 0;
int ay = 0;
int ay_ = 0;
int az = 0;
int az_ = 0;

double vx=0;
double vy=0;
double vz=0;
double v=0;

double axx=0;
double ayy=0;
double azz=0;

double roll = 0;
double pitch = 0;

const double gravity = 9.81;
double kx = 1;
double nx = 0;
double ky = 0;
double ny = 0;
double kz = 0;
double nz = 0;

bool pom1=true;
char karak=' ';


bool stopGraphing = false;
int counter = 0;
char inChar=' ';
int state = 0;
void setup() {

  Serial.begin(9600);

  display.setBrightness(7);

  Timer1.initialize(100000);
  Timer1.attachInterrupt(timerIsr);

  pinMode(touchPin, INPUT);
  pinMode(redPin, OUTPUT);   //iskljuci se crvena dioda
  pinMode(greenPin, OUTPUT); //iskljuci se zelena dioda

  attachInterrupt(digitalPinToInterrupt(touchPin), displayVoltage,RISING);

}

void loop() {



    //deo za kalibraciju
    if (inChar == 'x' ){
        //racuna k i n za x osu i to posle salje pajtonu da upise u tekstualnu datoteku
         v=vx;
         if (state == 1 && counter == 0 ){

         ax = scaleVoltage(vx); //traje 5s
         state = 0;
         counter=1;
         }
         if (state==1 && counter==1){
         ax_ = scaleVoltage(vx); //traje 5s
         state = 0;
         counter=0;
         inChar = ' ';

         kx = readK(ax,ax_); //racuna k za x osu
         nx = readN(ax,kx);  //racuna n za x osu
         Serial.println(kx); //salje k za x osu
         Serial.println(nx); //salje nz a x osu
         }
        }

       if (inChar == 'y'){
        //racuna k i n za y osu i to posle salje pajtonu da upise u tekstualnu datoteku
        v=vy;

        if (state == 1 && counter == 0 ){
        ay = scaleVoltage(vy); //traje 5s
        state = 0;
        counter=1;
        }
        if (state==1 && counter==1){
        ay_ = scaleVoltage(vy);
        state = 0;
        counter=0;
        inChar = ' ';

        ky = readK(ay,ay_); //racuna k za y osu
        ny = readN(ay,ky);  //racuna n za y osu
        Serial.println(ky); //salje k za y osu
        Serial.println(ny); //salje n za y osu
        }
        }

       if (inChar == 'z'){
        //racuna k i n za z osu i to posle salje pajtonu da upise u tekstualnu datoteku
        v=vz;

        if (state==1 && counter == 0 ){
        az = scaleVoltage(vz);
        state = 0;
        counter=1;
        touchVal=0;

        }
        if (state==1 && counter==1){
        az_ = scaleVoltage(vz);
        state = 0;
        counter=0;
        inChar = ' ';

        kz = readK(az,az_); //racuna k za z osu
        nz = readN(az,kz);  //racuna n za z osu
        Serial.println(kz); //salje k za z osu
        Serial.println(nz); //salje n za z osu
        }

  }


  if(inChar == 'L'){

      // deo za letenje

                axx=scaleVoltage(vx)*kx+nx;  //racuna ubrzanje po x osi
                ayy=scaleVoltage(vy)*ky+ny;  //racuna ubrzanje po y osi
                azz=scaleVoltage(vz)*kz+nz;  //racuna ubrzanje po z osi

                Serial.println(axx);
                Serial.println(ayy);
                Serial.println(azz);

                roll = getRoll(axx,ayy,azz);  //racuna se ugao skretanja
                pitch = getPitch(axx,ayy,azz); //racuna se ugao propinjanja
                display.showNumberDec((int)pitch);

                if(pitch<0){
                  //za negativan ugao svetli zelena dioda
                  digitalWrite(greenPin, LOW);
                  brighterLight(pitch,redPin);
                  }
                else{
                  //za pozitivan ugao svetli crvena dioda
                  digitalWrite(redPin, LOW);
                  brighterLight(pitch,greenPin);
                  }


  }


  if(inChar != '.' ){

                  digitalWrite(greenPin, LOW);
                  digitalWrite(redPin, LOW);
                  display.showNumberDec(0);
  }





}

void serialEvent(){


    if(pom1==true){

  inChar=(char)Serial.read();
  pom1=!pom1;
    }
   else{
    karak=(char)Serial.read();
    pom1=!pom1;
   }
  }

void timerIsr(){

    vx=analogRead(A0);
    vy=analogRead(A1);
    vz=analogRead(A2);

  }

void brighterLight(int angle,int ledPin){

  //povecanjem ugla dioda svetli jace

  int sensorValue = abs(angle);
  float scaled = ((float)sensorValue / 90.0)  * 255.0; // skalira od 0 - 255 vrednost

  digitalWrite(ledPin, scaled ); // pojacava jacinu svetljenja diode

  }


void displayVoltage(){

    // ispisuje napon na dispeju
    int d=int( 5000* v/1023);

     display.showNumberDec(d);
     state=1;

    }

int scaleVoltage(double v){
    //skalira napon u milivolte
      return(v*5000/1023);
      }
double readK(double U, double U_){
  //na osnovu jednacina racuna vrednost k
  return(2*gravity/(U-U_));
  }
double readN(double U, double k){
  //na osnovu jednacina racuna vrednost n
  return(gravity - k*U);
}
double getRoll(int ax, int ay, int az){
  //racuna ugao skretanja
  return(atan2(ay,(sqrt(0.0+ax*ax + az*az)))*180/3.14);
}

double getPitch(int ax, int ay, int az){
  //racuna ugao propinjanja
  double angle = atan2(ax,(sqrt(0.0+ay*ay + az*az)))*180/3.14; //pretvara ugao u stepen
  return( angle );
}
