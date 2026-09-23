import pytest

from pycptcity import cpt, find_cpt, lucky, cpt_names


class TestCpt:
    def test_mpl_inferno_10(self):
        out = cpt("mpl_inferno", 10)
        assert out == [
            "#000004", "#1B0C41", "#4B0C6B", "#781C6D",
            "#A52C60", "#CE4346", "#ED6925", "#FB9906",
            "#F7D03C", "#FCFFA4",
        ]

    def test_mpl_inferno_rev(self):
        assert cpt("mpl_inferno", 1, rev=True) == ["#FCFFA4"]
        fwd = cpt("mpl_inferno", 10)
        assert cpt("mpl_inferno", 10, rev=True) == fwd[::-1]

    def test_colorrampalette(self):
        fun = cpt("mpl_inferno", colorrampalette=True)
        assert callable(fun)
        assert fun(10) == cpt("mpl_inferno", 10)
        assert len(fun(5)) == 5
        assert len(fun(20)) == 20

    def test_colorrampalette_5(self):
        fun = cpt("mpl_inferno", colorrampalette=True)
        assert fun(5) == ["#000004", "#560F6D", "#BB3654", "#F98C09", "#FCFFA4"]

    def test_colorrampalette_1(self):
        fun = cpt("mpl_inferno", colorrampalette=True)
        assert fun(1) == ["#000004"]

    def test_idv_temperature(self):
        assert cpt("idv_temperature", 5) == [
            "#0000FA", "#005CFA", "#00BCFA", "#9CFF00", "#FF1E00",
        ]

    def test_arendal_arctic(self):
        assert cpt("arendal_arctic", 5) == [
            "#2F3869", "#7780AF", "#B2EA8E", "#F3EA82", "#B8A75E",
        ]

    def test_frgb(self):
        assert cpt("arendal_arctic", 5, frgb=(0.3, 1, 1)) == [
            "#0E3869", "#2480AF", "#35EA8E", "#49EA82", "#37A75E",
        ]

    def test_spider_miles_leap_of_faith(self):
        assert cpt("spider_miles_leap_of_faith", 8) == [
            "#0A0A2A", "#1C1C4C", "#55264C", "#D32F34",
            "#D32F34", "#EEBFC2", "#F3F3F3", "#0A0A2A",
        ]

    def test_bhw(self):
        assert cpt("bhw_bhw1_bhw1_01", 4) == [
            "#FFB032", "#F57150", "#DC498F", "#B538EE",
        ]

    def test_unknown_palette(self):
        with pytest.raises(KeyError):
            cpt("nonexistent_palette_xyz")

    def test_hex_format(self):
        cols = cpt("mpl_inferno", 10)
        assert all(len(c) == 7 and c[0] == "#" for c in cols)


class TestFindCpt:
    def test_temperature(self):
        assert find_cpt("temperature") == [
            "arendal_temperature", "idv_temperature",
            "jjg_misc_temperature", "kst_03_red_temperature",
        ]

    def test_case_sensitive(self):
        assert find_cpt("Temperature", ignore_case=False) == []

    def test_regex(self):
        out = find_cpt("^mpl_")
        assert len(out) > 0
        assert all(x.startswith("mpl_") for x in out)

    def test_fixed(self):
        out = find_cpt("rain", fixed=True)
        assert all("rain" in x.lower() for x in out)

    def test_no_match(self):
        assert find_cpt("zzz_nonexistent_xyz") == []


class TestNoaa:
    """NOAA palettes (author works for NOAA)."""

    EXPECTED = [
        "noaa", "noaa_storm",
        "noaa_nws", "noaa_nhc", "noaa_nexrad",
        "noaa_goes", "noaa_buoy", "noaa_ncei",
        "noaa_nmfs", "noaa_jetstream", "noaa_tornado",
        "noaa_wind_chill", "noaa_heat_index", "noaa_coastal",
    ]

    def test_no_space_prefix(self):
        assert not [n for n in cpt_names() if n.startswith("space_noaa")]

    def test_discoverable(self):
        found = find_cpt("noaa")
        for name in self.EXPECTED:
            assert name in found, name

    def test_all_render(self):
        for name in self.EXPECTED:
            cols = cpt(name, n=10)
            assert len(cols) == 10
            assert all(len(c) == 7 and c[0] == "#" for c in cols), name

    def test_noaa_uses_emblem_blues_and_whites(self):
        cols = cpt("noaa", n=5)
        assert cols[0].upper() == "#0B2D72"  # emblem deep navy sea
        assert cols[-1].upper() == "#FFFFFF"  # emblem white gull

    def test_nws_is_noaa_navy_to_white(self):
        cols = cpt("noaa_nws", n=2)
        assert cols[0].upper() == "#0B2D72"  # NOAA navy
        assert cols[1].upper() == "#F7FBFF"  # near-white

    def test_nhc_follows_saffir_simpson(self):
        cols = cpt("noaa_nhc", n=5)
        assert cols[0].upper() == "#2ECC71"   # cat 1 green
        assert cols[-1].upper() == "#8E44AD"  # cat 5 magenta

    def test_nexrad_radar_scale(self):
        cols = cpt("noaa_nexrad", n=7)
        assert cols[0].upper() == "#00FFFF"   # low dBZ cyan
        assert cols[-1].upper() == "#FFFFFF"  # extreme white

    def test_wind_chill_cold_to_coldest(self):
        cols = cpt("noaa_wind_chill", n=2)
        assert cols[0].upper() == "#FFFFFF"   # mild white
        assert cols[1].upper() == "#0B2D72"   # deep cold navy

    def test_colorrampalette(self):
        for name in ("noaa_nhc", "noaa_nexrad", "noaa_goes"):
            fun = cpt(name, colorrampalette=True)
            assert callable(fun)
            assert len(fun(5)) == 5


class TestLucky:
    def test_reproducible(self):
        a = lucky(1, message=False, nseed=1)
        b = lucky(1, message=False, nseed=1)
        assert a == b

    def test_returns_list(self):
        cols = lucky(10, message=False, nseed=42)
        assert len(cols) == 10

    def test_colorrampalette(self):
        fun = lucky(1, message=False, nseed=1, colorrampalette=True)
        assert callable(fun)
        assert len(fun(5)) == 5


class TestNames:
    def test_count(self):
        assert len(cpt_names()) == 7716

    def test_contains_known(self):
        names = cpt_names()
        assert "mpl_inferno" in names
        assert "spider_miles_leap_of_faith" in names
