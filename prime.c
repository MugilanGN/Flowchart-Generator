#include <stdio.h>  
#include <math.h>  
  
int main()  
{  
    int start, end, count, prime, inum;  
  
    printf("Enter start and end value\n");  
    scanf("%d%d", &start, &end);  
  
    printf("\n\nPrime Numbers from %d to %d are:\n", start, end);  
    while(start <= end)  
    {  
        inum  = sqrt(start);  
        count = 2;  
        prime = 1;  
  
        while(count <= inum)  
        {  
            if(start%count == 0)  
            {  
                prime = 0;  
                break;  
            }  
            count++;  
        }  
  
        if(prime) printf("%d, ", start);  
        start++;  
    }  
    printf("\n\n");  
  
    return 0;  
}  
