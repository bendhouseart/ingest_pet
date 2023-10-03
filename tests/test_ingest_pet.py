import pytest
#from ingest_pet.ingest_pet import get_versions, zip_nifti, write_out_dataset_description_json
#from ingest_pet.ingest_pet import collect_anat, collect_pet, associate_anat_pet
import subprocess


def test_anat_in_no_session_folder(anat_in_no_session_folder):
    subprocess.run(["tree", anat_in_no_session_folder])
    pass

def test_anat_in_first_session_folder(anat_in_first_session_folder):
    subprocess.run(["tree", anat_in_first_session_folder])
    pass

def test_anat_in_first_session_folder_multi_sessions(anat_in_first_session_folder_multi_sessions):
    subprocess.run(["tree", anat_in_first_session_folder_multi_sessions])
    pass

def test_anat_in_each_session_folder(anat_in_each_session_folder):
    subprocess.run(["tree", anat_in_each_session_folder])
    pass