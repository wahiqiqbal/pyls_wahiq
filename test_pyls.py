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


def test_get_details():
    test_data = [
        {"name": "testfile.txt", "type": "f", "size": 2048, "mod_time": datetime(2002, 2, 9, 20, 1, 2)},
        {"name": "comp350_A2", "type": "d", "size": 0, "mod_time": datetime(2002, 2, 9, 20, 1, 2)},
    ]

    output = formatResults(test_data, long_format=True, filetype=True)
    assert output == [
        "2002-02-09 20:01:02\t2048\ttestfile.txt",
        "2002-02-09 20:01:02\t0\tcomp350_A2/",
    ]

def test_get_details_detailed():
    test_data = [
        {"name": "testfile.txt", "type": "f", "size": 2048, "mod_time": datetime(2002, 2, 9, 20, 1, 2)},
        {"name": "comp350_A2", "type": "d", "size": 0, "mod_time": datetime(2002, 2, 9, 20, 1, 2)},
    ]

    output = formatResults(test_data, long_format=True, filetype=False)
    assert output == [
        "2002-02-09 20:01:02\t2048\ttestfile.txt",
        "2002-02-09 20:01:02\t0\tcomp350_A2/",
    ]

def test_formatResults_filetype():
    sample_results = [
        {"name": "testfile.txt", "type": "f"},
        {"name": "comp350_A2", "type": "d"},
    ]
    formatted = formatResults(sample_results, long_format=False, filetype=True)
    assert formatted == ["testfile.txt", "comp350_A2/"]

def test_format_results_basic():
    test_data = [
        {"name": "testfile.txt", "type": "f"},
        {"name": "comp350_A2", "type": "d"},
    ]

    output = formatResults(test_data, long_format=False, filetype=False)
    assert output == ["testfile.txt", "comp350_A2/"]

def test_show_results(capsys):
    show = ["testfile.txt", "comp350_A2"]

    show_results(show)

    captured = capsys.readouterr()
    assert captured.out == "testfile.txt\ncomp350_A2\n"

