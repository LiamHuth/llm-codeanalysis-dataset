# author: Liam Huth
# December 2023


def createPath():
    path = input("Enter the path you want to create")
    vulnerableFunction(path)
    print("hacked!")

def vulnerableFunction(path):
    path = 2 * path
    return path

createPath()