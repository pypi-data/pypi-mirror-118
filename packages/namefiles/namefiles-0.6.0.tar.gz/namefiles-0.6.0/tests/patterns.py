from namefiles import _FilenamePartSchema, get_filename_convention


def test_vargroup_for_fix():
    """
    For fixing a bug leading to wrong extracted vargroups.

    Reason was a logical error within the pattern.

    """
    default_schema = get_filename_convention()
    vargroup_schema = default_schema["properties"]["vargroup"]
    part_schema = _FilenamePartSchema("test", **vargroup_schema)

    remaining_filename, extracted_part = part_schema.extract_part("#_1.2e-01")
    assert extracted_part == ["1.2e-01"]

    remaining_filename, extracted_part = part_schema.extract_part("#_1.2e-01_01")
    assert extracted_part == ["1.2e-01", "01"]

    remaining_filename, extracted_part = part_schema.extract_part("#_2.4e+01_1.2e-01_01")
    assert extracted_part == ["2.4e+01", "1.2e-01", "01"]
