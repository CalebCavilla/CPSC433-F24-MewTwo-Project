# CPSC433-F24-MewTwo-Project

## Important Notes

- DUE DATE: December 9th

# Running the Code

At the current stage of development, run the following input in the terminal

```
startState.py ./test.txt 1 1 1 1 1 1 1 1
```

or to run only the parser

```
parserFile.py ./test.txt 1 1 1 1 1 1 1 1
```

## Commit Conventions

Any time you want to make changes to the project, you should create a new branch (or work on an existing branch) and then merge to master through a pull request. Do not push commits directly to master.

Branching Conventions: - Name - Feature name

For commit messages, read: https://cbea.ms/git-commit/ for a general guideline on how to format and articulate your git messages.

Important Notes: - Keep commits small, you do not have to commit for every line of code but every time you add a new function or a notable feature, make a commit. Do not commit multiple features at once.

## Coding Practices

### Header

- Every file you work on should have a header in the following format:

```java
/**
* Authors: <Full-name (UCID)>
* CPSC433 F24
* References:
*    - Reference 1: Link 1
*    - Reference 2: Link 2
*   ...
*/
```

Example of this below:

```java
/**
* Authors: Caleb Cavilla (30145972), Aoi Ueki (99999999)
* CPSC433 F24
* References:
*     - Java Docs: https://docs.oracle.com/javase/8/docs/api/
*     - Coding Tutorial: https://www.youtube.com/watch?v=dQw4w9WgXcQ
*/
```

If you are adding to a file with an existing header, simply add your name and UCID to the authors list

### Comments

Every time you create a chunk or line of code where it is not immediately obvious what the code is doing you should comment. Comments should go above if describing a chunk of code, and to the right if describing a particular line of code.

#### Examples

```java
// Add two integers (code chunk)
int a = 2
int b = 1
int sum = a + b
```

```java
int x = 3252
boolean even = (x % 2) == 0 // Check if a number is even (code line)
```

Every single function should have proper documentation, including a description, author tag, param tag, and returns tag.

#### Examples

```java
/**
* Add two integers
* @author: Caleb Cavilla
* @param a the first integer to be added
* @param b the second integer to be added
* @return the calculated sum of the integers as an integer
*/
public int add(int a, int b){}
```

## TO-DO LIST
