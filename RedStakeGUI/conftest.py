from tkinter import TclError

import pytest

from RedStakeGUI.main import MainApp
from RedStakeGUI.views.cad_opener import CADOpenerView
from RedStakeGUI.views.close_job_search import CloseJobSearchView
from RedStakeGUI.views.file_entry import FileEntryView
from RedStakeGUI.views.file_status_checker import FileStatusCheckerView
from RedStakeGUI.views.intake_sheet import IntakeSheetView
from RedStakeGUI.views.website_search import WebsiteSearchView


@pytest.fixture(scope="module")
def test_address() -> str:
    """Fixture to get a test address.

    Returns:
        str: The test address.
    """
    return "1234 main street"


@pytest.fixture(scope="module")
def test_subdivision() -> str:
    """Fixture to get a test subdivision.

    Returns:
        str: The test subdivision.
    """
    return "Whitakers Landing"


@pytest.fixture(scope="module")
def test_file_number() -> str:
    """Fixture to get a test file number.

    Returns:
        str: The test file number.
    """
    return "23050226"


@pytest.fixture(scope="module")
def test_sarasota_parcel_id() -> str:
    """Fixture to get a test parcel id.

    Returns:
        str: The test parcel id.
    """
    return "0057150069"


@pytest.fixture(scope="module")
def test_file_entry_data() -> dict[str, str]:
    """Fixture to get a test file entry data.

    Returns:
        dict[str, str]: The test file entry data.
    """
    fields = {
        "Job Date": "2021-01-01",
        "Fieldwork Date": "2021-01-01",
        "Inhouse Date": "2021-01-01",
        "Job Number": "50050101",
        "Parcel ID": "0057150069",
        "County": "Sarasota",
        "Entry By": "TEST",
        "Fieldwork Crew": "CREW",
        "Inhouse Assigned To": "ASSIGNED",
        "Requested Services": "SURVEY",
        "Contact Information": "CONTACT",
        "Additional Information": "ADDITIONAL",
    }
    return fields


@pytest.fixture(scope="module")
def main_app() -> MainApp:
    """Fixture to get the main app.

    Yields:
        MainApp: The main app.
    """
    try:
        app = MainApp()  # Initialize your Tkinter app here
    except (
        TclError
    ):  # Tkinter might raise a TclError if GUI can't be initialized
        pytest.skip("Unable to initialize Tkinter GUI")
    else:
        yield app
        app.destroy()


@pytest.fixture(scope="module")
def close_job_tab(main_app: MainApp) -> CloseJobSearchView:
    """Fixture to get the close job tab from the main app.

    Args:
        main_app (MainApp): The main app.

    Yields:
        CloseJobSearchView: The close job tab.
    """
    tab = main_app.notebook_tabs["Close Job Search"]
    yield tab
    tab.destroy()


@pytest.fixture(scope="module")
def file_status_tab(main_app: MainApp) -> FileStatusCheckerView:
    """Fixture to get the file status tab from the main app.

    Args:
        main_app (MainApp): The main app.

    Yields:
        FileStatusCheckerView: The file status tab.
    """
    tab = main_app.notebook_tabs["File Status"]
    yield tab
    tab.destroy()


@pytest.fixture(scope="module")
def file_entry_tab(main_app: MainApp) -> FileEntryView:
    """Fixture to get the file entry tab from the main app.

    Args:
        main_app (MainApp): The main app.

    Yields:
        FileEntryView: The file entry tab.
    """
    tab = main_app.notebook_tabs["File Entry"]
    yield tab
    tab.destroy()
