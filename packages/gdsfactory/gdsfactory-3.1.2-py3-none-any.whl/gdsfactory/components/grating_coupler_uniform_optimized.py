import pathlib
from typing import Tuple

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.taper import taper as taper_function
from gdsfactory.types import ComponentFactory

data_path = pathlib.Path(__file__).parent / "csv_data"


@gf.cell
def grating_coupler_uniform_optimized(
    widths: Tuple[float, ...] = (0.5, 0.2, 0.3),
    width_grating: float = 11.0,
    length_taper: float = 150.0,
    width: float = 0.5,
    partial_etch: bool = False,
    layer: Tuple[int, int] = gf.LAYER.WG,
    layer_partial_etch: Tuple[int, int] = gf.LAYER.SLAB150,
    taper: ComponentFactory = taper_function,
    taper_port_name: str = "o1",
    polarization: str = "te",
    wavelength: float = 1500.0,
) -> Component:
    """Grating coupler uniform (not focusing)

    Args:
        widths: of each teeth
        width_grating: 11
        length_taper: 150
        width: 0.5
        partial_etch: False


    """
    # returns a fiber grating
    c = Component()
    x = 0

    if partial_etch:
        partetch_overhang = 5

        # make the etched areas (opposite to teeth)
        for i, wt in enumerate(widths):
            if i % 2 == 1:
                _compass = gf.components.compass(
                    size=[wt, width_grating + partetch_overhang * 2],
                    layer=layer_partial_etch,
                )
                cgrating = c.add_ref(_compass)
                cgrating.x += x + wt / 2
            x += wt

        # draw the deep etched square around the grating
        xgrating = np.sum(widths)
        deepbox = c.add_ref(
            gf.components.compass(size=[xgrating, width_grating], layer=layer)
        )
        deepbox.movex(xgrating / 2)
    else:
        for i, wt in enumerate(widths):
            if i % 2 == 0:
                cgrating = c.add_ref(
                    gf.components.compass(size=[wt, width_grating], layer=layer)
                )
                cgrating.x += x + wt / 2
            x += wt

    taper_ref = c << taper(
        length=length_taper,
        width1=width,
        width2=width_grating,
        port=None,
        layer=layer,
    )
    taper_ref.xmax = 0
    c.polarization = polarization
    c.wavelength = wavelength
    if taper_port_name not in taper_ref.ports:
        raise ValueError(f"{taper_port_name} not in {list(taper_ref.ports.keys())}")
    c.add_port(name="o1", port=taper_ref.ports[taper_port_name])
    gf.asserts.grating_coupler(c)
    return c


@gf.cell
def grating_coupler_uniform_1etch_h220_e70(**kwargs):
    csv_path = data_path / "grating_coupler_1etch_h220_e70.csv"
    import pandas as pd

    d = pd.read_csv(csv_path)
    return grating_coupler_uniform_optimized(
        widths=tuple(d["widths"]), partial_etch=True, **kwargs
    )


@gf.cell
def grating_coupler_uniform_2etch_h220_e70(**kwargs):
    csv_path = data_path / "grating_coupler_2etch_h220_e70_e220.csv"
    import pandas as pd

    d = pd.read_csv(csv_path)
    return grating_coupler_uniform_optimized(
        widths=tuple(d["widths"]), partial_etch=True, **kwargs
    )


@gf.cell
def grating_coupler_uniform_1etch_h220_e70_taper_w11_l200(**kwargs):
    from gdsfactory.components.taper_from_csv import taper_w11_l200

    return grating_coupler_uniform_1etch_h220_e70(taper=taper_w11_l200)


@gf.cell
def grating_coupler_uniform_1etch_h220_e70_taper_w10_l200(**kwargs):
    from gdsfactory.components.taper_from_csv import taper_w10_l200

    return grating_coupler_uniform_1etch_h220_e70(
        taper=taper_w10_l200, width_grating=10
    )


@gf.cell
def grating_coupler_uniform_1etch_h220_e70_taper_w10_l100(**kwargs):
    from gdsfactory.components.taper_from_csv import taper_w10_l100

    return grating_coupler_uniform_1etch_h220_e70(
        taper=taper_w10_l100, width_grating=10
    )


if __name__ == "__main__":
    # csv_path = data_path / "grating_coupler_2etch_h220_e70_e220.csv"
    # import pandas as pd

    # d = pd.read_csv(csv_path)

    # widths = [0.3, 0.5, 0.3]
    # c = grating_coupler_uniform_optimized(widths=widths, partial_etch=False)
    # c = grating_coupler_uniform_optimized(widths=widths, partial_etch=True)

    # c = grating_coupler_uniform_1etch_h220_e70()
    # c = grating_coupler_uniform_2etch_h220_e70()
    c = grating_coupler_uniform_1etch_h220_e70_taper_w11_l200()
    # c = grating_coupler_uniform_1etch_h220_e70_taper_w10_l200()
    # c = grating_coupler_uniform_1etch_h220_e70_taper_w10_l100()
    # print(c.ports)
    c.show()
