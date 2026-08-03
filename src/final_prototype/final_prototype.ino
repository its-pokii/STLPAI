const int segA = 4;
const int segB = 8;
const int segC = 2;
const int segD = 3;
const int segE = 6;
const int segF = 5;
const int segG = 7;

// NEW: digit-select pins for a 4-digit display (one per digit, left to right)
// Adjust these to whatever pins you wired the digit commons to.
const int digit1 = A0; // leftmost  (thousands)
const int digit2 = A1; //           (hundreds)
const int digit3 = A2; //           (tens)
const int digit4 = A3; // rightmost (units)
const int digitPins[4] = {digit1, digit2, digit3, digit4};

const int ledGreen  = 11;
const int ledYellow = 10;
const int ledRed    = 9;

const int YELLOW_TIME = 3; // fixed, always follows green

const int segPins[7] = {segA, segB, segC, segD, segE, segF, segG};

// 1 = segment SHOULD BE ON (logical, inverted below for common anode)
const bool digits[10][7] = {
  {1,1,1,1,1,1,0}, // 0
  {0,1,1,0,0,0,0}, // 1
  {1,1,0,1,1,0,1}, // 2
  {1,1,1,1,0,0,1}, // 3
  {0,1,1,0,0,1,1}, // 4
  {1,0,1,1,0,1,1}, // 5
  {1,0,1,1,1,1,1}, // 6
  {1,1,1,0,0,0,0}, // 7
  {1,1,1,1,1,1,1}, // 8
  {1,1,1,1,0,1,1}  // 9
};

void setup() {
  for (int i = 0; i < 7; i++) pinMode(segPins[i], OUTPUT);
  for (int i = 0; i < 4; i++) pinMode(digitPins[i], OUTPUT);

  pinMode(ledGreen, OUTPUT);
  pinMode(ledYellow, OUTPUT);
  pinMode(ledRed, OUTPUT);

  disableAllDigits();
  allOff();
  Serial.begin(9600);
  Serial.println("READY");
}

// Turn off every digit's common pin.
// NOTE: assumes digit pin HIGH = that digit enabled (common anode via
// transistor driven active-high). If your digits are inverted, swap
// HIGH/LOW here.
void disableAllDigits() {
  for (int i = 0; i < 4; i++) digitalWrite(digitPins[i], LOW);
}

// Write segment pattern for a single digit value (0-9), or blank if value < 0.
void setSegments(int value) {
  if (value < 0 || value > 9) {
    for (int i = 0; i < 7; i++) digitalWrite(segPins[i], HIGH); // all off (common anode)
    return;
  }
  for (int i = 0; i < 7; i++) {
    digitalWrite(segPins[i], digits[value][i] ? LOW : HIGH); // common anode
  }
}

// Light ONE digit position briefly (call rapidly in a loop to multiplex).
void showDigitAt(int position, int value) {
  disableAllDigits();
  setSegments(value);
  digitalWrite(digitPins[position], HIGH); // enable this digit
  delayMicroseconds(1500);                 // brief on-time, then move to next digit
}

// Splits num into up to 4 digits (thousands/hundreds/tens/units),
// blanking unused leading digits (no leading zeros), and multiplexes
// the whole display for approximately duration_ms milliseconds.
void showNumberFor(int num, unsigned long duration_ms) {
  if (num < 0) num = 0;
  if (num > 9999) num = 9999;

  int d[4];
  d[0] = num / 1000;
  d[1] = (num / 100) % 10;
  d[2] = (num / 10) % 10;
  d[3] = num % 10;

  // Blank leading zero digits (but keep at least the units digit).
  bool leading = true;
  for (int i = 0; i < 3; i++) {
    if (leading && d[i] == 0) {
      d[i] = -1; // blank
    } else {
      leading = false;
    }
  }

  unsigned long start = millis();
  while (millis() - start < duration_ms) {
    for (int i = 0; i < 4; i++) {
      showDigitAt(i, d[i]);
    }
  }
  disableAllDigits();
}

void allOff() {
  digitalWrite(ledGreen, LOW);
  digitalWrite(ledYellow, LOW);
  digitalWrite(ledRed, LOW);
}

void countdown(int seconds) {
  for (int i = seconds; i >= 0; i--) {
    showNumberFor(i, 1000); // multiplex the full 4-digit number for ~1 second
  }
}

void runGreen(int seconds) {
  allOff();
  digitalWrite(ledGreen, HIGH);
  countdown(seconds);

  allOff();
  digitalWrite(ledYellow, HIGH);
  countdown(YELLOW_TIME);

  allOff();
  Serial.println("DONE");
}

void runRed(int seconds) {
  allOff();
  digitalWrite(ledRed, HIGH);
  countdown(seconds);

  allOff();
  Serial.println("DONE");
}

void loop() {
  if (Serial.available() > 0) {
    String line = Serial.readStringUntil('\n');
    line.trim();

    if (line.startsWith("G")) {
      int seconds = line.substring(1).toInt();
      runGreen(seconds);
    }
    else if (line.startsWith("R")) {
      int seconds = line.substring(1).toInt();
      runRed(seconds);
    }
  }
}