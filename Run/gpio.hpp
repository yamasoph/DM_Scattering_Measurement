#include <iostream>
#include <pigpiod_if2.h>
#include <lgpio.h>

class gpio{
    public:
        gpio(){gpio(4);}
        gpio(int);
        void setMode(int, int);
        int read(int);
    private:
        int state;
        int pi;
};
