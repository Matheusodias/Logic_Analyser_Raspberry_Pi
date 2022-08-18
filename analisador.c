//Aluno: Matheus Oliveira Dias
//Matrícula: 18/0025104 

#include <stdio.h>
#include <unistd.h>
#include <wiringPi.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h>
#include <time.h>

void signal_handler(int x);

float FREQ_DIV = 125.0f; // Divide 125Mhz by this to get your freq
long int freq;
long int time_difference;
long int start_time;
struct timespec gettime_now;
int ts;
int pino = 0;
int n_amostras = 0;

int main(int argc, const char * argv[])
{	
	unsigned int j;

	int pin = atoi(argv[1]);
	freq = atoi(argv[2]);
	n_amostras = atoi(argv[3]);
	int t = (1000000/freq);
	
	ts = t;
	pino = pin;
	clock_gettime(CLOCK_REALTIME, &gettime_now);
	start_time = gettime_now.tv_nsec;		//Get nS value

	
	printf("Pino de leitura = %d\n",pino);
	printf("Frequencia em Hz de amostragem = %d\n",freq);
	printf("Numero ts = %d\n",ts);
	
	wiringPiSetup();
	pinMode(pino, INPUT);																			//Pino selecionado como saída
	
	struct sigaction act;
    act.sa_handler = signal_handler;
    sigaction(SIGALRM, &act, 0);

//	signal(SIGALRM, &alarme);
	ualarm(10, 0);
	
//	while(1)
//	{
//		printf("tah aqui\n");
//		usleep(5000000);
//	}
	
	return 0;
}

void signal_handler(int x)
{
	printf("Chegou aqui pino = %d e num amostras = %d\n",pino,n_amostras);
	int i = 0;
	char buffer[n_amostras-1];
	while(i < n_amostras)
	{
		//printf("%d\n",digitalRead(pino));
		buffer[i] = (digitalRead(pino))+'0';
		//printf("buffer %d = %c\n",i,buffer[i]);
		usleep(ts);																					//Nível lógico alto (t% de cíclo útil)
		i += 1;
	}
	
	FILE *fp = fopen("amostas.txt", "a+");
	if (fp == NULL) 
		return 0;
	

	fputs(buffer, fp);
	fputs("\n", fp);
	//printf("\nString: %s\n",buffer);
}
