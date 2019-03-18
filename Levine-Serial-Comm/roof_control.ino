// roof_control.ino
// last modified: 20171223
// Roof control for the 31inch shed at Anderson Mesa.
// Commands:
//  OPEN[,N]  - open the roof for N seconds. (open also works)
//  CLOSE[,N] - close the roof for N seconds. (close also works)
//  STOP      - stop motion
//  H         - Print Help
//   If N is omitted from OPEN or CLOSE, it sets to the default value for
//   full open or close motion.

// sel@ell 2017feb14
// changed the delay(), which blocks, for a non-blocking
//  version using millis(), which would allow for polling an input
//  line to check for interrupts or state changes externally.

//----------------------------------------------------------------------
// Hardcoded Variables that you might want to change
int openOPin  =  8;  // Output pin for OPEN  - use pin 8
int closeOPin =  9;  // Output pin for CLOSE - use pin 9
int openIPin  =  2;  // Input pin for OPENED limit switch - pin 2
int closeIPin =  3;  // Input pin for CLOSED limit switch - pin 3

int deftim[2] = { 17, 17 }; // Default # of seconds for opening and closing
//----------------------------------------------------------------------


int dio_o;           // input digital I/O bit for OPENED limit
int dio_c;           // input digital I/O bit for CLOSED limit

int ci;              // ci == chkcmd return, 
int di, odi;         // di, odi == polldi return, and prior value
int scnt, oscnt;     // scnt == count of seconds of command execution, & prior

int op_line  = 0;          // Output line to push
int ipdat[2] = { 0, 0 };   // for constructing command and args (M,N)
                           // M == direction, N == # of seconds
// accepts two argument command in the format M,N\n
// M == line to pulse 0 == SET ALL LOW, 1  == OPEN, 2 == CLOSE
// N == length of blink in 0.01sec integer units (ie 100 == 1second)

int ibyte = 0;             // single input byte readback from serial line
int ipart = 0;             // index for command string parts 1 = cmd, 2 = arg

int i, j;                  // loop indices

unsigned long dly;         // # of milliseconds to hold the line high
unsigned long otim;        // old time
unsigned long ctim;        // current time

String istr;               // input string, for later conversion

//----------------------------------------------------------------------
// One time setup operations
//  Set the output and input DIO lines
//  Set up serial communications
void setup() {
  pinMode(openOPin,  OUTPUT);  // init digital pin for OPEN for output
  pinMode(closeOPin, OUTPUT);  // init digital pin for CLOSE for output

  pinMode(openIPin,  INPUT);   // init digital pin for OPENED limit input
  pinMode(closeIPin, INPUT);   // init digital pin for CLOSED limit input
// or maybe use INPUT_PULLUP if inverted input

  Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
  while (!Serial) {
    ;  // wait for the serial port to connect
  }
  Serial.println ("Roof Control - Serial Port Connected");
  helppg();
  Serial.print (" > ");
}

//----------------------------------------------------------------------
// Main loop
void loop() {
  // check digital input bits in case a limit switch has been hit
  di = polldi();
  odi = di;
//  Serial.print ("IBits = ");
//  Serial.println (di, BIN);

  // Prompt
  if ( j == 0 ) {
    Serial.print (" > ");
    j = 1;
  }

  // check for and retrieve data from serial input
  if (Serial.available() > 0) {
    ibyte = Serial.read();        // read a byte

    if (isAlpha(ibyte)) {         // Accept letters
      istr += char(ibyte);        // add new byte to an ALPHA string

    } else if (isDigit(ibyte)) {  // accept digits
      istr += ibyte - '0';        // subtract off the ascii value of zero

    } else if ( ibyte == ',' ) {  // ',' is the delim between cmd and arg
      if (istr == "OPEN"         || istr == "open"  || istr == "1") {
        ipdat[0] = 1;
      } else if (istr == "CLOSE" || istr == "close" || istr == "2") {
        ipdat[0] = 2;
      } else {                  // anything else gets translated to STOP
        ipdat[0] = 0;
      }
      istr = "";
      ipart = 1;
    } else if ( ibyte == '\n' ) { // newline is cmd end
      if (ipart == 0) {           // optional argument not given
        if (istr == "OPEN"         || istr == "open"  || istr == "1") {
          ipdat[0] = 1;
        } else if (istr == "CLOSE" || istr == "close" || istr == "2") {
          ipdat[0] = 2;
        } else if (istr == "H" || istr == "h" || istr == "help") {
          helppg();               // print help page
          ipdat[0] = 0;
        } else {                  // anything else gets translated to STOP
          ipdat[0] = 0;
        }
        if (ipdat[0] == 1) {
          ipdat[1] = deftim[0];
        } else if (ipdat[0] == 2) {
          ipdat[1] = deftim[1];
        }
      } else {                      // optional argument IS given
        ipdat[1] = istr.toInt();    // convert arg to integer
      }
      istr = "";
      ipart = 2;
    }

  // have a complete command, process it
  } else if ( ipart == 2 ) {      
    Serial.print ("\nReceived: " );
    Serial.print (ipdat[0]);
    Serial.print (", ");
    Serial.println (ipdat[1]);

    // ensure push time is within reasonable limits
    if ( ipdat[1] < 0 ) {
      Serial.println ("Time < 0, set to 0");
      ipdat[1] = 0;
    } else if ( ipdat[1] > 50 ) {
      Serial.println ("Time > 50, set to 50");
      ipdat[1]  = 50;
    }

    dly = 1000 * long(ipdat[1]);   // set line hold time in milliseconds
    
    if        (ipdat[0] == 0) {   // 0->Set all lines LOW
      Serial.println ("Set all outputs to LOW");
    } else if (ipdat[0] == 1) {   // 1->Send OPEN cmd for arg seconds
      Serial.print ("Open for ");
      Serial.print (dly);
      Serial.println (" milliseconds");
    } else if (ipdat[0] == 2) {   // 2-> Send CLOSE cmd for arg seconds
      Serial.print ("Close for ");
      Serial.print (dly);
      Serial.println (" milliseconds");
    } else {                      // anything but 0, 1, or 2 set all low
      Serial.println ("Invalid option - Set all outputs to LOW");
      ipdat[0] = 0;
    }
    
    if (ipdat[0] == 0) {          // Set bits low
      digitalWrite(openOPin, LOW);
      digitalWrite(closeOPin, LOW);
      Serial.println ("All bits set to LOW");
    } else if ( ((ipdat[0] == 1) || (ipdat[0] == 2)) 
                && (ipdat[1] > 0) ) {  // Push OPEN or CLOSE button

      if (ipdat[0] == 1) {
        Serial.print (" OPEN == ");
        op_line = openOPin;
      } else {
        Serial.print (" CLOSE == ");
        op_line = closeOPin;
      }

      Serial.print (ipdat[0]);
      Serial.print (" DIO out line = ");
      Serial.println (op_line);

      otim = millis(); // loop start time
      scnt  = 0;
      oscnt = 0;
      digitalWrite(op_line, HIGH);      // Push the button
      do {
        ctim = millis();
        // kludge for handling crossing the end of the day
        //  means there is a ~1minute window where it might run long
        if ( ctim < otim ) {
          otim = ctim;
        }
        delay (1);
        // Print # of seconds
        scnt = int((ctim - otim) / 1000);
        if ( scnt > oscnt ) {
          Serial.print (scnt);
          Serial.println (".. ");
          oscnt = scnt;
        }
        // Check the user interface for input to stop motion
        ci = chkcmd();
        if (ci > 0) {
          Serial.println ("STOPPING MOTION");
        }          
      } while ( (ctim - otim < dly) && (ci == 0) );
      digitalWrite(op_line, LOW);
      Serial.println (" Done");
    }
    
    ipart    = 0;
    ipdat[0] = 0;
    ipdat[1] = 0;
    op_line  = 0;
    j = 0;

  } else {
    delay (1000);
  }
}

// chkcmd - check the user command line
//          for use to check for anything to stop motion
// returns: 1 == got a character
//          0 == nothing was input
int chkcmd() {
  if (Serial.available() > 0) {
    ibyte = Serial.read();        // read a byte
    return ( 1 );
  }
  return ( 0 );
}

// polldi - poll the input dio lines
//  The OpenLimit  is 0x1
//  The CloseLimit is 0x2
//  Returns the logical OR of both limits
int polldi() {
  dio_o = digitalRead(openIPin);
  dio_c = digitalRead(closeIPin);
  return ( (dio_c * 2) | (dio_o) );
}

// helppg - cmnd summary
void helppg() {
  Serial.println ("Commands: OPEN[,N]  == Open the roof");
  Serial.println ("          CLOSE[,N] == Close the roof");
  Serial.println ("          H == print this help page");
  Serial.println ("           N is an optional number of seconds to");
  Serial.println ("           hold down the button for the motion.");
  Serial.println ("          Any entry during a motion will cause it");
  Serial.println ("          to stop, even just hitting <RETURN>.");
  Serial.println (" Version: 2017Dec23");
}
