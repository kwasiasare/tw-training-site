# -*- coding: utf-8 -*-
"""Render lecture slides (PNG) + per-slide narration text for one instructor video.
Sample topic: Month 1 - Functions in Python."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))
VID = os.path.join(OUT, 'videos', 'M1_Functions')
os.makedirs(VID, exist_ok=True)

W, H = 1280, 720
NAVY = (0x1F, 0x3A, 0x5F)
ACCENT = (0x2E, 0x86, 0xC1)
WHITE = (0xFF, 0xFF, 0xFF)
DARK = (0x22, 0x2A, 0x33)
GREY = (0x66, 0x66, 0x66)
CODEBG = (0xF2, 0xF4, 0xF7)
GREEN = (0x1E, 0x8A, 0x4C)

F = 'C:/Windows/Fonts/'
font_title = ImageFont.truetype(F + 'arialbd.ttf', 46)
font_h = ImageFont.truetype(F + 'arialbd.ttf', 40)
font_body = ImageFont.truetype(F + 'arial.ttf', 32)
font_code = ImageFont.truetype(F + 'consola.ttf', 24)
font_small = ImageFont.truetype(F + 'arial.ttf', 20)
font_big = ImageFont.truetype(F + 'arialbd.ttf', 64)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# slide dicts: type 'title' or 'content'. content has title, bullets[], code(optional)
SLIDES = [
    {'type': 'title',
     'title': 'Functions in Python',
     'sub': 'Month 1 - Python Foundations  |  Lesson 6',
     'narration': "Welcome to Month One of your journey from maths graduate to AI engineer. "
                  "In this lesson we'll cover one of the most important ideas in all of programming: functions. "
                  "By the end you'll know how to write your own functions, pass them information, get results back, "
                  "and organise your code into reusable modules."},
    {'type': 'content',
     'title': 'Why functions?',
     'bullets': [
        'A function is a reusable, named block of code.',
        'Write the logic once, call it as many times as you like.',
        'They make code shorter, clearer, and easier to fix.',
        'Think of them like mathematical functions: input goes in, output comes out.'],
     'narration': "So why do we need functions? Imagine you have a piece of logic you use again and again. "
                  "Without functions you'd copy and paste it everywhere, and if you found a bug you'd have to fix it in every copy. "
                  "A function lets you write that logic once, give it a name, and reuse it. "
                  "As a maths graduate, this will feel familiar: a function takes an input, does something, and returns an output. "
                  "Same idea, just in code."},
    {'type': 'content',
     'title': 'Defining a function',
     'bullets': [
        'Use the def keyword, a name, parentheses, and a colon.',
        'The indented block below is the function body.',
        'Calling it runs that body.'],
     'code': "def greet():\n    print(\"Hello, world!\")\n\ngreet()   # call it\n# Output: Hello, world!",
     'narration': "Here's how we define a function. We use the keyword def, short for define, followed by the name we choose, "
                  "then parentheses, then a colon. Everything indented underneath is the function's body. "
                  "In this example the function is called greet, and its body prints Hello, world. "
                  "Defining a function does not run it. To run it, we call it by writing its name followed by parentheses. "
                  "When we call greet, Python runs the body and prints the message."},
    {'type': 'content',
     'title': 'Parameters and arguments',
     'bullets': [
        'Parameters are inputs listed in the parentheses.',
        'Arguments are the actual values you pass when calling.',
        'This makes a function flexible.'],
     'code': "def greet(name):\n    print(\"Hello, \" + name + \"!\")\n\ngreet(\"Dami\")    # Hello, Dami!\ngreet(\"Ada\")     # Hello, Ada!",
     'narration': "Functions become powerful when they take inputs. The names inside the parentheses are called parameters. "
                  "Here, name is a parameter. When we call the function, the real values we hand over, like the text Dami or Ada, "
                  "are called arguments. The same function now greets anyone, depending on the argument we pass. "
                  "One definition, many uses."},
    {'type': 'content',
     'title': 'Returning values',
     'bullets': [
        'Use return to send a result back to the caller.',
        'The returned value can be stored in a variable.',
        'A function without return gives back None.'],
     'code': "def add(a, b):\n    return a + b\n\ntotal = add(3, 4)\nprint(total)   # 7",
     'narration': "Often we don't just want a function to do something, we want it to give us a value back. "
                  "That's what the return keyword does. Here, the add function takes two numbers and returns their sum. "
                  "We capture that result in a variable called total, and print it to get seven. "
                  "Be careful: if a function has no return statement, it automatically gives back the special value None."},
    {'type': 'content',
     'title': 'Default and keyword arguments',
     'bullets': [
        'Default values are used when no argument is given.',
        'Keyword arguments name the value explicitly.',
        'Both make functions easier and safer to call.'],
     'code': "def greet(name, greeting=\"Hello\"):\n    return greeting + \", \" + name\n\ngreet(\"Dami\")                 # Hello, Dami\ngreet(\"Dami\", greeting=\"Hi\")   # Hi, Dami",
     'narration': "You can give parameters default values. Here, greeting defaults to Hello. "
                  "If we don't supply a greeting, Python uses that default. "
                  "We can also pass arguments by name, which we call keyword arguments. "
                  "Writing greeting equals Hi makes our intent crystal clear and lets us skip or reorder optional inputs. "
                  "This is something you'll see constantly when working with libraries and A I tools later."},
    {'type': 'content',
     'title': 'Scope: local vs global',
     'bullets': [
        'Variables created inside a function are local to it.',
        'They disappear once the function finishes.',
        'Keep functions self-contained; pass data in, return data out.'],
     'code': "def square(x):\n    result = x * x   # local variable\n    return result\n\nprint(square(5))   # 25\n# print(result)    # Error: result is not defined here",
     'narration': "Here's a concept that trips up beginners: scope. A variable you create inside a function only exists inside that function. "
                  "We call it a local variable. Once the function finishes, that variable is gone. "
                  "In this example, result lives only inside square. Trying to use it outside causes an error. "
                  "The clean habit is to keep functions self-contained: pass data in through parameters, and send data out through return."},
    {'type': 'content',
     'title': 'Modules: reuse across files',
     'bullets': [
        'A module is just a Python file with functions in it.',
        'Import it to reuse those functions elsewhere.',
        'The standard library gives you thousands for free.'],
     'code': "# file: mymath.py\ndef add(a, b):\n    return a + b\n\n# file: main.py\nimport mymath\nprint(mymath.add(2, 3))   # 5\n\nimport math\nprint(math.sqrt(16))      # 4.0",
     'narration': "Once you have useful functions, you'll want to reuse them across different files. "
                  "That's what modules are for. A module is simply a Python file containing functions. "
                  "You bring it into another file using the import keyword. "
                  "Here we import our own module called mymath, and we also import the built-in math module to use its square-root function. "
                  "Python's standard library gives you thousands of ready-made functions for free, just an import away."},
    {'type': 'content',
     'title': 'Common mistakes',
     'bullets': [
        'Defining a function but forgetting to call it.',
        'Confusing print and return - print shows, return gives back a value.',
        'Forgetting the colon, or wrong indentation in the body.',
        'Expecting a local variable to exist outside the function.'],
     'narration': "Let's flag the mistakes that catch nearly everyone at first. "
                  "One: defining a function but never calling it, then wondering why nothing happens. "
                  "Two: confusing print and return. Print just shows text on screen; return hands a value back so your program can use it. "
                  "Three: forgetting the colon after the parentheses, or getting the indentation wrong. "
                  "And four: expecting a local variable to be available outside its function. "
                  "Watch for these and you'll save yourself hours of debugging."},
    {'type': 'content',
     'title': 'Recap & your task',
     'bullets': [
        'def names a reusable block; call it with ().',
        'Parameters take input; return sends output back.',
        'Defaults and keywords make calls flexible.',
        'Modules let you reuse and import functions.',
        'Practice: rewrite a past script using functions.'],
     'narration': "Let's recap. The def keyword defines a reusable, named block of code that you run by calling it. "
                  "Parameters let you pass information in, and return sends a result back out. "
                  "Default and keyword arguments make your functions flexible to call. "
                  "And modules let you organise and reuse functions across your whole project. "
                  "Your task before the next lesson: take one of your earlier scripts and rewrite it using functions. "
                  "That single exercise will lock in everything we covered today. Great work, and I'll see you in the next lesson."},
]


def draw_footer(d, idx, total):
    d.line([(60, H - 60), (W - 60, H - 60)], fill=(0xDD, 0xDD, 0xDD), width=1)
    d.text((60, H - 48), 'Maths -> AI Course   |   Month 1: Python Foundations   |   Functions',
           font=font_small, fill=GREY)
    label = f'{idx}/{total}'
    d.text((W - 60 - d.textlength(label, font=font_small), H - 48), label, font=font_small, fill=GREY)


def render_title(s, idx, total):
    img = Image.new('RGB', (W, H), NAVY)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 300, W, 308], fill=ACCENT)
    t = s['title']
    d.text(((W - d.textlength(t, font=font_big)) / 2, 200), t, font=font_big, fill=WHITE)
    sub = s['sub']
    d.text(((W - d.textlength(sub, font=font_body)) / 2, 330), sub, font=font_body, fill=(0xCF, 0xE2, 0xF3))
    foot = 'An instructor lesson  -  generated study video'
    d.text(((W - d.textlength(foot, font=font_small)) / 2, 640), foot, font=font_small, fill=(0xAE, 0xD6, 0xF1))
    return img


def render_content(s, idx, total):
    img = Image.new('RGB', (W, H), WHITE)
    d = ImageDraw.Draw(img)
    # header band
    d.rectangle([0, 0, W, 110], fill=NAVY)
    d.rectangle([0, 110, W, 117], fill=ACCENT)
    d.text((60, 30), s['title'], font=font_h, fill=WHITE)
    y = 160
    for b in s.get('bullets', []):
        lines = wrap(d, b, font_body, W - 200)
        d.ellipse([62, y + 12, 74, y + 24], fill=ACCENT)
        for i, ln in enumerate(lines):
            d.text((100, y), ln, font=font_body, fill=DARK)
            y += 44
        y += 10
    # code block
    if s.get('code'):
        code_lines = s['code'].split('\n')
        ch = 34 * len(code_lines) + 30
        cy = max(y + 10, H - 80 - ch)
        d.rectangle([60, cy, W - 60, cy + ch], fill=CODEBG)
        d.rectangle([60, cy, 66, cy + ch], fill=ACCENT)
        ty = cy + 15
        for ln in code_lines:
            color = GREEN if ln.strip().startswith('#') else NAVY
            d.text((90, ty), ln, font=font_code, fill=color)
            ty += 34
    draw_footer(d, idx, total)
    return img


total = len(SLIDES)
for i, s in enumerate(SLIDES, 1):
    if s['type'] == 'title':
        img = render_title(s, i, total)
    else:
        img = render_content(s, i, total)
    img.save(os.path.join(VID, f'slide_{i:02d}.png'))
    with open(os.path.join(VID, f'narr_{i:02d}.txt'), 'w', encoding='utf-8') as f:
        f.write(s['narration'])

with open(os.path.join(VID, 'count.txt'), 'w') as f:
    f.write(str(total))
print(f'Rendered {total} slides + narration to {VID}')
