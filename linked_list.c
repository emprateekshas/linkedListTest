#include "linked_list.h"

int count = 0;
LLNODE *createNode(int data) {
    LLNODE *newNode = (LLNODE *)malloc(sizeof(LLNODE));
    if (newNode != NULL) {
        newNode->data = data;
        newNode->next = NULL;
    }
    return newNode;
}           

 
int addListNode(LLNODE **headPPtr, LLNODE *addNode)
{
    LLNODE* nodePtr;
    LLNODE **nextPPtr;
    LLNODE *newNode;
    if(!headPPtr || !addNode)
    {
        return -1;
    }    
    nextPPtr = headPPtr;
    nodePtr = *headPPtr;

 

    newNode = (LLNODE*)malloc(sizeof(LLNODE));
    if(!newNode)
    {
        return -2;
    }    
    memcpy(newNode, addNode, sizeof(LLNODE));
    if(!nodePtr)
    {
        *nextPPtr = newNode;
        printf("Added element %d to the empty list\n", newNode->data);
    }
    else
    {
        while(nodePtr)
        {
            if(nodePtr->data > addNode->data)
            {
                break;
            }
            nextPPtr = &(nodePtr->next);
            nodePtr = nodePtr->next;
        }
        newNode->next = *nextPPtr;
        *nextPPtr = newNode;
        printf("Added element is: %d \n", newNode->data);
    }
    count++;

    return 0;  
}            

 

int deleteListNode(LLNODE **headPPtr, LLNODE *delNode)
{
     LLNODE **nextPPtr;
     LLNODE *nodePtr;
     if(!headPPtr)
     {
         return -1;
     }    
     nextPPtr = headPPtr;
     nodePtr = *headPPtr;

 

     while(nodePtr)
     {
         if(nodePtr->data == delNode->data)
         {
             *nextPPtr = nodePtr->next;
             int deleted = nodePtr->data;
             free(nodePtr); 
             printf("The deleted node data is: %d", deleted); 
             count--;
             return deleted;
         }
         nextPPtr = &(nodePtr->next);
         nodePtr = nodePtr->next;
     }
     printf("%d not present in the list\n",delNode->data);
     return -1;            
}   
int deleteListNodeFirst(LLNODE **lhead)
{
    LLNODE *delNode;
    LLNODE *nodeptr;
    if(!nodeptr)
    {
        return -1;
    }
    nodeptr = *lhead;
    *lhead = nodeptr->next;
    nodeptr->next = NULL;
    delNode = (LLNODE *)malloc(sizeof(LLNODE));
    if (!delNode)
    {
        return -1; // Return error if memory allocation fails
    }
    memcpy(delNode, nodeptr, sizeof(LLNODE));
    printf("The deleted node data is: %d\n", delNode->data);
    free(nodeptr);
    count--;
    return 0;
}

 

 

int deleteListLast(LLNODE **lhead)
{
    LLNODE *delNode;
    LLNODE *nodeptr;
    LLNODE **nextpptr;

 

    if (!lhead || !*lhead) 
    {
        return -1; // Return error if list is empty or lhead is NULL
    }

 

    nextpptr = lhead;
    nodeptr = *lhead;

 

    while (nodeptr->next)
    {
        nextpptr = &(nodeptr->next);
        nodeptr = nodeptr->next;
    }

 

    *nextpptr = NULL; // Remove the last node from the list

 

 

    // Allocate memory for delNode and copy data
    delNode = (LLNODE *)malloc(sizeof(LLNODE));
    if (!delNode)
    {
        return -1; // Return error if memory allocation fails
    }
    memcpy(delNode, nodeptr, sizeof(LLNODE));

 

    // Free the memory of the last node
    free(nodeptr);

 

    printf("The deleted node data is: %d\n", delNode->data);
    count--;

 

    return 0;
}

 

 

 

/*
int deleteListLast(LLNODE **lhead)
{
    LLNODE *delNode;
    LLNODE *nodeptr;
    LLNODE **nextpptr;
    if (!lhead) 
    {
        return -1;
    }
    nextpptr = lhead;
    nodeptr = *lhead;
    while(nodeptr)
    {
        if(nodeptr->next == NULL)
        {
             break;
        }
        nextpptr = &(nodeptr ->next);
        nodeptr = nodeptr->next;
    }

 

 

    *nextpptr =NULL;
    nodeptr->next = NULL;
    memcpy(delNode, nodeptr, sizeof(LLNODE));
    free(nodeptr);
    printf("The deleted node data is: %d\n", nodeptr->data);
    count--;
    return 0;
}
*/
void display(LLNODE *head)
{
    if (!head) 
    {
        return;
    }
    LLNODE *curr = head;
    while(curr->next !=NULL)
    {
        printf("%d", curr->data);
        if (curr->next != NULL) 
        {
            printf(", ");
        }
        curr = curr->next;
    }
    printf("%d", curr->data);
    printf("\n");
}        

 

int main()
{
     //setbuf(stdout, NULL);
     LLNODE *head = NULL;
     //LLNODE node1;
     int choice;
     int data;
     do
     {
           printf("\n1. Add an element \n2. Delete an element from list \n3. Delete first element\n4. Delete last element\n5. Display the elements \nEnter your choice: ");
     scanf("%d", &choice);
           switch(choice)
        {
         case 1: 
             printf("Enter the element to be added: ");
             scanf("%d",&data);
             createNode(data);
             addListNode(&head, createNode(data));
             break;

 

         case 2:
             if(!head)
                 printf("Linked list is empty\n");
             else
             {
             printf("Enter the element you want to delete: ");
             scanf("%d", &data);
             LLNODE *delNode = (LLNODE *)malloc(sizeof(LLNODE));
                     delNode->data = data;                    
                       deleteListNode(&head, delNode);
             }
             break;
        case 3:
                 if(!head)
                     printf("Linked list is empty\n");
                 else        
                     deleteListNodeFirst(&head);
                 break;
        case 4:
             if(!head)
                 printf("Linked list is empty\n");
             else
                 deleteListLast(&head); 
             break;             
        case 5:
             printf("List Element Count: %d \n",count);
             if(count > 0)
                 printf("List Elements: ");
                 display(head);
             break;
        default:
                printf("Invalid choice\n");
                break;             
          }
      }while(choice != 9999); 
}
