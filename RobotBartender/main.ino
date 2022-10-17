// constants won't change
const int RELAY_PIN = 2;  // the Arduino pin, which connects to the IN pin of relay
int n = 0;
// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin A5 as an output.
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  pinMode(RELAY_PIN, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(RELAY_PIN, HIGH); // turn on pump 5 seconds
  delay(5000);
  digitalWrite(RELAY_PIN, LOW);  // turn off pump 5 seconds
  delay(5000);
  int n = n+1;
  Serial.print(n);
}