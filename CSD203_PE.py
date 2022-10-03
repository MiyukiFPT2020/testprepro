# this is PE test for CSD203. Do not delete this line
# your code here

import functools
import re


class Node:
    def __init__(self, key, item):
        self.key = key
        self.item = item
        self.next = None

    def hasNext(self):
        return self.next is not None

    def __lt__(self, other):
        return self.item.__lt__(other.item)


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def isEmpty(self):
        return self.head is None

    def getHead(self):
        return self.head

    def getPrevious(self, key):
        if self.isEmpty() or self.getHead().key == key:
            return
        currentNode = self.getHead()
        while currentNode and currentNode != self.tail:
            if currentNode.next.key == key:
                return currentNode
            currentNode = currentNode.next
        return

    def addLast(self, key, item):
        newNode = Node(key, item)
        if self.tail is None:
            self.head = self.tail = newNode
        else:
            self.tail.next = newNode
            self.tail = newNode
        return newNode

    # Search node based on key
    def search(self, key):
        ret = None
        if not self.isEmpty():
            for cursor in self:
                if cursor.key == key:
                    ret = cursor
        return ret

    def deleteFirst(self):
        if not self.isEmpty():
            head = self.head
            if head.hasNext():
                self.head = self.head.next
            else:
                self.head = None
                self.tail = None
            return head
        return

    def delete(self, key):
        if not self.isEmpty():
            deleted = self.search(key)
            if deleted:
                previous = self.getPrevious(key)
                if previous:
                    previous.next = deleted.next
                else:
                    self.deleteFirst()
                if deleted == self.tail:
                    self.tail = previous
            return deleted
        return

    def count(self):
        return sum(1 for i in self)

    # Return the min node in the list
    def findMin(self):
        minNode = None
        # End if list in empty
        if not self.isEmpty():
            for cursor in self:
                if minNode is None:
                    minNode = cursor
                else:
                    if cursor.item < minNode.item:
                        minNode = cursor
        return minNode

    def getAllItems(self):
        items = []
        for node in self:
            items.append(node.item)
        return items

    def sort(self):
        sortedList = []
        if not self.isEmpty():
            sortedList = sorted(self)
        return sortedList

    def __iter__(self):
        return self.SinglyLinkListIterator(self.head)

    class SinglyLinkListIterator:

        def __init__(self, head: Node):
            self.__cursor = None
            self.__nextNode = head

        def __next__(self):
            self.__cursor = self.__nextNode
            if not self.__cursor:
                raise StopIteration
            self.__nextNode = self.__nextNode.next
            return self.__cursor


# ----------------------------------------- MODEL ----------------------------------------------
@functools.total_ordering
class Library:
    def __init__(self, code: str, name: str, Author: str, price: float = 0.0):
        if not self.isValidName(name):
            raise ValueError("Name is not valid")
        if not self.isValidPrice(price):
            raise ValueError("Price is not valid")
        self.__code = code.upper()
        self.__name = name
        self.__author = Author
        self.__price = float(price)

    def __repr__(self):
        return f"Code: {self.__code}| Name: {self.__name}| Author: {self.__author}|Price: {self.__price}",

    def __str__(self):
        return f"Code: {self.__code}| Name: {self.__name}| Author: {self.__author}|Price: {self.__price}"

    @property
    def code(self):
        return self.__code

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, newName: str):
        if not Library.isValidName(newName):
            raise ValueError("Name is not valid")
        self.__name = newName

    @property
    def Author(self):
        return self.__author

    @Author.setter
    def Author(self, newAuthor: str):
        self.__author = newAuthor

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, newPrice: float):
        if not self.isValidPrice(newPrice):
            raise ValueError("Price is not valid")
        self.__price = float(newPrice)

    def __lt__(self, other):
        if self.__price < other.__price:
            return True
        if self.__name < other.__name:
            return True
        return False

    def __eq__(self, other):
        return (self.__price, self.__name) == (other.__price, other.__name)

    @classmethod
    def isValidName(cls, newName: str):
        isValid = True
        pattern = re.compile(r"^([A-Za-z\s]){3,50}$")
        if not pattern.match(newName):
            isValid = False
        else:
            optimizedName = re.sub(r'\s+', " ", newName.strip())
            numOfCharacters = 0
            tokens = optimizedName.split(" ")
            for token in tokens:
                tokenLength = len(token)
                if not tokenLength > 1:
                    isValid = False
                    break
                numOfCharacters += tokenLength
            if isValid:
                if numOfCharacters < 3 or numOfCharacters > 50:
                    isValid = False
        return isValid

    @classmethod
    def isValidPrice(cls, price):
        noError = True
        try:
            price = float(price)
        except ValueError:
            return False
        if price < 0:
            noError = False
        return noError


# ----------------------------------------- CONTROLLER ----------------------------------------------

class LibraryManagement:

    def __init__(self):
        self.__numOfBooks = 0
        self.sl = SinglyLinkedList()

    def addBook(self, code: str, name: str, Author: str, price: float = 0.0):
        newBook = Library(code, name, Author, price)
        added = self.sl.addLast(newBook.code, newBook)
        if added:
            self.__numOfBooks = self.__numOfBooks + 1

    def search(self, code: str):
        found = self.sl.search(code.strip().upper())
        if found:
            return found.item
        return

    def __internalSearch(self, code: str):
        found = self.sl.search(code.strip().upper())
        if found:
            return found
        return

    def updateName(self, code: str, newName: str):
        found = self.__internalSearch(code).item
        if found and self.isValidName(newName):
            found.name = newName
            return True
        return False

    def updateAuthor(self, code: str, newAuthor: str):
        found = self.__internalSearch(code).item
        if found:
            found.Author = newAuthor
            return True
        return False

    def updatePrice(self, code: str, newPrice: float):
        found = self.__internalSearch(code).item
        if found and self.isValidPrice(newPrice):
            found.price = newPrice
            return True
        return False

    def deleteBook(self, code: str):
        deleted = self.sl.delete(code.strip().upper())
        if deleted:
            self.__numOfBooks = self.__numOfBooks - 1
            return deleted.item
        return

    # Sort student list based on mark
    def sort(self):
        return self.sl.sort()

    def showAllBookAscendingOrder(self):
        for node in self.sort():
            print(f"{node.item}")

    # Return number of books
    def count(self):
        return self.__numOfBooks

    def isValidCode(self, code: str):
        return self.search(code) is None

    @staticmethod
    def isValidName(name: str):
        return Library.isValidName(name)

    @staticmethod
    def isValidPrice(price: float):
        return Library.isValidPrice(price)

# ----------------------------------------- VIEW ----------------------------------------------


class Menu:
    def __init__(self):
        self.manager = LibraryManagement()

    @staticmethod
    def isInteger(num):
        try:
            int(num)
        except ValueError:
            return False
        return True

    @staticmethod
    def showMainMenu():
        print("\n")
        print("PROGRAMMING of MANAGE STUDENT")
        print("|------------------------MENU-------------------------|")
        print("||  1.Add books to the library.                      ||")
        print("||  2.Delete a book based on via code                ||")
        print("||  3.Update a book based on via code                ||")
        print("||  4.Search a book based on via code                ||")
        print("||  5.Display all books in library                   ||")
        print("||  0. Quit                                          ||")
        print("|-----------------------------------------------------|")

    def addStudentForm(self):
        print("Add books to the library: ")
        isValid = False
        while not isValid:
            code = input("Enter Book's code: ")
            isValid = self.manager.isValidCode(code)
            if not isValid:
                print("Code has existed, please enter again")

        isValid = False
        while not isValid:
            name = input("Enter Book's name: ")
            isValid = self.manager.isValidName(name)
            if not isValid:
                print("Name is not valid, please enter again")

        Author = input("Enter Book's author: ")

        isValid = False
        while not isValid:
            price = input("Enter Book's price: ")
            isValid = self.manager.isValidPrice(price)
            if not isValid:
                print("Price is not valid, please enter again")

        try:
            self.manager.addBook(code, name, Author, price)
        except ValueError as e:
            print(e)
        else:
            print("---> Added successfully <---")

    def searchBook(self):
        print("-----------------WELCOME TO SEARCH BOOK FUNCTION----------------")
        code = input("Please enter Book's ID: ")
        result = self.manager.search(code)
        if result is None:
            print("Not found")
        else:
            print("Found: {}".format(result))

    def deleteBook(self):
        print("-----------------WELCOME TO DELETE BOOK FUNCTION----------------")
        code = input("Please enter Book's ID: ")
        found = self.manager.search(code)
        if found:
            print(f"Info {found}")
            confirm = input("Are you sure to delete [Y/N]: ").upper()
            if confirm == "Y":
                if self.manager.deleteBook(code):
                    print("---> Delete successfully <---")
        else:
            print("Code does not exist")

    def updateName(self, code: str):
        isSuccess = False
        while not isSuccess:
            newName = input("Enter new name: ")
            isSuccess = self.manager.updateName(code, newName)
            if not isSuccess:
                print("Name is not valid, please enter again")

    def updateAuthor(self, code: str):
        newAuthor = input("Enter new Author: ")
        isSuccess = self.manager.updateAuthor(code, newAuthor)

    def updatePrice(self, code):
        isSuccess = False
        while not isSuccess:
            newPrice = input("Enter new price: ")
            isSuccess = self.manager.updatePrice(code, newPrice)
            if not isSuccess:
                print("Price is not valid, please enter again")

    def updateStudent(self):
        print("-------------- UPDATE BOOK INFORMATION---------------------")
        continues = "Y"
        while continues == "Y":
            code = input("Please enter Book's ID : ")
            found = self.manager.search(code)
            if found:
                switcher = {
                    "1": self.updateName,
                    "2": self.updateAuthor,
                    "3": self.updatePrice,
                }
                oldInfo = str(found)
                print("Old Information: " + oldInfo)
                print("1: Update New Name | 2. Update New Author | 3. Update New Price |")
                choice = input("Enter your options: ")
                try:
                    switcher.get(choice, lambda x: print("not a valid code"))(code)
                except ValueError as e:
                    print(e)
                if oldInfo != str(found):
                    print(f"Update successfully ---> New info {found}")
            else:
                print("Code does not exist")

            continues = input("Do you want to continue?[y/n]: ").upper()

    def Display_allBooks_inLibrary(self):
        if self.manager.count() > 0:
            self.manager.showAllBookAscendingOrder()
        else:
            print("Nothing to show")

    # Handle all logic functionalities
    def core(self):
        switcher = {
            "1": self.addStudentForm,
            "2": self.deleteBook,
            "3": self.updateStudent,
            "4": self.searchBook,
            "5": self.Display_allBooks_inLibrary
        }
        while True:  # Run to the end of the world
            self.clearScreen()
            self.showMainMenu()
            choice = input("Please enter your choice: ")
            if choice != "0":
                switcher.get(choice, lambda: print("not a valid code"))()
                input("Press Enter to continue...")
            else:
                print("Bye")
                return

    @staticmethod
    def clearScreen():
        print('\n' * 2)  # prints 20 line breaks


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mn = Menu()
    mn.core()

