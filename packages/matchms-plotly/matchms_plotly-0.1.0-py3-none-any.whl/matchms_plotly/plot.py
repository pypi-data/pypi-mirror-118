from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from matchms import Spectrum
import plotly.graph_objects as go


def plot_spectrum(spectrum: Spectrum, **kwargs: str) -> go.Figure:
    """
    Plot a single spectrum.

    Args:
        spectrum: a Matchms Spectrum instance.
        kwargs: keywords args used as Plotly figure layout args.

    Returns:
        A Plotly figure.
    """

    figure = _set_figure(**kwargs)
    _add_trace(figure, _get_spectrum_data(spectrum))
    figure.update_traces(line={"width": 1})
    return figure


def plot_spectra(
    spectrum_up: Spectrum, spectrum_down: Spectrum, **kwargs: str
) -> go.Figure:
    """
    Plot two spectrums in the "up and down" fashion.

    Args:
        spectrum_up: a Matchms Spectrum instance to be plot on upper side.
        spectrum_down: a Matchms Spectrum instance to be plot on lower side.
        kwargs: keywords args used as Plotly figure layout args.

    Returns:
        A Plotly figure.
    """

    figure = _set_figure(**kwargs)
    factor = 1
    for name, spectrum in enumerate((spectrum_up, spectrum_down)):
        data = _get_spectrum_data(spectrum)
        data["y"] = np.array([_factor_value(value, factor) for value in data["y"]])
        _add_trace(figure, data, name=str(name))
        factor *= -1
    figure.update_traces(line={"width": 1})
    return figure


def _set_figure(**kwargs: str) -> go.Figure:
    fig = go.Figure()
    _kwargs = {"xaxis_title": "m/z", "yaxis_title": "intensity"}
    _kwargs.update(kwargs)
    fig.update_layout(**_kwargs)
    return fig


_DATA_TYPE = Dict[str, np.ndarray]


def _add_trace(figure: go.Figure, data: _DATA_TYPE, name: str = "") -> None:
    figure.add_trace(
        go.Scatter(
            x=data["x"],
            y=data["y"],
            mode="lines+markers",
            name=name,
        )
    )


def _get_spectrum_data(spectrum: Spectrum) -> _DATA_TYPE:
    df = pd.DataFrame(
        {"intensities": spectrum.peaks.intensities, "mz": spectrum.peaks.mz}
    )
    df["blank"] = None
    df["zero"] = 0
    df["mz1"] = df.mz
    df["mz2"] = df.mz
    return {
        "x": np.concatenate(df.loc[:, [f"mz{idx}" for idx in ("", "1", "2")]].values),
        "y": np.concatenate(df.loc[:, ("zero", "intensities", "blank")].values),
    }


def _factor_value(value: Optional[float], factor: int) -> Optional[float]:
    if value is not None:
        value = value * factor
    return value
