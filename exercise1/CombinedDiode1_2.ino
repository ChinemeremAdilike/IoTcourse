// ========= ALL OF TASK 2 DIODE ARE INCLUDED IN THIS CODE =========
// 2 = delay() blink, 3 = millis() blink, 4 = millis() + Serial printing
#define TASK_MODE 4
// ===========================================

// === Hardware setup ===
// ESP32: GPIO 4 -> resistor -> LED anode (A), LED cathode (C) -> GND
const int LED_PIN = 4;

// Blink timings (same for all tasks)
const unsigned long ON_MS  = 500;   // 0.5 s ON
const unsigned long OFF_MS = 2000;  // 2 s OFF

// State for the non-blocking (millis) tasks
unsigned long ledTimer   = 0;
unsigned long printTimer = 0;
bool ledState = LOW;

// ---------- Task 2: Blocking version (delay) ----------
void runTask2_DelayBlink() {
  digitalWrite(LED_PIN, HIGH);  // LED ON
  delay(ON_MS);                 // 0.5 s
  digitalWrite(LED_PIN, LOW);   // LED OFF
  delay(OFF_MS);                // 2 s
}

// ---------- Task 3: Non-blocking blink with millis ----------
void runTask3_MillisBlink() {
  unsigned long now = millis();

  if (ledState == HIGH && (now - ledTimer >= ON_MS)) {
    ledState = LOW;
    ledTimer = now;
    digitalWrite(LED_PIN, ledState);
  } else if (ledState == LOW && (now - ledTimer >= OFF_MS)) {
    ledState = HIGH;
    ledTimer = now;
    digitalWrite(LED_PIN, ledState);
  }
}

// ---------- Task 4: Non-blocking blink + elapsed seconds ----------
void runTask4_MillisBlinkAndPrint() {
  unsigned long now = millis();

  // LED state machine (same as Task 3)
  if (ledState == HIGH && (now - ledTimer >= ON_MS)) {
    ledState = LOW;
    ledTimer = now;
    digitalWrite(LED_PIN, ledState);
  } else if (ledState == LOW && (now - ledTimer >= OFF_MS)) {
    ledState = HIGH;
    ledTimer = now;
    digitalWrite(LED_PIN, ledState);
  }

  // Print elapsed seconds once per second (non-blocking)
  if (now - printTimer >= 1000) {
    printTimer = now;
    Serial.print("Running for: ");
    Serial.print(now / 1000);
    Serial.println(" s");
  }
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, ledState);

#if (TASK_MODE == 4)
  Serial.begin(115200);              // Only required for Task 4
  Serial.println("Task 4: Non-blocking blink + elapsed seconds");
#elif (TASK_MODE == 3)
  // Optional: uncomment if you want a banner in Task 3
  // Serial.begin(115200);
  // Serial.println("Task 3: Non-blocking blink");
#elif (TASK_MODE == 2)
  // Task 2 uses only pinMode(), digitalWrite(), delay()
#endif
}

void loop() {
#if (TASK_MODE == 4)
  runTask4_MillisBlinkAndPrint();
#elif (TASK_MODE == 3)
  runTask3_MillisBlink();
#elif (TASK_MODE == 2)
  runTask2_DelayBlink();
#else
  // Fallback: Task 2 behavior
  runTask2_DelayBlink();
#endif
}