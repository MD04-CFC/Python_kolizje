import tkinter as tk
import math
import re


class CircleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dodawanie i zaznaczanie kół (środek w 0,0)")

        self.canvas_width = 500
        self.canvas_height = 500
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=4)

        self.center_x = self.canvas_width // 2
        self.center_y = self.canvas_height // 2

        self.canvas.create_line(self.center_x, 0, self.center_x, self.canvas_height, fill="gray", dash=(4, 2))
        self.canvas.create_line(0, self.center_y, self.canvas_width, self.center_y, fill="gray", dash=(4, 2))

        tk.Label(root, text="X:").grid(row=1, column=0)
        self.x_entry = tk.Entry(root)
        self.x_entry.grid(row=1, column=1)

        tk.Label(root, text="Y:").grid(row=1, column=2)
        self.y_entry = tk.Entry(root)
        self.y_entry.grid(row=1, column=3)

        self.add_button = tk.Button(root, text="Dodaj koło", command=self.add_circle)
        self.add_button.grid(row=2, column=0, columnspan=4)

        self.start_button = tk.Button(root, text="Start", command=self.start_algorithm)
        self.start_button.grid(row=3, column=0, columnspan=4)

        self.clear_button = tk.Button(root, text="Wyczyść", command=self.clear_canvas)
        self.clear_button.grid(row=4, column=0, columnspan=4)

        self.circle_list = tk.Text(root, width=77, height=10, state="disabled", bg="lightgray")
        self.circle_list.grid(row=5, column=0, columnspan=4, pady=10)

        self.circles = []
        self.scale = 50
        self.circle_radius = 50

    def validate_input(self, value):
        pattern = r"^-?\d\.\d{2}$"
        return re.match(pattern, value) and -5.00 <= float(value) <= 5.00

    def update_circle_list(self):
        self.circle_list.config(state="normal")
        self.circle_list.delete("1.0", tk.END)
        for idx, (x, y) in enumerate(self.circles, start=1):
            self.circle_list.insert(tk.END, f"{idx}. Środek: ({x:.2f}, {y:.2f})\n")
        self.circle_list.config(state="disabled")

    def add_circle(self):
        x_value = self.x_entry.get()
        y_value = self.y_entry.get()

        # Usuwamy poprzednie komunikaty o błędach
        self.circle_list.config(state="normal")
        self.circle_list.delete("1.0", tk.END)

        # Walidacja współrzędnych
        if not (self.validate_input(x_value) and self.validate_input(y_value)):
            self.circle_list.insert(tk.END,
                                    "Wprowadź prawidłowe współrzędne w formacie X.XX z przedziału -5.00 do 5.00\n")
            self.circle_list.config(state="disabled")
            return

        x = float(x_value)
        y = float(y_value)

        canvas_x = self.center_x + x * self.scale
        canvas_y = self.center_y - y * self.scale

        circle_id = self.canvas.create_oval(canvas_x - self.circle_radius, canvas_y - self.circle_radius,
                                            canvas_x + self.circle_radius, canvas_y + self.circle_radius,
                                            outline="blue", width=2)

        self.circles.append((x, y, circle_id))
        self.update_circle_list()

    def start_algorithm(self):
        intersecting_circles = self.find_intersecting_circles([(cx, cy) for cx, cy, _ in self.circles])
        intersecting_ids = set()

        unique_intersections = set()
        for (x1, y1), (x2, y2) in intersecting_circles:
            unique_intersections.add(tuple(sorted([(x1, y1), (x2, y2)])))
            for cx, cy, cid in self.circles:
                if (cx, cy) == (x1, y1) or (cx, cy) == (x2, y2):
                    intersecting_ids.add(cid)

        for _, _, cid in self.circles:
            if cid in intersecting_ids:
                self.canvas.itemconfig(cid, outline="red", width=2)
            else:
                self.canvas.itemconfig(cid, outline="blue", width=2)

        self.update_intersecting_list(unique_intersections)

    def update_intersecting_list(self, intersecting_circles):
        self.circle_list.config(state="normal")
        self.circle_list.delete("1.0", tk.END)
        self.circle_list.insert(tk.END, "Przecinające się okręgi:\n")
        for (x1, y1), (x2, y2) in intersecting_circles:
            self.circle_list.insert(tk.END,
                                    f"Okrąg o środku ({x1:.2f}, {y1:.2f}) i okrąg o środku ({x2:.2f}, {y2:.2f}) przecinają się\n")
        self.circle_list.config(state="disabled")

    def find_intersecting_circles(self, points):
        points.sort(key=lambda p: p[0])
        return self.divide_and_conquer(points)

    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def merge_and_find(self, left, right):
        result = []
        all_points = left + right
        all_points.sort(key=lambda p: p[1])
        for i in range(len(all_points)):
            for j in range(i + 1, len(all_points)):
                if all_points[j][1] - all_points[i][1] > 2:
                    break
                if self.distance(all_points[i], all_points[j]) <= 2:
                    result.append((all_points[i], all_points[j]))
        return result

    def divide_and_conquer(self, points):
        if len(points) <= 1:
            return []
        if len(points) == 2:
            if self.distance(points[0], points[1]) <= 2:
                return [(points[0], points[1])]
            else:
                return []
        mid = len(points) // 2
        left = points[:mid]
        right = points[mid:]

        left_result = self.divide_and_conquer(left)
        right_result = self.divide_and_conquer(right)
        cross_result = self.merge_and_find(left, right)

        return left_result + right_result + cross_result

    def clear_canvas(self):
        self.canvas.delete("all")
        self.circles.clear()

        self.canvas.create_line(self.center_x, 0, self.center_x, self.canvas_height, fill="gray", dash=(4, 2))
        self.canvas.create_line(0, self.center_y, self.canvas_width, self.center_y, fill="gray", dash=(4, 2))

        self.update_circle_list()


if __name__ == "__main__":
    root = tk.Tk()
    app = CircleApp(root)
    root.mainloop()
