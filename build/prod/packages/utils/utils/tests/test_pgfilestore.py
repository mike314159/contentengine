import sys
sys.path.insert(0, "..")


# Execute with pytest -s test_pgfilestore.py

import pytest
from utils.pgfilestore import PGFileStore
from utils.secrets_store import get_secret
import os
import time

db_config = get_secret("render_pg_connect")
#print(json.dumps(db_config, indent=4))

@pytest.fixture(scope="module")
def file_store():
    """Fixture to initialize PGFileStore before tests and close db connection after."""
    app = 'pytest'
    collection = 'test_files'
    fs = PGFileStore(app, collection, db_config)
    yield fs
    fs.conn.close()

@pytest.fixture
def create_temp_files():
    """Fixture to create and remove temporary files used in tests."""
    filenames = ['test_file.txt', 'test_delete.txt']
    for filename in filenames:
        with open(filename, 'w') as f:
            print("Wrote file: ", filename)
            f.write(f'Content of {filename}')
    yield filenames
    # Clean up files after tests
    for filename in filenames:
        os.remove(filename)

def test_save_and_pull_file(file_store, create_temp_files):
    test_id = 'test_file'
    src_filename = create_temp_files[0]  # Using the first temp file for upload and download test

    # Save the file
    assert file_store.save_file(test_id, src_filename), "Failed to save file."

    # Pull the file to a new destination
    dest_filename = 'test_file_copy.txt'
    assert file_store.pull_file(test_id, dest_filename), "Failed to pull file."

    # Check contents of the pulled file
    with open(dest_filename, 'r') as f:
        contents = f.read()
    assert contents == 'Content of test_file.txt', "File contents do not match."

    # Clean up the destination file after test
    os.remove(dest_filename)

def test_file_exists(file_store, create_temp_files):
    test_id = 'test_file'
    # Checking the existence of the file just uploaded in previous test
    assert file_store.file_exists(test_id), "File should exist."
    # Checking a non-existent file
    assert not file_store.file_exists('non_existent_file'), "File should not exist."

def test_delete_file(file_store, create_temp_files):
    test_id = 'test_file_to_delete'
    src_filename = create_temp_files[1]  # Using the second temp file for deletion test
    # Create a file and then delete it
    assert file_store.save_file(test_id, src_filename), "Failed to save file for deletion."
    assert file_store.delete_file(test_id), "Failed to delete file."
    assert not file_store.file_exists(test_id), "File should have been deleted."

def test_pull_file_with_old_timestamp(file_store, create_temp_files):
    test_id = 'test_file'
    dest_filename = 'test_file_older.txt'
    current_time = int(time.time())
    # Ensure the file is not pulled if its last_mod_ts is older than current_time + 10 seconds
    assert not file_store.pull_file(test_id, dest_filename, after_ts=current_time + 10), "Should not pull older file."

    # Clean up the destination file if created
    if os.path.exists(dest_filename):
        os.remove(dest_filename)

def test_list_file_ids(file_store):
    # Prepare data: Create a temporary file and save some files with known IDs
    temp_filename = 'test_file.txt'
    with open(temp_filename, 'w') as f:
        f.write("Dummy content for testing.")

    known_ids = ['id1', 'id2', 'id3']
    try:
        for file_id in known_ids:
            assert file_store.save_file(file_id, temp_filename), f"Failed to save file with ID {file_id}"

        # Test the list_file_ids function
        fetched_ids = file_store.list_file_ids()
        assert all(file_id in fetched_ids for file_id in known_ids), "Not all known file IDs were fetched correctly."
    finally:
        # Clean up: Delete temporary file and files after test
        os.remove(temp_filename)
        for file_id in known_ids:
            file_store.delete_file(file_id)