from typing import Union, Optional, List, Tuple

from Utilities.Converter import Conversion

class Signal:
    """
    Abstract base class for all signal sources used in SPICE netlists.

    Provides the interface for formatting a SPICE-compatible signal source string.
    Derived classes must override `to_string()` to return the appropriate SPICE signal string.
    """
    def __init__(self) -> None:
        super().__init__()

    def to_string(self) -> str:
        """
        Returns:
            str: SPICE-compatible string representation of the signal.
        """
        return "SignalBase"

    def __str__(self) -> str:
        """
        Returns:
            str: Alias for `to_string()`.
        """
        return self.to_string()

class PULSE(Signal):
    """
    Represents a PULSE waveform for transient simulation in SPICE.

    Defines a piecewise linear pulse with rise/fall time, width, period, and number of cycles.
    Useful for modeling digital or repetitive switching signals in time-domain simulations.
    """
    def __init__(
        self,
        v1:   Union[float, int, str],
        v2:   Union[float, int, str],
        td:   Union[float, int, str],
        tr:   Union[float, int, str],
        tf:   Union[float, int, str],
        pw:   Union[float, int, str],
        per:  Union[float, int, str],
        np:   Union[float, int, str],
    ) -> None:
        """
        Args:
            v1 (Union[float, int, str]): Initial voltage.
            v2 (Union[float, int, str]): Final voltage.
            td (Union[float, int, str]): Delay time (s).
            tr (Union[float, int, str]): Rise time (s).
            tf (Union[float, int, str]): Fall time (s).
            pw (Union[float, int, str]): Pulse width (s).
            per (Union[float, int, str]): Period (s).
            np (Union[float, int, str]): Number of pulses/cycles.
        """
        super().__init__()
        self.v1   = Conversion.spice(v1)
        self.v2   = Conversion.spice(v2)
        self.td   = Conversion.spice(td)
        self.tr   = Conversion.spice(tr)
        self.tf   = Conversion.spice(tf)
        self.pw   = Conversion.spice(pw)
        self.per  = Conversion.spice(per)
        self.np   = Conversion.spice(np)

    def to_string(self) -> str:
        """
        Returns:
            str: SPICE PULSE() source string.
        """
        return (
            f"PULSE({self.v1} {self.v2} {self.td}s {self.tr}s {self.tf}s {self.pw}s {self.per}s {self.np})"
        )

    @property
    def v1(self) -> str:
        return self._v1
    @v1.setter
    def v1(self, val: Union[float, int, str]) -> None:
        self._v1 = Conversion.spice(val)

    @property
    def v2(self) -> str:
        return self._v2
    @v2.setter
    def v2(self, val: Union[float, int, str]) -> None:
        self._v2 = Conversion.spice(val)

    @property
    def td(self) -> str:
        return self._td
    @td.setter
    def td(self, val: Union[float, int, str]) -> None:
        self._td = Conversion.spice(val)

    @property
    def tr(self) -> str:
        return self._tr
    @tr.setter
    def tr(self, val: Union[float, int, str]) -> None:
        self._tr = Conversion.spice(val)

    @property
    def tf(self) -> str:
        return self._tf
    @tf.setter
    def tf(self, val: Union[float, int, str]) -> None:
        self._tf = Conversion.spice(val)

    @property
    def pw(self) -> str:
        return self._pw
    @pw.setter
    def pw(self, val: Union[float, int, str]) -> None:
        self._pw = Conversion.spice(val)

    @property
    def per(self) -> str:
        return self._per
    @per.setter
    def per(self, val: Union[float, int, str]) -> None:
        self._per = Conversion.spice(val)

    @property
    def np(self) -> str:
        return self._np
    @np.setter
    def np(self, val: Union[float, int, str]) -> None:
        self._np = Conversion.spice(val)
    
class SIN(Signal):
    """
    Represents a sinusoidal source signal for SPICE simulation.

    Defines a sine waveform with offset, amplitude, frequency, delay, damping factor, and phase.
    Suitable for AC analysis and time-domain oscillatory signals.
    """
    def __init__(
        self,
        vo:    Union[float, int, str],
        va:    Union[float, int, str],
        freq:  Union[float, int, str],
        td:    Union[float, int, str],
        theta: Union[float, int, str],
        phase: Union[float, int, str],
    ) -> None:
        """
        Args:
            vo (Union[float, int, str]): Offset voltage.
            va (Union[float, int, str]): Amplitude.
            freq (Union[float, int, str]): Frequency (Hz).
            td (Union[float, int, str]): Delay time (s).
            theta (Union[float, int, str]): Damping factor.
            phase (Union[float, int, str]): Phase angle (deg or rad).
        """
        super().__init__()
        self.vo    = Conversion.spice(vo)
        self.va    = Conversion.spice(va)
        self.freq  = Conversion.spice(freq)
        self.td    = Conversion.spice(td)
        self.theta = Conversion.spice(theta)
        self.phase = Conversion.spice(phase)

    def to_string(self) -> str:
        """
        Returns:
            str: SPICE SIN() source string.
        """
        return f'SIN({self.vo} {self.va} {self.freq} {self.td}s {self.theta} {self.phase})'

    @property
    def vo(self) -> str:
        return self._vo
    @vo.setter
    def vo(self, val: Union[float, int, str]) -> None:
        self._vo = Conversion.spice(val)

    @property
    def va(self) -> str:
        return self._va
    @va.setter
    def va(self, val: Union[float, int, str]) -> None:
        self._va = Conversion.spice(val)

    @property
    def freq(self) -> str:
        return self._freq
    @freq.setter
    def freq(self, val: Union[float, int, str]) -> None:
        self._freq = Conversion.spice(val)

    @property
    def td(self) -> str:
        return self._td
    @td.setter
    def td(self, val: Union[float, int, str]) -> None:
        self._td = Conversion.spice(val)

    @property
    def theta(self) -> str:
        return self._theta
    @theta.setter
    def theta(self, val: Union[float, int, str]) -> None:
        self._theta = Conversion.spice(val)

    @property
    def phase(self) -> str:
        return self._phase
    @phase.setter
    def phase(self, val: Union[float, int, str]) -> None:
        self._phase = Conversion.spice(val)
    
class EXP(Signal):
    """
    Represents an exponential waveform for SPICE transient simulation.

    Defines an exponential rise followed by an exponential fall with specified time constants.
    Useful for modeling charging and discharging waveforms.
    """
    def __init__(
        self,
        v1:   Union[float, int, str],
        v2:   Union[float, int, str],
        td1:  Union[float, int, str],
        tau1: Union[float, int, str],
        td2:  Union[float, int, str],
        tau2: Union[float, int, str],
    ) -> None:
        """
        Args:
            v1 (Union[float, int, str]): Initial voltage.
            v2 (Union[float, int, str]): Final voltage.
            td1 (Union[float, int, str]): Rise delay (s).
            tau1 (Union[float, int, str]): Rise time constant (s).
            td2 (Union[float, int, str]): Fall delay (s).
            tau2 (Union[float, int, str]): Fall time constant (s).
        """
        super().__init__()
        self.v1   = Conversion.spice(v1)
        self.v2   = Conversion.spice(v2)
        self.td1  = Conversion.spice(td1)
        self.tau1 = Conversion.spice(tau1)
        self.td2  = Conversion.spice(td2)
        self.tau2 = Conversion.spice(tau2)

    def to_string(self) -> str:
        """
        Returns:
            str: SPICE EXP() source string.
        """
        return f'EXP({self.v1} {self.v2} {self.td1}s {self.tau1}s {self.td2}s {self.tau2}s)'

    @property
    def v1(self) -> str:
        return self._v1
    @v1.setter
    def v1(self, val: Union[float, int, str]) -> None:
        self._v1 = Conversion.spice(val)

    @property
    def v2(self) -> str:
        return self._v2
    @v2.setter
    def v2(self, val: Union[float, int, str]) -> None:
        self._v2 = Conversion.spice(val)

    @property
    def td1(self) -> str:
        return self._td1
    @td1.setter
    def td1(self, val: Union[float, int, str]) -> None:
        self._td1 = Conversion.spice(val)

    @property
    def tau1(self) -> str:
        return self._tau1
    @tau1.setter
    def tau1(self, val: Union[float, int, str]) -> None:
        self._tau1 = Conversion.spice(val)

    @property
    def td2(self) -> str:
        return self._td2
    @td2.setter
    def td2(self, val: Union[float, int, str]) -> None:
        self._td2 = Conversion.spice(val)

    @property
    def tau2(self) -> str:
        return self._tau2
    @tau2.setter
    def tau2(self, val: Union[float, int, str]) -> None:
        self._tau2 = Conversion.spice(val)
        
class PWL(Signal):
    """
    Piecewise Linear (PWL) waveform definition for SPICE sources.

    Starts with an initial time-voltage pair followed by additional time-voltage pairs.
    Optionally supports ramp resistance (R) and time delay (TD).
    Used for arbitrary input signals and waveform shaping in transient simulation.
    """
    def __init__(
        self,
        t1: Union[float, int, str],
        v1: Union[float, int, str],
        tv: Optional[List[Tuple[Union[float, int, str], Union[float, int, str]]]] = None,
        r:  Optional[Union[float, int, str]] = None,
        td: Optional[Union[float, int, str]] = None,
    ) -> None:
        """
        Args:
            t1 (Union[float, int, str]): First time point (s).
            v1 (Union[float, int, str]): First voltage value.
            tv (Optional[List[Tuple[Union[float, int, str], Union[float, int, str]]]]): Additional time-voltage pairs.
            r (Optional[Union[float, int, str]]): Ramp resistance.
            td (Optional[Union[float, int, str]]): Time delay (s).
        """
        super().__init__()
        self.t1 = Conversion.spice(t1)
        self.v1 = Conversion.spice(v1)
        self.tv = [(Conversion.spice(t), Conversion.spice(v)) for t, v in (tv or [])]
        self.r  = Conversion.spice(r) if r is not None else None
        self.td = Conversion.spice(td) if td is not None else None

    def to_string(self) -> str:
        """
        Returns:
            str: SPICE PWL() source string.
        """
        points = [(self.t1, self.v1)] + self.tv
        points_str = " ".join(f"{t}s {v}" for t, v in points)
        extras = []
        if self.r:
            extras.append(f"r={self.r}")
        if self.td:
            extras.append(f"td={self.td}s")
        extra_str = " ".join(extras)
        return f'PWL({points_str}) {extra_str}'.strip()

    @property
    def t1(self) -> str:
        return self._t1
    @t1.setter
    def t1(self, val: Union[float, int, str]) -> None:
        self._t1 = Conversion.spice(val)

    @property
    def v1(self) -> str:
        return self._v1
    @v1.setter
    def v1(self, val: Union[float, int, str]) -> None:
        self._v1 = Conversion.spice(val)

    @property
    def tv(self) -> List[Tuple[str, str]]:
        return self._tv
    @tv.setter
    def tv(self, val: Optional[List[Tuple[Union[float, int, str], Union[float, int, str]]]]) -> None:
        if val is None:
            self._tv = []
        else:
            self._tv = [(Conversion.spice(t), Conversion.spice(v)) for t, v in val]

    @property
    def r(self) -> Optional[str]:
        return self._r
    @r.setter
    def r(self, val: Optional[Union[float, int, str]]) -> None:
        if val is None:
            self._r = None
        else:
            self._r = Conversion.spice(val)

    @property
    def td(self) -> Optional[str]:
        return self._td
    @td.setter
    def td(self, val: Optional[Union[float, int, str]]) -> None:
        if val is None:
            self._td = None
        else:
            self._td = Conversion.spice(val)

class SFFM(Signal):
    """
    Single-Sideband Frequency Modulated (SFFM) signal for SPICE sources.

    Modulates a carrier frequency using a modulation index and frequency.
    Phase offsets for modulation and carrier are also supported.
    """
    def __init__(
        self,
        v0:     Union[float, int, str],
        va:     Union[float, int, str],
        fm:     Union[float, int, str],
        mdi:    Union[float, int, str],
        fc:     Union[float, int, str],
        td:     Union[float, int, str],
        phasem: Union[float, int, str],
        phasec: Union[float, int, str],
    ) -> None:
        """
        Args:
            v0 (Union[float, int, str]): Offset voltage.
            va (Union[float, int, str]): Amplitude.
            fm (Union[float, int, str]): Modulation frequency (Hz).
            mdi (Union[float, int, str]): Modulation index.
            fc (Union[float, int, str]): Carrier frequency (Hz).
            td (Union[float, int, str]): Delay time (s).
            phasem (Union[float, int, str]): Modulation phase.
            phasec (Union[float, int, str]): Carrier phase.
        """
        super().__init__()
        self.v0     = Conversion.spice(v0)
        self.va     = Conversion.spice(va)
        self.fm     = Conversion.spice(fm)
        self.mdi    = Conversion.spice(mdi)
        self.fc     = Conversion.spice(fc)
        self.td     = Conversion.spice(td)
        self.phasem = Conversion.spice(phasem)
        self.phasec = Conversion.spice(phasec)

    def to_string(self) -> str:
        """
        Returns:
            str: SPICE SSFM() source string.
        """
        return (
            f'SSFM({self.v0} {self.va} {self.fm} {self.mdi} {self.fc} {self.td} {self.phasem} {self.phasec})'
        )

    @property
    def v0(self) -> str:
        return self._v0
    @v0.setter
    def v0(self, val: Union[float, int, str]) -> None:
        self._v0 = Conversion.spice(val)

    @property
    def va(self) -> str:
        return self._va
    @va.setter
    def va(self, val: Union[float, int, str]) -> None:
        self._va = Conversion.spice(val)

    @property
    def fm(self) -> str:
        return self._fm
    @fm.setter
    def fm(self, val: Union[float, int, str]) -> None:
        self._fm = Conversion.spice(val)

    @property
    def mdi(self) -> str:
        return self._mdi
    @mdi.setter
    def mdi(self, val: Union[float, int, str]) -> None:
        self._mdi = Conversion.spice(val)

    @property
    def fc(self) -> str:
        return self._fc
    @fc.setter
    def fc(self, val: Union[float, int, str]) -> None:
        self._fc = Conversion.spice(val)

    @property
    def td(self) -> str:
        return self._td
    @td.setter
    def td(self, val: Union[float, int, str]) -> None:
        self._td = Conversion.spice(val)

    @property
    def phasem(self) -> str:
        return self._phasem
    @phasem.setter
    def phasem(self, val: Union[float, int, str]) -> None:
        self._phasem = Conversion.spice(val)

    @property
    def phasec(self) -> str:
        return self._phasec
    @phasec.setter
    def phasec(self, val: Union[float, int, str]) -> None:
        self._phasec = Conversion.spice(val)
        
class AM(Signal):
    """
    Amplitude Modulated (AM) signal for SPICE sources.

    Defines a carrier modulated by a sine wave. Includes amplitude, frequency, delay,
    modulation index, and optional modulation/carrier phase shifts.
    """
    def __init__(
        self,
        vo:     Union[float, int, str],
        va:     Union[float, int, str],
        fm:     Union[float, int, str],
        mdi:    Union[float, int, str],
        fc:     Union[float, int, str],
        td:     Union[float, int, str],
        phasem: Optional[Union[float, int, str]] = None,
        phasec: Optional[Union[float, int, str]] = None,
    ) -> None:
        """
        Args:
            vo (Union[float, int, str]): Offset voltage.
            va (Union[float, int, str]): Amplitude.
            fm (Union[float, int, str]): Modulation frequency (Hz).
            mdi (Union[float, int, str]): Modulation index.
            fc (Union[float, int, str]): Carrier frequency (Hz).
            td (Union[float, int, str]): Delay time (s).
            phasem (Optional[Union[float, int, str]]): Modulation phase.
            phasec (Optional[Union[float, int, str]]): Carrier phase.
        """
        super().__init__()
        self.vo     = Conversion.spice(vo)
        self.va     = Conversion.spice(va)
        self.fm     = Conversion.spice(fm)
        self.mdi    = Conversion.spice(mdi)
        self.fc     = Conversion.spice(fc)
        self.td     = Conversion.spice(td)
        self.phasem = Conversion.spice(phasem) if phasem is not None else None
        self.phasec = Conversion.spice(phasec) if phasec is not None else None

    def to_string(self) -> str:
        """
        Returns:
            str: SPICE AM() source string.
        """
        return (
            f'AM({self.vo} {self.va} {self.fm} {self.mdi} {self.fc} {self.td} {self.phasem} {self.phasec})'
        )

    @property
    def vo(self) -> str:
        return self._vo
    @vo.setter
    def vo(self, val: Union[float, int, str]) -> None:
        self._vo = Conversion.spice(val)

    @property
    def va(self) -> str:
        return self._va
    @va.setter
    def va(self, val: Union[float, int, str]) -> None:
        self._va = Conversion.spice(val)

    @property
    def fm(self) -> str:
        return self._fm
    @fm.setter
    def fm(self, val: Union[float, int, str]) -> None:
        self._fm = Conversion.spice(val)

    @property
    def mdi(self) -> str:
        return self._mdi
    @mdi.setter
    def mdi(self, val: Union[float, int, str]) -> None:
        self._mdi = Conversion.spice(val)

    @property
    def fc(self) -> str:
        return self._fc
    @fc.setter
    def fc(self, val: Union[float, int, str]) -> None:
        self._fc = Conversion.spice(val)

    @property
    def td(self) -> str:
        return self._td
    @td.setter
    def td(self, val: Union[float, int, str]) -> None:
        self._td = Conversion.spice(val)

    @property
    def phasem(self) -> Optional[str]:
        return self._phasem
    @phasem.setter
    def phasem(self, val: Optional[Union[float, int, str]]) -> None:
        self._phasem = Conversion.spice(val) if val is not None else None

    @property
    def phasec(self) -> Optional[str]:
        return self._phasec
    @phasec.setter
    def phasec(self, val: Optional[Union[float, int, str]]) -> None:
        self._phasec = Conversion.spice(val) if val is not None else None
        
class TRNOISE(Signal):
    """
    Transient Noise waveform definition for SPICE voltage/current sources.

    Models noise with amplitude, time/spectral characteristics, and optional
    RTS (Random Telegraph Signal) behavior using capture and emission timing parameters.
    Format: TRNOISE(na nt nalpha namp [rtsam rtscapt rtsemt])
    """
    def __init__(
        self,
        na:       Union[float, int, str],
        nt:       Union[float, int, str],
        nalpha:   Union[float, int, str],
        namp:     Union[float, int, str],
        rtsam:    Optional[Union[float, int, str]] = None,
        rtscapt:  Optional[Union[float, int, str]] = None,
        rtsemt:   Optional[Union[float, int, str]] = None,
    ) -> None:
        """
        Args:
            na (Union[float, int, str]): Noise amplitude.
            nt (Union[float, int, str]): Noise temperature or time constant.
            nalpha (Union[float, int, str]): Spectral exponent (e.g., 0=white, 1=pink).
            namp (Union[float, int, str]): Amplitude scaling factor for the noise signal.
            rtsam (Optional[Union[float, int, str]]): RTS signal amplitude.
            rtscapt (Optional[Union[float, int, str]]): RTS capture time (s).
            rtsemt (Optional[Union[float, int, str]]): RTS emission time (s).
        """
        super().__init__()
        self.na      = Conversion.spice(na)
        self.nt      = Conversion.spice(nt)
        self.nalpha  = Conversion.spice(nalpha)
        self.namp    = Conversion.spice(namp)
        self.rtsam   = Conversion.spice(rtsam)   if rtsam   is not None else None
        self.rtscapt = Conversion.spice(rtscapt) if rtscapt is not None else None
        self.rtsemt  = Conversion.spice(rtsemt)  if rtsemt  is not None else None

    def to_string(self) -> str:
        """
        Returns:
            str: SPICE-formatted TRNOISE() source signal, including optional RTS parameters.
        """
        values = [self.na, self.nt, self.nalpha, self.namp]
        if self.rtsam is not None:
            values.append(self.rtsam)
        if self.rtscapt is not None:
            values.append(self.rtscapt)
        if self.rtsemt is not None:
            values.append(self.rtsemt)
        return f"TRNOISE({ ' '.join(map(str, values)) })"
    
 
class TRRANDOM(Signal):
    """
    Transient Random waveform generator for SPICE simulation.

    Defines a random signal generator with a specified type, seed time (TS),
    and optional delay time (TD) and additional parameters.
    """
    def __init__(
        self,
        typ:    Union[float, int, str],
        ts:     Union[float, int, str],
        td:     Optional[Union[float, int, str]] = None,
        param1: Optional[Union[float, int, str]] = None,
        param2: Optional[Union[float, int, str]] = None,
    ) -> None:
        """
        Args:
            typ (Union[float, int, str]): Random signal type.
            ts (Union[float, int, str]): Seed time (s).
            td (Optional[Union[float, int, str]]): Optional delay time (s).
            param1 (Optional[Union[float, int, str]]): Optional parameter 1.
            param2 (Optional[Union[float, int, str]]): Optional parameter 2.
        """
        super().__init__()
        self.type   = typ
        self.ts     = ts
        self.td     = td
        self.param1 = param1
        self.param2 = param2

    def to_string(self) -> str:
        """
        Returns:
            str: SPICE TRRANDOM() source string.
        """
        parts = [self.type, self.ts]
        if self.td is not None:
            parts.append(self.td)
        if self.param1 is not None:
            parts.append(self.param1)
        if self.param2 is not None:
            parts.append(self.param2)
        # Remove None values and ensure all are strings
        parts = [str(Conversion.spice(p)) for p in parts if p is not None]
        return f'TRRANDOM({ " ".join(parts) })'

    @property
    def type(self) -> str:
        return self._type
    @type.setter
    def type(self, val: Union[float, int, str]) -> None:
        self._type = Conversion.spice(val)

    @property
    def ts(self) -> str:
        return self._ts
    @ts.setter
    def ts(self, val: Union[float, int, str]) -> None:
        self._ts = Conversion.spice(val)

    @property
    def td(self) -> Optional[str]:
        return self._td
    @td.setter
    def td(self, val: Optional[Union[float, int, str]]) -> None:
        self._td = Conversion.spice(val) if val is not None else None

    @property
    def param1(self) -> Optional[str]:
        return self._param1
    @param1.setter
    def param1(self, val: Optional[Union[float, int, str]]) -> None:
        self._param1 = Conversion.spice(val) if val is not None else None

    @property
    def param2(self) -> Optional[str]:
        return self._param2
    @param2.setter
    def param2(self, val: Optional[Union[float, int, str]]) -> None:
        self._param2 = Conversion.spice(val) if val is not None else None
        
class EXTERNAL(Signal):
    """
    Placeholder for externally defined signal sources.

    Intended for future support of imported signal shapes or dynamically defined external waveforms.
    Raises NotImplementedError if instantiated.
    """
    def __init__(self) -> None:
        super().__init__()
        raise NotImplementedError("EXTERNAL signal type is not implemented yet.")

    def to_string(self) -> str:
        """
        Returns:
            str: Placeholder string "EXTERNAL".
        """
        return "EXTERNAL"