import pathlib
import pytest
import shutil
import tempfile

# our first steps to testing are to build the different types of bids datasets that we expect to encounter
# these are:
# 1. a dataset with an anatomical scan at the top level and a pet scan below it in a session folder
# 2. a dataset with the anatomical scan pet scan contained in the same session folder
# 3. a dataset with the anatomical scan in the first session folder and multiple pet scan sessions that share that anatomical scan
# 4. a dataset with multiple anatomical scans and pet scans contained in the same session folder

# collect test bids dataset from data directory
data_dir = pathlib.Path(__file__).parent.parent / "data"

# 1
@pytest.fixture
def anat_in_no_session_folder(tmpdir):
    dest_dir = pathlib.Path(tmpdir) / "anat_in_subject_folder"
    shutil.copytree(data_dir, dest_dir)

    original_anat_folder = (
        dest_dir / "sub-01" / "ses-baseline" / "anat"
    )
    subject_folder = dest_dir / "sub-01"
    # now we move the anatomical folder in the first session of our test data into the subject level folder
    shutil.move(original_anat_folder, subject_folder)

    inherited_anat_folder = subject_folder / "anat"

    # and next remove the ses- entities from the files in the newly created anat folder
    for file in inherited_anat_folder.glob("sub-01_ses-baseline_*"):
        shutil.move(
            file,
            pathlib.Path(tmpdir)
            / "anat_in_subject_folder"
            / "sub-01"
            / "anat"
            / file.name.replace("ses-baseline_", ""),
        )
    return dest_dir

# 2
@pytest.fixture
def anat_in_first_session_folder(tmpdir):
    dest_dir = pathlib.Path(tmpdir) / "anat_in_first_session_folder"
    shutil.copytree(data_dir, dest_dir)
    return dest_dir

# 3
@pytest.fixture
def anat_in_first_session_folder_multi_sessions(tmpdir):
    dest_dir = pathlib.Path (tmpdir) / "anat_in_first_session_folder_multi_sessions"
    shutil.copytree(data_dir, dest_dir)

    # create a second session
    second_session_folder = (
        dest_dir / "sub-01" / "ses-second"
    )
    second_session_folder.mkdir(parents=True, exist_ok=True)

    shutil.copytree(
        dest_dir / "sub-01" / "ses-baseline",
        second_session_folder,
        dirs_exist_ok=True,
    )

    # replace the ses- entities in the files in the newly created second session folder
    for file in second_session_folder.glob("pet/*"):
        shutil.move(
            file,
            second_session_folder
            / "pet"
            / file.name.replace("ses-baseline_", "ses-second_"),
        )

    # remove anat in second session folder
    shutil.rmtree(second_session_folder / "anat")
    
    return dest_dir

# 4
@pytest.fixture
def anat_in_each_session_folder(tmpdir):
    dest_dir = pathlib.Path(tmpdir) / "anat_in_each_session_folder"
    shutil.copytree(data_dir, dest_dir)

    # create a second session
    second_session_folder = (
        dest_dir / "sub-01" / "ses-second"
    )
    second_session_folder.mkdir(parents=True, exist_ok=True)

    shutil.copytree(
        dest_dir / "sub-01" / "ses-baseline",
        second_session_folder,
        dirs_exist_ok=True,
    )

    # replace the ses- entities in the files in the newly created second session folder
    for file in second_session_folder.glob("pet/*"):
        shutil.move(
            file,
            second_session_folder
            / "pet"
            / file.name.replace("ses-baseline_", "ses-second_"),
        )

    for file in second_session_folder.glob("anat/*"):
        shutil.move(
            file,
            second_session_folder
            / "anat"
            / file.name.replace("ses-baseline_", "ses-second_"),
        )
    return dest_dir
