def is_dark(wf):
    if not wf.alfred_env.get('theme_background'):
        return True
    rgb = [int(x) for x in wf.alfred_env['theme_background'][5:-6].split(',')]
    return (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255 < 0.5


def get_icon(wf, name):
    name = '%s-dark' % name if is_dark(wf) else name
    return "icons/%s.png" % name


def search_key_for_action(action):
    """ Name and description are search keys. """
    elements = []
    elements.append(action['name'])
    elements.append(action['description'])
    return u' '.join(elements)
