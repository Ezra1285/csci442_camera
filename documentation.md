## Statements

# For loop

The for loop statement in catscript is one of the main control flow options. It is used to loop through a list or repeat a set of instructions. Here is an example of the for loop:
```
for(i in [1,2,3]){
   print(i)
}
```
In this example the for loop is used to iterate through a list and print out its contents. 

To use the for loop, use the keyword “for” followed by the control statement then brackets for the code body. In the control statement, put an identifier followed by the keyword “in” then the object you want to iterate through. In the example above, “i” is the identifier and the list “[1,2,3]” is what the loop is iterating through. In this case “i” would evaluate to an integer “1” the first time through the loop, and “2” and “3” respectively until there are no more objects in the list.

The for loop also creates its own scope. “I” will not be accessible outside of the loop. Changing of the scope also does not allow for shadowing. If “i” is declared before the for loop, there will be a compile time error where “i” is not allowed to be redeclared.

# If Statement

The if statement in catscript is another of the control flow options. It uses the keyword “if” followed by a comparison statement, then a body and an optional “else” statement. Here is an example of the if statement:
```
var x = 3
if(x>4){
    print("higher than 4")
}else{
    print("lower than 4")
}
```
In this example the if statement is comparing x to 4, and splitting the control flow to change the print statement. If x is greater than 4, then the first print statement is executed, but if x is less than or equal to 4 then the second print statement will execute. 

The if statement also changes scope. After the comparison statement is executed, the body that is used creates its own scope. One thing to note is that at compile time, there will still be an error if there are scoping issues, even if the branch isn’t used.

# Function Definition

The function definition is the last control flow statement. It uses the keyword “function” followed by the identifier, then the arguments with optional types, the return type, a body, then a “return” keyword if the function is non-void.
```
function foo(x :int) :int{
    return x
}
```
In this example the function has the identifier “foo”, with one argument that has to be an integer, and a return type of integer. The body just returns “x”., but it can contain any number of statements.

The function changes scope, so “x” cannot be used outside of the function.

# Function call

The function call statement is used to invoke a function. It takes a number of arguments equal to the number defined in the function definition, and has an identifier to identify the function it is referring to. 
```
foo(1,2)
```
In this example, foo is the identifier, and “1” and “2” are the arguments passed to the function definition. 

# Print statement

The print statement takes an expression and prints its value to the console. It can only take 1 argument, it does not support multiple arguments like other languages.
```
print(1)
```
In this example, it prints “1” to the console.

# Variable Statement

The variable statement starts with the “var” keyword, then an identifier, and takes the right hand side of the equals and assigns it to the identifier.
```
var a = [1, 2, 3]
```
In this example, the list “[1,2,3]” is assigned to a. “Var” automatically boxes the type for the identifier from the type that it is assigned from.

## Expressions

# Equality
The equality expression returns a boolean value based on whether two expressions are equivalent.
```
1 == 1
```
In this example, the result would be true

#Comparison
The comparison expression returns a boolean value based on whether one expression is greater or less than another expression.
```
2 >= 1
```
In this example, 2 is greater than 1, so true is returned.

# Additive
The additive expression takes two expressions and adds or subtracts them.
```
1 + 1
```
# Factor
The factor expression takes two expressions and multiplies or divides them.
```
1*3
```
# Unary
The unary expression negates the value, either with a “not” or “-”
```
-1
```
# Literals:
There are five literals in Catscript: int, string, list, bool, and object. Examples of these types are:
```
1
"1"
[1,1]
true
object
```


