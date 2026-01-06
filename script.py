import random

hooks = [
    "Most people don’t know this about cars, and once you hear it, you can’t unhear it.",
    "This completely changes how driving actually feels.",
    "Almost nobody realizes this while driving, but it explains everything.",
    "This is why cars feel different today, even when they’re faster.",
    "This car fact sounds fake, but it’s actually real."
]

openers = [
    "Two cars can be going the exact same speed, yet feel completely different to the driver.",
    "Cars today are faster than ever, but somehow they don’t feel that way.",
    "Speed isn’t just about numbers on the dashboard, it’s about perception.",
    "Your brain decides how fast a car feels long before you check the speedometer.",
    "Driving feel has very little to do with horsepower alone."
]

build_up = [
    "That sensation comes from sound, vibration, feedback, and how connected you feel to the road.",
    "It’s the noise you hear, the way the car moves, and how much information reaches your body.",
    "Your senses detect speed through vibration and sound before your eyes do.",
    "Every small signal tells your brain whether something feels fast or calm.",
    "Those signals stack together to create excitement."
]

modern_cars = [
    "Modern cars are specifically designed to hide speed from the driver.",
    "Newer cars are built to feel stable and calm, even when moving quickly.",
    "Comfort and safety now come before raw feedback.",
    "Technology smooths out most of the sensations you used to feel.",
    "Driving today is heavily filtered by computers."
]

details = [
    "Quieter cabins with heavy insulation.",
    "Electronic steering that removes resistance.",
    "Computer-controlled throttle response.",
    "Stability systems correcting every movement.",
    "Suspension tuned to absorb everything."
]

contrast = [
    "Older cars didn’t filter any of that.",
    "There was nothing separating you from the road.",
    "Every vibration, sound, and movement came straight to the driver.",
    "That’s why even slow speeds felt intense.",
    "Driving demanded attention and respect."
]

realization = [
    "That’s why slower cars used to feel exciting.",
    "That’s why speed felt more dramatic in the past.",
    "That’s why driving felt more alive.",
    "That’s why people still talk about how cars used to feel.",
    "That’s why excitement isn’t just about speed."
]

loops = [
    "And once you notice this, you’ll feel it every time you drive.",
    "That realization completely changes how driving feels.",
    "And after this, cars won’t feel the same again.",
    "That’s the part most drivers never consciously realize.",
    "And now you’ll start noticing it everywhere."
]

script = f"""{random.choice(hooks)} {random.choice(openers)} {random.choice(build_up)} {random.choice(modern_cars)} {random.choice(details)} {random.choice(details)} {random.choice(contrast)} {random.choice(realization)} {random.choice(loops)}"""

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script.strip())

print("Generated fast-paced 40s script:")
print(script)
