import shopping


def test_row_translate_values():
    assert shopping.row_translate_values({
        'Administrative': '0', 
        'Administrative_Duration': '0',
        'Informational': '0',
        'Informational_Duration': '0',
        'ProductRelated': '1',
        'ProductRelated_Duration': '0',
        'BounceRates': '0.2',
        'ExitRates': '0.2', 
        'PageValues': '0',
        'SpecialDay': '0',
        'Month': 'Feb',
        'OperatingSystems': '1',
        'Browser': '1',
        'Region': '1',
        'TrafficType': '1',
        'VisitorType': 'Returning_Visitor',
        'Weekend': 'FALSE',
        'Revenue': 'FALSE'}) == (0,[0, 0.0, 0, 0.0, 1, 0.0, 0.2, 0.2, 0.0, 0.0, 1, 1, 1, 1, 1, 1, 0])

    