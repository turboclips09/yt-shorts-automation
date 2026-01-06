import random

def pick_unique(pool, n):
    return random.sample(pool, n)

hooks = [
    "Cars today are faster than ever, yet they feel slower.",
    "This is why modern cars don’t feel as exciting anymore.",
    "Most people don’t realize this about how cars feel.",
    "This changes how you think about speed in cars.",
    "Cars didn’t always feel this calm while going fast."
]

openers = [
    "It has almost nothing to do with horsepower or top speed.",
    "It’s not about the engine or the numbers on the dashboard.",
    "Speed is not just a number, it’s a sensation.",
    "Your brain decides how fast a car feels before you look at the speedometer.",
    "Driving feel is mostly psychological."
]

sensory = [
    "Sound plays a huge role in how fast something feels.",
    "Vibration tells your body how much speed you’re carrying.",
    "Steering weight and feedback change perception instantly.",
    "Road noise and engine response shape excitement.",
    "The way a car reacts matters more than raw speed."
]

modern_design = [
    "Modern cars are designed to hide speed from the driver.",
    "New cars are built to feel stable and calm at all times.",
    "Comfort and safety now come before raw feedback.",
    "Technology smooths out almost every sensation.",
    "Computers filter most of what the driver used to feel."
]

details = [
    "Heavier sound insulation blocks noise.",
    "Electronic steering removes resistance.",
    "Throttle response is computer controlled.",
    "Suspension absorbs bumps aggressively.",
    "Stability systems correct every movement."
]

contrast = [
    "Older cars didn’t filter any of this.",
    "There was nothing separating the driver from the road.",
    "You felt every vibration and heard every sound.",
    "Even low speeds felt intense.",
    "Driving demanded attention."
]

realizations = [
    "That’s why slower cars used to feel exciting.",
    "That’s why speed felt dramatic years ago.",
    "That’s why driving felt more alive.",
    "That’s why people miss how cars used to feel.",
    "That’s why excitement isn’t just about speed."
]

loops = [
    "And once you notice this, you’ll feel it every time you drive.",
    "After this, cars won’t feel the same anymore.",
    "That realization completely changes how driving feels.",
    "Now you’ll start noticing it everywhere.",
    "That’s the detail most drivers never think about."
]

# Build script with guaranteed variety
hook = random.choice(hooks)
opener = random.choice(openers)

sensory_block = pick_unique(sensory, 2)
detail_block = pick_unique(details, 2)

script = (
    f"{hook} "
    f"{opener} "
    f"{sensory_block[0]} {sensory_block[1]} "
    f"{random.choice(modern_design)} "
    f"{detail_block[0]} {detail_block[1]} "
    f"{random.choice(contrast)} "
    f"{random.choice(realizations)} "
    f"{random.choice(loops)}"
)

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script.strip())

print("Generated premium, non-repetitive 35–45s script:")
print(script)
