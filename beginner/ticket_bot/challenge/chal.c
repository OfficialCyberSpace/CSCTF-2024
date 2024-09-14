//gcc -w -lm -fno-stack-protector -Wl,-z,no-relro -masm=intel Ticket-bot_v1.c 
#include <stdio.h>
#include <stdlib.h>

int seed;
int password;
int *passwd = &password;

int init(){

	setvbuf(stdin,0x0,2,0);
    setvbuf(stdout,0x0,2,0);

	FILE * fp;
	char urand[8];

	fp = fopen("/dev/urandom","rb");
	fgets(urand,8,fp);
	fclose(fp);

	int seed1 = urand;

	srand(seed1);

	int randnumber = rand();
	seed = randnumber % 10000000;
	srand(seed);

	password = rand();
	//printf("Admin Password = %d\n",password);

    return;
}

int wellcome(){

	int number = rand();
	printf("Wellcome to TicketBot v1.0 here is your ticketID %d\n",number);
    return;
}


void GrabNewTicket(){
	int number = rand();
	printf("your new ticketID is %d\n",number);
}

void ServiceLogin(){

	int Password;
	puts("Admin Password");
	scanf("%d",&Password);
	if (Password == password){
		AdminMenu();
	}
	else{
		puts("wrong Password");
		exit(0);
	}

}

void AdminMenu(){

	int newPassword;

	puts("========================");
	puts("1. change Admin Password");
	puts("2. reset all Tickets");
	puts("========================");

	int choice = 0;
	scanf("%d",&choice);
	getchar();


	if(choice == 1){
		puts("Enter new Password");
		scanf("%s",&newPassword);
		int pass = atoi(&newPassword);
		password = pass;
		puts("Password changed to");
		printf(&newPassword);
		}

	else if(choice == 2){
		puts("Reset done!");
		}


	else {
		exit(0);
		}
}

void menu(){

	puts("========================");
	puts("1. New Ticket");
	puts("2. Service Login");
	puts("========================");

	int choice = 0;
	scanf("%d",&choice);
	getchar();

	if(choice == 1){
		GrabNewTicket();
		}

	else if(choice == 2){
		ServiceLogin();
		}


	else {
		printf("that is not an option\n");
		}
}

int main(){
	init();
    wellcome();
    while(1==1){
    menu();
	}

    return 0;
}
