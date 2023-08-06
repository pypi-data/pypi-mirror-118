def opensource(module='tkextension'):
    if module == 'tkextension' or module == '__init__':
        file = open('__init__.py')
        get = file.read()
        file.close()
        return get
    elif module == 'about':
        file = open('about.py')
        get = file.read()
        file.close()
        return get
    elif module == 'canvas':
        file = open('canvas.py')
        get = file.read()
        file.close()
        return get
    elif module == 'blackboard':
        file = open('blackboard.py')
        get = file.read()
        file.close()
        return get
    elif module == 'timer':
        file = open('timer.py')
        get = file.read()
        file.close()
        return get
    elif module == 'tix':
        file = open('tix.py')
        get = file.read()
        file.close()
        return get
    elif module == 'turtle' or module == 'turtledrawer':
        file = open('tuterdrawer.py')
        get = file.read()
        file.close()
        return get
    elif module == 'value':
        file = open('value.py')
        get = file.read()
        file.close()
        return get
    elif module == 'system':
        file = open('system.py')
        get = file.read()
        file.close()
        return get
    else:
        raise AttributeError('\'opensource\' object has no attribute \'%s\'' % module)
