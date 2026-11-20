"""Render uml_lab9.png. Box positions and edges match uml_lab9.drawio."""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1820, 1000
LINE = "#333333"
DASH = "#666666"
LEFT_Q, RIGHT_Q = "«", "»"  # guillemets for stereotypes

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

f_title = ImageFont.truetype("arialbd.ttf", 16)
f_body = ImageFont.truetype("arial.ttf", 12)
f_small = ImageFont.truetype("arial.ttf", 11)


def draw_box(x, y, w, hh, ah, mh, name, attrs, methods, stereotype=None):
    """hh = header height, ah = attribute block, mh = method block (pixels)."""
    h = hh + ah + mh + 8
    d.rectangle([x, y, x + w, y + h], fill="#ffffff", outline=LINE, width=2)
    if stereotype:
        d.text((x + 6, y + 2), f"{LEFT_Q}{stereotype}{RIGHT_Q}", font=f_small, fill="#555555")
        d.text((x + 6, y + 16), name, font=f_title, fill="#000000")
    else:
        d.text((x + 6, y + 4), name, font=f_title, fill="#000000")
    yy = y + hh
    for block in (attrs, methods):
        if block:
            d.line([x, yy - 4, x + w, yy - 4], fill=LINE, width=1)
            for row in block:
                d.text((x + 6, yy), row, font=f_body, fill="#000000")
                yy += 20
    return (x, y, x + w, y + h)


def label(x, y, text):
    d.text((x, y), text, font=f_small, fill=LINE)


def unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    return dx / length, dy / length


def seg(a, b, dashed=False):
    if not dashed:
        d.line([a, b], fill=LINE, width=1)
        return
    # Dashed line drawn as short segments.
    n = 14
    for i in range(0, n, 2):
        t0, t1 = i / n, (i + 1) / n
        d.line([
            (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
            (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1),
        ], fill=DASH, width=1)


def hollow_triangle(a, tip):
    """Generalisation / realisation head at tip; stem comes from a."""
    ux, uy = unit(a, tip)
    base = (tip[0] - 14 * ux, tip[1] - 14 * uy)
    px, py = -uy, ux
    p1 = (base[0] + 7 * px, base[1] + 7 * py)
    p2 = (base[0] - 7 * px, base[1] - 7 * py)
    d.line([a, base], fill=LINE, width=1)
    d.polygon([tip, p1, p2], fill="#ffffff", outline=LINE)


def open_arrow(a, tip):
    """Open (V-shaped) arrowhead at tip, used for the dependency."""
    ux, uy = unit(a, tip)
    back = (tip[0] - 12 * ux, tip[1] - 12 * uy)
    px, py = -uy, ux
    d.line([tip, (back[0] + 5 * px, back[1] + 5 * py)], fill=DASH, width=1)
    d.line([tip, (back[0] - 5 * px, back[1] - 5 * py)], fill=DASH, width=1)


def diamond(owner, other, filled):
    """Association diamond at the owner end, line continues to other."""
    ux, uy = unit(owner, other)
    px, py = -uy, ux
    mid = (owner[0] + 12 * ux, owner[1] + 12 * uy)
    far = (owner[0] + 24 * ux, owner[1] + 24 * uy)
    left = (mid[0] + 7 * px, mid[1] + 7 * py)
    right = (mid[0] - 7 * px, mid[1] - 7 * py)
    d.line([far, other], fill=LINE, width=1)
    d.polygon([owner, left, far, right], fill=LINE if filled else "#ffffff", outline=LINE)


# --- classes -----------------------------------------------------------------
inv = draw_box(30, 30, 300, 30, 24, 90, "Inventory",
               ["- products: Product [0..*]"],
               ["+ addProduct(p): Boolean", "+ removeProduct(id): Product",
                "+ findProduct(id): Product"])
sup = draw_box(30, 260, 260, 30, 60, 44, "Supplier",
               ["- supplierId: String", "- name: String", "- contactEmail: String"],
               ["+ displayInformation()", "+ toDict()"])
prod = draw_box(430, 210, 340, 44, 100, 120, "Product",
                ["- productId: String", "- name: String", "- price: Float",
                 "- stock: Integer", "- supplier: Supplier"],
                ["+ updateStock(q): Void", "+ displayInformation()", "+ toDict()",
                 "+ {abstract} getFulfilmentInfo(): String"],
                stereotype="abstract")
phys = draw_box(330, 560, 240, 30, 24, 56, "PhysicalProduct",
                ["- weight: Float"],
                ["+ getFulfilmentInfo(): String", "+ calculateShippingCost(): Float"])
dig = draw_box(620, 560, 240, 30, 24, 36, "DigitalProduct",
               ["- downloadSize: Float"], ["+ getFulfilmentInfo(): String"])
can = draw_box(30, 560, 240, 44, 0, 30, "CanBeShipped", [],
               ["+ calculateShippingCost(): Float"], stereotype="interface")
fac = draw_box(760, 60, 360, 30, 0, 46, "ProductFactory", [],
               ["+ {static} create(type, id, name, price,",
                "stock, supplier, weight, size): Product"])
ord_ = draw_box(1140, 210, 330, 30, 64, 100, "Order",
                ["- orderId: String", "- orderLines: OrderLine [0..*]",
                 "- discount: DiscountStrategy [1]"],
                ["+ setDiscount(s): Void", "+ addOrderLine(p, q): Void",
                 "+ removeOrderLine(id): Boolean", "+ calculateTotal(): Float"])
ordl = draw_box(1140, 460, 330, 30, 44, 52, "OrderLine",
                ["- product: Product", "- quantity: Integer"],
                ["+ calculateSubtotal(): Float", "+ displayInformation()"])
strat = draw_box(1140, 620, 330, 44, 0, 26, "DiscountStrategy", [],
                 ["+ {abstract} apply(total): Float"], stereotype="abstract")
nod = draw_box(820, 760, 200, 30, 0, 26, "NoDiscount", [], ["+ apply(total): Float"])
pct = draw_box(1050, 760, 220, 30, 24, 26, "PercentageDiscount",
               ["- percent: Float"], ["+ apply(total): Float"])
blk = draw_box(1300, 760, 240, 30, 44, 26, "BulkDiscount",
               ["- threshold: Float", "- amount: Float"], ["+ apply(total): Float"])
stu = draw_box(1570, 760, 220, 30, 24, 26, "StudentDiscount",
               ["- percent: Float"], ["+ apply(total): Float"])

# --- relationships -----------------------------------------------------------
# Generalisation: PhysicalProduct and DigitalProduct -> Product
hollow_triangle((450, 560), (600, 482))
hollow_triangle((740, 560), (600, 482))

# Realisation: PhysicalProduct implements CanBeShipped
seg((330, 619), (270, 601), dashed=True)
hollow_triangle((330, 619), (270, 601))
label(268, 540, "implements")

# Aggregation: Inventory (0..*) to Product (0..*)
diamond((330, 120), (430, 240), filled=False)
label(338, 100, "0..*")
label(398, 178, "0..*")

# Association: Product (0..*) to Supplier (1)
seg((430, 340), (290, 331))
label(392, 314, "0..*")
label(296, 314, "1")

# Association: OrderLine (0..*) to Product (1)
seg((770, 440), (1140, 500))
label(776, 420, "1")
label(1096, 470, "0..*")

# Composition: Order (1) to OrderLine (0..*)
diamond((1305, 412), (1305, 460), filled=True)
label(1320, 414, "1")
label(1312, 440, "0..*")

# Aggregation: Order (0..*) to DiscountStrategy (1), routed down the right side
diamond((1470, 300), (1560, 300), filled=False)
seg((1560, 300), (1560, 659))
seg((1560, 659), (1470, 659))
label(1476, 282, "0..*")
label(1476, 640, "1")

# Generalisation: four strategies in one row under DiscountStrategy
seg((920, 728), (1680, 728))
for cx, top in ((920, 760), (1160, 760), (1420, 760), (1680, 760)):
    seg((cx, top), (cx, 728))
hollow_triangle((1305, 728), (1305, 698))

# Dependency: ProductFactory --<<creates>>--> Product
seg((940, 144), (600, 210), dashed=True)
open_arrow((940, 144), (600, 210))
label(660, 160, f"{LEFT_Q}creates{RIGHT_Q}")

img.save("uml_lab9.png")
print("uml_lab9.png written")
