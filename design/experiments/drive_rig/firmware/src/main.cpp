// USB-only B-G431B-ESC1 diagnostic. Disconnect battery AND motor leads.
// This program has no motor-drive commands, PWM, alignment or FOC code.
#include <Arduino.h>
#include <Wire.h>

#if !defined(ARDUINO_B_G431B_ESC1) || !defined(A_PHASE_UL)
#error "Build only for disco_b_g431b_esc1 with its board-specific pin map."
#endif

namespace {
constexpr uint32_t gateInputs[] = {
    A_PHASE_UH, A_PHASE_UL, A_PHASE_VH,
    A_PHASE_VL, A_PHASE_WH, A_PHASE_WL,
};
constexpr uint8_t sensorAddress = 0x36;
constexpr uint8_t statusRegister = 0x0B;
constexpr uint8_t rawAngleRegister = 0x0C;
constexpr uint32_t reportPeriodMs = 100;
uint32_t lastReportMs = 0;
char boardId[25] = {};

void holdGateInputsLow() {
  for (const auto pin : gateInputs) {
    digitalWrite(pin, LOW);
  }
}

bool readRegisters(uint8_t firstRegister, uint8_t *bytes, size_t count) {
  Wire.beginTransmission(sensorAddress);
  Wire.write(firstRegister); // Register pointer only; no sensor settings written.
  if (Wire.endTransmission(false) != 0) {
    return false;
  }
  if (Wire.requestFrom(sensorAddress, count, true) != count) {
    while (Wire.available()) {
      Wire.read();
    }
    return false;
  }
  for (size_t i = 0; i < count; ++i) {
    bytes[i] = static_cast<uint8_t>(Wire.read());
  }
  return true;
}

void report() {
  uint8_t status = 0;
  uint8_t angleBytes[2] = {};
  const bool i2cOk = readRegisters(statusRegister, &status, 1) &&
                    readRegisters(rawAngleRegister, angleBytes, 2);
  const bool detected = (status & 0x20) != 0;
  const bool weak = (status & 0x10) != 0;
  const bool strong = (status & 0x08) != 0;
  const bool fieldOk = i2cOk && detected && !weak && !strong;
  const uint16_t raw = ((uint16_t(angleBytes[0]) << 8) | angleBytes[1]) & 0x0FFF;

  Serial.print("{\"firmware\":\"tidybot-usb-diag-0.1\",\"board_id\":\"");
  Serial.print(boardId);
  Serial.print("\",\"uptime_ms\":");
  Serial.print(millis());
  Serial.print(",\"motor_drive\":false,\"i2c_ok\":");
  Serial.print(i2cOk ? "true" : "false");
  Serial.print(",\"field_ok\":");
  Serial.print(fieldOk ? "true" : "false");
  Serial.print(",\"magnet_detected\":");
  Serial.print(i2cOk ? (detected ? "true" : "false") : "null");
  Serial.print(",\"field_weak\":");
  Serial.print(i2cOk ? (weak ? "true" : "false") : "null");
  Serial.print(",\"field_strong\":");
  Serial.print(i2cOk ? (strong ? "true" : "false") : "null");
  Serial.print(",\"raw_angle\":");
  if (i2cOk) {
    Serial.print(raw);
  } else {
    Serial.print("null");
  }
  Serial.println("}");
}
} // namespace

void setup() {
  // Both L6387 inputs low commands each half-bridge off (L6387E datasheet).
  // USB-only operation and disconnected motor leads are still required:
  // this application cannot control reset, bootloader or pre-flash firmware.
  holdGateInputsLow();
  for (const auto pin : gateInputs) {
    pinMode(pin, OUTPUT);
  }
  holdGateInputsLow();
  snprintf(boardId, sizeof(boardId), "%08lX%08lX%08lX",
           static_cast<unsigned long>(HAL_GetUIDw0()),
           static_cast<unsigned long>(HAL_GetUIDw1()),
           static_cast<unsigned long>(HAL_GetUIDw2()));
  Serial.begin(115200); // USART2 PB3/PB4 through the attached ST-LINK VCP.
  Wire.setSDA(PB7);
  Wire.setSCL(PB8);
  Wire.begin();
  Wire.setClock(100000);
}

void loop() {
  holdGateInputsLow();
  const uint32_t now = millis();
  if (uint32_t(now - lastReportMs) >= reportPeriodMs) {
    lastReportMs = now;
    report();
  }
  // Incoming serial bytes are deliberately not interpreted as commands.
  // Wire/USB delays may delay reports; this is not a motion-control watchdog.
}
