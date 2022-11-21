import numpy as np
import numpy.testing as npt 

import micromodelsim as mmsim


def test__vec2vec_rotmat():
    np.random.seed(123)
    for _ in range(int(1e4)):
        v = np.random.random(3) - 0.5
        k = np.random.random(3) - 0.5
        R = mmsim._vec2vec_rotmat(v, k)
        aligned_v = R @ v
        assert (np.linalg.norm(v) - np.linalg.norm(aligned_v)) < 1e-10
        assert np.all(
            (k / np.linalg.norm(k) - aligned_v / np.linalg.norm(aligned_v)) < 1e-10
        )


def test_Gradient():
    npt.assert_raises(ValueError, mmsim.Gradient, bvals=np.zeros(3), bvecs=np.zeros((3, 2)))
    npt.assert_raises(ValueError, mmsim.Gradient, bvals=np.zeros((3, 3)), bvecs=np.zeros((3, 3)))
    npt.assert_raises(ValueError, mmsim.Gradient, bvals=np.zeros(3), bvecs=np.zeros((2, 3)))
