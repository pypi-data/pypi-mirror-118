from click.testing import CliRunner
from namefiles import cli


runner = CliRunner()


def test_cli_disassemble():
    response = runner.invoke(
        cli, ["split", "/a/path/A#EBRA#ZOOINTOWN#_6m_10y.animal.txt"]
    )
    assert response.exit_code == 0

    expected_lines = [
            "identifier: A",
            "    sub_id: EBRA",
            " source_id: ZOOINTOWN",
            "  vargroup: ['6m', '10y']",
            "   context: animal",
            " extension: .txt",
            " root_path: /a/path",
    ]
    for expectation in expected_lines:
        assert expectation in response.output
