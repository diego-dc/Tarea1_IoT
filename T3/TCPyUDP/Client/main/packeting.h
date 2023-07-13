char* header(char protocol, char transportLayer);
unsigned short dataLength(char protocol);

unsigned short messageLength(char protocol);

char* mensaje(char protocol, char transportLayer);

char* dataprotocol1(char* header, int status);
char* dataprotocol2(char* header, int status);
char* dataprotocol3(char* header, int status);
char* dataprotocol4(char* header, int status);
char* dataprotocol5(char* header, int status);
