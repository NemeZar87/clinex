import os

"""if os.path.exists("/home/"):
    from .servidor import *
else:
    from .local import *"""

# Agregué ésto por si lo querían usar, va en realizar sería una alternativa
# (2/11/24)

if os.name == "nt":
    from .local import *
else:
    from .servidor import *