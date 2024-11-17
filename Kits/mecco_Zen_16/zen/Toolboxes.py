# python

class Toolboxes(object):
    """This class provides a means of appending new toolboxes to the Zen
    toolboxes list. Appending this list using the `add` method will register
    your toolbox for display in the list, but note that you must then append
    your form to the Zen toolboxes with the appropriate command filter. See
    Zen documentation details and boilerplate."""

    _toolboxes = [
        ('context', 'Context'),
        ('curves', 'Curves'),
        ('fusion', 'Mesh Fusion'),
        ('uv', 'UV'),
        ('paint', 'Paint'),
        ('sculpt', 'Sculpt'),
        ('animate', 'Animate'),
        ('game', 'Game'),
        ('actors', 'Actors'),
        ('deformers', 'Deformers'),
        ('dynamics', 'Dynamics'),
        ('particlePaint', 'Particle Paint'),
        ('vmap', 'Vertex Maps'),
        ('hair', 'Hair'),
        ('particles', 'Particles'),
        ('setup', 'Setup'),
        ('commandRegions', 'Command Regions'),
        ('ik', 'Inverse Kinematics'),
        ('topo', 'Retopology'),
        ('render', 'Render'),
        ('modifiers', 'Modifiers')
    ]

    @classmethod
    def add(cls, name, label):
        """Registers a toolbox name in the Zen toolbox selector list. Once
        registered, the toolbox will be listed in the Zen toolboxes
        Form Command List.

        Note that you must then append
        your form to the Zen toolboxes with the appropriate command filter. See
        Zen documentation details and boilerplate.

        :param name:    (str) the internal name for the toolbox
        :param label:   (str) the pretty name for the toolbox (displayed in menus)
        """
        cls._toolboxes.append((name, label))

    def get(self):
        """Returns a list of all registered toolboxes. Returned as tuples
        in the format (name, label)"""
        return sorted(self._toolboxes, key=lambda x: x[1])
