import os
from ConfigFiles import Config as cfg, Config_App as cfg_app


# Get main directory
cfg.root_dir = os.path.dirname(os.path.abspath(__file__))

# initial globals
cfg.init()
# Create app layout
cfg_app.setup_canvas()

cfg.root.mainloop()
