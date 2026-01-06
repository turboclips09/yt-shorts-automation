import random

hooks = [
    "Most people don’t know this about cars.",
    "This changes how you think about driving.",
    "Almost nobody realizes this while driving.",
    "This is why cars don’t feel the same anymore.",
    "This car fact sounds fake, but it’s real."
]

openers = [
    "Two cars can be going the exact same speed and feel completely different.",
    "Cars today are faster than ever, yet they feel slower.",
    "Speed isn’t just about numbers on the dashboard.",
    "Your brain decides how fast a car feels, not the speedometer.",
    "Driving feel has almost nothing to do with horsepower."
]

build_up = [
    "That feeling comes from sound, vibration, and feedback.",
    "It’s the noise you hear and the movement you feel.",
    "Your body senses speed long before your eyes do.",
    "The way a car reacts tells your brain how fast you’re going.",
    "Every small sensation adds to the experience."
]

modern_cars = [
    "Modern cars are designed to hide speed.",
    "New cars are built to feel calm, even when moving fast.",
    "Comfort has replaced raw feedback.",
    "Technology now smooths everything out.",
    "Driving is more controlled than ever."
]

details = [
    "Quieter cabins.",
    "Electronic steering.",
    "Computer-controlled throttle.",
    "Heavy sound insulation.",
    "Stability systems correcting everything."
]

contrast = [
    "Older cars didn’t hide any of that.",
    "Older cars felt fast even at low speeds.",
    "There was nothing filtering the experience.",
    "You felt every bump and vibration.",
    "Driving demanded attention."
]

realization = [
    "That’s why slower cars used to feel exciting.",
    "That’s why speed felt more intense years ago.",
    "That’s why driving felt more alive.",
    "That’s why people remember how cars used to feel.",
    "That’s why excitement isn’t just about speed."
]

loops = [
    "And once you notice it, you can’t unfeel it.",
    "That’s why driving feels different now.",
    "And that realization changes everything.",
    "That’s the part most drivers never notice.",
    "And now you’ll notice it every time you drive."
]

script = f"""
{random.choice(hooks)}

{random.choice(openers)}

{random.choice(build_up)}

{random.choice(modern_cars)}
{random.choice(details)}
{random.choice(details)}

{random.choice(contrast)}

{random.choice(realization)}

{random.choice(loops)}
"""

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script.strip())

print("Generated 30–40s scroll-stopping car script:")
print(script)
