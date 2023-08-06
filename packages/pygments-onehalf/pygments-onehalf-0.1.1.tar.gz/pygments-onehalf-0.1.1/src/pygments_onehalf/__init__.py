"""One Half color scheme for Pygments."""

import pkg_resources

from .onehalf import OneHalfDark, OneHalfLight

# Attempt to expose the package version as __version__ (see PEP 396).
try:
    __version__ = pkg_resources.get_distribution(__name__).version
except pkg_resources.DistributionNotFound:  # pragma: no cover
    pass


__all__ = ["OneHalfDark", "OneHalfLight"]
