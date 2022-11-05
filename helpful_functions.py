
def give_rect_movement(object_rect, velocity_x=0, velocity_y=0, acceleration_x=0, acceleration_y=0):
    if acceleration_y == 0 and acceleration_x == 0:
        object_rect.y += velocity_y
        object_rect.x += velocity_x
    elif acceleration_y != 0:
        velocity_y += acceleration_y
        object_rect.y += velocity_y
        return velocity_y
    elif acceleration_x != 0:
        velocity_x += acceleration_x
        object_rect.x += velocity_x
        return velocity_x
    else:
        velocity_y += acceleration_y
        velocity_x += acceleration_x
        object_rect.y += velocity_y
        object_rect.x += velocity_x
        return velocity_x, velocity_y


def vector_between_points(first_point, second_point):
    i = 0
    vector = []
    try:
        for _ in range(len(first_point)):
            length = second_point[i] - first_point[i]
            vector.append(length)
            i += 1
        return vector
    except IndexError:
        print("Error: Points must have same length")


def run_once(func):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return func(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

