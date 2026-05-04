#include <DFRobot_RGBMatrix.h>
#define OE    9
#define LAT   10
#define CLK   11
#define A     A0
#define B     A1
#define C     A2
#define D     A3
#define E     A4
#define WIDTH 64
#define _HIGH 64
DFRobot_RGBMatrix matrix(A, B, C, D, E, CLK, LAT, OE, false, WIDTH, _HIGH);

String serialBuf = "";
int lastPct   = -1;
int lastMorts = -1;
int lastLevel = -1;

uint8_t avatar[16][16][3] = {
  {{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0}},
  {{0,0,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{0,0,0}},
  {{0,0,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{0,0,0}},
  {{0,0,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{0,0,0}},
  {{0,0,0},{7,5,0},{7,5,0},{0,0,0},{0,1,1},{0,1,1},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{0,1,1},{0,1,1},{0,1,1},{7,5,0},{7,5,0},{0,0,0}},
  {{0,0,0},{7,5,0},{7,5,0},{0,2,2},{0,7,7},{0,6,6},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{0,6,6},{0,7,7},{0,3,3},{7,5,0},{7,5,0},{0,0,0}},
  {{0,0,0},{7,5,0},{7,5,0},{0,2,2},{0,7,7},{0,6,6},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{0,6,6},{0,7,7},{0,3,3},{7,5,0},{7,5,0},{0,0,0}},
  {{0,0,0},{7,5,0},{7,5,0},{6,5,0},{6,5,0},{6,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{6,5,0},{6,5,0},{6,5,0},{7,5,0},{7,5,0},{0,0,0}},
  {{0,0,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{0,0,0}},
  {{0,0,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{0,0,0}},
  {{0,0,0},{7,5,0},{1,1,0},{0,4,4},{0,4,4},{0,4,4},{0,4,4},{0,4,4},{0,4,4},{0,4,4},{0,4,4},{0,4,4},{0,4,4},{0,0,0},{7,5,0},{0,0,0}},
  {{0,0,0},{7,5,0},{1,1,0},{0,7,7},{0,7,7},{0,7,7},{0,7,7},{0,7,7},{0,7,7},{0,7,7},{0,7,7},{0,7,7},{0,7,7},{0,0,0},{7,5,0},{0,0,0}},
  {{0,0,0},{7,5,0},{4,3,0},{3,2,0},{3,3,0},{3,2,0},{3,3,0},{3,2,0},{3,3,0},{3,2,0},{3,3,0},{3,2,0},{3,3,0},{4,3,0},{7,5,0},{0,0,0}},
  {{0,0,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{0,0,0}},
  {{0,0,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{7,5,0},{0,0,0}},
  {{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0}}
};

void setup() {
  Serial.begin(115200);
  matrix.begin();
  matrix.fillScreen(matrix.Color333(0, 0, 0));
}
void loop() {
  while (Serial.available()) {
    char c = (char)Serial.read();
    if (c == '\n') {
      serialBuf.trim();
      if (serialBuf.startsWith("L:")) {
        int val = serialBuf.substring(2).toInt();
        if (val != lastLevel) { lastLevel = val; afficherLevel(val); afficherAvatar(); }
      } else if (serialBuf.startsWith("D:")) {
        int val = serialBuf.substring(2).toInt();
        if (val != lastMorts) { lastMorts = val; afficherMorts(val); }
      } else if (serialBuf.startsWith("P:")) {
        int val = serialBuf.substring(2).toInt();
        if (val != lastPct) { lastPct = val; afficherProgression(val); }
      }
      serialBuf = "";
    } else if (c != '\r') {
      serialBuf += c;
    }
  }
}
void afficherLevel(int num) {
  matrix.fillRect(0, 0, 64, 8, matrix.Color333(0, 0, 0));
  matrix.setTextWrap(false);
  matrix.setTextSize(1);
  matrix.setTextColor(matrix.Color333(0, 7, 0));
  matrix.setCursor(1, 0);
  matrix.print("Level : ");
  matrix.print(num);
}
void afficherMorts(int morts) {
  matrix.fillRect(0, 56, 64, 8, matrix.Color333(0, 0, 0));
  matrix.setTextWrap(false);
  matrix.setTextSize(1);
  matrix.setTextColor(matrix.Color333(7, 0, 0));
  matrix.setCursor(1, 56);
  matrix.print("Morts : ");
  matrix.print(morts);
}
void afficherProgression(int pct) {
  int barY = 10;
  int barH = 8;
  int barW = 62;
  int filled = (int)((long)pct * barW / 100);
  matrix.fillRect(0, barY, 64, barH, matrix.Color333(0, 0, 0));
  matrix.fillRect(1, barY + 1, barW, barH - 2, matrix.Color333(0, 2, 0));
  if (filled > 0)
    matrix.fillRect(1, barY + 1, filled, barH - 2, matrix.Color333(0, 7, 0));
  matrix.drawRect(0, barY, barW + 2, barH, matrix.Color333(7, 7, 7));
}
void afficherAvatar() {
  int px = 24, py = 20;
  for (int y = 0; y < 16; y++) {
    for (int x = 0; x < 16; x++) {
      matrix.drawPixel(px + x, py + y, matrix.Color333(avatar[y][x][0], avatar[y][x][1], avatar[y][x][2]));
    }
  }
}
