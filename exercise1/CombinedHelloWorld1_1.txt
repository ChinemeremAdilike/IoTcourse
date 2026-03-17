int n = 0;
void setup() {
  Serial.begin(115200);
}

void loop() {
  Serial.print("Hello from Chinemerem! ");
  Serial.println(n);
  n=n+1;
  delay(1000);  
  if (n==10) n =0;
}