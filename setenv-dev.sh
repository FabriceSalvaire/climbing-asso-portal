####################################################################################################
#
# Settings for development
#
####################################################################################################

# Enter Python virtualenv
py36

# Add current directory in front of the Python path
append_to_python_path_if_not $PWD

####################################################################################################
#
# Set some environment varables
#

# Settings Module path
export DJANGO_SETTINGS_MODULE='ClimbingAssoPortalSite.settings.dev'

# Colors for logging
export DJANGO_COLORS='light;warning=red
