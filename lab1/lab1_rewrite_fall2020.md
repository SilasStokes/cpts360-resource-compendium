# CS360 LAB ASSIGNMENT #1

- Due & Demo: 9-3-2020
- Email YOUR code and output file to TA BEFORE the DEMO
- Demo YOUR work to TA via ZOOM session; TA will post demo schedule

## Contents

- [CS360 LAB ASSIGNMENT #1](#cs360-lab-assignment-1)
  - [Contents](#contents)
  - [Part 1: Partition Table](#part-1-partition-table)
    - [OBJECTIVES](#objectives)
    - [Intro: What is a Partition Table?](#intro-what-is-a-partition-table)
    - [Part 1 Requirements:](#part-1-requirements)
    - [Starter Code](#starter-code)
      - [How to create a disk file of 2880 512-byte sectors OR 1440 1K blocks](#how-to-create-a-disk-file-of-2880-512-byte-sectors-or-1440-1k-blocks)
    - [Algorithm for Part1 of LAB1:](#algorithm-for-part1-of-lab1)
  - [Part 2: myprintf Function](#part-2-myprintf-function)
    - [2-1. Write YOUR own prints(char \*s) function to print a string.](#2-1-write-your-own-printschar-s-function-to-print-a-string)
    - [2-2. Write YOUR own format functions](#2-2-write-your-own-format-functions)
    - [2-3: Implement yor own myprintf function](#2-3-implement-yor-own-myprintf-function)
    - [2-4: Using your new function](#2-4-using-your-new-function)
  - [Help Info](#help-info)
    - [Algorithm](#algorithm)
  - [To Do:](#to-do)

## Part 1: Partition Table

### OBJECTIVES

Partition table, fdisk, structures in C, open-read files

### Intro: What is a Partition Table?

A disk (floppy disk, hard disk, USB drive, SD cards, etc.) consists of 512-byte sectors, which are counted linearly as sector 0,1,2,....

A disk is usually divided into several partitions. The partitions are recorded in a partition table at the beginning (the 0th sector) of the disk, called the Master Boot Record (MBR). Inside the MBR, the partition table begins at the byte offset 0x1BE. The Partitin Table contains 4 entries, each 16 bytes long, defined in the following C structure.

```c
typedef unsigned char  u8;
typedef unsigned short u16;
typedef unsigned int   u32;

struct partition {
	u8 drive;             /* drive number FD=0, HD=0x80, etc. */

	u8  head;             /* starting head */
	u8  sector;           /* starting sector */
	u8  cylinder;         /* starting cylinder */

	u8  sys_type;         /* partition type: NTFS, LINUX, etc. */

	u8  end_head;         /* end head */
	u8  end_sector;       /* end sector */
	u8  end_cylinder;     /* end cylinder */

	u32 start_sector;     /* starting sector counting from 0 */
	u32 nr_sectors;       /* number of of sectors in partition */
  };

```

![figure 1](./fig-01.png)

heads, sectors, cylinders are for old floppy disks. Hard disks only use start_sector and nr_sectors.

Each partition has a type, which indicates what kind of file system the partition MAY contain. Consult Linux's fdisk to see the partition types.

If a partition is EXTEND type (type=5), the partition's area may be further divided into more partitions. The extended partitions forms a LINK-LIST as the following diagram shows.

```
------------------------------------------------------------------------------
Assume P4 is EXT type:

P4's beginSector = localMBR
                     P5's beginSector# relative to beginSector
                     P6's MBR's sector# = localMBR
                         (r.e. to P4)       P6's beginSector#
                                            P7's MBR r.e. to P4 --> etc.

The first sector of each extended partition is a localMBR. Each localMBR has a partition table which contains only 2 entries. The first entry defines the start sector and size of the extended partition. The second entry points to the next localMBR. All the localMBR's sector numbers are relative to P4's start sector. As usual, the link list ends with a 0.
-------------------------------------------------------------------------------
```

Since use fdisk on hard disks is risky, we shall use a VIRTUAL disk for this assignment. A virtual disk is just a file but its contents are exactly the same as a REAL disk. Download the file `~cs360/samples/LAB1/vdisk` to YOUR Linux. Then, run fdisk vdisk
'p' : to see the partition table
'q' : to quit fdisk

### Part 1 Requirements:

Write a C program to display the partition table of the vdisk in

- [ ] Linux fdisk 'p' output form for the first 4 partitions (%40),
- [ ] including ALL the extend partitions (%60) <== YOU BETTER DO THIS !!!!.

Turn in a printed HARD COPY containing your work.

### Starter Code

```c
/********* h1.c **********/
#include <stdio.h>
#include <string.h>

typedef struct person{
  char name[64];
  int  id;
  int  age;
  char gender;
}PERSON;

PERSON kcw, *p;

int main()
{

// Access struct fields by . operator: OK but ugly
   kcw.id = 12345678;
   kcw.age = 83;
   kcw.gender = 'M';

   p = &kcw;

// Deference pointer to struct, then use . operator: NOT GOOD either!
   (*p).id = 123;
   (*p).age = 120;

// Use pointer by -> operator is the BEST WAY:
   p->id = 12345678;
   p->age = 83;
   p->gender = 'M';
   strcpy(p->name, "k.c. wang");

   printf("name=%s id=%d age=%d gender=%c\n",
	 p->name, p->id, p->age, p->gender);
}
```

#### How to create a disk file of 2880 512-byte sectors OR 1440 1K blocks

```bash
dd if=/dev/zero of=disk bs=512 count=2880
```

```c
/********** h2.c *********/
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/types.h>
#include <unistd.h>

typedef struct person{
  char name[64];
  int  id;
  int  age;
  char gender;
}PERSON;

int write_sector(int fd, int sector, char *buf)
{
  int n;
  lseek(fd, sector*512, SEEK_SET); // advance to sector*512 bytes
  n = write(fd, buf, 512);         // write 512 bytes from buf[] to sector
  if (n != 512){
     printf("write failed\n");
     return -1;
  }
  return n;
}

PERSON kcw, *p;

int fd;
char buf[512];

int main()
{
  p = &kcw;

  strcpy(p->name, "k.c. Wang");
  p->id = 12345678;
  p->age = 83;
  p->gender = 'M';

  fd = open("disk", O_WRONLY);  // open disk file for WRITE
  printf("fd = %d\n", fd);      // show file descriptor number

  bzero(buf, 512);              // clear buf[ ] to 0's
  memset(buf, 0, 512);          // set buf[ ] to 0's

  memcpy(buf+256, p, sizeof(PERSON));

  write_sector(fd, 1234, buf);   // write buf[512] to sector 1234
}
```

```c
/*********** h3.c ***********/
// Assume disk sector 1234 contains a PERSON struct at byte offset 256

#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/types.h>
#include <unistd.h>

typedef struct person{
  char name[64];
  int  id;
  int  age;
  char gender;
}PERSON;

int read_sector(int fd, int sector, char *buf)
{
  int n;
  lseek(fd, sector*512, SEEK_SET);
  n = read(fd, buf, 512);
  if (n <= 0){
    printf("read failed\n");
    return -1;
  }
  return n;
}

PERSON kcw, *p;

int fd;
char buf[512];

int main()
{
  fd = open("disk", O_RDONLY);  // open disk for READ
  printf("fd = %d\n", fd);

  read_sector(fd, 1234, buf);   // READ sector 1234 into buf[ ]

  p = (PERSON *)(buf+256);      // OR p=(PERSON *)&buf[256];

  printf("name=%s id=%d age=%d gender=%c\n",
	 p->name, p->id, p->age, p->gender);

}
```

### Algorithm for Part1 of LAB1:

1. open diskimage file for READ
2. read Sector 0 into `char buf[512]`
3. `struct partition *p = (shut up)&buf[0x1BE]; // p points at P1`
4. use `p->` to print fields of `P1`
5. `p++; // p points at P2; print P2 information`
6. repeat for `p3`, `P4`
7. if `P4` is EXTENDED (type=5): read P4's begin_sector into `char buf[512]`

```
    localMBR at `0x1bE` has 2 entries = P5
                                      sector# of next localMBR
                                      (as a link list that ends with 0)
```

```c
/* sample code for Part 1 */
#include <stdio.h>
#include <fcntl.h>
#include <ext2fs/ext2_fs.h>  // Ubuntu User: sudo apt install e2fslibs-dev

#include <sys/types.h>
#include <unistd.h>

typedef unsigned char  u8;
typedef unsigned short u16;
typedef unsigned int   u32;

struct partition {
	u8 drive;         // 0x80 - active
	u8 head;          // starting head
	u8 sector;        // starting sector
	u8 cylinder;      // starting cylinder
	u8 sys_type;      // partition type
	u8 end_head;      // end head
	u8 end_sector;	  // end sector
	u8 end_cylinder;  // end cylinder
	u32 start_sector; // starting sector counting from 0
	u32 nr_sectors;   // nr of sectors in partition
};

char *dev = "vdisk";
int fd;

int read_sector(int fd, int sector, char *buf)
{
    // same as shown above
}

int main()
{
  struct partition *p;
  char buf[512];

  fd = open(dev, O_RDONLY);   // open dev for READ

   read(fd, buf, 512);        // read MBR into buf[]
   // read_sector(fd, 0, buf);    // OR call read_sector()
   p = (struct partition *)(&buf[0x1be]); // p->P1

   printf("%8d %8d %8x\n", p->start_sector, p->nr_sectors, p->sys_type);

   // Write YOUR code to print all 4 partitions


   // ASSUME P4 is EXTEND type;
   p += 3;      // p-> P4
   printf("P4 start_sector = %d\n", p->start_sector);

   read_sector(fd, p->start_sector, buf);

   p = (struct partition *)&buf[0x1BE];    // p->localMBR
   printf("FIRST entry of localMBR\n");
   printf("start_sector=%d, nsectors=%d\n", p->start_sector, p->nr_sectors);

   // Write YOUR code to get 2nd entry, which points to the next localMBR, etc.
   // NOTE: all sector numbers are relative to P4's start_sector
}
```

## Part 2: myprintf Function

### 2-1. Write YOUR own prints(char \*s) function to print a string.

Given:

```c
putchar(char c)
```

of Linux, which prints a char.

### 2-2. Write YOUR own format functions

Given: The following `printu()` function prints an unsigned integer.

```c
typedef unsigned int u32;

char *ctable = "0123456789ABCDEF";
int  BASE = 10;

int rpu(u32 x)
{
    char c;
    if (x){
       c = ctable[x % BASE];
       rpu(x / BASE);
       putchar(c);
    }
}

int printu(u32 x)
{
   (x==0)? putchar('0') : rpu(x);
   putchar(' ');
}
```

```
EXAMPLE:
Assume u32 x = 123;
1st call to rpu(x): x=123; x%10 = 3 ===>  c = '3';
2nd call to rpu(x): x=12;  x%10 = 2 ===>  c = '2';
3rd call          : x=1;   x%10 = 1 ===>  c = '1';
----------------------------------------------------
4th call          : x=0 => return ====> print '1';
                           return ====> print '2'
                           return ====> print '3'
```

```c
 int  printd(int x) // which print an integer (x may be negative!!!)
 int  printx(u32 x) // which print x in HEX   (start with 0x )
 int  printo(u32 x) // which print x in Octal (start with 0  )
```

### 2-3: Implement yor own myprintf function

Write YOUR own myprintf(char \*fmt, ...) function to print

```
char                      by %c
string                    by %s
unsigned integer          by %u
integer                   by %d
unsigned integer in OCT   by %o
unsigned integer in HEX   by %x
```

Ignore field width and precision, just print the items as specified.

### 2-4: Using your new function

In the int main(int argc, char *argv[ ], char *env[ ]) function, use YOUR myprintf() to print

```c
argc value
argv strings
env  strings
myprintf(
    "cha=%c string=%s      dec=%d hex=%x oct=%o neg=%d\n",
	'A',
    "this is a test",
    100,
    100,
    100,
    -100
);
```

## Help Info

NOTE: This assignment is for 32-bit GCC, which passes parameters on stack. Use the command

```bash
gcc -m32 t.c
```

to compile your C source files.

```c
int myprintf(char *fmt, ...)      // C compiler requires the 3 DOTs
```

Assume the call is

```c
myprintf(fmt, a,b,c,d);
Upon entry, the following diagram shows the stack contents.
```

```
               char *cp -> "...%c ..%s ..%u .. %d\n"
  HIGH               |                                              LOW
--------------------------- --|------------------------------------------
  | d   | c   | b   | a | fmt | retPC | ebp | locals |
  | --- | --- | --- |
  |     |
           int *ip            CPU.ebp
```

1. Let char \*cp point at the format string
2. Let int \*ip point at the first item to be printed on stack:

NOTE: In 32-bit mode, Every entry in the stack is 4-byte for chars, they are in the lowest byte (of the 4-byte entry) for strings, they are POINTERs to the actual strings.

### Algorithm

- Use `cp` to scan the format string:
  - spit out each char that's NOT %
  - for each \n, spit out an extra \r
  - Upon seeing a %: get next char, which must be one of 'c','s','u','d', 'o','x'
    - Then call YOUR
      ```c
      putchar(*ip); // for 'c';
      prints(*ip);  // for 's';
      printu(*ip);  // for 'u';
      printd(*ip);  // for 'd';
      printo(*ip);  // for 'o';
      printx(*ip);  // for 'x';
      ```
  - Advance ip to point to the next item on stack.

After implementing your `myprintf()` function, write C program to test your
`myprintf()` function first. Then use it in the assignment.

## To Do:

- [ ] Part 1
  - [ ] Write a C program to display the partition table of the vdisk in
    - [ ] Linux fdisk 'p' output form for the first 4 partitions (%40),
    - [ ] including ALL the extend partitions (%60) <== YOU BETTER DO THIS !!!!.
  - [ ] Turn in a printed HARD COPY containing your work.
- [ ] Part 2:
  - [ ] 2-1. Write YOUR own prints(char \*s) function to print a string (See Above)
  - [ ] 2-2. Write YOUR own format functions (See Above)
  - [ ] 2-3: Implement yor own myprintf function (See Above)
  - [ ] 2-4: Use your new myprintf function (See Above)
  - [ ] Write a function to test your new myprintf function
