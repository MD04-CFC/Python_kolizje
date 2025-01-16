import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def find_intersections(points):
    def divide_and_conquer(points_sorted_x, points_sorted_y):
        n = len(points_sorted_x)
        if n <= 3:  
            return brute_force(points_sorted_x)

        mid = n // 2
        mid_x = points_sorted_x[mid][0]
        left_x = points_sorted_x[:mid]
        right_x = points_sorted_x[mid:]
        
        left_y = [p for p in points_sorted_y if p[0] <= mid_x]
        right_y = [p for p in points_sorted_y if p[0] > mid_x]

        left_pairs = divide_and_conquer(left_x, left_y)
        right_pairs = divide_and_conquer(right_x, right_y)

        split_pairs = find_cross_pairs(points_sorted_y, mid_x)
        
        return left_pairs + right_pairs + split_pairs

    def brute_force(points):
        pairs = []
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                if distance(points[i], points[j]) <= 2:
                    pairs.append((points[i], points[j]))
        return pairs

    def find_cross_pairs(points_sorted_y, mid_x):
        strip = [p for p in points_sorted_y if abs(p[0] - mid_x) <= 2]
        pairs = []
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 8, len(strip))):  
                if distance(strip[i], strip[j]) <= 2:
                    pairs.append((strip[i], strip[j]))
        return pairs

    points_sorted_x = sorted(points, key=lambda p: p[0])
    points_sorted_y = sorted(points, key=lambda p: p[1])
    return divide_and_conquer(points_sorted_x, points_sorted_y)

# Przykład użycia
circles = [(1, 1), (2, 2), (4, 4), (5, 5), (3, 1)]
intersections = find_intersections(circles)
print("Przecinające się koła:", intersections)
