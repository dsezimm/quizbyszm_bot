import os
import sys
import random
import time
import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'quiz_django'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_django.settings')
django.setup()

from quiz_app.models import UserQuery, QuizResult
import telebot
from telebot import types

BOT_TOKEN = os.getenv('BOT_TOKEN', '8793268428:AAFPbARqJ6PcECDn5lQ8a41hvH18gKoxyg4')
bot = telebot.TeleBot(BOT_TOKEN)

sessions = {}
QUESTIONS_PER_QUIZ = 15



QUESTIONS = {
    'python': [

        # TOPIC: Basic Syntax 
        {
            "topic": "Basic Syntax",
            "question": "Which function prints text in Python?",
            "options": {"A": "echo()", "B": "print()", "C": "write()", "D": "output()"},
            "answer": "B",
            "hint": "This function is most commonly used for output 🖨️",
            "explanation": "print() is the standard output function. echo() is PHP, write() is used in other languages."
        },
        {
            "topic": "Basic Syntax",
            "question": "How do you write a comment in Python?",
            "options": {"A": "// text", "B": "/* text */", "C": "# text", "D": "-- text"},
            "answer": "C",
            "hint": "The hash symbol # ",
            "explanation": "# is a single-line comment in Python. // is used in Java/JS, -- in SQL."
        },
        {
            "topic": "Basic Syntax",
            "question": "What is the exponentiation operator in Python?",
            "options": {"A": "^", "B": "**", "C": "^^", "D": "pow"},
            "answer": "B",
            "hint": "Two multiplication symbols side by side ",
            "explanation": "** is the exponentiation operator. Note: ^ in Python is bitwise XOR, not exponentiation!"
        },
        {
            "topic": "Basic Syntax",
            "question": "What does the // operator do?",
            "options": {"A": "Comment", "B": "Regular division", "C": "Integer division", "D": "Remainder"},
            "answer": "C",
            "hint": "Two slashes = division without remainder ",
            "explanation": "// is floor division. 7 // 2 = 3 (the fractional part is discarded)."
        },
        {
            "topic": "Basic Syntax",
            "question": "What does 10 % 3 return?",
            "options": {"A": "3", "B": "1", "C": "0", "D": "2"},
            "answer": "B",
            "hint": "% — remainder of division ",
            "explanation": "10 / 3 = 3 with remainder 1. So 10 % 3 = 1."
        },
        {
            "topic": "Basic Syntax",
            "question": "How do you check the type of a variable?",
            "options": {"A": "typeof(x)", "B": "x.type()", "C": "type(x)", "D": "gettype(x)"},
            "answer": "C",
            "hint": "Built-in function, 4 letters ",
            "explanation": "type(x) returns the type. For example, type(5) → <class 'int'>."
        },
        {
            "topic": "Basic Syntax",
            "question": "What data type does input() return?",
            "options": {"A": "int", "B": "float", "C": "str", "D": "bool"},
            "answer": "C",
            "hint": "The user types text ",
            "explanation": "input() always returns str. To get a number you need: int(input())."
        },
        {
            "topic": "Basic Syntax",
            "question": "What is an f-string?",
            "options": {"A": "A fast string", "B": "A string with variables inside {}", "C": "A file type", "D": "A function"},
            "answer": "B",
            "hint": "f before the quotes = variables inside {} ",
            "explanation": "f'Hello {name}!' inserts variable values directly into the string. Introduced in Python 3.6."
        },

        # TOPIC: Data Types
        {
            "topic": "Data Types",
            "question": "How do you create an empty dictionary?",
            "options": {"A": "[]", "B": "()", "C": "{}", "D": "set()"},
            "answer": "C",
            "hint": "Curly braces with no elements ",
            "explanation": "{} creates an empty dict. [] is a list, () is a tuple, set() is an empty set."
        },
        {
            "topic": "Data Types",
            "question": "How does tuple differ from list?",
            "options": {"A": "Stores only numbers", "B": "Tuple is immutable", "C": "Tuple is faster", "D": "No difference"},
            "answer": "B",
            "hint": "One of them cannot be changed",
            "explanation": "tuple is immutable. Once created, you cannot add or remove elements."
        },
        {
            "topic": "Data Types",
            "question": "What does a set store?",
            "options": {"A": "Ordered elements", "B": "Duplicates", "C": "Unique elements", "D": "Key-value pairs"},
            "answer": "C",
            "hint": "No duplicates allowed!",
            "explanation": "set stores only unique elements. {1,2,2,3} automatically becomes {1,2,3}."
        },
        {
            "topic": "Data Types",
            "question": "How do you convert the string '42' to an integer?",
            "options": {"A": "str(42)", "B": "float('42')", "C": "int('42')", "D": "num('42')"},
            "answer": "C",
            "hint": "Use the type name as a function ",
            "explanation": "int('42') = 42. float('42') = 42.0. str(42) = '42' (the reverse)."
        },
        {
            "topic": "Data Types",
            "question": "What does bool('') return?",
            "options": {"A": "True", "B": "False", "C": "None", "D": "Error"},
            "answer": "B",
            "hint": "An empty string equals nothing ",
            "explanation": "An empty string is a falsy value. bool('') = False. Any non-empty string = True."
        },
        {
            "topic": "Data Types",
            "question": "How do you access a value in a dictionary by key?",
            "options": {"A": "d.get_value('key')", "B": "d['key']", "C": "d.key", "D": "d(key)"},
            "answer": "B",
            "hint": "Square brackets with the key name ",
            "explanation": "d['key'] is the main way. d.get('key') is safer — it won't raise an error if the key is missing."
        },
        {
            "topic": "Data Types",
            "question": "Which data type is immutable?",
            "options": {"A": "list", "B": "dict", "C": "set", "D": "tuple"},
            "answer": "D",
            "hint": "It cannot be changed after creation ",
            "explanation": "tuple is immutable. list, dict, set are mutable."
        },

        # TOPIC: Functions 
        {
            "topic": "Functions",
            "question": "What keyword is used to define a function?",
            "options": {"A": "func", "B": "function", "C": "def", "D": "fun"},
            "answer": "C",
            "hint": "Short for 'define' ",
            "explanation": "def stands for define. In JS/PHP it's function, in Go it's func."
        },
        {
            "topic": "Functions",
            "question": "What does return do?",
            "options": {"A": "Prints a value", "B": "Terminates the program", "C": "Returns a value from a function", "D": "Creates a variable"},
            "answer": "C",
            "hint": "Send the result back ",
            "explanation": "return sends a value back and ends the function. Without return, the function returns None."
        },
        {
            "topic": "Functions",
            "question": "What is a lambda?",
            "options": {"A": "A loop", "B": "An anonymous function", "C": "A class", "D": "A module"},
            "answer": "B",
            "hint": "A small function with no name ",
            "explanation": "lambda is an anonymous function. Example: add = lambda x, y: x + y."
        },
        {
            "topic": "Functions",
            "question": "What is *args?",
            "options": {"A": "A required argument", "B": "A dictionary of arguments", "C": "An arbitrary number of arguments", "D": "A return value"},
            "answer": "C",
            "hint": "The asterisk means any number ",
            "explanation": "*args accepts any number of positional arguments and collects them into a tuple."
        },
        {
            "topic": "Functions",
            "question": "What is **kwargs?",
            "options": {"A": "A list", "B": "Named arguments as a dictionary", "C": "Required arguments", "D": "Exponentiation"},
            "answer": "B",
            "hint": "Double asterisk = dictionary ",
            "explanation": "**kwargs collects named arguments into a dict. f(a=1, b=2) → kwargs = {'a':1,'b':2}."
        },
        {
            "topic": "Functions",
            "question": "What does a function return if it has no return statement?",
            "options": {"A": "0", "B": "False", "C": "None", "D": "An error"},
            "answer": "C",
            "hint": "Nothing = None in Python ",
            "explanation": "If a function has no return statement, Python automatically returns None."
        },

        # TOPIC: Lists 
        {
            "topic": "Lists",
            "question": "Which method adds an element to the end of a list?",
            "options": {"A": "add()", "B": "insert()", "C": "append()", "D": "push()"},
            "answer": "C",
            "hint": "Append = attach to the end ",
            "explanation": "append() adds one element to the end. extend() adds multiple. insert(i, x) adds at position i."
        },
        {
            "topic": "Lists",
            "question": "What does [1,2,3][1] return?",
            "options": {"A": "1", "B": "2", "C": "3", "D": "Error"},
            "answer": "B",
            "hint": "Indexing starts at zero! 0️",
            "explanation": "[0]=1, [1]=2, [2]=3. Indexing starts at 0."
        },
        {
            "topic": "Lists",
            "question": "What does pop() do?",
            "options": {"A": "Adds an element", "B": "Removes and returns the last element", "C": "Clears the list", "D": "Copies the list"},
            "answer": "B",
            "hint": "Pull out and remove ",
            "explanation": "pop() removes and returns the last element. pop(i) removes by index i."
        },
        {
            "topic": "Lists",
            "question": "What does [1,2,3,4][0:2] return?",
            "options": {"A": "[1,2,3]", "B": "[1,2]", "C": "[2,3]", "D": "[0,2]"},
            "answer": "B",
            "hint": "The end index is not included ",
            "explanation": "[0:2] — from index 0 up to (not including) 2. Elements [0]=1, [1]=2. Result: [1,2]."
        },
        {
            "topic": "Lists",
            "question": "How do you sort a list in descending order?",
            "options": {"A": "list.sort()", "B": "list.sort(reverse=True)", "C": "sorted(list, asc=False)", "D": "list.reverse_sort()"},
            "answer": "B",
            "hint": "reverse=True = descending ",
            "explanation": "sort(reverse=True) sorts in descending order. sort() or sort(reverse=False) — ascending."
        },

        # TOPIC: Loops 
        {
            "topic": "Loops",
            "question": "What does range(5) produce?",
            "options": {"A": "[1,2,3,4,5]", "B": "[0,1,2,3,4]", "C": "[0,1,2,3,4,5]", "D": "Error"},
            "answer": "B",
            "hint": "Starts at 0, end is not included ",
            "explanation": "range(5) = 0,1,2,3,4. Always starts at 0 unless specified otherwise."
        },
        {
            "topic": "Loops",
            "question": "What does break do?",
            "options": {"A": "Skips an iteration", "B": "Exits the loop", "C": "Restarts the loop", "D": "Pauses execution"},
            "answer": "B",
            "hint": "Break = exit ",
            "explanation": "break immediately exits the loop. continue skips the current iteration."
        },
        {
            "topic": "Loops",
            "question": "What does enumerate() do?",
            "options": {"A": "Counts elements", "B": "Gives index and value together", "C": "Reverses a list", "D": "Sorts a list"},
            "answer": "B",
            "hint": "Index + value together ",
            "explanation": "enumerate(['a','b']) gives (0,'a'), (1,'b'). Useful when you need both index and value."
        },
        {
            "topic": "Loops",
            "question": "Which loop runs while a condition is true?",
            "options": {"A": "for", "B": "while", "C": "loop", "D": "repeat"},
            "answer": "B",
            "hint": "While the condition holds ",
            "explanation": "while runs as long as the condition is True. for iterates over elements of a collection."
        },
        {
            "topic": "Loops",
            "question": "What will: for i in range(3): print(i) output?",
            "options": {"A": "1 2 3", "B": "0 1 2 3", "C": "0 1 2", "D": "1 2"},
            "answer": "C",
            "hint": "range(3) = 0,1,2 ",
            "explanation": "range(3) generates 0, 1, 2. print will output each value."
        },

        # TOPIC: OOP 
        {
            "topic": "OOP",
            "question": "What keyword is used to create a class?",
            "options": {"A": "object", "B": "struct", "C": "class", "D": "type"},
            "answer": "C",
            "hint": "Same as in Java ",
            "explanation": "class is the keyword for creating a class in Python."
        },
        {
            "topic": "OOP",
            "question": "What is __init__?",
            "options": {"A": "Destructor", "B": "Constructor", "C": "Print method", "D": "Static method"},
            "answer": "B",
            "hint": "Called when an object is created ",
            "explanation": "__init__ is the constructor, called automatically when an object is created."
        },
        {
            "topic": "OOP",
            "question": "What does self mean?",
            "options": {"A": "Current module", "B": "Parent class", "C": "Reference to the current object", "D": "Static method"},
            "answer": "C",
            "hint": "The object itself ",
            "explanation": "self is a reference to the current instance of the class. It is the first parameter of every method."
        },
        {
            "topic": "OOP",
            "question": "What is inheritance?",
            "options": {"A": "Copying a class", "B": "A child class receives properties of the parent", "C": "Deleting a class", "D": "Hiding data"},
            "answer": "B",
            "hint": "The child takes from the parent ",
            "explanation": "Inheritance allows a child class to use the methods and attributes of the parent class."
        },
        {
            "topic": "OOP",
            "question": "How do you call a parent class method?",
            "options": {"A": "parent.method()", "B": "super().method()", "C": "base.method()", "D": "this.method()"},
            "answer": "B",
            "hint": "super() = parent ",
            "explanation": "super() returns a reference to the parent class. super().__init__() calls the parent constructor."
        },

        # TOPIC: Error Handling 
        {
            "topic": "Error Handling",
            "question": "How do you catch an error in Python?",
            "options": {"A": "if/else", "B": "try/except", "C": "do/while", "D": "catch/throw"},
            "answer": "B",
            "hint": "Try / catch 🎣",
            "explanation": "try contains the code that might raise an error. except handles the error."
        },
        {
            "topic": "Error Handling",
            "question": "What does the finally block do?",
            "options": {"A": "Only runs on error", "B": "Always runs", "C": "Stops the program", "D": "Restarts try"},
            "answer": "B",
            "hint": "Always runs at the end ",
            "explanation": "finally always executes — whether or not an error occurred. Used to close files or connections."
        },
        {
            "topic": "Error Handling",
            "question": "How do you raise a custom error?",
            "options": {"A": "throw Error()", "B": "raise Exception()", "C": "error()", "D": "trigger_error()"},
            "answer": "B",
            "hint": "raise = throw an exception ",
            "explanation": "raise Exception('message') manually raises an exception."
        },
        {
            "topic": "Error Handling",
            "question": "What happens when you divide by zero?",
            "options": {"A": "Returns None", "B": "Returns 0", "C": "ZeroDivisionError", "D": "Infinity"},
            "answer": "C",
            "hint": "A special error type ",
            "explanation": "10 / 0 raises ZeroDivisionError. It should be handled with try/except."
        },
    ],

    'sql': [

        # TOPIC: SELECT 
        {
            "topic": "SELECT",
            "question": "What is the SQL data retrieval operator?",
            "options": {"A": "GET", "B": "FETCH", "C": "SELECT", "D": "RETRIEVE"},
            "answer": "C",
            "hint": "Choose = SELECT ",
            "explanation": "SELECT is the primary query operator. GET and FETCH are not standard SQL commands."
        },
        {
            "topic": "SELECT",
            "question": "How do you select all columns from a table?",
            "options": {"A": "SELECT all FROM t", "B": "SELECT * FROM t", "C": "SELECT % FROM t", "D": "GET * FROM t"},
            "answer": "B",
            "hint": "Asterisk = all ",
            "explanation": "SELECT * means select all columns."
        },
        {
            "topic": "SELECT",
            "question": "What operator filters rows in SQL?",
            "options": {"A": "HAVING", "B": "WHERE", "C": "FILTER", "D": "IF"},
            "answer": "B",
            "hint": "WHERE to look ",
            "explanation": "WHERE filters rows. HAVING filters groups after GROUP BY."
        },
        {
            "topic": "SELECT",
            "question": "How do you sort results in descending order?",
            "options": {"A": "ORDER BY col ASC", "B": "SORT BY col DESC", "C": "ORDER BY col DESC", "D": "ORDER col DOWN"},
            "answer": "C",
            "hint": "DESC = descending ",
            "explanation": "ORDER BY col DESC — descending. ASC — ascending (default)."
        },
        {
            "topic": "SELECT",
            "question": "What does DISTINCT do?",
            "options": {"A": "Sorts", "B": "Groups", "C": "Removes duplicates", "D": "Counts"},
            "answer": "C",
            "hint": "Unique values only ",
            "explanation": "SELECT DISTINCT removes duplicate rows from the result."
        },
        {
            "topic": "SELECT",
            "question": "How do you limit the number of rows returned?",
            "options": {"A": "TOP", "B": "LIMIT", "C": "MAX ROWS", "D": "ROWNUM"},
            "answer": "B",
            "hint": "Restrict = LIMIT ",
            "explanation": "LIMIT n restricts to n rows (MySQL, PostgreSQL, SQLite)."
        },
        {
            "topic": "SELECT",
            "question": "What does LIKE do?",
            "options": {"A": "Compares numbers", "B": "Pattern matching on strings", "C": "Joins tables", "D": "Groups rows"},
            "answer": "B",
            "hint": "Match a pattern ",
            "explanation": "LIKE 'A%' — starts with A. % means any characters, _ means one character."
        },
        {
            "topic": "SELECT",
            "question": "What does BETWEEN do?",
            "options": {"A": "Joins tables", "B": "Filters by a range", "C": "Compares strings", "D": "Groups rows"},
            "answer": "B",
            "hint": "Between two values ",
            "explanation": "WHERE age BETWEEN 18 AND 30 — from 18 to 30 inclusive."
        },

        # TOPIC: Aggregate Functions 
        {
            "topic": "Aggregate Functions",
            "question": "Which function counts rows?",
            "options": {"A": "SUM()", "B": "COUNT()", "C": "TOTAL()", "D": "NUM()"},
            "answer": "B",
            "hint": "COUNT = count ",
            "explanation": "COUNT(*) counts all rows. COUNT(col) — only rows where col is not NULL."
        },
        {
            "topic": "Aggregate Functions",
            "question": "What does MAX() return?",
            "options": {"A": "Average", "B": "Minimum", "C": "Maximum", "D": "Sum"},
            "answer": "C",
            "hint": "MAXimum ",
            "explanation": "MAX(col) returns the maximum value. MIN — minimum, AVG — average, SUM — total."
        },
        {
            "topic": "Aggregate Functions",
            "question": "What does AVG() do?",
            "options": {"A": "Maximum", "B": "Minimum", "C": "Sum", "D": "Average value"},
            "answer": "D",
            "hint": "AVG = Average ",
            "explanation": "AVG(col) returns the arithmetic mean of all values in the column."
        },
        {
            "topic": "Aggregate Functions",
            "question": "When is HAVING used?",
            "options": {"A": "Instead of WHERE", "B": "Filtering groups after GROUP BY", "C": "For sorting", "D": "For JOIN"},
            "answer": "B",
            "hint": "After GROUP BY ",
            "explanation": "HAVING filters groups. WHERE filters rows. WHERE cannot be used with aggregate functions."
        },
        {
            "topic": "Aggregate Functions",
            "question": "What does COUNT(*) count?",
            "options": {"A": "Only non-NULL rows", "B": "All rows including NULL", "C": "Unique rows", "D": "Maximum"},
            "answer": "B",
            "hint": "Asterisk = everything ",
            "explanation": "COUNT(*) counts ALL rows including NULL. COUNT(col) — only non-NULL."
        },
        {
            "topic": "Aggregate Functions",
            "question": "What does SUM() do?",
            "options": {"A": "Counts rows", "B": "Maximum", "C": "Sum of values", "D": "Average"},
            "answer": "C",
            "hint": "SUM = total ",
            "explanation": "SUM(col) adds up all values in the column. Ignores NULL."
        },

        # TOPIC: JOIN 
        {
            "topic": "JOIN",
            "question": "Which JOIN returns only matching rows from both tables?",
            "options": {"A": "LEFT JOIN", "B": "RIGHT JOIN", "C": "INNER JOIN", "D": "FULL JOIN"},
            "answer": "C",
            "hint": "Only the intersection ",
            "explanation": "INNER JOIN — only rows where there is a match in both tables."
        },
        {
            "topic": "JOIN",
            "question": "What does LEFT JOIN return?",
            "options": {"A": "Only the left table", "B": "All rows from the left + matches from the right", "C": "Only matches", "D": "All rows from both"},
            "answer": "B",
            "hint": "The left table is always complete ",
            "explanation": "LEFT JOIN — all rows from the left table. Where there is no match on the right — NULL."
        },
        {
            "topic": "JOIN",
            "question": "What does FULL OUTER JOIN return?",
            "options": {"A": "Only matches", "B": "Only the left table", "C": "Only the right table", "D": "All rows from both tables"},
            "answer": "D",
            "hint": "FULL = complete ",
            "explanation": "FULL OUTER JOIN — all rows from both tables. Where there is no match — NULL."
        },
        {
            "topic": "JOIN",
            "question": "What is a FOREIGN KEY?",
            "options": {"A": "A key from another database", "B": "A key linking tables", "C": "An index", "D": "An encrypted key"},
            "answer": "B",
            "hint": "A reference to another table ",
            "explanation": "FOREIGN KEY references the PRIMARY KEY of another table. Ensures referential integrity."
        },
        {
            "topic": "JOIN",
            "question": "How do you combine results from two SELECT statements?",
            "options": {"A": "JOIN", "B": "MERGE", "C": "UNION", "D": "COMBINE"},
            "answer": "C",
            "hint": "Combining queries ",
            "explanation": "UNION combines results of two SELECT statements. UNION ALL — including duplicates."
        },

        # TOPIC: Data Modification 
        {
            "topic": "Data Modification",
            "question": "How do you add a row to a table?",
            "options": {"A": "ADD INTO t VALUES", "B": "INSERT INTO t VALUES", "C": "PUT INTO t VALUES", "D": "SET INTO t VALUES"},
            "answer": "B",
            "hint": "INSERT = insert ",
            "explanation": "INSERT INTO table (col1, col2) VALUES (val1, val2) — adds a new row."
        },
        {
            "topic": "Data Modification",
            "question": "How do you update data in a table?",
            "options": {"A": "MODIFY t SET col=val", "B": "CHANGE t col=val", "C": "UPDATE t SET col=val", "D": "ALTER t SET col=val"},
            "answer": "C",
            "hint": "UPDATE = update ",
            "explanation": "UPDATE table SET col=value WHERE condition. Without WHERE it updates ALL rows!"
        },
        {
            "topic": "Data Modification",
            "question": "What does DELETE without WHERE do?",
            "options": {"A": "Drops the table", "B": "Deletes all rows", "C": "Does nothing", "D": "Raises an error"},
            "answer": "B",
            "hint": "No condition = deletes everything ",
            "explanation": "DELETE FROM table without WHERE deletes ALL rows! Always use WHERE."
        },
        {
            "topic": "Data Modification",
            "question": "What does DROP TABLE do?",
            "options": {"A": "Clears rows", "B": "Permanently deletes the table", "C": "Creates a copy", "D": "Renames the table"},
            "answer": "B",
            "hint": "Deletes forever ",
            "explanation": "DROP TABLE deletes the table and all its data. Irreversible! DELETE only removes rows."
        },
        {
            "topic": "Data Modification",
            "question": "What does ALTER TABLE do?",
            "options": {"A": "Deletes the table", "B": "Modifies the table structure", "C": "Moves data", "D": "Creates an index"},
            "answer": "B",
            "hint": "ALTER = change the structure ",
            "explanation": "ALTER TABLE modifies structure: add/drop a column, change a data type."
        },
        {
            "topic": "Data Modification",
            "question": "What command creates a table?",
            "options": {"A": "MAKE TABLE", "B": "BUILD TABLE", "C": "CREATE TABLE", "D": "NEW TABLE"},
            "answer": "C",
            "hint": "CREATE = create ",
            "explanation": "CREATE TABLE name (col1 type, col2 type) — creates a new table."
        },

        # TOPIC: NULL 
        {
            "topic": "NULL",
            "question": "How do you check if a value is NULL?",
            "options": {"A": "col = NULL", "B": "col == NULL", "C": "col IS NULL", "D": "col EQUALS NULL"},
            "answer": "C",
            "hint": "IS NULL, not = NULL ",
            "explanation": "IS NULL is the correct way. col = NULL always returns FALSE!"
        },
        {
            "topic": "NULL",
            "question": "What is NULL in SQL?",
            "options": {"A": "The number 0", "B": "An empty string", "C": "The absence of a value", "D": "False"},
            "answer": "C",
            "hint": "Not 0 and not an empty string ",
            "explanation": "NULL means the absence of a value. It is not equal to 0, an empty string, or False."
        },
        {
            "topic": "NULL",
            "question": "How do you find rows where a field is NOT NULL?",
            "options": {"A": "col != NULL", "B": "col <> NULL", "C": "col IS NOT NULL", "D": "NOT col = NULL"},
            "answer": "C",
            "hint": "IS NOT NULL ",
            "explanation": "IS NOT NULL is the correct check for the presence of a value."
        },
        {
            "topic": "NULL",
            "question": "What does NULL + 5 return in SQL?",
            "options": {"A": "5", "B": "0", "C": "NULL", "D": "An error"},
            "answer": "C",
            "hint": "NULL infects everything around it ",
            "explanation": "Any arithmetic with NULL produces NULL. NULL represents the unknown."
        },

        # TOPIC: GROUP BY 
        {
            "topic": "GROUP BY",
            "question": "What does GROUP BY do?",
            "options": {"A": "Sorts", "B": "Filters rows", "C": "Groups rows by value", "D": "Joins tables"},
            "answer": "C",
            "hint": "GROUP = group ",
            "explanation": "GROUP BY groups rows with the same value. Used together with aggregate functions."
        },
        {
            "topic": "GROUP BY",
            "question": "What is a PRIMARY KEY?",
            "options": {"A": "The first column", "B": "A unique row identifier", "C": "A required field", "D": "An index"},
            "answer": "B",
            "hint": "The main key — unique for every row ",
            "explanation": "PRIMARY KEY uniquely identifies each row. It cannot be NULL."
        },
        {
            "topic": "GROUP BY",
            "question": "What are indexes used for?",
            "options": {"A": "Storing data", "B": "Speeding up search", "C": "Encryption", "D": "Backup"},
            "answer": "B",
            "hint": "Like a table of contents in a book ",
            "explanation": "An index speeds up search. But it slows down INSERT/UPDATE/DELETE."
        },

        # TOPIC: Transactions 
        {
            "topic": "Transactions",
            "question": "What does COMMIT do?",
            "options": {"A": "Rolls back changes", "B": "Saves the transaction", "C": "Starts a transaction", "D": "Deletes data"},
            "answer": "B",
            "hint": "Commit = save permanently ",
            "explanation": "COMMIT saves all transaction changes to the database. ROLLBACK — undoes them."
        },
        {
            "topic": "Transactions",
            "question": "What does ROLLBACK do?",
            "options": {"A": "Saves changes", "B": "Creates a table", "C": "Undoes transaction changes", "D": "Drops the database"},
            "answer": "C",
            "hint": "Roll back = undo ",
            "explanation": "ROLLBACK undoes all changes made in the current transaction."
        },
        {
            "topic": "Transactions",
            "question": "What is a VIEW?",
            "options": {"A": "A temporary table", "B": "A saved SELECT as a virtual table", "C": "A backup", "D": "An index type"},
            "answer": "B",
            "hint": "A virtual table ",
            "explanation": "VIEW is a virtual table based on a SELECT statement. Data is not stored physically."
        },
    ]
}

#  HELPERS

def save_query(message, command='message'):
    user = message.from_user
    UserQuery.objects.create(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        command=command,
        message_text=message.text or '',
    )

def get_name(message):
    u = message.from_user
    return u.first_name or u.username or 'user'

def get_topic_summary(topic_key):
    """Returns the question count per topic."""
    counts = {}
    for q in QUESTIONS[topic_key]:
        t = q['topic']
        counts[t] = counts.get(t, 0) + 1
    return counts

def make_topic_kb():
    kb = types.InlineKeyboardMarkup()
    py_count = len(QUESTIONS['python'])
    sql_count = len(QUESTIONS['sql'])
    kb.add(
        types.InlineKeyboardButton(f'🐍 Python', callback_data='topic_python'),
        types.InlineKeyboardButton(f'🗄️ SQL', callback_data='topic_sql'),
    )
    return kb

def make_answer_kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton('A', callback_data='ans_A'),
        types.InlineKeyboardButton('B', callback_data='ans_B'),
        types.InlineKeyboardButton('C', callback_data='ans_C'),
        types.InlineKeyboardButton('D', callback_data='ans_D'),
    )
    kb.add(types.InlineKeyboardButton('💡 Hint', callback_data='hint'))
    return kb


#  11 COMMANDS

# 1️ /start
@bot.message_handler(commands=['start'])
def cmd_start(message):
    save_query(message, '/start')
    name = get_name(message)
    text = (
        f"👋 Hello, *{name}*!\n\n"
        "I am a bot for testing your knowledge of Python and SQL 🤖\n\n"
        "📋 *Commands:*\n"
        "/quiz — start a quiz\n"
        "/topics — list of topics\n"
        "/score — my results\n"
        "/analyze — see which topics need work\n"
        "/explain — explanation of the last wrong answer\n"
        "/hint — hint (during a quiz)\n"
        "/reset — stop current quiz\n"
        "/feedback — rate the bot ⭐\n"
        "/about — about the bot\n"
        "/help — full guide\n\n"
        "Let's go! 🚀 /quiz"
    )
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True)    
    kb.add(
        types.KeyboardButton('🎯 Quiz'),
        types.KeyboardButton('📊 Score'),
    )
    kb.add(
    types.KeyboardButton('📚 Topics'),
    types.KeyboardButton('🔍 Analyze'),
    )
    kb.add(
        types.KeyboardButton('💡 Hint'),
        types.KeyboardButton('📖 Explain'),
    )
    kb.add(
        types.KeyboardButton('🔄 Reset'),
        types.KeyboardButton('⭐ Feedback'),
    )
    kb.add(
        types.KeyboardButton('ℹ️ About'),
        types.KeyboardButton('🆘 Help'),
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=kb)


# 2️ /help
@bot.message_handler(commands=['help'])
def cmd_help(message):
    save_query(message, '/help')
    text = (
        "🆘 *Full Guide*\n\n"
        "*How a quiz works:*\n"
        "1️⃣ /quiz → choose a topic\n"
        "2️⃣ 15 random questions are drawn from the database\n"
        "3️⃣ Answer using the A/B/C/D buttons\n"
        "4️⃣ You can use the 💡 Hint button at any time\n"
        "5️⃣ After the quiz, use /analyze to review your performance\n\n"
        "*All commands:*\n"
        "/start — main menu\n"
        "/help — this guide\n"
        "/quiz — new quiz\n"
        "/topics — topics\n"
        "/score — my results\n"
        "/analyze — topic-by-topic analysis\n"
        "/explain — explanation of last wrong answer\n"
        "/hint — hint\n"
        "/reset — stop quiz\n"
        "/feedback — rate the bot\n"
        "/about — about the bot"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


# 3️ /quiz
@bot.message_handler(commands=['quiz'])
def cmd_quiz(message):
    save_query(message, '/quiz')
    bot.send_message(
        message.chat.id,
        f"📝 *{get_name(message)}*, choose a topic:\n\n"
        f"_{QUESTIONS_PER_QUIZ} random questions will be drawn from the database!_",
        parse_mode='Markdown',
        reply_markup=make_topic_kb()
    )


# 4️ /topics
@bot.message_handler(commands=['topics'])
def cmd_topics(message):
    save_query(message, '/topics')
    py_summary = get_topic_summary('python')
    sql_summary = get_topic_summary('sql')

    py_lines = '\n'.join(f"  • {t}: {c} questions" for t, c in py_summary.items())
    sql_lines = '\n'.join(f"  • {t}: {c} questions" for t, c in sql_summary.items())

    text = (
        f"📚 *Topics:*\n\n"
        f"🐍 *Python* — {len(QUESTIONS['python'])} questions:\n{py_lines}\n\n"
        f"🗄️ *SQL* — {len(QUESTIONS['sql'])} questions:\n{sql_lines}\n\n"
        f"🎲 Each quiz picks *{QUESTIONS_PER_QUIZ}* random questions!"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


# 5️ /score
@bot.message_handler(commands=['score'])
def cmd_score(message):
    save_query(message, '/score')
    uid = message.from_user.id
    results = QuizResult.objects.filter(telegram_id=uid).order_by('-completed_at')[:10]
    if not results:
        bot.send_message(message.chat.id, "📊 No results yet. Let's start: /quiz")
        return
    lines = ["📊 *Your latest results:*\n"]
    for i, r in enumerate(results, 1):
        e = "🏆" if r.percentage >= 80 else ("👍" if r.percentage >= 60 else ("📚" if r.percentage >= 40 else "😤"))
        lines.append(
            f"{i}. {e} *{r.get_topic_display()}* — "
            f"{r.score}/{r.total} ({r.percentage:.1f}%) | ⏱ {r.time_spent:.1f}s | "
            f"📅 {r.completed_at.strftime('%d.%m.%y %H:%M')}"
        )
    lines.append("\n🔍 Topic analysis: /analyze")
    bot.send_message(message.chat.id, '\n'.join(lines), parse_mode='Markdown')


# 6️ /explain — full explanation of the last wrong answer
@bot.message_handler(commands=['explain'])
def cmd_explain(message):
    save_query(message, '/explain')
    uid = message.from_user.id
    session = sessions.get(uid, {})
    last_wrong = session.get('last_wrong')

    if not last_wrong:
        bot.send_message(
            message.chat.id,
            "❓ No wrong answer to explain.\n\n"
            "After you get a question wrong during a quiz, type /explain!"
        )
        return

    text = (
        f"📖 *Explanation of your last wrong answer:*\n\n"
        f"❓ *Question:*\n{last_wrong['question']}\n\n"
        f"❌ *Your answer:* {last_wrong['user_answer']}) {last_wrong['user_option']}\n"
        f"✅ *Correct answer:* {last_wrong['correct']}) {last_wrong['correct_option']}\n\n"
        f"💡 *Explanation:*\n{last_wrong['explanation']}\n\n"
        f"📚 *Topic:* {last_wrong['topic']}"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


# 7️ /about
@bot.message_handler(commands=['about'])
def cmd_about(message):
    save_query(message, '/about')
    py_count = len(QUESTIONS['python'])
    sql_count = len(QUESTIONS['sql'])
    text = (
        "🤖 *Programming Quiz Bot*\n\n"
        "A Telegram bot for testing your knowledge of Python and SQL.\n\n"
        f"📊 *Question database:*\n"
        f"  🐍 Python: {py_count} questions\n"
        f"  🗄️ SQL: {sql_count} questions\n"
        f"  🎲 {QUESTIONS_PER_QUIZ} random questions per quiz\n\n"
        "🛠 *Technologies:*\n"
        "  • pyTelegramBotAPI\n"
        "  • Django + SQLite\n"
        "  • Python 3.x\n\n"
        "👨‍💻 *Author:* dsezimm\n"
        "🎓 Final project for Python course, 2026\n"
        "🔗 github.com/dsezimm/quiz-bot"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


# 8️ /feedback
@bot.message_handler(commands=['feedback'])
def cmd_feedback(message):
    save_query(message, '/feedback')
    kb = types.InlineKeyboardMarkup(row_width=5)
    kb.add(
        types.InlineKeyboardButton('1⭐', callback_data='rate_1'),
        types.InlineKeyboardButton('2⭐', callback_data='rate_2'),
        types.InlineKeyboardButton('3⭐', callback_data='rate_3'),
        types.InlineKeyboardButton('4⭐', callback_data='rate_4'),
        types.InlineKeyboardButton('5⭐', callback_data='rate_5'),
    )
    bot.send_message(
        message.chat.id,
        "⭐ *Rate the bot:*\n\nChoose a score from 1 to 5:",
        parse_mode='Markdown',
        reply_markup=kb
    )


# 9️ /hint - hint during a quiz
@bot.message_handler(commands=['hint'])
def cmd_hint(message):
    save_query(message, '/hint')
    uid = message.from_user.id
    session = sessions.get(uid)
    if not session:
        bot.send_message(message.chat.id, "❓ No active quiz. Let's start: /quiz")
        return
    q = session['questions'][session['index']]
    hint = q.get('hint', 'No hint available 🤷')
    session['hints_used'] = session.get('hints_used', 0) + 1
    bot.send_message(message.chat.id, f"💡 *Hint:*\n{hint}", parse_mode='Markdown')


# 10 /analyze — topic-by-topic analysis
@bot.message_handler(commands=['analyze'])
def cmd_analyze(message):
    save_query(message, '/analyze')
    uid = message.from_user.id
    session = sessions.get(uid, {})
    topic_errors = session.get('topic_errors', {})
    topic_correct = session.get('topic_correct', {})

    if not topic_errors and not topic_correct:
        bot.send_message(
            message.chat.id,
            "📊 No data yet.\n\nFirst complete a quiz: /quiz\nThen type /analyze!"
        )
        return

    lines = ["🔍 *Topic-by-topic analysis:*\n"]

    # Collect all topics
    all_topics = set(list(topic_errors.keys()) + list(topic_correct.keys()))

    topic_stats = []
    for topic in all_topics:
        errors = topic_errors.get(topic, 0)
        correct = topic_correct.get(topic, 0)
        total = errors + correct
        pct = (correct / total * 100) if total > 0 else 0
        topic_stats.append((topic, errors, correct, total, pct))

    # Sort from worst to best
    topic_stats.sort(key=lambda x: x[4])

    for topic, errors, correct, total, pct in topic_stats:
        if pct >= 80:
            emoji = "🟢"
            status = "Good!"
        elif pct >= 50:
            emoji = "🟡"
            status = "Needs practice"
        else:
            emoji = "🔴"
            status = "Review required!"

        lines.append(
            f"{emoji} *{topic}*\n"
            f"   ✅ {correct} correct | ❌ {errors} wrong | {pct:.0f}% | {status}"
        )

    # Worst and best topics
    if topic_stats:
        worst = topic_stats[0]
        best = topic_stats[-1]
        lines.append(f"\n{'─'*30}")
        lines.append(f"⚠️ *Most mistakes in:* {worst[0]} ({worst[1]} wrong)")
        lines.append(f"👉 *Recommendation:* study this topic again!")
        if best[4] > worst[4]:
            lines.append(f"\n✅ *Best topic:* {best[0]} ({best[4]:.0f}%)")

    lines.append("\n🔄 New quiz: /quiz")
    bot.send_message(message.chat.id, '\n'.join(lines), parse_mode='Markdown')


# 1️1 /reset
@bot.message_handler(commands=['reset'])
def cmd_reset(message):
    save_query(message, '/reset')
    uid = message.from_user.id
    if uid in sessions:
        sessions.pop(uid)
        bot.send_message(message.chat.id, "🔄 Quiz stopped.\n\nStart a new one: /quiz")
    else:
        bot.send_message(message.chat.id, "❓ No active quiz. Let's start: /quiz")


#  CALLBACKS

@bot.callback_query_handler(func=lambda c: c.data.startswith('rate_'))
def handle_rating(call):
    stars = int(call.data.split('_')[1])
    UserQuery.objects.create(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        command='message',
        message_text=f"[RATING] {stars}/5 {'⭐' * stars}",
    )
    messages = {
        1: "Sorry to hear that... We'll work to improve! 💪",
        2: "Thanks! We'll take your feedback into account 🙏",
        3: "Not bad! We'll keep improving 👍",
        4: "Thanks! Great rating 😊",
        5: "Amazing! We're so happy! 🎉",
    }
    bot.edit_message_text(
        f"{'⭐' * stars} — {messages[stars]}",
        call.message.chat.id, call.message.message_id
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith('topic_'))
def handle_topic(call):
    topic = call.data.split('_')[1]
    uid = call.from_user.id

    # Pick 15 random questions from the 40 in the database
    all_questions = QUESTIONS[topic].copy()
    random.shuffle(all_questions)
    selected = all_questions[:QUESTIONS_PER_QUIZ]

    sessions[uid] = {
        'topic': topic,
        'questions': selected,
        'index': 0,
        'score': 0,
        'start_time': time.time(),
        'hints_used': 0,
        'wrong_answers': [],
        'topic_errors': {},
        'topic_correct': {},
        'last_wrong': None,
    }

    label = '🐍 Python' if topic == 'python' else '🗄️ SQL'
    total_in_db = len(QUESTIONS[topic])
    bot.edit_message_text(
        f"✅ Topic: *{label}*\n"
        f"🎲 *{QUESTIONS_PER_QUIZ}* random questions selected from {total_in_db}!\n\n"
        "💡 You can use the Hint button on each question.\n"
        "🚀 Let's go!",
        call.message.chat.id, call.message.message_id, parse_mode='Markdown'
    )
    send_question(call.message.chat.id, uid)


@bot.callback_query_handler(func=lambda c: c.data == 'hint')
def handle_hint_btn(call):
    uid = call.from_user.id
    session = sessions.get(uid)
    if not session:
        bot.answer_callback_query(call.id, "No active quiz. /quiz")
        return
    q = session['questions'][session['index']]
    hint = q.get('hint', 'No hint available')
    session['hints_used'] = session.get('hints_used', 0) + 1
    bot.answer_callback_query(call.id, f"💡 {hint}", show_alert=True)


@bot.callback_query_handler(func=lambda c: c.data.startswith('ans_'))
def handle_answer(call):
    uid = call.from_user.id
    session = sessions.get(uid)
    if not session:
        bot.answer_callback_query(call.id, "Let's start a quiz: /quiz")
        return

    answer = call.data.split('_')[1]
    idx = session['index']
    q = session['questions'][idx]
    correct = q['answer']
    topic_name = q.get('topic', 'Unknown')

    # Save to database
    UserQuery.objects.create(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        command='answer',
        message_text=f"Q{idx+1} [{topic_name}]: {answer}, correct: {correct}",
    )

    if answer == correct:
        session['score'] += 1
        session['topic_correct'][topic_name] = session['topic_correct'].get(topic_name, 0) + 1
        feedback = "✅ *Correct!*\n📖 Explanation: /explain"
        bot.answer_callback_query(call.id, "✅ Correct!")
    else:
        # Save wrong answer info
        session['topic_errors'][topic_name] = session['topic_errors'].get(topic_name, 0) + 1
        session['last_wrong'] = {
            'question': q['question'],
            'user_answer': answer,
            'user_option': q['options'].get(answer, ''),
            'correct': correct,
            'correct_option': q['options'].get(correct, ''),
            'explanation': q.get('explanation', ''),
            'topic': topic_name,
        }
        session['wrong_answers'].append(session['last_wrong'])
        feedback = (
            f"❌ *Wrong!* Correct answer: *{correct})*\n"
            f"📖 Get explanation: /explain"
        )
        bot.answer_callback_query(call.id, f"❌ Wrong! Answer: {correct})")

    session['index'] += 1

    # Remove buttons
    try:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    except Exception:
        pass

    bot.send_message(call.message.chat.id, feedback, parse_mode='Markdown')
    time.sleep(0.4)

    # Check if session still exists
    if uid in sessions:
        send_question(call.message.chat.id, uid)
    else:
        finish_quiz(call.message.chat.id, uid)


def send_question(chat_id, uid):
    session = sessions.get(uid)
    if not session:
        bot.send_message(chat_id, "❓ Session not found. New quiz: /quiz")
        return

    questions = session.get('questions', [])
    idx = session.get('index', 0)

    # If questions are exhausted — show result
    if not questions or idx >= len(questions):
        finish_quiz(chat_id, uid)
        return

    q = questions[idx]
    options_text = '\n'.join(f"*{k})* {v}" for k, v in q['options'].items())
    topic_label = q.get('topic', '')
    text = (
        f"❓ *Question {idx+1}/{len(questions)}*"
        + (f" _{topic_label}_" if topic_label else "")
        + f"\n\n{q['question']}\n\n{options_text}"
    )
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=make_answer_kb())


def finish_quiz(chat_id, uid):
    # Collect all data first, then update the session
    session = sessions.get(uid)
    if not session:
        return

    score = session['score']
    total = len(session['questions'])
    topic = session['topic']
    time_spent = round(time.time() - session['start_time'], 2)
    percentage = (score / total) * 100 if total > 0 else 0
    hints = session.get('hints_used', 0)
    wrong_count = len(session.get('wrong_answers', []))
    topic_errors = dict(session.get('topic_errors', {}))
    topic_correct = dict(session.get('topic_correct', {}))
    wrong_answers = list(session.get('wrong_answers', []))
    last_wrong = session.get('last_wrong')

    # Save to database
    try:
        QuizResult.objects.create(
            telegram_id=uid,
            username=None,
            topic=topic,
            score=score,
            total=total,
            percentage=percentage,
            time_spent=time_spent,
        )
    except Exception as db_err:
        print(f"DB error: {db_err}")

    # Result message
    if percentage >= 80:
        e, verdict = "🏆", "Excellent result!"
    elif percentage >= 60:
        e, verdict = "👍", "Good job!"
    elif percentage >= 40:
        e, verdict = "📚", "Needs more practice!"
    else:
        e, verdict = "😤", "This topic needs serious review!"

    label = '🐍 Python' if topic == 'python' else '🗄️ SQL'

    worst_line = ""
    if topic_errors:
        worst = max(topic_errors.items(), key=lambda x: x[1])
        worst_line = f"\n⚠️ *Weakest topic:* {worst[0]} ({worst[1]} wrong)\n"

    text = (
        f"📌 *Quiz finished!*\n\n"
        f"📚 Topic: *{label}*\n"
        f"✅ Score: *{score}/{total}* ({percentage:.1f}%)\n"
        f"❌ Wrong: *{wrong_count}*\n"
        f"⏱ Time: *{time_spent}* sec\n"
        f"💡 Hints used: *{hints}*\n"
        f"{worst_line}\n"
        f"*{verdict}*\n\n"
        "📊 Topic analysis: /analyze\n"
        "📖 Last wrong answer: /explain\n"
        "🔄 New quiz: /quiz"
    )

    bot.send_message(chat_id, text, parse_mode='Markdown')

    # Keep session data for /analyze and /explain 
    sessions[uid] = {
        'topic': topic,
        'questions': [],
        'index': 0,
        'score': score,
        'start_time': 0,
        'hints_used': hints,
        'wrong_answers': wrong_answers,
        'topic_errors': topic_errors,
        'topic_correct': topic_correct,
        'last_wrong': last_wrong,
    }


# Any other message 

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    save_query(message, 'message')
    text = message.text

    if text == '🎯 Quiz':
        cmd_quiz(message)
    elif text == '📊 Score':
        cmd_score(message)
    elif text == '📚 Topics':
        cmd_topics(message)
    elif text == '🔍 Analyze':
        cmd_analyze(message)
    elif text == '💡 Hint':
        cmd_hint(message)
    elif text == '📖 Explain':
        cmd_explain(message)
    elif text == '🔄 Reset':
        cmd_reset(message)
    elif text == '⭐ Feedback':
        cmd_feedback(message)
    elif text == 'ℹ️ About':
        cmd_about(message)
    elif text == '🆘 Help':
        cmd_help(message)
    else:
        bot.send_message(
            message.chat.id,
            "📩 Message received!\n\n"
            "All commands: /help\n"
            "Start a quiz: /quiz"
        )


# Entry point 

if __name__ == '__main__':
    py_count = len(QUESTIONS['python'])
    sql_count = len(QUESTIONS['sql'])
    print(f"🤖 Quiz Bot started!")
    print(f"📊 Python questions | SQL questions")
    print(f"🎲 {QUESTIONS_PER_QUIZ} random questions per quiz")
    print(f" 11 commands active")
    print(f"🌐 Admin panel: http://127.0.0.1:8000/admin")
    print("Stop: Ctrl+C\n")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
    