def calculator():
    num1 = int(input ("Please pick a number. "))
    num2 = int(input ("Please pick a second number. "))
    oper = input ("Would you like to *,/,+,-? ")
    if (oper == "+"):
        print (num1 + num2)
    elif (oper == "/"):
        print (num1/num2)
    elif (oper == "*"):
        print (num1*num2)
    else:
        print (num1 - num2)
