# homework 1
## The sample code supports only '+' and '-'. Modify the program and support '*' and '/'.
```module_program_hw1.py```
* I added a new function called evaluate_mul_and_div to first calculate the multiplication and division.
* Then I passed onto evaluate function to calculate the addition and subtraction which had already been defined from the beggining.
# homework 2
## Add test cases to the run_test() function.
```module_program_hw2.py```
* I added test cases to the run_test() function that used *  or /.
# homework 3
## Support '(' and ')'. Add test cases to the run_test() function.
```module_program_hw3.py```
* I added a new function called evaluate_parentheses to first calculate the expression inside the parentheses.
* then I passed onto evaluate function to calculate the addition, subtraction, multiplication, and division.
### Test cases output
```
==== Test started! ====
PASS! (1+2 = 3.000000)
PASS! (1.0+2.1-3 = 0.100000)
PASS! (1.0+2.1-3.0 = 0.100000)
PASS! (2*4/2+1+2*1 = 7.000000)
PASS! (2*4/2+1+2*1-1 = 6.000000)
PASS! (((2+2)+1) = 5.000000)
PASS! (((2+2)*3) = 12.000000)
PASS! (((2+2)*3)+1 = 13.000000)
PASS! (((2+2)*3)+1+1 = 14.000000)
==== Test finished! ====
```
# homework 4
## Support abs(), int() and round(). Add test cases to the run_test() function.
### What I did
1. I defined the abs(), int() and round() functions.
2. I edited the evaluate_parentheses function to calculate abs(), int() and round() functions if they were outside on the left of the parentheses.
3. I had to edit the evaluate_mul_and_div because after I edited the evaluate_parentheses function it would add PLUS token at the front of the calculation result
    * Therefore, the evaluate_mul_and_div function would have to ingnore the PLUS token when it is next to a MULTIPLY or DIVIDE token.
4. I added test cases to the run_test() function that used abs(), int() and round().



### Test cases output
```
==== Test started! ====
PASS! (1+2 = 3.000000)
PASS! (1.0+2.1-3 = 0.100000)
PASS! (1.0+2.1-3.0 = 0.100000)
PASS! (2*4/2+1+2*1 = 7.000000)
PASS! (2*4/2+1+2*1-1 = 6.000000)
PASS! (((2+2)+1) = 5.000000)
PASS! (((2+2)*3) = 12.000000)
PASS! (((2+2)*3)+1 = 13.000000)
PASS! (((2+2)*3)+1+1 = 14.000000)
PASS! (abs(-1) = 1.000000)
PASS! (round(1.5) = 2.000000)
PASS! (int(1.5) = 1.000000)
PASS! (int(-1.6) = -1.000000)
PASS! (12+abs(int(round(-1.55)+abs(int(-2.3+4)))) = 13.000000)
PASS! (12+abs(int(round(-1.55)+abs(int(-2.3+4)))+1) = 12.000000)
PASS! (round(1.5)+int(1.5) = 3.000000)
PASS! (round(-1.5+int(1.5))*int(1.5) = -1.000000)
==== Test finished! ====
```
