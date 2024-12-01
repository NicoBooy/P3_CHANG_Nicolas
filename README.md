# P3_CHANG_Nicolas

**Duality Code**  
Let's solve this LP problem using pulp and Python

## Primal
maximize : $x_1 + 4x_2 + 2x_3 $

subject to :  
$5x_1 + 2x_2 + 2x_3 \leq 145$  
$4x_1 + 8x_2 - 8x_3 \leq 260$  
$x_1 + x_2 + 4x_3 \leq 190$  
$x \geq 0$  


## Dual
minimize : $145y_1 + 260y_2 + 190y_3$  

subject to :  
$5y_1 + 4y_2 + y_3 \geq 1$  
$2y_1 + 8y_2 + y_3 \geq 4$  
$2y_1 - 8y_2 + 4y_3 \geq 2$  
$y \geq 0$  


*Question 2 : verify that  Q=(x1,x2,x3)=(0,52.5,20) is a feasible solution for the primal*  
This corresponds to the step 6 of the code : checking if Q respects all the constraints in Primal to be a feasible solution  

*Question 3 : Use CS to determine a candidate solution to the dual.*  
This corresponds to the step 12 of the code : If a primal slack is strictly positive, the corresponding variable in the dual must be zero and vice versa for primal AND dual.  

*Question 4 : Is Q the solution for the primal problem?*  
This corresponds to the last line of the code : If Q respects the constraints in Primal (question 2) and the Complementary Slackness (question 3) then, Q is the solution for the primal problem






