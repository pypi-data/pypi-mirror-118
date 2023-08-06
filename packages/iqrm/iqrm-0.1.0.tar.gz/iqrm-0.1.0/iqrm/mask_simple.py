#
# OLD VERSION OF THE ALGORITHM
# *** DO NOT COMMIT THIS ***
#


def iqrm_mask_simple(x, radius=5, threshold=3.0):
    """
    Compute the IQRM mask for one-dimensional input data x.
    The input 'x' is expected to represent a per-channel statistic that measures RFI contamination
    in a block of time-frequency data. Any statistic can be used, but an important requirement is
    that larger values must indicate higher levels of RFI contamination.

    Parameters
    ----------
    x : list or ndarray
        Input data (1-dimensional)
    radius : int, optional
        Radius in number of elements. If a float is passed, it is truncated.
    threshold : float, optional
        Flagging threshold in number of Gaussian sigmas

    Returns
    -------
    mask : ndarray
        Boolean mask with the same size as the input 'x', where 'True' denotes an outlier
    votes_cast : dict of sets
        Dictionary of sets, where the keys are input array indices i that have cast at least one 
        vote, and the values are the set of array indices that received a vote from i.
    """
    x = np.asarray(x)
    n = len(x)
    radius = int(radius)

    if not radius > 0:
        raise ValueError("radius must be > 0")

    threshold = float(threshold)
    if not threshold > 0:
        raise ValueError("threshold must be > 0")

    mask = np.zeros_like(x, dtype=bool)

    for lag in genlags(radius):
        d = lagged_diff(x, lag)
        mask |= outlier_mask(d, threshold)
    return mask