from dipy.core.gradients import gradient_table
import dipy.reconst.dti as dti
import dipy.reconst.qti as qti
import numpy as np
import numpy.testing as npt

import micromodelsim as mmsim


def test_add_noise():
    np.random.seed(123)
    signals = np.ones(int(1e6))
    for snr in [10, 100, 1000]:
        noisy_signals = mmsim.add_noise(signals, snr)
        assert signals.shape == noisy_signals.shape
        assert noisy_signals.min() > 0
        assert abs(np.mean(noisy_signals) - 1) < 1e-2
        assert abs(snr - 1 / np.std(noisy_signals)) / snr < 1e-2
    return


def test_compartment_model_simulation():
    # odf_sh = np.zeros(mmsim.n_coeffs)
    # odf_sh[0] = 0.2820947917738782  # unifrom ODF
    # Confirm correct signal decay using isotropic diffusion
    # Confirm directionality using a known ODF of aligned fibres
    # Confirm correct variance using QTI to invert the signal
    assert True


def test_dtd_simulation():

    np.random.seed(123)

    # Test input validation
    npt.assert_raises(
        TypeError, mmsim.dtd_simulation, gradient=1, dtd=np.zeros((1, 3, 3))
    )
    npt.assert_raises(
        TypeError,
        mmsim.dtd_simulation,
        gradient=mmsim.Gradient(np.zeros(1), np.zeros((1, 3))),
        dtd=1,
    )
    npt.assert_raises(
        ValueError,
        mmsim.dtd_simulation,
        gradient=mmsim.Gradient(np.zeros(1), np.zeros((1, 3))),
        dtd=np.zeros(1),
    )
    npt.assert_raises(
        TypeError,
        mmsim.dtd_simulation,
        gradient=mmsim.Gradient(np.zeros(1), np.zeros((1, 3))),
        dtd=np.zeros((2, 3, 3)),
        p=1,
    )
    npt.assert_raises(
        ValueError,
        mmsim.dtd_simulation,
        gradient=mmsim.Gradient(np.zeros(1), np.zeros((1, 3))),
        dtd=np.zeros((2, 3, 3)),
        p=np.zeros(1),
    )
    npt.assert_raises(
        ValueError,
        mmsim.dtd_simulation,
        gradient=mmsim.Gradient(np.zeros(1), np.zeros((1, 3))),
        dtd=np.zeros((2, 3, 3)),
        p=np.ones(3),
    )

    # Test ADC
    for i in range(100):
        b = 5 * np.random.random()
        D = 5 * np.random.random()
        bvals = np.array([b])
        bvecs = np.array([[1, 0, 0]])
        gradient = mmsim.Gradient(bvals, bvecs)
        dtd = D * np.eye(3)[np.newaxis]
        signals = mmsim.dtd_simulation(gradient, dtd)
        assert abs(signals - np.exp(-b * D)) < 1e-7

    # Test DTI
    bvals = np.concatenate((np.zeros(1), 0.5 * np.ones(48)))
    bvecs = np.vstack((np.zeros(3), mmsim.vertices_48))
    gradient = mmsim.Gradient(bvals, bvecs)
    for i in range(100):
        k = np.random.normal(size=3)
        R = mmsim._vec2vec_rotmat(np.array([1, 0, 0]), k)
        evals = 5 * np.random.random(3)
        D = R @ np.array([[evals[0], 0, 0], [0, evals[1], 0], [0, 0, evals[2]]]) @ R.T
        dtd = D[np.newaxis]
        signals = mmsim.dtd_simulation(gradient, dtd)
        gtab = gradient_table(bvals, bvecs)
        dtimodel = dti.TensorModel(gtab)
        dtifit = dtimodel.fit(signals)
        assert (dtifit.quadratic_form - D).max() < 1e-5

    # Test QTI
    bvals = np.concatenate((np.zeros(1), 0.25 * np.ones(48), 0.5 * np.ones(48)))
    bvecs = np.vstack((np.zeros(3), mmsim.vertices_48, mmsim.vertices_48))
    lte_gradient = mmsim.Gradient(bvals, bvecs)
    pte_gradient = mmsim.Gradient(bvals, bvecs, bten_shape="planar")
    for i in range(100):
        dtd = np.random.random((1000, 3, 3))
        for j in range(dtd.shape[0]):
            k = np.random.normal(size=3)
            R = mmsim._vec2vec_rotmat(np.array([1, 0, 0]), k)
            evals = np.random.random(3)
            dtd[j] = (
                R
                @ np.array([[evals[0], 0, 0], [0, evals[1], 0], [0, 0, evals[2]]])
                @ R.T
            )
        signals = np.concatenate(
            (
                mmsim.dtd_simulation(lte_gradient, dtd),
                mmsim.dtd_simulation(pte_gradient, dtd),
            )
        )
        gtab = gradient_table(
            bvals=np.concatenate((bvals, bvals)),
            bvecs=np.concatenate((bvecs, bvecs)),
            btens=np.array(["LTE" for _ in bvals] + ["PTE" for _ in bvals]),
        )
        qtimodel = qti.QtiModel(gtab)
        qtifit = qtimodel.fit(signals[np.newaxis], mask=np.ones(1).astype(bool))
        assert (
            qti.from_6x6_to_21x1(qti.dtd_covariance(dtd))[:, 0] - qtifit.params[0, 7::]
        ).max() < 1e-3
