import sys
import json


class Shape:
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        shape_type = data["name"]
        if shape_type == "Point":
            return Point(data["x"], data["y"])
        elif shape_type == "Line":
            return Line(data["x1"], data["y1"], data["x2"], data["y2"])
        elif shape_type == "Circle":
            return Circle(data["x"], data["y"], data["r"])
        elif shape_type == "Square":
            return Square(data["x"], data["y"], data["side"])
        return None


class Point(Shape):
    def __init__(self, x, y):
        super().__init__('Point')
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"


class Line(Shape):
    def __init__(self, x1, y1, x2, y2):
        super().__init__('Line')
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return f"Line(({self.x1}, {self.y1}) -> ({self.x2}, {self.y2}))"


class Circle(Shape):
    def __init__(self, x, y, r):
        if r <= 0:
            raise ValueError("Radius must be greater than zero.")
        super().__init__('Circle')
        self.x = x
        self.y = y
        self.r = r

    def __str__(self):
        return f"Circle(center=({self.x}, {self.y}), radius={self.r})"


class Square(Shape):
    def __init__(self, x, y, side):
        if side <= 0:
            raise ValueError("Side length must be greater than zero.")
        super().__init__('Square')
        self.x = x
        self.y = y
        self.side = side

    def __str__(self):
        return f"Square(top-left=({self.x}, {self.y}), side={self.side})"


shapes = []
FILE_NAME = "shapes.json"


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def load_shapes():
    global shapes
    try:
        with open(FILE_NAME, "r") as f:
            data = json.load(f)
            shapes = [Shape.from_dict(shape) for shape in data]
    except (FileNotFoundError, json.JSONDecodeError):
        shapes = []


def save_shapes():
    with open(FILE_NAME, "w") as f:
        json.dump([shape.to_dict() for shape in shapes], f)


def create_shape(args):
    if not args:
        print("Invalid command. Use 'create [shape] [parameters]'.")
        return
    shape_type = args[0]
    if not all(is_int(arg) for arg in args[1:]):
        print("Coordinates and dimensions must be numbers.")
        return
    try:
        if shape_type == "point":
            shapes.append(Point(int(args[1]), int(args[2])))
        elif shape_type == "line":
            shapes.append(Line(int(args[1]), int(args[2]), int(args[3]), int(args[4])))
        elif shape_type == "circle":
            shapes.append(Circle(int(args[1]), int(args[2]), int(args[3])))
        elif shape_type == "square":
            shapes.append(Square(int(args[1]), int(args[2]), int(args[3])))
        else:
            print("Unknown shape type")
            return
        save_shapes()
        print(f"{shape_type.capitalize()} created successfully.")
    except ValueError as e:
        print(e)
    except (IndexError, ValueError):
        print("Invalid parameters. Please provide correct numeric values.")



def list_shapes():
    if not shapes:
        print("No shapes created.")
    else:
        for i, shape in enumerate(shapes):
            print(f"[{i}] {shape}")


def delete_shape(args):
    try:
        index = int(args[0])
        if 0 <= index < len(shapes):
            confirm = input(f"Are you sure you want to delete {shapes[index]}? (yes/no): ").strip().lower()
            if confirm == "yes":
                del shapes[index]
                save_shapes()
                print("Shape deleted.")
            else:
                print("Deletion canceled.")
        else:
            print("Invalid index: out of range")
    except (IndexError, ValueError):
        print("Invalid index")


def main():
    print("CLI Vector Editor Commands:")
    print("  create point x y         - Create a point")
    print("  create line x1 y1 x2 y2  - Create a line")
    print("  create circle x y r      - Create a circle (radius must be > 0)")
    print("  create square x y side   - Create a square (top-left corner, side length > 0)")
    print("  list                     - List all shapes")
    print("  delete index             - Delete a shape by index (with confirmation)")
    print("  exit                     - Exit the program")
    load_shapes()
    while True:
        command = input("Enter command: ").strip().split()
        if not command:
            continue
        if command[0] == "create":
            create_shape(command[1:])
        elif command[0] == "list":
            list_shapes()
        elif command[0] == "delete":
            delete_shape(command[1:])
        elif command[0] == "exit":
            print("Exiting...")
            sys.exit()
        else:
            print("Unknown command")


if __name__ == "__main__":
    main()