import random
import datetime

hooks = [
    "Most people don’t notice this.",
    "This car feels illegal to drive.",
    "This is why this car feels different.",
    "This car was built without thinking twice.",
    "This car doesn’t follow normal rules."
]

bodies = [
    "It looks normal at first glance, but once it starts moving, everything changes.",
    "The engine sound alone tells you this car was not built for comfort.",
    "Every turn feels aggressive, every acceleration feels intentional.",
    "This car prioritizes speed and feel over logic and safety.",
    "It’s the kind of car that rewards confidence, not hesitation."
]

details = [
    "The suspension is stiff.",
    "The acceleration is instant.",
    "The steering feels raw.",
    "The exhaust is loud and unapologetic.",
    "The driving position feels low and focused."
]

loops = [
    "And that’s why driving it feels unforgettable.",
    "That’s why this car leaves a lasting impression.",
    "And that’s why people still talk about it.",
    "That’s why this kind of car is rare today.",
    "And that’s why this feeling is hard to replace."
]

script = f"""
{random.choice(hooks)}

{random.choice(bodies)}

{random.choice(details)}
{random.choice(details)}

{random.choice(loops)}
"""

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script.strip())

print("Generated stock-friendly script:")
print(script)
