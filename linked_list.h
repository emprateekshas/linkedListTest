#ifndef NEW_LINKED_H
#define NEW_LINKED_H
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct llnode_t
{
    struct llnode_t *next;
    int data;
} LLNODE;

int addListNode(LLNODE **listHead, LLNODE *newNode);
int deleteListNode(LLNODE **headPPtr, LLNODE *delNode);
void display(LLNODE *head);
#endif
