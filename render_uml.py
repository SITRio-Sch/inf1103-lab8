"""Render uml_lab9.png from the class layout below (matches uml_lab9.drawio)."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1500, 1000
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

f_title = ImageFont.truetype("arialbd.ttf", 16)
f_body = ImageFont.truetype("arial.ttf", 12)
f_small = ImageFont.truetype("arial.ttf", 11)



def draw_box(x, y, w, hh, ah, mh, name, attrs, methods, abstract, iface):
    h = hh + ah + mh + 8
    d.rectangle([x, y, x + w, y + h], fill="#ffffff", outline="#333333", width=2)
    label = name
    if abstract:
        d.text((x + 6, y + 2), "«abstract»", font=f_small, fill="#555555")
        d.text((x + 6, y + 16), label, font=f_title, fill="#000000")
    elif iface:
        d.text((x + 6, y + 2), "«interface»", font=f_small, fill="#555555")
        d.text((x + 6, y + 16), label, font=f_title, fill="#000000")
    else:
        d.text((x + 6, y + 4), label, font=f_title, fill="#000000")
    yy = y + hh
    if attrs:
        d.line([x, y + hh - 4, x + w, y + hh - 4], fill="#333333", width=1)
        for a in attrs:
            d.text((x + 6, yy), a, font=f_body, fill="#000000")
            yy += 20
    if methods:
        d.line([x, yy - 4, x + w, yy - 4], fill="#333333", width=1)
        for m in methods:
            d.text((x + 6, yy), m, font=f_body, fill="#000000")
            yy += 20
    return (x, y, x + w, y + h)


def anchor(box, side):
    x0, y0, x1, y1 = box
    if side == "l":
        return (x0, (y0 + y1) / 2)
    if side == "r":
        return (x1, (y0 + y1) / 2)
    if side == "t":
        return ((x0 + x1) / 2, y0)
    return ((x0 + x1) / 2, y1)


def line(a, b, dashed=False, label=None, label_pos=None):
    if dashed:
        # draw a dashed line by segments
        import math
        n = 12
        for i in range(n):
            t0, t1 = i / n, (i + 0.6) / n
            d.line([
                (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
                (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1),
            ], fill="#666666", width=1)
    else:
        d.line([a, b], fill="#333333", width=1)
    if label:
        px, py = label_pos if label_pos else ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 8)
        d.text((px, py), label, font=f_small, fill="#333333")


def triangle(a, b):
    """Hollow generalisation arrow head at b (parent end)."""
    import math
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    tip = b
    back = 14
    spread = 7
    p1 = (tip[0] - back * math.cos(ang) + spread * math.sin(ang),
          tip[1] - back * math.sin(ang) - spread * math.cos(ang))
    p2 = (tip[0] - back * math.cos(ang) - spread * math.sin(ang),
          tip[1] - back * math.sin(ang) + spread * math.cos(ang))
    d.line([a, p1], fill="#333333", width=1)
    d.line([a, p2], fill="#333333", width=1)
    d.line([p1, tip], fill="#ffffff", width=2)
    d.line([p2, tip], fill="#ffffff", width=2)
    d.line([p1, p2], fill="#333333", width=1)


def diamond(a, b, filled=True):
    """Association diamond at a (owner end)."""
    import math
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    cx, cy = a[0] + 12 * math.cos(ang), a[1] + 12 * math.sin(ang)
    long, short = 12, 8
    px = [cx + long * math.cos(ang), cx + short * math.sin(ang),
          cx - long * math.cos(ang), cx - short * math.sin(ang)]
    py = [cy + long * math.sin(ang), cy - short * math.cos(ang),
          cy - long * math.sin(ang), cy + short * math.cos(ang)]
    d.line([b, (px[0], py[0])], fill="#333333", width=1)
    pts = [(px[0], py[0]), (px[1], py[1]), (px[2], py[2]), (px[3], py[3])]
    if filled:
        d.polygon(pts, fill="#333333")
    else:
        d.polygon(pts, outline="#333333", width=1)
    d.line([a, (px[2], py[2])], fill="#333333", width=1)


# --- classes -----------------------------------------------------------
inv = draw_box(30, 30, 300, 30, 24, 90, "Inventory",
               ["- products: Product [0..*]"],
               ["+ addProduct(p): Boolean", "+ removeProduct(id): Product",
                "+ findProduct(id): Product"], False, False)
sup = draw_box(30, 260, 260, 30, 60, 44, "Supplier",
               ["- supplierId: String", "- name: String", "- contactEmail: String"],
               ["+ displayInformation()", "+ toDict()"], False, False)
prod = draw_box(430, 210, 340, 44, 100, 120, "Product",
                ["- productId: String", "- name: String", "- price: Float",
                 "- stock: Integer", "- supplier: Supplier"],
                ["+ updateStock(q): Void", "+ displayInformation()", "+ toDict()",
                 "+ {abstract} getFulfilmentInfo(): String"], True, False)
phys = draw_box(330, 560, 240, 30, 24, 56, "PhysicalProduct",
                ["- weight: Float"],
                ["+ getFulfilmentInfo(): String", "+ calculateShippingCost(): Float"],
                False, False)
dig = draw_box(620, 560, 240, 30, 24, 36, "DigitalProduct",
               ["- downloadSize: Float"], ["+ getFulfilmentInfo(): String"], False, False)
can = draw_box(30, 560, 240, 44, 0, 30, "CanBeShipped", [],
               ["+ calculateShippingCost(): Float"], False, True)
fac = draw_box(760, 60, 360, 30, 0, 46, "ProductFactory", [],
               ["+ {static} create(type, id, name, price,", "stock, supplier, weight, downloadSize): Product"],
               False, False)
ord_ = draw_box(1140, 210, 330, 30, 44, 100, "Order",
                ["- orderId: String", "- orderLines: OrderLine [1..*]",
                 "- discount: DiscountStrategy [1]"],
                ["+ setDiscount(s): Void", "+ addOrderLine(p, q): Void",
                 "+ removeOrderLine(id): Boolean", "+ calculateTotal(): Float"], False, False)
ordl = draw_box(1140, 460, 330, 30, 44, 52, "OrderLine",
                ["- product: Product", "- quantity: Integer"],
                ["+ calculateSubtotal(): Float", "+ displayInformation()"], False, False)
strat = draw_box(1140, 620, 330, 44, 0, 26, "DiscountStrategy",
                [], ["+ {abstract} apply(total): Float"], True, False)
nod = draw_box(430, 760, 200, 30, 0, 26, "NoDiscount", [], ["+ apply(total): Float"], False, False)
pct = draw_box(660, 760, 220, 30, 24, 26, "PercentageDiscount",
              ["- percent: Float"], ["+ apply(total): Float"], False, False)
blk = draw_box(910, 760, 240, 30, 44, 26, "BulkDiscount",
              ["- threshold: Float", "- amount: Float"], ["+ apply(total): Float"], False, False)
stu = draw_box(1180, 760, 220, 30, 24, 26, "StudentDiscount",
               ["- percent: Float"], ["+ apply(total): Float"], False, False)

# --- relationships -----------------------------------------------------
triangle(anchor(phys, "t"), anchor(prod, "b"))          # PhysicalProduct -> Product
triangle(anchor(dig, "t"), anchor(prod, "b"))           # DigitalProduct -> Product
line(anchor(phys, "l"), anchor(can, "r"), dashed=True,
     label="implements", label_pos=(250, 585))
diamond(anchor(inv, "r"), anchor(prod, "l"), filled=False)  # aggregation: Inventory uses Product
line(anchor(prod, "l"), anchor(sup, "r"), label="1", label_pos=(340, 250))
line(anchor(ordl, "l"), anchor(prod, "r"), label="1", label_pos=(900, 480))
diamond(anchor(ord_, "b"), anchor(ordl, "t"), filled=True)  # composition: Order owns OrderLine
# Aggregation diamond: the client owns the strategy and orders can share it.
diamond((1360, 392), anchor(strat, "t"), filled=False)
d.text((1352, 545), "1", font=f_small, fill="#333333")
triangle(anchor(nod, "r"), anchor(strat, "l"))
triangle(anchor(pct, "r"), anchor(strat, "l"))
triangle(anchor(blk, "r"), anchor(strat, "l"))
triangle(anchor(stu, "t"), anchor(strat, "b"))          # StudentDiscount -> DiscountStrategy
line(anchor(fac, "b"), anchor(prod, "t"), dashed=True,
     label="creates()", label_pos=(720, 175))

img.save("uml_lab9.png")
print("uml_lab9.png written")
