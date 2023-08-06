
from . import NAME


def _get_version():
    try:
        from pkg_resources import DistributionNotFound, get_distribution
    except ImportError:
        pass
    else:
        try:
            return get_distribution(NAME).version
        except DistributionNotFound as e1:  # Run without install
            print(e1)
        except ValueError as e2:  # Python 3 setup
            print(e2)
        except TypeError as e3:  # Python 2 setup
            print(e3)


def _get_version_by_importlib():
    try:
        from importlib.metadata import version, PackageNotFoundError
        return version(NAME)
    except PackageNotFoundError as e4:
        # package is not installed
        print(e4)


# try two methods to get version, or at last return dev as version
__version__ = _get_version() or _get_version_by_importlib() or 'dev'
