"""Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Curabitur egestas aliquam eros, et luctus felis accumsan a. Mauris
scelerisque sapien non mi vehicula facilisis. Cum sociis natoque
penatibus et magnis dis parturient montes, nascetur ridiculus mus.
Vivamus eget purus ac arcu aliquam vulputate vitae et diam. Nullam sit
amet diam condimentum, laoreet turpis nec, venenatis sem. Morbi mi
tortor, vestibulum sit amet nisi non, euismod suscipit lectus. Ut
vitae est nisi. Quisque et posuere tortor. Maecenas suscipit ut leo
vitae hendrerit.
"""

def aenean_interdum(f):
    """Cras ut convallis sapien.

    Aliquam suscipit, enim lacinia lacinia rhoncus, sapien est feugiat
    nulla, ac dictum orci magna tincidunt ipsum. Quisque posuere
    sodales turpis sit amet tincidunt. Nam tincidunt dolor volutpat
    sapien auctor fringilla. Pellentesque arcu turpis, tincidunt
    ultrices dignissim in, vestibulum id urna. Curabitur congue
    pulvinar arcu ac iaculis. Pellentesque habitant morbi tristique
    senectus et netus et malesuada fames ac turpis egestas. Fusce enim
    nisi, porta sed ligula ut, fermentum hendrerit sapien. Sed
    imperdiet eu quam faucibus faucibus.
    """

    print f.__doc__
    f.__doc__ += '\nNullam id feugiat orci, nec bibendum lacus.\n'
    return f

@aenean_interdum
def donec_porttitor(whats_up):
    """Nulla nec venenatis turpis, fermentum tristique dolor.

    Morbi sodales risus at purus commodo, et pellentesque orci
    blandit. Donec lacinia tortor eu mi maximus, sed suscipit ipsum
    lobortis. Sed id sollicitudin enim, id feugiat eros. Aenean
    accumsan felis ac neque dapibus fringilla. Nam et posuere erat, in
    pulvinar metus. Donec vitae maximus tellus, non feugiat nisl. Ut
    efficitur mattis lacus vitae feugiat. In rutrum ligula ut erat
    viverra interdum. Pellentesque vulputate commodo ligula, in
    euismod velit dapibus at. Pellentesque eget posuere mauris. Donec
    dictum maximus lacus, eu rutrum massa.
    """

    print whats_up.__doc__
    return whats_up

@donec_porttitor
class vestibulum_ante(object):
    """Pellentesque habitant morbi tristique senectus et netus et
    malesuada fames ac turpis egestas.

    Nunc id risus tellus. Nulla ullamcorper dui a urna sollicitudin
    sodales. Ut diam augue, sollicitudin maximus euismod eu, cursus a
    dolor. Integer tempor iaculis dignissim. Etiam pulvinar quis nulla
    eu molestie. In maximus, justo in congue lobortis, libero enim
    pulvinar dolor, non hendrerit lorem magna sit amet
    tellus. Suspendisse in tempus est. Nam congue scelerisque diam,
    quis consequat orci aliquam ut. Donec sed mauris in leo ultrices
    maximus ullamcorper eget arcu. Donec ac urna in dui efficitur
    suscipit ac eu ipsum. Aenean ac facilisis nisi. Etiam elit libero,
    vulputate at orci accumsan, dignissim volutpat nibh. Aliquam
    bibendum felis a erat iaculis, auctor hendrerit felis luctus. Duis
    nec hendrerit nisi.
    """

    pass

print __doc__
print aenean_interdum.__doc__
print donec_porttitor.__doc__
print vestibulum_ante.__doc__
