---
course: dami-ai-career
title: Object-oriented programming
month: 1
monthTitle: Python Foundations + Git
lesson: 7
summary: Bundle data and behaviour together using classes and objects, so your code models real things
  and stays organised as it grows.
objectives:
- Explain what a class and an object are, and how they relate
- Define a class with the class keyword and create instances
- Use __init__ to set up an object's attributes
- Write methods that act on an object's own data via self
- Distinguish instance attributes from class attributes
- Understand inheritance to reuse and extend a class
- Recognise when objects make code clearer than loose functions
video: m1-l07-oop.mp4
quiz:
- q: What is the relationship between a class and an object?
  options:
  - They are the same thing
  - A class is a blueprint; an object is a built instance of it
  - An object is a blueprint; a class is built from it
  - A class is a function and an object is its return value
  answer: 1
  why: A class describes what objects of that type look like and do; each object is a concrete instance
    created from that blueprint.
- q: What does the __init__ method do?
  options:
  - Imports the class
  - Deletes an object
  - Runs automatically when an object is created to set up its attributes
  - Prints the object
  answer: 2
  why: __init__ is the constructor — Python calls it automatically when you create an instance, so you
    can set the object's starting attributes.
- q: What does the self parameter refer to inside a method?
  answer: The particular object the method is being called on, so the method can read and change that
    object's own attributes.
  why: Each method receives self as its first parameter; it lets the method work with the specific instance's
    data.
- q: Which line correctly creates an object from a class named Dog?
  options:
  - Dog.new()
  - d = Dog()
  - d = new Dog
  - create Dog()
  answer: 1
  why: In Python you call the class like a function — Dog() — which builds and returns a new instance.
- q: In one sentence, what is inheritance?
  answer: A way to build a new class on top of an existing one so it reuses that class's attributes and
    methods and can add or override its own.
  why: Inheritance lets a child class reuse a parent's code and specialise it, avoiding duplication.
- q: What is the difference between a class attribute and an instance attribute?
  options:
  - There is no difference
  - A class attribute is shared by all instances; an instance attribute belongs to one object
  - A class attribute belongs to one object; an instance attribute is shared
  - Both are always shared
  answer: 1
  why: Class attributes are defined on the class and shared; instance attributes are set per object, usually
    in __init__ via self.
resources:
- label: Python docs — Classes (official tutorial 9)
  url: https://docs.python.org/3/tutorial/classes.html
- label: 'Python Crash Course (Eric Matthes) — Chapter 9: Classes'
- label: Real Python — Object-Oriented Programming (OOP) in Python 3
  url: https://realpython.com/python3-object-oriented-programming/
- label: Real Python — Inheritance and Composition in Python
  url: https://realpython.com/inheritance-composition-python/
---

## Why objects?

So far you've kept **data** in variables and **behaviour** in functions, separately. Object-oriented programming, or OOP, lets you bundle related data and the functions that act on it into one thing called an **object**.

Think of a bank account: it has data (a balance, an owner) and behaviour (deposit, withdraw). Keeping these together in one object is cleaner than passing a loose balance variable around between functions.

## Classes vs objects

A **class** is a blueprint. An **object** (also called an *instance*) is a concrete thing built from that blueprint. One class, many objects — just like one cookie cutter makes many cookies.

```python
class Dog:
    pass

rex = Dog()      # an object
bella = Dog()    # another object
```

## The __init__ method and self

`__init__` runs automatically when you create an object. It sets up the object's starting **attributes**. The first parameter, `self`, refers to the specific object being built.

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

rex = Dog("Rex", 3)
print(rex.name)   # Rex
```

## Methods

A **method** is a function defined inside a class. It always takes `self` first, so it can use the object's own data.

```python
class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        return self.name + " says woof!"

rex = Dog("Rex")
print(rex.bark())   # Rex says woof!
```

## Inheritance

**Inheritance** lets a new class build on an existing one, reusing its code and adding or changing behaviour. The new class is the *child*; the original is the *parent*.

```python
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return "..."

class Cat(Animal):
    def speak(self):
        return self.name + " says meow"

print(Cat("Bella").speak())   # Bella says meow
```

## Your task

Write a `BankAccount` class with a balance, plus `deposit` and `withdraw` methods that update it.
