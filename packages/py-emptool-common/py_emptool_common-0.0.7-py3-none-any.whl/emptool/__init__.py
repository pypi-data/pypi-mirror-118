# from pkg_resources import get_distribution, DistributionNotFound

# try:
#     __version__ = get_distribution(__name__).version
# except DistributionNotFound:
#     pass  # package is not installed



__all__ = ["common"]
# from common import get_hello

# for root, dirs, files in os.walk(dirname(__file__)):
#     for filepath in files:
#         root, ext = os.path.splitext(filepath)
#         if ext == ".py" and root != "__init__":
#             __all__.append(root)
#     break