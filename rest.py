import requests
import zipfile
import os

class Rest:
    """
    Represents a REST client for interacting with a server API.

    Attributes
    ----------
    server : str
        The base URL of the server.
    api_key : str
        The API key for authentication.
    authorization : str
        The authorization token.
    headers : dict
        The headers for the HTTP requests.

    Methods
    -------
    _make_request(method, endpoint, params=None, json=None, files=None):
        A generic function to make an HTTP request.

    """

    def __init__(self, server='http://inventory01.smartlab.th-deg.de:8081/api/v3', 
                       api_key='123', authorization='Bearer 123'):
        """
        Initializes the Rest client with server, API key, and authorization token.

        Parameters
        ----------
        server : str
            The base URL of the server.
        api_key : str
            The API key for authentication.
        authorization : str
            The authorization token.
        """
        self.server = server
        self.api_key = api_key
        self.authorization = authorization
        self.headers = {
            'Authorization': self.authorization, 
            'api_key': self.api_key, 
            'accept': 'application/json'
        }

    def zipdir(self, path, zip_filename):
        """
        Zips the contents of a directory and returns the path of the zipped file.

        Parameters
        ----------
        path : str
            The path to the directory to zip.
        zip_filename : str
            The name of the resulting zip file.

        Returns
        -------
        str
            The path of the created zip file.
        """
        if not zip_filename.endswith('.zip'):
            zip_filename += '.zip'
        
        output_dir = './inventory_station/src/images'
        zip_file_path = os.path.join(output_dir, zip_filename)

        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as ziph:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.join(path, '..'))
                    ziph.write(file_path, arcname)

        return os.path.abspath(zip_file_path)
            

    def _make_request(self, method, endpoint, params=None, json=None, files=None):
        """
        A generic function to make an HTTP request.

        Parameters
        ----------
        method : str
            The HTTP method ('GET', 'POST', 'PUT', etc.).
        endpoint : str
            The API endpoint.
        params : dict, optional
            The URL parameters for the request.
        json : dict, optional
            The JSON data to send in the request body.
        files : dict, optional
            Files to be uploaded.

        Returns
        -------
        dict or str
            The response JSON if the request is successful, otherwise an error message.
        """
        url = f"{self.server}{endpoint}"
        
        try:
            response = requests.request(method, url, headers=self.headers, params=params, json=json, files=files)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return f"Error - {method} request to {endpoint}: {e}"

    def search_for_item_by_name(self, item_name):
        """
        Searches for an item by name.

        Parameters
        ----------
        item_name : str
            The name of the item to search for.

        Returns
        -------
        dict or str
            The response JSON if the request is successful, otherwise an error message.
        """
        return self._make_request('GET', '/item/search', params={'item_name': item_name})

    def find_item_by_id(self, item_id):
        """
        Finds an item by ID.

        Parameters
        ----------
        item_id : int
            The ID of the item to find.

        Returns
        -------
        dict or str
            The response JSON if the request is successful, otherwise an error message.
        """
        return self._make_request('GET', f'/item/{item_id}')

    def insert_new_item(self, new_item):
        """
        Inserts a new item.

        Parameters
        ----------
        new_item : dict
            The new item data to insert.

        Returns
        -------
        dict or str
            The response JSON if the request is successful, otherwise an error message.
        """
        return self._make_request('POST', '/item', json=new_item)

    def update_item(self, updated_item):
        """
        Updates an existing item.

        Parameters
        ----------
        updated_item : dict
            The updated item data.

        Returns
        -------
        dict or str
            The response JSON if the request is successful, otherwise an error message.
        """
        return self._make_request('PUT', '/item', json=updated_item)

    def search_for_box_with_rfid(self, box_rfid):
        """
        Searches for a box by RFID.

        Parameters
        ----------
        box_rfid : str
            The RFID of the box to search for.

        Returns
        -------
        dict or str
            The response JSON if the request is successful, otherwise an error message.
        """
        return self._make_request('GET', '/box/search', params={'box_rfid': box_rfid})

    def find_box_by_id(self, box_id):
        """
        Finds a box by ID.

        Parameters
        ----------
        box_id : int
            The ID of the box to find.

        Returns
        -------
        dict or str
            The response JSON if the request is successful, otherwise an error message.
        """
        return self._make_request('GET', f'/box/{box_id}')

    def insert_new_box(self, new_box):
        """
        Inserts a new box.

        Parameters
        ----------
        new_box : dict
            The new box data to insert.

        Returns
        -------
        dict or str
            The response JSON if the request is successful, otherwise an error message.
        """
        return self._make_request('POST', '/box', json=new_box)
    
    def get_location_by_id(self, location_id):
        return self._make_request('GET', f'/location/{location_id}')
    
    def search_for_location_by_id(self, location_id):
        return self._make_request('GET', f'/location/search', params={'location_id': location_id})

    def upload_file(self, item_id, file_path, endpoint, params=None, file_type='image/jpeg'):
        """
        Uploads a file for a specific item.

        Parameters
        ----------
        item_id : int
            The ID of the item.
        file_path : str
            The path to the file to upload.
        endpoint : str
            The API endpoint to upload the file to.
        params : dict, optional
            Parameters to include in the request.
        file_type : str, optional
            The MIME type of the file. Defaults to 'image/jpeg'.

        Returns
        -------
        dict or str
            The response JSON if the request is successful, otherwise an error message.
        """
        if not os.path.isfile(file_path):
            return f"Error: The file {file_path} does not exist."

        file_name = os.path.basename(file_path)
        files = {'file': (file_name, open(file_path, 'rb'), file_type)}
        return self._make_request('POST', endpoint.format(item_id), params=params, files=files)

    def upload_picture(self, item_id, image_path):
        """
        Uploads a picture for a specific item.

        Parameters
        ----------
        item_id : int
            The ID of the item.
        image_path : str
            The path to the image file.

        Returns
        -------
        dict or str
            The response JSON if the request is successful, otherwise an error message.
        """
        return self.upload_file(item_id, image_path, f'/item/{{}}/uploadPicture', params={'item_picture': 'fdti_adapter.jpg'}, file_type='image/jpeg')

    def upload_datasheet(self, item_id, datasheet_path):
        """
        Uploads a datasheet for a specific item.

        Parameters
        ----------
        item_id : int
            The ID of the item.
        datasheet_path : str
            The path to the datasheet file.

        Returns
        -------
        dict or str
            The response JSON if the request is successful, otherwise an error message.
        """
        return self.upload_file(item_id, datasheet_path, f'/item/{{}}/uploadDatasheet', params={'item_datasheet': 'DS_FT232R.pdf'}, file_type='application/pdf')

    def upload_trainings_picture(self, item_id, segmented_images_path):
        """
        Uploads training pictures for a specific item.

        Parameters
        ----------
        item_id : int
            The ID of the item.
        segmented_images_path : str
            The path to the directory containing segmented images.

        Returns
        -------
        dict or str
            The response JSON if the request is successful, otherwise an error message.
        """
        zip_file_name = 'segmented_images.zip'
        zip_segmented_images_path = self.zipdir(segmented_images_path, zip_file_name)
        return self.upload_file(item_id, zip_segmented_images_path, f'/item/{{}}/uploadTrainingPicture', params={'item_training_pictures': zip_file_name}, file_type='application/zip')


if __name__ == '__main__':

    img = '/home/thd/test/iot_inventory_control/inventory_station/src/images/original/ftdi_232_adapter.png'
    seg = '/home/thd/test/iot_inventory_control/inventory_station/src/images/segmented/2024-07-08'
    zipped = '/home/thd/test/iot_inventory_control/inventory_station/src/images/segmented_images.zip'
    ds = '/home/thd/DS_FT232R.pdf'
    
    newItem = {
        "item_id": "5",
        "item_name": "test",
        "item_picture": "test.png",
        "item_datasheet": "",
        "item_audiofile": "",
        "item_training_pictures": "",
        "item_deprecated": "active",
    }
    newBox = {
        "box_id": "2",
        "box_rfid": "86195789552",
        "box_label_name": "",
        "default_location_id": "1",
        "item_id": "2",
        "location_id": "1",
    }

    # Example usage
    rest = Rest()
    #print(rest.find_item_by_id(1))
    # Uncomment as needed for testing
    #print(rest.search_for_item_by_name('FTDI 232 Adapter'))
    # print(rest.insert_new_item(newItem))
    # print(rest.update_item(newItem))
    print(rest.find_box_by_id(1))
    #print(rest.search_for_box_with_rfid('010101ff'))
    # print(rest.insert_new_box(newBox))
    # print(rest.upload_picture(5, img))
    # print(rest.upload_trainings_picture(5, seg))
    # print(rest.upload_datasheet(5, ds))
    #print(rest.get_location_by_id(3))
    #print(rest.search_for_location_by_id(1))
