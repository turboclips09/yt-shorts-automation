import random

hooks = [
    "A slow 90s car can feel scarier than a modern supercar.",
    "This sounds wrong, but old cars felt faster than new ones.",
    "Modern cars are quicker, yet driving feels boring.",
    "Driving used to feel illegal. Now it feels sanitized.",
    "Cars didn’t always feel this numb."
]

examples = [
    "A basic hatchback at 60 used to make your heart race.",
    "Even low speeds felt intense in older cars.",
    "You felt every vibration through the steering wheel.",
    "The engine noise alone made you nervous.",
    "Mistakes actually had consequences."
]

emotions = [
    "That tension is what made driving exciting.",
    "Fear is part of thrill.",
    "Your body knew you were moving fast.",
    "Driving demanded respect.",
    "You stayed fully alert."
]

blame = [
    "Modern cars are designed to calm you down.",
    "Speed is now hidden on purpose.",
    "Feeling speed is considered unsafe.",
    "Computers filter everything you feel.",
    "Comfort replaced excitement."
]

contrast = [
    "Thick insulation kills sound.",
    "Electronic steering removes resistance.",
    "Stability systems correct your mistakes.",
    "Suspension isolates the road.",
    "The car no longer talks to you."
]

loops = [
    "Once you notice this, driving won’t feel the same.",
    "That’s why modern speed feels empty.",
    "That’s what people actually miss.",
    "And now you know what’s gone.",
    "You’ll feel this every time you drive."
]

script = " ".join([
    random.choice(hooks),
    random.choice(examples),
    random.choice(emotions),
    random.choice(blame),
    random.choice(contrast),
    random.choice(loops)
])

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script)

print("🔥 Specific, opinionated Shorts script:")
print(script)
