import tkinter as tk
import math

class CircleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dodawanie i zaznaczanie kół (środek w 0,0)")
        
        self.canvas_width = 1000
        self.canvas_height = 700
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
        
        self.clear_button = tk.Button(root, text="Wyczyść", command=self.clear_canvas)
        self.clear_button.grid(row=3, column=0, columnspan=4)
        

        self.circle_list = tk.Text(root, width=50, height=10, state="disabled", bg="lightgray")
        self.circle_list.grid(row=4, column=0, columnspan=4, pady=10)
        
        self.circles = []


    def update_circle_list(self):
        self.circle_list.config(state="normal")
        self.circle_list.delete("1.0", tk.END)
        for idx, (x, y) in enumerate(self.circles, start=1):
            self.circle_list.insert(tk.END, f"{idx}. Środek: ({x:.2f}, {y:.2f})\n")
        self.circle_list.config(state="disabled")
        
        
    def add_circle(self):
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            r = 1
            
            canvas_x = self.center_x + x
            canvas_y = self.center_y - y
            
            self.canvas.create_oval(canvas_x-r, canvas_y-r, canvas_x+r, canvas_y+r, outline="blue", width=2)
            self.circles.append((x, y))
            self.update_circle_list()
            
        except ValueError:
            tk.messagebox.showerror("Błąd", "Wprowadź prawidłowe współrzędne liczbowe!")


    def clear_canvas(self):
        self.canvas.delete("all")
        self.circles.clear()

        self.canvas.create_line(self.center_x, 0, self.center_x, self.canvas_height, fill="gray", dash=(4, 2))
        self.canvas.create_line(0, self.center_y, self.canvas_width, self.center_y, fill="gray", dash=(4, 2))
        self.update_circle_list()


    def find_intersecting_circles(self, points):
        points.sort(key=lambda p: p[0])

        result = self.divide_and_conquer(points)

        indexed_result = [((points.index(p1), points.index(p2))) for p1, p2 in result]
        return indexed_result
    
    
    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


    def merge_and_find(self, left, right):
        result = []
        all_points = left + right
        all_points.sort(key=lambda p: p[1])  # y
        for i in range(len(all_points)):
            for j in range(i + 1, len(all_points)):
                if all_points[j][1] - all_points[i][1] > 2:  
                    break
                if self.distance(all_points[i], all_points[j]) <= 2:
                    result.append((all_points[i], all_points[j]))
        return result


    def divide_and_conquer(self,points):
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




if __name__ == "__main__":
    root = tk.Tk()
    app = CircleApp(root)
    root.mainloop()

    
    
    
