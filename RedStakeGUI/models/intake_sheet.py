from ..constants import PARCEL_DATA_MAP, PARCEL_DATA_COUNTIES
import ttkbootstrap as ttk
from src.county_data_collectors.base_collector import BaseParcelDataCollector


class IntakeSheetModel:
    INFO_LABEL_CODES = {
        1: "Please enter a County.",
        2: "Please enter a Parcel ID number.",
        3: "Please enter a Parcel ID number and a county.",
        4: "Error: Parcel ID number {parcel_id} not found in {county}.",
        5: "Please enter a Phone Number and/or Email Address.",
        6: "Please enter the name of the person requesting the survey.",
        7: "Please enter the address of the person requesting the survey.",
        8: "Please enter the Scope of Work.",
        9: "Retrieving data for Parcel ID number: {parcel_id}...",
        10: "Data retrieved for Parcel ID number: {parcel_id}.",
        11: "Data unavailable for County: {county}.",
    }

    GUI_TO_PARCEL_KEY_MAP = {
        "Address": "PRIMARY_ADDRESS",
        "Zip Code": "PROP_ZIP",
        "Plat": "SUBDIVISION",
    }

    def __init__(self, inputs: dict, info_label: ttk.Label):
        self.info_label = info_label
        self.inputs = inputs

    def get_county_data_collector(self) -> BaseParcelDataCollector:
        """This method will return the specific data collector class for
        the county specified in the County dropdown menu.

        Returns:
            BaseParcelDataCollector: The data collector class for the
                county specified in the County dropdown menu.
                BaseParcelDataCollector is an abstract base class.
        """
        parcel_id = self.inputs["Parcel ID"].get().strip()
        county = self.inputs["County"].get().strip()

        if parcel_id == "" and county == "":
            self.update_info_label(3)
            return
        if parcel_id == "":
            self.update_info_label(2)
            return
        if county == "":
            self.update_info_label(1)
            return
        if county not in PARCEL_DATA_COUNTIES:
            self.update_info_label(11, county=county)
            return

        self.update_info_label(9, parcel_id=parcel_id)
        return PARCEL_DATA_MAP[county]

    def display_parcel_data(self) -> None:
        """This method will display the parcel data for the parcel ID
        number entered in the Parcel ID field. It will also display the
        address, zip code, and plat name for the parcel ID number."""
        county_data_collector = self.get_county_data_collector()
        if county_data_collector is None:
            return

        parcel_id = self.inputs["Parcel ID"].get().strip()
        try:
            parcel = county_data_collector(parcel_id)
            parcel_data = parcel.parcel_data
        except IndexError:
            self.update_info_label(
                4, parcel_id=parcel_id, county=county_data_collector.COUNTY
            )
            return

        self.update_inputs(parcel_data)
        self.update_info_label(10, parcel_id=parcel_id)
        print(parcel_data)

    def update_inputs(self, parcel_data: dict) -> None:
        """This method will update the Address, Zip Code, and Plat
        fields with the data from the parcel data dictionary. It will
        also update the Lot & Block and Plat Book & Page fields.

        Args:
            parcel_data (dict): The parcel data dictionary.
        """
        for gui_key, parcel_data_key in self.GUI_TO_PARCEL_KEY_MAP.items():
            self.inputs[gui_key].delete(0, "end")
            self.inputs[gui_key].insert(0, parcel_data[parcel_data_key])

        self.update_lot_and_block(parcel_data)
        self.update_plat_book_and_page(parcel_data)

    def update_lot_and_block(self, parcel_data: dict) -> None:
        """This method will update the Lot & Block field with the data
        from the parcel data dictionary.

        Args:
            parcel_data (dict): The parcel data dictionary.
        """
        lot = parcel_data["LOT"]
        block = parcel_data["BLOCK"]
        lot_and_block = ""
        if lot != "":
            if block != "":
                lot_and_block = f"LOT {lot}, BLOCK {block}"
            else:
                lot_and_block = f"LOT {lot}"

        self.inputs["Lot & Block"].delete(0, "end")
        self.inputs["Lot & Block"].insert(0, lot_and_block)

    def update_plat_book_and_page(self, parcel_data: dict) -> None:
        """This method will update the Plat Book & Page field with the
        data from the parcel data dictionary.

        Args:
            parcel_data (dict): The parcel data dictionary.
        """
        plat_book = parcel_data["PLAT_BOOK"]
        plat_page = parcel_data["PLAT_PAGE"]
        plat_book_and_page = ""
        if plat_book != "":
            if plat_page != "":
                plat_book_and_page = f"BOOK {plat_book}, PAGE {plat_page}"
            else:
                plat_book_and_page = f"BOOK {plat_book}"

        self.inputs["Plat Book & Page"].delete(0, "end")
        self.inputs["Plat Book & Page"].insert(0, plat_book_and_page)

    def update_info_label(self, code: int, **kwargs) -> None:
        """This method will update the info label with the text from the
        INFO_LABEL_CODES dictionary.

        Args:
            code (int): The code for the text to be displayed in the
                info label.
            **kwargs: The format keyword arguments for the text to be
                displayed in the info label.

        """
        text = self.INFO_LABEL_CODES[code].format(**kwargs)
        self.info_label.config(text=text)