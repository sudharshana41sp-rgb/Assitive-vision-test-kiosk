#include<reg51.h>
sbit rs=P1^0;
sbit en = P1^0;
void cmd (int);
void data1 (char);
void lcd();
void delay();
void dispaly(char *);

void main()
{
lcd();
display("Hai");
}

void lcd()
{
	cmd(0x38);
	cmd(0x0e);
	cmd(0x01);
	cmd(0x06);
	cmd(0x80);
}

void cmd(int a)
{
	P3=a;
	rs=0;
	en=1;
	delay();
	en=0;
}

void data1(char j)
{
	P3=j;
	rs=1;
	en=1;
	delay();
	en=0;
}

void display(char *s)
{
while(*s!='\0')
{
data1(*s);
s++;
}