import numpy as np

import phenom

import lal
import lalsimulation as lalsim

from scipy.interpolate import InterpolatedUnivariateSpline as IUS

import wispy.rotations


def gen_fd_wf_params(
    m1=50,
    m2=50,
    S1x=0,
    S1y=0,
    S1z=0,
    S2x=0,
    S2y=0,
    S2z=0,
    distance=1,
    inclination=0,
    phiRef=0,
    longAscNodes=0,
    eccentricity=0,
    meanPerAno=0,
    deltaF=1 / 16,
    f_min=10,
    f_max=200,
    f_ref=30,
    LALpars=None,
    approximant=lalsim.IMRPhenomD,
):
    p = dict(
        m1=m1,
        m2=m2,
        S1x=S1x,
        S1y=S1y,
        S1z=S1z,
        S2x=S2x,
        S2y=S2y,
        S2z=S2z,
        distance=distance,
        inclination=inclination,
        phiRef=phiRef,
        longAscNodes=longAscNodes,
        eccentricity=eccentricity,
        meanPerAno=meanPerAno,
        deltaF=deltaF,
        f_min=f_min,
        f_max=f_max,
        f_ref=f_ref,
        LALpars=LALpars,
        approximant=approximant,
    )

    return p


def gen_fd_wf(p, f_min=None, f_max=None, units="Hz"):
    """
    units: {str:"Mf"} other choice is "Hz"
    f_min, f_max are in units of input `units`
    returned frequencies are in units of input `units`
    """
    p = p.copy()

    M = p["m1"] + p["m2"]

    p.update({"m1": p["m1"] * lal.MSUN_SI})
    p.update({"m2": p["m2"] * lal.MSUN_SI})

    hp, _ = lalsim.SimInspiralChooseFDWaveform(**p)

    f = np.arange(hp.data.length) * hp.deltaF

    if units == "Mf":
        # convert to geometric units
        f = phenom.HztoMf(f, M)
    elif units == "Hz":
        pass

    if f_min is None:
        f_min = f[0]
    if f_max is None:
        f_max = f[-1]

    mask = (f >= f_min) & (f <= f_max)

    hp = hp.data.data[mask]
    f = f[mask]

    amp = np.abs(hp)
    phase = np.unwrap(np.angle(hp))

    return f, amp, phase


def gen_td_wf_params(
    m1=50,
    m2=50,
    S1x=0,
    S1y=0,
    S1z=0,
    S2x=0,
    S2y=0,
    S2z=0,
    distance=1,
    inclination=0,
    phiRef=0,
    longAscNodes=0,
    eccentricity=0,
    meanPerAno=0,
    deltaT=1 / 4096,
    f_min=30,
    f_ref=30,
    LALpars=None,
    approximant=lalsim.SEOBNRv4,
):
    p = dict(
        m1=m1,
        m2=m2,
        s1x=S1x,
        s1y=S1y,
        s1z=S1z,
        s2x=S2x,
        s2y=S2y,
        s2z=S2z,
        distance=distance,
        inclination=inclination,
        phiRef=phiRef,
        longAscNodes=longAscNodes,
        eccentricity=eccentricity,
        meanPerAno=meanPerAno,
        deltaT=deltaT,
        f_min=f_min,
        f_ref=f_ref,
        params=LALpars,
        approximant=approximant,
    )

    return p


def gen_td_wf(p, t_min=-500, t_max=50):
    """
    returned times are in geometric units
    """
    p = p.copy()

    M = p["m1"] + p["m2"]

    p.update({"m1": p["m1"] * lal.MSUN_SI})
    p.update({"m2": p["m2"] * lal.MSUN_SI})

    hp, hc = lalsim.SimInspiralChooseTDWaveform(**p)

    t = np.arange(hp.data.length) * hp.deltaT + np.float(hp.epoch)
    t = phenom.StoM(t, M)

    if t_min is None:
        t_min = t[0]
    if t_max is None:
        t_max = t[-1]

    mask = (t >= t_min) & (t <= t_max)

    hp = hp.data.data[mask]
    hc = hc.data.data[mask]
    t = t[mask]

    h = hp - 1.0j * hc

    amp = np.abs(h)
    phase = np.unwrap(np.angle(h))

    return t, amp, phase


def gen_td_modes_wf_params(
    m1=50,
    m2=50,
    S1x=0,
    S1y=0,
    S1z=0,
    S2x=0,
    S2y=0,
    S2z=0,
    distance=1,
    deltaT=1 / 4096,
    phiRef=0.0,
    f_min=10,
    f_ref=10,
    LALpars=None,
    approximant=lalsim.SEOBNRv4P,
    lmax_dummy=2,
):
    """
    lmax_dummy {int: 2}: old option for XLALSimInspiralChooseTDModes.
    """

    p = dict(
        m1=m1,
        m2=m2,
        S1x=S1x,
        S1y=S1y,
        S1z=S1z,
        S2x=S2x,
        S2y=S2y,
        S2z=S2z,
        phiRef=phiRef,
        r=distance,
        deltaT=deltaT,
        f_min=f_min,
        f_ref=f_ref,
        LALpars=LALpars,
        lmax=lmax_dummy,
        approximant=approximant,
    )

    return p


def gen_td_modes_wf(
    p, modes=[[2, 2]], eob_all_ell_2_modes=False, t_min=None, t_max=None
):
    """
    input:
        p {dict} normally the output of gen_td_modes_wf_params
        modes {list of 2-tuples: [[2,2]]}
            modes to generate
            Note: Depending on the waveform model used
            you might need to explicitly provide both positive and
            negative modes.
        eob_all_ell_2_modes {bool: False}
            only valid if SEOBNRv4P or SEOBNRv4PHM models are chosen.
            If True then returns all ell=2 modes and overwrites input 'modes'
    returns:
        times {array} in units of seconds
        hlms {dict} contains time domain hlm modes
    """
    p = p.copy()

    if [2, 2] not in modes:
        raise NotImplementedError(
            "[2,2] mode not in modes.\
Currently we assume that this mode exists."
        )

    if p["LALpars"] is None:
        p["LALpars"] = lal.CreateDict()

    ma = lalsim.SimInspiralCreateModeArray()
    for l, m in modes:
        lalsim.SimInspiralModeArrayActivateMode(ma, l, m)
    lalsim.SimInspiralWaveformParamsInsertModeArray(p["LALpars"], ma)

    M = p["m1"] + p["m2"]
    p.update({"m1": p["m1"] * lal.MSUN_SI})
    p.update({"m2": p["m2"] * lal.MSUN_SI})

    hlms_lal = lalsim.SimInspiralChooseTDModes(**p)

    hlms = {}

    if p["approximant"] in [lalsim.SEOBNRv4P, lalsim.SEOBNRv4PHM]:
        if eob_all_ell_2_modes:
            modes = [[2, 2], [2, 1], [2, 0], [2, -1], [2, -2]]

    for l, m in modes:
        tmp = lalsim.SphHarmTimeSeriesGetMode(hlms_lal, l, m)
        if l == 2 and m == 2:
            length_22 = tmp.data.length
            dt_22 = tmp.deltaT
            epoch_22 = tmp.epoch
        hlms.update({(l, m): tmp.data.data})

    assert (
        p["deltaT"] == dt_22
    ), f"input deltaT = {p['deltaT']} does not match waveform dt = {dt_22}."

    t = np.arange(length_22) * dt_22 + np.float(epoch_22)

    t = phenom.StoM(t, M)

    if t_min is None:
        t_min = t[0]
    if t_max is None:
        t_max = t[-1]

    mask = (t >= t_min) & (t <= t_max)
    t = t[mask]
    for key in hlms.keys():
        hlms[key] = hlms[key][mask]

    return t, hlms


def gen_td_coprec_data(
    p, modes=[[2, 2]], eob_all_ell_2_modes=False, t_min=None, t_max=None
):
    """This function simply calls `gen_td_modes_wf`
    but then also decomposes the data into the coprecessing frame
    and returns the hlm modes and in coprec frame and returns
    the alpha, beta, gamma precession angles

    Returns a dictionary containing this data

    Args:
        p ([type]): [description]
        modes (list, optional): [description]. Defaults to [[2, 2]].
        eob_all_ell_2_modes (bool, optional): [description]. Defaults to False.
        t_min ([type], optional): [description]. Defaults to None.
        t_max ([type], optional): [description]. Defaults to None.
    """
    times, hlms = gen_td_modes_wf(
        p,
        modes=modes,
        eob_all_ell_2_modes=eob_all_ell_2_modes,
        t_min=t_min,
        t_max=t_max,
    )

    thetaJN, alpha0, phi_aligned = wispy.rotations.compute_L_to_J_angles(
        mass1=p["m1"],
        mass2=p["m2"],
        f_ref=p["f_min"],
        inc=0,
        phiref=p["phiRef"],
        spin1x=p["S1x"],
        spin1y=p["S1y"],
        spin1z=p["S1z"],
        spin2x=p["S2x"],
        spin2y=p["S2y"],
        spin2z=p["S2z"],
    )

    wr = wispy.rotations.WaveformRotations(
        times=times,
        hlms=hlms,
        frame="inertial-L",
        alpha0=alpha0,
        thetaJN=thetaJN,
        phi0=phi_aligned,
    )

    import matplotlib
    import matplotlib.pyplot as plt

    print(p)
    print(p["S1x"])
    print(p["S1y"])
    print(p["S1z"])
    print(p["S2x"])
    print(p["S2y"])
    print(p["S2z"])

    plt.figure(figsize=(14, 4))
    for key in wr.hlms.keys():
        plt.plot(wr.times, np.abs(wr.hlms[key]), label=f"{key}")
    plt.legend()
    plt.show()

    wr.from_inertial_frame_to_coprecessing_frame()

    amp_22 = amp_from_complex(wr.hlms[(2, 2)])
    amp_21 = amp_from_complex(wr.hlms[(2, 1)])

    phi_22 = unwrapped_angle_from_complex(wr.hlms[(2, 2)])
    phi_21 = unwrapped_angle_from_complex(wr.hlms[(2, 1)])

    data = dict(
        times=times,
        amp_22=amp_22,
        amp_21=amp_21,
        phi_22=phi_22,
        phi_21=phi_21,
        alpha=wr.alpha,
        beta=wr.beta,
        gamma=wr.gamma,
    )

    return data


def amp_from_complex(z):
    return np.abs(z)


def unwrapped_angle_from_complex(z):
    return np.unwrap(np.angle(z))


def peak_align_shift(x, amp, npts=1e6, dx_npts=10):
    """
    computes time shift to peak align at zero
    """
    peak_i = amp.argmax()
    iamp = IUS(x, amp)
    dx = x[1] - x[0]
    new_x = np.linspace(x[peak_i] - dx_npts * dx, x[peak_i] + dx_npts * dx, int(npts))

    new_a = iamp(new_x)
    peak_i_new = new_a.argmax()
    tshift = new_x[peak_i_new]

    return tshift


def peak_align_interp(x, y, shift):
    """
    returns new y-data (on same x grid)
    with a peak closer to time = zero.
    """

    new_iy = IUS(x - shift, y)
    new_y = new_iy(x)
    return new_y


def td_amp_scale(mtot, distance):
    """
    mtot in solar masses
    distance in m
    M*G/c^2 * M_sun / dist
    """
    return mtot * lal.MRSUN_SI / distance


def fd_amp_scale(mtot, distance):
    """
    mtot in solar masses
    distance in m
    M*G/c^2 * M_sun / dist
    """
    return mtot * lal.MRSUN_SI * mtot * lal.MTSUN_SI / distance
