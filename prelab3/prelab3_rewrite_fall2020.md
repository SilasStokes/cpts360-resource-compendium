
# LAB 3 Pre-Work: Processes in an OS Kernel
- DUE: 9-22-2020
- Answer questions below. Submit a (text-edit) file to TA

## Table Of Contents
- [LAB 3 Pre-Work: Processes in an OS Kernel](#lab-3-pre-work-processes-in-an-os-kernel)
  - [Table Of Contents](#table-of-contents)
  - [1. READ List: Chapter 3: 3.1-3.5](#1-read-list-chapter-3-31-35)
  - [2. Download samples/LAB3pre/mtx. Run it under Linux.](#2-download-sampleslab3premtx-run-it-under-linux)
  - [3. COMMANDS:](#3-commands)
  - [4. REQUIREMENTS](#4-requirements)
    - [Step 1: test fork](#step-1-test-fork)
    - [Step 2: Test sleep/wakeup](#step-2-test-sleepwakeup)
    - [Step 3: test child exit/parent wait](#step-3-test-child-exitparent-wait)
      - [CASE 1: child exit first, parent wait later](#case-1-child-exit-first-parent-wait-later)
      - [CASE 2: parent wait first, child exit later](#case-2-parent-wait-first-child-exit-later)
    - [Step 4: test Orphans](#step-4-test-orphans)

## 1. READ List: Chapter 3: 3.1-3.5

- What's a process? (Page 102) __________________________________________________
	     
Each process is represented by a PROC structure.
Read the PROC structure in 3.4.1 on Page 111 and answer the following questions:

What's the meaning of:
- pid, ppid? _____________________________________
- status? ________________________________________
- priority? _______________________________________
- event? _________________________________________
- exitCode? ______________________________________

READ 3.5.2 on Process Family Tree. What are the
- PROC pointers child, sibling, parent used for?______________________________
	     
## 2. Download samples/LAB3pre/mtx. Run it under Linux.
MTX is a multitasking system which simulates process operations of fork, exit, wait, sleep, wakeup in a Unix/Linux kernel

```c   
/*********** A Multitasking System ************/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "type.h"    // PROC struct and system constants
	
// global variables:
PROC proc[NPROC], *running, *freeList, *readyQueue, *sleepList; 

running    = pointer to the current running proc
freeList   = a list of all FREE PROCs
readyQueue = a priority queue of procs READY to run
sleepList  = a list of SLEEP procs, if any.
```

Run mtx. It first initialize the system, creates an initial process P0. P0 has the lowest priority 0, all other processes have priority 1. 

After initialization, P0 forks a child process P1, switch process to run P1. The display looks like the following

```
Welcome to KCW's Multitasking System
1. init system
freeList = [0 0]->[1 0]->[2 0]->[3 0]->[4 0]->[5 0]->[6 0]->[7 0]->[8 0]->NULL
2. create initial process P0
freeList = [1 0]->[2 0]->[3 0]->[4 0]->[5 0]->[6 0]->[7 0]->[8 0]->NULL
init complete: P0 running
3. P0 fork P1
4. P0 switch process to P1
P0: switch task
proc 0 in scheduler()
readyQueue = [1 1]->[0 0]->NULL
next running = 1
proc 1 resume to body()

proc 1 running: Parent=0 childList = NULL
freeList  = [2 0]->[3 0]->[4 0]->[5 0]->[6 0]->[7 0]->[8 0]->NULL
readQueue = [0 0]->NULL
sleepList = NULL
input a command: [ps|fork|switch|exit|sleep|wakeup|wait] : 
```
## 3. COMMANDS:
- ps     : display procs with pid, ppid, status; same as ps in Unix/Linux
- fork   : READ kfork()   on Page 109: What does it do? __________________________
- switch : READ tswitch() on Page 108: What does it do? __________________________
- exit   : READ kexit()   on Page 112: What does it do? __________________________
- sleep  : READ ksleep()  on Page 111: What does it do? __________________________
- wakeup : READ kwakeup() on Page 112: What does it do? __________________________
- wait   : READ kwait()   on Page 114: What does it do? __________________________

## 4. REQUIREMENTS 
### Step 1: test fork
- While P1 running, enter fork: What happens? __________________________________
- Enter fork many times; How many times can P1 fork? ________________
  - Why? __________________
- Enter Control-c to end the program run.


### Step 2: Test sleep/wakeup
Run mtx again.
- While P1 running, fork a child P2;
- Switch to run P2.
  - Where did P1 go? ___________________
  - WHY? ______________________
- P2: Enter sleep, with a value, e.g.123 to let P2 SLEEP.
  - What happens? _______________________
  - WHY? ______________________________________
- Now, P1 should be running. Enter wakeup with a value, e.g. 234
  - Did any proc wake up? _____________________ 
  - WHY? ____________________________
- P1: Enter wakeup with 123
  - What happens? ________________________________ 
  - WHY? __________________________


### Step 3: test child exit/parent wait
When a proc dies (exit) with a value, it becomes a ZOMBIE, wakeup its parent.
Parent may issue wait to wait for a ZOMBIE child, and frees the ZOMBIE

- Run mtx;
  - P1: enter wait;
    - What happens? ________________ 
    - WHY? _________________

#### CASE 1: child exit first, parent wait later
- P1: fork a child P2, switch to P2.
- P2: enter exit, with a value, e.g. 123 ==> P2 will die with exitCode=123.
  - Which process runs now? _______________________
  -  WHY? ____________________
- Enter ps to see the proc status:
  - P2 status = ? ____________________________
- (P1 still running) enter wait;
  - What happens?_______________________________
- enter ps;
  - What happened to P2?__________________________

#### CASE 2: parent wait first, child exit later
- P1: enter fork to fork a child P3
- P1: enter wait;
  - What happens to P1? ______________________
  - WHY? ______________
- P3: Enter exit with a value; 
  - What happens? ___________________________________
- P1: enter ps; 
  - What's the status of P3?_________________ 
  - WHY? _________________
	     
### Step 4: test Orphans
	     
When a process with children dies first, all its children become orphans.
In Unix/Linux, every process (except P0) MUST have a unique parent.
So, all orphans become P1's children. Hence P1 never dies.

- Run mtx again.
  - P1: fork child P2, Switch to P2.
  - P2: fork several children of its own, e.g. P3, P4, P5 (all in its childList).
  - P2: exit with a value. 
  - P1 should be running WHY?___________________________________________________
  - P1: enter ps to see proc status: which proc is ZOMBIE?______________________
  - What happened to P2's children? ____________________________________________
  - P1: enter wait; What happens? ________________________________________________
  - P1: enter wait again;
    - What happens?__________________ 
    - WHY?__________________
  - How to let P1 READY to run again?_________________________________________



  