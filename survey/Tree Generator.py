import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(20, 12))
ax.set_xlim(0, 1600)
ax.set_ylim(0, 600)
ax.axis('off')

# Utility to draw node
def draw_node(x, y, text, shape='ellipse', color='#fff4cc'):
    if shape == 'ellipse':
        ellipse = patches.Ellipse((x, y), width=160, height=60, edgecolor='black', facecolor=color, linewidth=2)
        ax.add_patch(ellipse)
    elif shape == 'rect':
        rect = patches.Rectangle((x-50, y-25), 100, 50, edgecolor='black', facecolor=color, linewidth=2)
        ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=10)

# Utility to draw line with optional label
def draw_edge(x1, y1, x2, y2, label=None, align='left'):
    ax.plot([x1, x2], [y1, y2], color='black', linewidth=2)
    if label:
        lx = (x1 + x2) / 2
        ly = (y1 + y2) / 2
        if align == 'left':
            ax.text(lx - 10, ly, label, ha='right', va='center', fontsize=9)
        else:
            ax.text(lx + 10, ly, label, ha='left', va='center', fontsize=9)

# Coordinates for each level
level_y = {
    1: 60,
    2: 140,
    3: 260,
    4: 400,
    5: 550
}

# Level 1
draw_node(800, level_y[1], "employment_status", color='#cce5ff')
draw_edge(800, level_y[1]+30, 500, level_y[2]-30, "unemployed", 'left')
draw_edge(800, level_y[1]+30, 1100, level_y[2]-30, "stable", 'right')

# Level 2
draw_node(500, level_y[2], "assets")
draw_node(1100, level_y[2], "income")

# Level 3
draw_edge(500, level_y[2]+30, 300, level_y[3]-30, "< 10.000", 'left')
draw_edge(500, level_y[2]+30, 700, level_y[3]-30, "≥ 10.000", 'right')
draw_node(300, level_y[3], "credit_history")
draw_node(700, level_y[3], "credit_history")

draw_edge(1100, level_y[2]+30, 900, level_y[3]-30, "< 50.000", 'left')
draw_edge(1100, level_y[2]+30, 1300, level_y[3]-30, "≥ 50.000", 'right')
draw_node(900, level_y[3], "assets")
draw_node(1300, level_y[3], "credit_history")

# Level 4 + Early exits
# From 300
draw_edge(300, level_y[3]+30, 200, level_y[4]-30, "bad", 'left')
draw_edge(300, level_y[3]+30, 400, level_y[4]-30, "good", 'right')
draw_node(200, level_y[4], "loan_amount")
draw_node(400, level_y[4], "loan_amount")

# From 700 - ends early at loan_amount
draw_node(700, level_y[4], "loan_amount")

# From 900
draw_edge(900, level_y[3]+30, 800, level_y[4]-30, "< 20.000", 'left')
draw_edge(900, level_y[3]+30, 1000, level_y[4]-30, "≥ 20.000", 'right')
draw_node(800, level_y[4], "loan_amount")
draw_node(1000, level_y[4], "loan_amount")

# From 1300
draw_edge(1300, level_y[3]+30, 1200, level_y[4]-30, "excellent", 'left')
draw_edge(1300, level_y[3]+30, 1400, level_y[4]-30, "bad", 'right')
draw_node(1200, level_y[4], "loan_amount")
draw_node(1400, level_y[4], "loan_amount")

# Leaves
leaf_xs = [150, 250, 370, 470, 670, 770, 970, 1070, 1170, 1270, 1370, 1470]
for i, x in enumerate(leaf_xs):
    draw_edge(x, level_y[4]+30, x, level_y[5]-30,
              "< 10.000" if i % 2 == 0 else "≥ 10.000",
              'left' if i % 2 == 0 else 'right')
    status = "denied" if i % 2 == 0 else "approved"
    color = '#ffcccc' if status == "denied" else '#ccffcc'
    draw_node(x, level_y[5], status, shape='rect', color=color)

plt.show()
