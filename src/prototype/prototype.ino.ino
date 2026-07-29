const int segA = 4;
const int segB = 5;
const int segC = 8;
const int segD = 7;
const int segE = 6;
const int segF = 3;
const int segG = 2;
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
  pinMode(ledGreen, OUTPUT);
  pinMode(ledYellow, OUTPUT);
  pinMode(ledRed, OUTPUT);
  allOff();
  Serial.begin(9600);
  Serial.println("READY");
}

void showDigit(int num) {
  if (num < 0 || num > 9) return;
  for (int i = 0; i < 7; i++) {
    digitalWrite(segPins[i], digits[num][i] ? LOW : HIGH); // common anode
  }
}

void allOff() {
  digitalWrite(ledGreen, LOW);
  digitalWrite(ledYellow, LOW);
  digitalWrite(ledRed, LOW);
}

void countdown(int seconds) {
  for (int i = seconds; i >= 0; i--) {
    showDigit(min(i, 9));
    delay(1000);
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