import random

HOOKS = [
    "Here’s a car truth that ruins modern driving forever.",
    "Modern cars didn’t get boring by accident.",
    "This is why driving today feels impressive but empty.",
    "The biggest lie about fast cars isn’t speed.",
]

CORE = [
    "In the 90s, a 300-horsepower car felt terrifying.",
    "Today, normal family sedans quietly make the same power.",
    "Yet most drivers feel less excitement than ever.",
    "That’s because speed was never the thrill.",
    "Old cars demanded attention, skill, and respect.",
    "Steering fought back, brakes scared you, mistakes punished you.",
    "Your brain stayed fully alert every second behind the wheel.",
    "Modern cars remove that tension on purpose.",
    "Electronics fix slides before you even sense them.",
    "Automatic gearboxes decide when excitement is allowed.",
    "Some sports cars fake engine sound through speakers.",
    "You’re not driving faster — you’re being protected from feeling it.",
]

TWISTS = [
    "That’s why slower cars used to feel alive.",
    "That’s why fast cars today feel forgettable.",
    "Comfort killed connection.",
    "Safety killed involvement.",
]

LOOPS = [
    "Once you notice this, driving never feels the same.",
    "Now pay attention next time you drive.",
]

script = " ".join(
    random.sample(HOOKS, 1)
    + random.sample(CORE, 9)
    + random.sample(TWISTS, 2)
    + random.sample(LOOPS, 1)
)

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script)

print(script)
