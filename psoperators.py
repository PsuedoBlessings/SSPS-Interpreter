from colors import *
from psexpressions import StringValue, DictionaryValue, CodeArrayValue

class PSOperators:
    def __init__(self, scoperule):
        #stack variables
        self.opstack = []  #assuming top of the stack is the end of the list
        self.dictstack = []  #assuming top of the stack is the end of the list
        self.isstatic = False #assuming that it is dynamic
        if(scoperule == "static"): # checking if the PSOperator needs to be static 
            self.isstatic = True
        # The environment that the REPL evaluates expressions in.
        # Uncomment this dictionary in part2
        self.builtin_operators = {
            "add":self.add,
            "sub":self.sub,
            "mul":self.mul,
            "mod":self.mod,
            "eq":self.eq,
            "lt": self.lt,
            "gt": self.gt,
            "dup": self.dup,
            "exch":self.exch,
            "pop":self.pop,
            "copy":self.copy,
            "count": self.count,
            "clear":self.clear,
            "stack":self.stack,
            "dict":self.psDict,
            "string":self.string,
            "length":self.length,
            "get":self.get,
            "put":self.put,
            "getinterval":self.getinterval,
            "putinterval":self.putinterval,
            "search" : self.search,
            "begin":self.begin,
            "end":self.end,
            "def":self.psDef,
            "if":self.psIf,
            "ifelse":self.psIfelse,
            "for":self.psFor
        }
    #------- Operand Stack Helper Functions --------------
    
    """
        Helper function. Pops the top value from opstack and returns it.
    """
    def opPop(self):
        if len(self.opstack) > 0:
            x = self.opstack[len(self.opstack) - 1]
            self.opstack.pop(len(self.opstack) - 1)
            return x
        else:
            print("Error: opPop - Operand stack is empty")

    """
       Helper function. Pushes the given value to the opstack.
    """
    def opPush(self,value):
        self.opstack.append(value)

    #------- Dict Stack Helper Functions --------------
    """
       Helper function. Pops the top dictionary from dictstack and returns it.
    """  
    def dictPop(self):
            if len(self.dictstack) > 0:
                x = self.dictstack[len(self.dictstack) - 1]
                self.dictstack.pop(len(self.dictstack) - 1)
                return x
            else:
                print("Error: dictPop - Dictionary stack is empty")

    """
       Helper function. Pushes the given dictionary onto the dictstack. 
    """   
    def dictPush(self,d):
        if (self.isstatic):
                    self.dictstack.append((d))
        else:
            if(isinstance(d, dict)):
                self.dictstack.append(d)
            elif(isinstance(d, DictionaryValue)):
                self.dictstack.append(d.value)
            else:
                print("Error: dictPush - Operand is not a DictionaryValue")

    """
       Helper function. Adds name:value pair to the top dictionary in the dictstack.
       (Note: If the dictstack is empty, first adds an empty dictionary to the dictstack then adds the name:value to that. 
    """  
    def define(self,name, value):
        if(self.isstatic):
            if(len(self.dictstack) > 0): # checking if there's already a dictionary in the dictionary stack
                ActionRecall = self.dictPop()
                ActionRecall[1][name] = value
                self.dictPush(ActionRecall) # it will pop the top dictionary and add the name:value pair, then it will push back the dictionary
            else: # There's no dictionaries in the dictionary stack
                self.dictPush((0,{})) # pushes an empty dictionary
                ActionRecall = self.dictPop()
                ActionRecall[1][name] = value
                self.dictPush(ActionRecall) # it will pop the top dictionary and add the name:value pair, then it will push back the dictionary
        else:
            if(len(self.dictstack) > 0): # checking if there's already a dictionary in the dictionary stack
                NewDictionary = self.dictPop()
                NewDictionary[name] = value
                self.dictPush(NewDictionary) # it will pop the top dictionary and add the name:value pair, then it will push back the dictionary
            else: # There's no dictionaries in the dictionary stack
                self.dictPush(DictionaryValue({})) # pushes an empty dictionary
                NewDictionary = self.dictPop()
                NewDictionary[name] = value
                self.dictPush(NewDictionary) # refer to line 87

    """
       Helper function. Searches the dictstack for a variable or function and returns its value. 
       (Starts searching at the top of the dictstack; if name is not found returns None and prints an error message.
        Make sure to add '/' to the begining of the name.)
    """
    def lookup(self,name):
        if (self.isstatic):
            self.StaticLink(len(name ,self.dictstack) - 1)

        else:    
            if(len(self.dictstack) > 0): # checking that there is something in the dictionary stack
                DictArray= []
                
                for x in range(len(self.dictstack)):
                    TopDictionary = self.dictPop() # getting the top dictionary
                    if ('/' + name) in TopDictionary: #checking if the name is in the dictionary
                        self.dictPush(TopDictionary) 
                        for dictionary in DictArray: # pushing all the other dictionaries back
                            self.dictPush(dictionary) 
                        return TopDictionary[('/' + name)]
                    else: # couldn't find the name
                        DictArray.append(TopDictionary)
                # if the for loop ends before finding the name then it go to our error case
                print("Error: lookup - Could not find name in Dictionary Stack")
                for dictionary in DictArray: # pushing all the other dictionaries back
                    self.dictPush(dictionary)
                return None 
            else: # There's nothing in the dictionary stack
                print("Error: lookup - Dictionary Stack is Empty")
    
    #------- Arithmetic Operators --------------

    """
       Pops 2 values from opstack; checks if they are numerical (int); adds them; then pushes the result back to opstack. 
    """  
    def add(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op1 + op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: add expects 2 operands")

    """
       Pops 2 values from opstack; checks if they are numerical (int); subtracts them; and pushes the result back to opstack. 
    """ 
    def sub(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op2 - op1)
            else:
                print("Error: sub - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: sub expects 2 operands")

    """
        Pops 2 values from opstack; checks if they are numerical (int); multiplies them; and pushes the result back to opstack. 
    """
    def mul(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op2 * op1)
            else:
                print("Error: mul - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: mul expects 2 operands")

    """
        Pops 2 values from stack; checks if they are int values; calculates the remainder of dividing the bottom value by the top one; 
        pushes the result back to opstack.
    """
    def mod(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op2 % op1)
            else:
                print("Error: mod - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: mod expects 2 operands")

    """ Pops 2 values from stacks; if they are equal pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StringValue values, compares the `value` attributes of the StringValue objects;
          - if they are DictionaryValue objects, compares the objects themselves (i.e., ids of the objects).
        """
    def eq(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            TorF = False
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)): # comparing integers
                if op1 == op2:
                    TorF = True
            elif (isinstance(op1, bool) and isinstance(op2, bool)): # comparing Booleans
                if op1 == op2:
                    TorF = True
            elif (isinstance(op1, StringValue) and isinstance(op2, StringValue)): #comparing StringsVaules
                if op1.value == op2.value:
                    TorF = True
            elif (isinstance(op1, DictionaryValue) and isinstance(op2, DictionaryValue)): #comparing DictionaryValues
                if id(op1) == id(op2):
                    TorF = True
            else:
                print("Error: eq - one of the operands is not the same type")
                self.opPush(op1)
                self.opPush(op2)
                pass
            self.opPush(TorF)            
        else:
            print("Error: eq expects 2 operands")

    """ Pops 2 values from stacks; if the bottom value is less than the second, pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StringValue values, compares the `value` attributes of them;
          - if they are DictionaryValue objects, compares the objects themselves (i.e., ids of the objects).
    """  
    def lt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            TorF = False
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)): # comparing integers
                if op1 > op2:
                    TorF = True
            elif (isinstance(op1, bool) and isinstance(op2, bool)): # comparing Booleans
                if op1 > op2:
                    TorF = True
            elif (isinstance(op1, StringValue) and isinstance(op2, StringValue)): #comparing StringsVaules
                if op1.value > op2.value:
                    TorF = True
            elif (isinstance(op1, DictionaryValue) and isinstance(op2, DictionaryValue)): #comparing DictionaryValues
                if id(op1) > id(op2):
                    TorF = True
            else:
                print("Error: lt - one of the operands is not the same type as the other")
                self.opPush(op1)
                self.opPush(op2)
                pass
            self.opPush(TorF)            
        else:
            print("Error: lt expects 2 operands")


    """ Pops 2 values from stacks; if the bottom value is greater than the second, pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StringValue values, compares the `value` attributes of them;
          - if they are DictionaryValue objects, compares the objects themselves (i.e., ids of the objects).
    """  
    def gt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            TorF = False
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)): # comparing integers
                if op1 < op2:
                    TorF = True
            elif (isinstance(op1, bool) and isinstance(op2, bool)): # comparing Booleans
                if op1 < op2:
                    TorF = True
            elif (isinstance(op1, StringValue) and isinstance(op2, StringValue)): #comparing StringsVaules
                if op1.value < op2.value:
                    TorF = True
            elif (isinstance(op1, DictionaryValue) and isinstance(op2, DictionaryValue)): #comparing DictionaryValues
                if id(op1) < id(op2):
                    TorF = True
            else:
                print("Error: lt - one of the operands is not the same type as the other")
                self.opPush(op1)
                self.opPush(op2)
                pass
            self.opPush(TorF)            
        else:
            print("Error: lt expects 2 operands")

    #------- Stack Manipulation and Print Operators --------------
    """
       This function implements the Postscript "pop operator". Calls self.opPop() to pop the top value from the opstack and discards the value. 
    """
    def pop (self):
        if (len(self.opstack) > 0):
            self.opPop()
        else:
            print("Error: pop - not enough arguments")

    """
       Prints the opstack and dictstack. The end of the list is the top of the stack. 
    """
    def stack(self):
        if(self.isstatic):
            print(OKGREEN+"**opstack**")
            for item in reversed(self.opstack):
                print(item)
            print("-----------------------"+CEND)
            print(RED+"**dictstack**")
            for item in reversed(self.dictstack):
                print(item)
            print("-----------------------"+ CEND)
        else:
            print(OKGREEN+"**opstack**")
            for item in reversed(self.opstack):
                print(item)
            print("-----------------------"+CEND)
            print(RED+"**dictstack**")
            for item in reversed(self.dictstack):
                print(item)
            print("-----------------------"+ CEND)


    """
       Copies the top element in opstack.
    """
    def dup(self):
        if (len(self.opstack) > 0):
            element = self.opPop()
            # we push the element twice because we popped the original element
            self.opPush(element)
            self.opPush(element)
        else:
            print("Error: dup - not enough arguments")

    """
       Pops an integer count from opstack, copies count number of values in the opstack. 
    """
    def copy(self):
        if (len(self.opstack) > 0):
            count = self.opPop()
            stack = []
            if (len(self.opstack) > count - 1):
                while count != 0:
                    count -= 1
                    stack.append(self.opPop())
                stack += stack # making sure to also add the original values back as well
                for element in reversed(stack):
                    self.opPush(element)
            elif (count == 0):
                pass
            else:
                print("Error: copy - not enough arguments")
        else:
            print("Error: copy - not enough arguments")

    """
        Counts the number of elements in the opstack and pushes the count onto the top of the opstack.
    """
    def count(self):
        self.opPush(len(self.opstack))

    """
       Clears the opstack.
    """
    def clear(self):
        for element in range(len(self.opstack)):
            self.opPop()
        
    """
       swaps the top two elements in opstack
    """
    def exch(self):
        if (len(self.opstack) >= 2):
            stack = []
            for element in range(2):
                stack.append(self.opPop())
            for element in stack:
                self.opPush(element)
        else:
            print ("Error: exch - not enough arguments")


    # ------- String and Dictionary creator operators --------------

    """ Creates a new empty string  pushes it on the opstack.
    Initializes the characters in the new string to \0 , i.e., ascii NUL """
    def string(self):
        if(len(self.opstack) > 0): # checking if theres another value
            size = self.opPop()
            if(isinstance(size, int)):
                String = ''
                for count in range(size):
                    String += '\0'
                self.opPush(StringValue('(' + String + ')'))
            else: # size isn't an integer
                self.opPush(size)
                print("Error: string - Operand is not an integer")
        else: # there's no other value
            print("Error: string - Not enough arguements")
    
    """Creates a new empty dictionary  pushes it on the opstack """
    def psDict(self):
        self.opPop()
        emptydictionary = DictionaryValue({})
        self.opPush(emptydictionary)

    # ------- String and Dictionary Operators --------------
    """ Pops a string or dictionary value from the operand stack and calculates the length of it. Pushes the length back onto the stack.
       The `length` method should support both DictionaryValue and StringValue values.
    """
    def length(self):
        if(len(self.opstack) > 0): # making sure there is atleast one value in there
            StrDictValue = self.opPop()
            if (isinstance(StrDictValue, StringValue)): # checking if the operand popped is either a StringValue
                self.opPush(StrDictValue.length() - 2)
            elif(isinstance(StrDictValue, DictionaryValue)): # checking if the operand popped is either a DictionaryValue
                self.opPush(StrDictValue.length())
            else:
                self.opPush(StrDictValue) # pushing back the original value as the operator was not able to compute
                print ("Error: length - the top operand is niether a DictionaryValue or StringValue")
        else:
            print ("Error: length - not enough arguements")


    """ Pops either:
         -  "A (zero-based) index and an StringValue value" from opstack OR 
         -  "A `name` (i.e., a key) and DictionaryValue value" from opstack.  
        If the argument is a StringValue, pushes the ascii value of the the character in the string at the index onto the opstack;
        If the argument is an DictionaryValue, gets the value for the given `name` from DictionaryValue's dictionary value and pushes it onto the opstack
    """
    def get(self):
        if(len(self.opstack) >= 2): # making sure there's enough arguements
            IndexOrName = self.opPop()
            StrDictValue = self.opPop()
            if(isinstance(StrDictValue, StringValue)): # checking if the second operand is a StringValue
                if(isinstance(IndexOrName, int)): # checking if the first operand is a int/index
                    if((len(StrDictValue.value) - 2) > IndexOrName): # checking that the index is smaller than the string
                        self.opPush(ord(StrDictValue.value[IndexOrName + 1]))
                    else:
                        print ("Error: get - index is too large for string")
                        self.opPush(StrDictValue)
                        self.opPush(IndexOrName)
                else:
                    print("Error: get - There are no Index/Integer")
                    self.opPush(StrDictValue)
                    self.opPush(IndexOrName)
            elif(isinstance(StrDictValue, DictionaryValue)): # checking if the second operand is a DictionaryValue
                if(StrDictValue.value.get(IndexOrName) != None): # checking if the first operand is in the dictionary stack
                    self.opPush(StrDictValue.value.get(IndexOrName))
                else:
                    print ("Error: get - `name` could not be looked up in first operand")
                    self.opPush(StrDictValue)
                    self.opPush(IndexOrName)
            else:
                print("Error: get - operand is not an index or `name`")
                self.opPush(StrDictValue)
                self.opPush(IndexOrName)
        else:
            print("Error: get - not enough arguements")
    """
    Pops either:
    - "An `item`, a (zero-based) `index`, and an StringValue value from  opstack", OR
    - "An `item`, a `name`, and a DictionaryValue value from  opstack". 
    If the argument is a StringValue, replaces the character at `index` of the StringValue's string with the character having the ASCII value of `item`.
    If the argument is an DictionaryValue, adds (or updates) "name:item" in DictionaryValue's dictionary `value`.
    """
    def put(self):
        if(len(self.opstack) >= 3): # making sure there's enough arguements
            Item = self.opPop()
            IndexOrName = self.opPop()
            StrDictValue = self.opPop()
            if(isinstance(StrDictValue, StringValue)): # checking if the second operand is a StringValue
                if(isinstance(IndexOrName, int)): # checking if the first operand is a int/index
                    if((len(StrDictValue.value) - 2) > IndexOrName): # checking that the index is smaller than the string
                        if(isinstance(Item, int)): # checking if Item is an integer
                            StrDictValue.value = StrDictValue.value[:(IndexOrName+1)] + chr(Item) + StrDictValue.value[(IndexOrName+1)+1:]
                        else:
                            ("Error: get - `Item` is not an integer")
                            self.opPush(Item)
                            self.opPush(StrDictValue)
                            self.opPush(IndexOrName)
                    else:
                        print ("Error: get - index is too large for string")
                        self.opPush(Item)
                        self.opPush(StrDictValue)
                        self.opPush(IndexOrName)
                else:
                    print("Error: put - operand is not a Integer")
            elif(isinstance(StrDictValue, DictionaryValue)): # checking if the second operand is a DictionaryValue
                StrDictValue.value[IndexOrName] = Item
            else:
                print("Error: get - operand is neither a StringValue or Dictionary")
                self.opPush(Item)
                self.opPush(StrDictValue)
                self.opPush(IndexOrName)
        else:
            print("Error: get - not enough arguements")

    """
    getinterval is a string only operator, i.e., works only with StringValue values. 
    Pops a `count`, a (zero-based) `index`, and an StringValue value from  opstack, and 
    extracts a substring of length count from the `value` of StringValue starting from `index`,
    pushes the substring back to opstack as a StringValue value. 
    """ 
    def getinterval(self):
        if(len(self.opstack) >= 3):
            count = self.opPop()
            index = self.opPop()
            StrVal = self.opPop()
            if(isinstance(StrVal, StringValue)): # checking if StrVal is a StringValue
                if(isinstance(count, int) and (isinstance(index, int) and (index >= 0))): # checking if count and index is an int and index is equal or biger than 0
                    if((StrVal.length()-2) > (index) and (StrVal.length()-2) > (index+count+1)):
                        self.opPush(StringValue('('+StrVal.value[index+1:index+1+count]+')'))
                    else:
                        print("Error: getinterval - Operands are too high to evalute slice")
                        self.opPush(StrVal)
                        self.opPush(index)
                        self.opPush(count)
                else: # Either Count or Index isn't an integer, or Index isn't equal or more than 0
                    print("Error: getinterval - Operand are either not an Integer or Index is less than 0")
                    self.opPush(StrVal)
                    self.opPush(index)
                    self.opPush(count)
            else: # StrVal is not a StringValue
                print("Error: getinterval - Operand is not a StringValue")
                self.opPush(StrVal)
                self.opPush(index)
                self.opPush(count)

    """
    putinterval is a string only operator, i.e., works only with StringValue values. 
    Pops a StringValue value, a (zero-based) `index`, a `substring` from  opstack, and 
    replaces the slice in StringValue's `value` from `index` to `index`+len(substring)  with the given `substring`s value. 
    """
    def putinterval(self):
        if(len(self.opstack) >= 3):
            substring = self.opPop()
            index = self.opPop()
            StrVal = self.opPop()
            if(isinstance(StrVal, StringValue)): # checking if StrVal is a StringValue
                if(isinstance(substring, StringValue) and (isinstance(index, int) and (index >= 0))): # checking if count and index is an int and index is equal or biger than 0
                    if((StrVal.length()-2) > (index) and (StrVal.length()-2) >= (index+(substring.length() - 2))):
                        StrVal.value = StrVal.value[:index+1]+substring.value[1:-1]+StrVal.value[index+substring.length()-1:]
                    else:
                        print("Error: getinterval - Operands are too high to evalute slice")
                        self.opPush(StrVal)
                        self.opPush(index)
                        self.opPush(substring)
                else: # Either Count or Index isn't an integer, or Index isn't equal or more than 0
                    print("Error: getinterval - Operand are either not an Integer or StringValue, or Index is less than 0")
                    self.opPush(StrVal)
                    self.opPush(index)
                    self.opPush(substring)
            else: # StrVal is not a StringValue
                print("Error: getinterval - Operand is not a StringValue")
                self.opPush(StrVal)
                self.opPush(index)
                self.opPush(substring)

    """
    search is a string only operator, i.e., works only with StringValue values. 
    Pops two StringValue values: delimiter and inputstr
    if delimiter is a sub-string of inputstr then, 
       - splits inputstr at the first occurence of delimeter and pushes the splitted strings to opstack as StringValue values;
       - pushes True 
    else,
        - pushes  the original inputstr back to opstack
        - pushes False
    """
    def search(self):
        if(len(self.opstack) >= 2):
            delimiter = self.opPop()
            inputstr = self.opPop()
            if(isinstance(inputstr, StringValue) and isinstance(delimiter, StringValue)): # making sure both of the operands are strings
                delimiterString = delimiter.value.replace("(", "")
                inputstrString = inputstr.value.replace("(", "")
                delimiterString = delimiterString.replace(")", "")
                inputstrString = inputstrString.replace(")", "")
                if delimiterString in inputstrString: # looking for the delimiter in inputstr
                    index = inputstrString.find(delimiterString) #index will be the starting index of the delimiter
                    self.opPush(StringValue('(' + inputstrString[(index+len(delimiterString)):]+ ')')) # this will push the string at the back of our delimiter and add back the parenthesis
                    self.opPush(delimiter)
                    self.opPush(StringValue('(' + inputstrString[:index] + ')')) # this will push the string infront of our delimiter and add back the parenthesis
                    self.opPush(True)
                        
                else:
                    self.opPush(inputstr)
                    self.opPush(False)
            else:
                print("Error: search - either operands are not strings")
                self.opPush(inputstr)
                self.opPush(delimiter)
        else:
            print("Error: search - not enough arguements")


    # ------- Operators that manipulate the dictstact --------------
    """ begin operator
        Pops a DictionaryValue value from opstack and pushes it's `value` to the dictstack."""
    def begin(self):
        if(len(self.opstack) > 0):
            DictVal = self.opPop()
            if(isinstance(DictVal, DictionaryValue)):
                self.dictPush(DictVal.value)
            else:
                print("Error: begin - operand is not a DictionaryValue")
                self.opPush(DictVal)
        else:
            print("Error: begin - Not enough arguements")

    """ end operator
        Pops the top dictionary from dictstack."""
    def end(self):
        if(len(self.dictstack) > 0):
           self.dictPop()
        else:
            print("Error: end - Not enough arguements")
        
    """ Pops a name and a value from stack, adds the definition to the dictionary at the top of the dictstack. """
    def psDef(self):
        if(len(self.opstack) >= 2):
            value = self.opPop()
            name = self.opPop()
            if(isinstance(name, str) and ('/' in name)):
                self.define(name, value)
            else:
                print("Error: psDef - The second operand is not a name")
                self.opPush(name)
                self.opPush(value)
        else:
            print("Error: psDef - Not enough arguements")
    # ------- if/ifelse Operators --------------
    """ if operator
        Pops a CodeArrayValue object and a boolean value, if the value is True, executes (applies) the code array by calling apply.
       Will be completed in part-2. 
    """
    def psIf(self):
        CodeArrVal = self.opPop()
        Boolean = self.opPop()
        if(self.isstatic):
            if Boolean:
                CodeArrVal.apply(self, len(self.dictstack)-1)
        else:
            if Boolean:
                CodeArrVal.apply(self, None)

    """ ifelse operator
        Pops two CodeArrayValue objects and a boolean value, if the value is True, executes (applies) the bottom CodeArrayValue otherwise executes the top CodeArrayValue.
        Will be completed in part-2. 
    """
    def psIfelse(self):
        CodeArrVal = self.opPop()
        CodeArrVal2 = self.opPop()
        Boolean = self.opPop()
        if(self.isstatic):
            if Boolean:
                CodeArrVal2.apply(self, len(self.dictstack)-1)
            else:
                CodeArrVal.apply(self, len(self.dictstack)-1)
        else:
            if Boolean:
                CodeArrVal2.apply(self, None)
            else:
                CodeArrVal.apply(self, None)
        

    #------- Loop Operators --------------
    """
       Implements for operator.   
       Pops a CodeArrayValue object, the end index (end), the increment (inc), and the begin index (begin) and 
       executes the code array for all loop index values ranging from `begin` to `end`. 
       Pushes the current loop index value to opstack before each execution of the CodeArrayValue. 
       Will be completed in part-2. 
    """ 
    def psFor(self):
        CodeArrVal = self.opPop()
        end = self.opPop()
        inc = self.opPop()
        begin = self.opPop()
        if(self.isstatic):
            for index in range(begin, end + inc, inc):
                self.opPush(index)
                CodeArrVal.apply(self, len(self.dictstack)-1)
        else:
            for index in range(begin, end + inc, inc):
                self.opPush(index)
                CodeArrVal.apply(self, None)

    """ Cleans both stacks. """      
    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []

    """ Will be needed for part2"""
    def cleanTop(self):
        if len(self.opstack)>1:
            if self.opstack[-1] is None:
                self.opstack.pop()

    #------- Static Operators --------------
    def StaticLink(self, name, index): # static 
        if('/'+name in self.dictstack[index][1]):
            return index
        elif(index == 0):
            return 0
        else:
            return self.StaticLink(name, self.dictstack[index][0])
    
    def StaticLookup(self, name, index): # 
        if('/'+name in self.dictstack[index][1]):
            return self.dictstack[index][0]
        elif(index == 0):
            return None
        else:
            return self.StaticLookup(name, self.dictstack[index][0])
