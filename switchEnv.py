from __future__ import print_function

import sys

import inspect
from os.path import dirname



env_path = r"Y:\0_ENV_TEST"
dev_path = r"C:\Users\Polar Media\Documents\GitHub\MasterEnv"





# I'm going to define this little function to make this cleaner
# It's going to have a flag to let you specify the userPath you want to clear out
# But otherwise I'd going to assume that it's the userPath you're running the script from (__file__)
def resetSessionForScript(userPath = None):
    if userPath is None:
        userPath = dirname( __file__ )
    # Convert this to lower just for a clean comparison later
    userPath = userPath.lower()

    toDelete = []
    # Iterate over all the modules that are currently loaded
    for key, module in sys.modules.iteritems():
        # There's a few modules that are going to complain if you try to query them
        # so I've popped this into a try/except to keep it safe
        try:
            # Use the "inspect" library to get the moduleFilePath that the current module was loaded from
            moduleFilePath = inspect.getfile( module ).lower()

            # Don't try and remove the startup script, that will break everything
            if moduleFilePath == __file__.lower():
                continue

            # If the module's filepath contains the userPath, add it to the list of modules to delete
            if moduleFilePath.startswith( userPath ):
                print("Removing %s" % key)
                toDelete.append( key )
        except:
            pass

    # If we'd deleted the module in the loop above, it would have changed the size of the dictionary and
    # broken the loop. So now we go over the list we made and delete all the modules
    for module in toDelete:
        del (sys.modules[module])


resetSessionForScript()



def sw_global():

    if dev_path in sys.path:
        sys.path.remove(dev_path)

    if env_path not in sys.path:
        sys.path.append(env_path)


def sw_dev():


    if env_path in sys.path:
        sys.path.remove( env_path )

    if dev_path not in sys.path:
        sys.path.append( dev_path )






#########################################

# # So now you can either put this at the top of your script
# resetSessionForScript( r"C:\MyTool\TheToolIWantToRestart)

# Or just
resetSessionForScript()

# # Personally, I only want this behaviour to be called for me while I'm debugging so I'd probably add it in a condition like
# import getpass

# if getpass.getuser() == "nrodgers":
#     resetSessionForScript()