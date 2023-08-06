# Musiio Validate TSV

This library helps to validate tsv files before uploading them to the Musiio Search API (https://search.musiio.com/api#postIndex). 

## Installation

```bash
pip install musiio_validate_tsv
```

## Basic Usage
```python
from musiio_validate_tsv.validate_tsv import ValidateTSV
validate_tsv = ValidateTSV()
errors, processed_rows = validate_tsv.process_tsv(tsv_file_path="tracks_list.tsv")
```
### Output Parameters
| Field Name   | Type   | Description|
|---|---|---|
|  processed_rows | array  | Contains a list of dictionaries each containing a mapping of the column names to the corresponding row data. Set to None if there are errors.|
| errors   | array   | Contains a list of dictionaries each containing a mapping indicating the row number and the error associated with that row. Set to None if there are no errors.|

#### Output Example
```python
processed_rows = [
    {
            "customer_track_id": "fake_id",
            "customer_filename": "fake_filename"
    }
]

errors = [
    {
        "row_number": 1,
        "error_message": "Missing required field : audio_url"
    }
]
```

## Advanced Usage

### Custom Fields
This is for specifying custom column added in the tsv. The format is as follows:
```python
custom_fields = {
        "field_name": {
            "required": "True", # Boolean
            "internal_id": "internal_field_id", # String
            "type": "int" # string which can be int|string|date|float
        }
}
```

#### Example
```python
from musiio_validate_tsv.validate_tsv import ValidateTSV
validate_tsv = ValidateTSV()
errors, processed_rows = validate_tsv.process_tsv(
            tsv_file_path="data_with_custom_fields.tsv",
            custom_fields={
                "region code": {
                    "required": False,
                    "internal_id": "region_code",
                    "type": "string"
                },
                "release date": {
                    "required": False,
                    "internal_id": "release date",
                    "type": "date"
                }
            })
```
#### Sample Output
The custom field values get put under a special key called `custom_properties`
```python
processed_rows = [
    {
        "customer_track_id": "fake_id",
        "customer_filename": "fake_filename",
        "custom_properties": {
            "region_code": ["eu"],
            "release date": ["2012-12-05"]
        }
    }
]
```

### Max Errors
This is to limit number of error rows returned by the tsv

#### Example
```python
from musiio_validate_tsv.validate_tsv import ValidateTSV
validate_tsv = ValidateTSV()
errors, processed_rows = validate_tsv.process_tsv(tsv_file_path="tests/test_data/process_tsv_invalid_max_error_rows.tsv",
                                                  max_errors=5)
```



