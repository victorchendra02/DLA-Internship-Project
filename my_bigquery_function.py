import pandas as pd

from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud.exceptions import NotFound


"""
SCHEMA EXAMPLE\n
schema = [
    bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("class", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("name", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("timestamp", "TIMESTAMP", mode="NULLABLE"),
]
"""


class bcolors:
    FAIL = "\033[91m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    OKBLUE = "\033[94m"
    HEADER = "\033[95m"
    OKCYAN = "\033[96m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def create_dataset(credentials_path, new_dataset_name):
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    client = bigquery.Client(credentials=credentials)

    new_dataset_name = f"{client.project}.{new_dataset_name}"

    dataset = bigquery.Dataset(new_dataset_name)

    dataset.location = "US"

    # Send the dataset to the API for creation, with an explicit timeout.
    # Raises google.api_core.exceptions.Conflict if the Dataset already
    # exists within the project.
    dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
    print(
        f"Dataset created {bcolors.OKGREEN}{client.project}.{dataset.dataset_id}{bcolors.ENDC}"
    )


def create_table(credentials_path, dataset_name, new_table_name, schema):
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    client = bigquery.Client(credentials=credentials)

    new_table_name = f"{client.project}.{dataset_name}.{new_table_name}"

    table = bigquery.Table(new_table_name, schema=schema)
    table = client.create_table(table)  # Make an API request.
    print(
        f"Table created {bcolors.OKGREEN}{table.project}.{table.dataset_id}.{table.table_id}{bcolors.ENDC}"
    )


def table_insert_rows(credentials_path, dataset_name, table_name, rows_to_insert:list[dict]):
    """
    Example:\n
    rows_to_insert must be a records\n
    [
        {"Name": "John", "Age": 25, "City": "New York"},
        {"Name": "Emily", "Age": 30, "City": "London"},
        {"Name": "Michael", "Age": 35, "City": "Paris"}
    ]
    """

    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    client = bigquery.Client(credentials=credentials)

    table_id = f"{client.project}.{dataset_name}.{table_name}"
    errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
    if errors == []:
        print(f"{bcolors.OKGREEN}New rows have been added{bcolors.ENDC}")
    else:
        print(f"Encountered errors while inserting rows: {errors}")


def load_table_dataframe(credentials_path:str, table_id:str, df: pd.DataFrame, write_disposition_="WRITE_TRUNCATE"):
    """
    Example:\n
    `credentials_path   = 'dla-internship-program.json'`
    `table_id           = 'tablename'`
    `df                 = pd.DataFrame()`
    `write_disposition_ = 'WRITE_TRUNCATE|WRITE_APPEND|WRITE_EMPTY'`
    """
    
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, 
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    client = bigquery.Client(credentials=credentials)
    
    dataframe = pd.DataFrame(
        df.to_dict(orient='records'),
        # In the loaded table, the column order reflects the order of the
        # columns in the DataFrame.
        columns=list(df.columns),
        # # Optionally, set a named index, which can also be written to the
        # # BigQuery table.
        # index=pd.Index(
        #     [u"Q24980", u"Q25043", u"Q24953", u"Q16403"], name="wikidata_id"
        # ),
    )
    
    job_config = bigquery.LoadJobConfig(
        # # Specify a (partial) schema. All columns are always written to the
        # # table. The schema is used to assist in data type definitions.
        # schema=[
        #     # Specify the type of columns whose type cannot be auto-detected. For
        #     # example the "title" column uses pandas dtype "object", so its
        #     # data type is ambiguous.
        #     bigquery.SchemaField("title", bigquery.enums.SqlTypeNames.STRING),
        #     # Indexes are written if included in the schema by name.
        #     bigquery.SchemaField("wikidata_id", bigquery.enums.SqlTypeNames.STRING),
        # ],
        # # Optionally, set the write disposition. BigQuery appends loaded rows
        # # to an existing table by default, but with WRITE_TRUNCATE write
        # # disposition it replaces the table with the loaded data.
        write_disposition=write_disposition_,
    )
    
    job = client.load_table_from_dataframe(dataframe, table_id, job_config=job_config)
    job.result()

    table = client.get_table(table_id)
    print(f"Loaded {bcolors.OKBLUE}{table.num_rows} rows{bcolors.ENDC} and {bcolors.OKBLUE}{len(table.schema)} columns{bcolors.ENDC} to {bcolors.OKGREEN}{table_id}{bcolors.ENDC}")
    return table


def dataset_exists(credentials_path, dataset_name):
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    client = bigquery.Client(credentials=credentials)

    dataset_name = f"{client.project}.{dataset_name}"

    try:
        client.get_dataset(dataset_name)  # Make an API request.
        print(f"Dataset {bcolors.FAIL}{dataset_name}{bcolors.ENDC} already exists")
        return "Found"
    except NotFound:
        print(f"Dataset {bcolors.OKBLUE}{dataset_name}{bcolors.ENDC} is not found")
        return "NotFound"


def table_exists(credentials_path, dataset_name, table_name):
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    client = bigquery.Client(credentials=credentials)

    table_id = f"{client.project}.{dataset_name}.{table_name}"

    try:
        client.get_table(table_id)  # Make an API request.
        print("Table {} already exists.".format(table_id))
    except NotFound:
        print("Table {} is not found.".format(table_id))
    finally:
        return client.get_table(table_id)


def delete_dataset(credentials_path, dataset_name):
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    client = bigquery.Client(credentials=credentials)

    dataset_name = f"{client.project}.{dataset_name}"

    # Use the delete_contents parameter to delete a dataset and its contents.
    # Use the not_found_ok parameter to not receive an error if the dataset has already been deleted.
    client.delete_dataset(dataset_name, delete_contents=True, not_found_ok=True)  # Make an API request.
    print(f"Dataset deleted {bcolors.FAIL}'{dataset_name}'{bcolors.ENDC}")


def delete_table(credentials_path, table_id: str) -> None:
    """
    Example:\n
    `table_id = 'projcet.dataset.table'`
    """
    
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    client = bigquery.Client(credentials=credentials)

    # If the table does not exist, delete_table raises
    # google.api_core.exceptions.NotFound unless not_found_ok is True.
    client.delete_table(table_id, not_found_ok=True)  # Make an API request.
    print(f"Deleted table {bcolors.FAIL}'{table_id}'{bcolors.ENDC}.")


def update_table(credentials, query_update: str) -> int:
    """
    UPDATE `project.dataset.table`
    SET column1 = ?,
        column2 = ?,
        column3 = ?,
        ...
    WHERE condition_column = ?;
    """
    
    client = bigquery.Client(credentials=credentials)
    query_job = client.query(query_update)
    query_job.result()

    assert query_job.num_dml_affected_rows is not None

    print(f"DML query modified {query_job.num_dml_affected_rows} rows.")
    return query_job.num_dml_affected_rows
