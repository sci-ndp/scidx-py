# query_array

Download a subset of an array within a dataset previously registered as external data with sciDX.

## Parameters
- `source` (str): the name of the external source.
- `var_name` (str): the name of the array to access.
- `lb` (tuple of ints): the lower-bounds of array indices to access.
- `ub` (tuple of ints): the upper-bounds of array indices to access.
- `dataset_name` (str): The name of the dataset. (Optional)
- `dataset_title` (str): The title of the dataset. (Optional)
- `owner_org` (str): The ID of the organization. (Optional)
### Temporal search parameters
- `timestamp` (str or datetime): find a result nearest in time to the given timestamp. (Optional)
- `time_direction` (TimeDirection): either `TimeDirection.FUTURE` or `TimeDirection.PAST`. If the former, and `timestamp` is given, then "nearest in time" looks forward in time; if the latter, backwards. Default behavior is forward-looking. (Optional)
- `start_time` and `end_time` (str or datetime): these two parameters define a time interval that filters results. If either is absent, then the interval is endless in that direction. If `timestamp` is set, these parameters are ignored. (Optional)

## Returns

- A `list` of `tuples`, one for each matching registered dataset, in ascending order by `timestamp`. Each tuple consists of:

1. The subsetted data for the requested variable or `None` if no data is available.
2. The timestamp of the dataset or `None` if it is not timestamped.
3. A metadata `dict` associated with the registered datasest in sciDX

## Raises

- `Exception`: if the query fails for any reason other than no results found.

## Example

```python
from scidx.client import sciDXClient
from datetime import datetime
import requests


# Initialize the client
client = sciDXClient(api_url)

# Query the goes18 source, which has been previously registered
result = client.query_array(
            source="goes18",
            var_name="Mask", 
            lb = (10, 20), 
            ub = (200,300),
            start_time="2024-01-06T0532", end_time="2024-01-06T0542"
        )

Return to [Usage](../usage.md)