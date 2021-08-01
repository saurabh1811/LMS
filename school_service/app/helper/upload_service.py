import os
from multiprocessing.pool import ThreadPool
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient
from app.core.settings import AzureConfig


 
# Replace with the local folder which contains the image files for upload

 
class AzureBlobFileUploader:
    def __init__(self):
        self.sas_token = AzureConfig().sas_token
        self.MY_CONNECTION_STRING = AzureConfig().MY_CONNECTION_STRING
        self.blob_service_client =  BlobServiceClient.from_connection_string(self.MY_CONNECTION_STRING)

    def upload_all_images_in_folder(self):
        LOCAL_IMAGE_PATH = "REPLACE_THIS"
        all_file_names = [f for f in os.listdir(LOCAL_IMAGE_PATH)
                    if os.path.isfile(os.path.join(LOCAL_IMAGE_PATH, f)) and ".jpg" in f]
        result = self.run(all_file_names)
        return int(result)
    
    def run(self,all_file_names):
        # Upload 10 files at a time!
        with ThreadPool(processes=int(10)) as pool:
            return pool.map(self.upload_image, all_file_names)

    def upload_image(self,file_name):
        LOCAL_IMAGE_PATH="folder_path"
        MY_IMAGE_CONTAINER = "myimages"
        blob_client = self.blob_service_client.get_blob_client(container=MY_IMAGE_CONTAINER, blob=file_name)
        upload_file_path = os.path.join(LOCAL_IMAGE_PATH, file_name)
        # Create blob on storage Overwrite if it already exists!
        image_content_setting = ContentSettings(content_type='image/jpeg')
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data,overwrite=True,content_settings=image_content_setting)
        return file_name

 
    def upload_single_file(self,file_name, filepath, user_container):
        blob_client = self.blob_service_client.get_blob_client(container=user_container, blob=file_name)
        upload_file_path = os.path.join(filepath, file_name)
        # Create blob on storage Overwrite if it already exists!
        image_content_setting = ContentSettings(content_type='image/jpeg')
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data,overwrite=True,content_settings=image_content_setting)
        return file_name
    
    def check_container(self, container_name):
        container = ContainerClient.from_connection_string(self.MY_CONNECTION_STRING, container_name)
        try:
            blobClientContainer = container.get_container_properties()
            return True
        except Exception as e:
            return False

    
    def upload_single_file_data(self,file_name, data, user_container):
        if self.check_container(user_container):
            blob_client = self.blob_service_client.get_blob_client(container=user_container, blob=file_name)
        else:
            blob_container = self.blob_service_client.create_container(user_container)
            blob_client = self.blob_service_client.get_blob_client(container=user_container, blob=file_name)
        image_content_setting = ContentSettings(content_type='image/png')
        blob_client.upload_blob(data,overwrite=True,content_settings=image_content_setting)
        return blob_client.url
    
    def delete_file_data(self, file_name, user_container):
        container_client = ContainerClient.from_connection_string(conn_str=self.MY_CONNECTION_STRING, container_name=user_container)
        data_id = container_client.delete_blob( blob=file_name)
        return data_id

# Initialize class and upload files
azure_blob_file_uploader = AzureBlobFileUploader()
