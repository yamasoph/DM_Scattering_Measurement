Encoder: Encoder.cpp sharedMemory.cpp gpio.cpp
	sudo g++ -Wall -pthread -o Encoder Encoder.cpp sharedMemory.cpp gpio.cpp -lpigpiod_if2 -lrt -llgpio -Ofast
	sudo g++ -Wall -pthread -shared -fPIC -o Encoder.so Encoder.cpp sharedMemory.cpp gpio.cpp -lpigpiod_if2 -lrt -llgpio -Ofast
	
clean:
	rm -f *.o output
	rm -f *.so output
