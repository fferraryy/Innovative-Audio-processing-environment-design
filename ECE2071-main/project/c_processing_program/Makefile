.PHONY: all
all: moving_average csv_to_wav Makefile

.PHONY: moving_average
moving_average: moving_average.o implement_moving_average.o Makefile
	gcc -o a.out moving_average.o implement_moving_average.o -o moving_average_impl

test_moving_average.o: test_moving_average.c Makefile
	gcc -c test_moving_average.c
moving_average.o: moving_average.c moving_average.h Makefile
	gcc -c moving_average.c
implement_moving_average.o : implement_moving_average.c Makefile
	gcc -c implement_moving_average.c


.PHONY: csv_to_wav
csv_to_wav: csv_to_wav.c Makefile
	gcc -o csv_to_wav csv_to_wav.c
