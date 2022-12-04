import math
import tkinter
import colorsys

def from_hsv(h, s, v):
    rgb = colorsys.hsv_to_rgb(h, s, v)
    return from_rgb(rgb[0], rgb[1], rgb[2])

def from_rgb(r, g, b):
    # Convert floats to 8 bit integer
    r = math.floor(r * 255)
    g = math.floor(g * 255)
    b = math.floor(b * 255)

    # Return the color string
    return "#%02x%02x%02x" % (r, g, b)


def calculate_entropy(data: bytes):
    # First create a count of each independent value
    mapping = {}
    for byte in data:
        if byte in mapping:
            mapping[byte] += 1
        else:
            mapping[byte] = 1

    # Turn the counts into probabilities
    for entry in mapping:
        mapping[entry] /= len(data)

    # Calculate shannon entropy
    acc = 0
    for entry in mapping:
        acc += mapping[entry] * math.log2(1 / mapping[entry])

    # Return the result
    return acc


# init tk
root = tkinter.Tk()

# create canvas
ctx = tkinter.Canvas(root, bg="white", height=1000, width=800)

# read in the binary file and calculate entropy chunk by chunk
blob = open("blob.bin", "rb")
chunk_size = 2048
total_chunks = 1495 * 2
entropy = []
max_entropy = 0
for i in range(0, total_chunks):
    data = blob.read(chunk_size)
    calc_ent = calculate_entropy(data)
    entropy.append(calc_ent)
    if calc_ent > max_entropy:
        max_entropy = calc_ent

# Grid Parameters
cells_x = 40
cells_y = 80
size_x = 20
size_y = 10

# Draw grid
chunk = 0
for y in range(0, cells_y, 1):
    halt = False
    for x in range(0, cells_x, 1):
        x_grad = x / cells_x
        y_grad = y / cells_y
        ctx.create_rectangle(size_x * x, size_y * y, size_x * x + size_x, size_y * y + size_y, fill=from_rgb(entropy[chunk] / max_entropy, entropy[chunk] / max_entropy, entropy[chunk] / max_entropy))
        chunk += 1

        if chunk == total_chunks:
            halt = True
            break

    if halt:
        break

# add to window and show
ctx.pack()
root.mainloop()
