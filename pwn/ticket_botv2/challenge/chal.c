//gcc -w -lm -fstack-protector-all -Wl,-z,no-relro -masm=intel Ticket-botv2.c
#include <stdio.h>
#include <stdlib.h>

int seed;
int password;
int *passwd = &password;
int ticketcounter = 0;
char tickets[5][32];
int currentticketid;

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

  password = rand();
}

int wellcome(){

  printf("Wellcome to TicketBot v2.0 here is your ticketID %d\n",ticketcounter);
  currentticketid = ticketcounter;
  puts("Please tell me why your here:");
  scanf("%32s",&tickets[ticketcounter]);
    return;
}

int GrabNewTicket(){
  ticketcounter++;
  currentticketid = ticketcounter;
  if(ticketcounter > 5){
    ticketcounter = 0;
  }

  printf("your new ticketID is %d\n",ticketcounter);

  puts("Please tell me why your here:");
  scanf("%32s",&tickets[ticketcounter]);
}

int ServiceLogin(){

  int Password;
  puts("Admin Password");
  scanf("%d",&Password);
  if (Password == password){
    AdminMenu();
  }
  else{
    puts("Wrong Password");
    exit(0);
  }
} 

int ViewTicket(){

  int id = 0;
  puts("please enter your ticketID");
  scanf("%d",&id);
  if(id == currentticketid){
    write(1,&tickets[id],32);
    puts("\n");
  }
  else{
    puts("sorry that is not your ticket!");
  }
}

int AdminMenu(){

  puts("========================");
  puts("1. change Admin Password");
  puts("2. reset all Tickets");
  puts("========================");

  int choice = 0;
  scanf("%d",&choice);
  getchar();

  if(choice == 1){
    adminpass();
    }

  else if(choice == 2){
    puts("Reset done!");
    }
  return;
}

int adminpass(){
    int newPassword;
    puts("Enter new Password");
    scanf("%s",&newPassword);
    int pass = atoi(&newPassword);
    puts("Password changed to");
    printf(&newPassword);
}

int menu(){

  puts("========================");
  puts("1. New Ticket");
  puts("2. View Ticket");
  puts("3. Service Login");
  puts("========================");

  int choice = 0;
  scanf("%d",&choice);
  getchar();

  if(choice == 1){
    GrabNewTicket();
    }

  else if(choice == 2){
    ViewTicket();
    }

  else if(choice == 3){
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
    
    return 0;}
