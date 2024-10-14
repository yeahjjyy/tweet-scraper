import os
import random

from configs.configs import root_path


def modify_random_canvas_js():

    with open(os.path.join(root_path, 'browser', 'js', 'random_canvas_template.js'), encoding='utf-8') as f:
        js = f.read()
    salts = ['rsalt', 'gsalt', 'bsalt', 'asalt']
    for salt in salts:
        salt_random = random.randint(-3, 3)
        js = js.replace(salt, str(salt_random))
    js_script_name = 'random_canvas.js'
    with open(os.path.join(root_path, 'browser', 'js', 'random_canvas.js'), 'w', encoding='utf-8') as f:
        f.write(js)
    return js_script_name
