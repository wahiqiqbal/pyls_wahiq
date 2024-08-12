from datetime import datetime
from pyls import get_info_from_directory, formatResults, show_results

def test_get_file_info(tmp_path):
    test_file = tmp_path / "testfile.txt"
    test_file.write_text("this is a test file for the comp assignment")
    tempdirectory = tmp_path / "comp350_A2"
    tempdirectory.mkdir()

    file_info = get_info_from_directory(tmp_path)

    names = [info["name"] for info in file_info]
    assert "testfile.txt" in names
    assert "comp350_A2" in names

