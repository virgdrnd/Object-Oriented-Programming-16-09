##**Operator Overloading**

#Problem 1:

class ComplexNumber:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        return ComplexNumber(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return ComplexNumber(self.real - other.real, self.imag - other.imag)

    def __str__(self):
        return f"{self.real} + {self.imag}i"


#Problem 2:
class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __gt__(self, other):
        return self.age > other.age

  #Problem 4:

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z


#Problem 5:
class Circle:
    def __init__(self, radius):
        self.radius = radius

    def __lt__(self, other): return self.radius < other.radius
    def __gt__(self, other): return self.radius > other.radius
    def __eq__(self, other): return self.radius == other.radius
    def __ne__(self, other): return self.radius != other.radius
    def __ge__(self, other): return self.radius >= other.radius
    def __le__(self, other): return self.radius <= other.radius

  #Problem 6:
  import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __lt__(self, other): return self.distance() < other.distance()
    def __gt__(self, other): return self.distance() > other.distance()
    def __eq__(self, other): return self.distance() == other.distance()
    def __ne__(self, other): return self.distance() != other.distance()
    def __ge__(self, other): return self.distance() >= other.distance()
    def __le__(self, other): return self.distance() <= other.distance()

  #Problem 7

class Matrix:
    def __init__(self, data):
        self.data = data

    def __mul__(self, other):
        rows_a = len(self.data)
        cols_a = len(self.data[0])
        cols_b = len(other.data[0])
        result = [[0] * cols_b for _ in range(rows_a)]

        for i in range(rows_a):
            for j in range(cols_b):
                for k in range(cols_a):
                    result[i][j] += self.data[i][k] * other.data[k][j]
        return Matrix(result)


##**Inheritance**

#problem 1:
class Vehicle:
    def drive(self):
        return "Driving a vehicle"

class Car(Vehicle):
    def drive(self):
        return "Driving a car"

class Bicycle(Vehicle):
    def drive(self):
        return "Riding a bicycle"


#Problem 2:
class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def introduce(self):
        return f"Hi, I'm {self.name}, {self.age} years old, living in {self.address}."

class Student(Person):
    def __init__(self, name, age, address, field_of_study):
        super().__init__(name, age, address)
        self.field_of_study = field_of_study

    def introduce(self):
        return f"Hi, I'm {self.name}, studying {self.field_of_study}."

class Employee(Person):
    def __init__(self, name, age, address, company):
        super().__init__(name, age, address)
        self.company = company

    def introduce(self):
        return f"Hi, I'm {self.name}, working at {self.company}."


#Problem 3:
class BankAccount:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def transfer(self, destination, amount):
        if self.withdraw(amount):
            destination.deposit(amount)
            return True
        return False

class SavingsAccount(BankAccount):
    def __init__(self, account_number, balance=0, interest_rate=0.02):
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        self.balance += self.balance * self.interest_rate

    def check_balance(self):
        return self.balance
      
