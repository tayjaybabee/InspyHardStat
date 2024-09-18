class SensorDataParser:
    def __init__(self, data):
        """
        Initialize the parser with the raw sensor data.

        Parameters:
        data (dict): The raw hierarchical sensor data.
        """
        self.data = data

    def parse(self):
        """
        Parse the raw sensor data and return a formatted dictionary.

        Returns:
        dict: Parsed sensor data as a nested dictionary.
        """
        return self._process_node(self.data)

    def _process_node(self, node):
        """
        Recursively process each node in the sensor data.

        Parameters:
        node (dict): A single node in the sensor data.

        Returns:
        dict: Parsed node data as a nested dictionary based on Text.
        """
        # Create the base node structure with the sensor information
        parsed_node = {
            'id': node.get('id'),
            'min': node.get('Min'),
            'value': node.get('Value'),
            'max': node.get('Max'),
            'sensor_id': node.get('SensorId', None),
            'type': node.get('Type', None),
            'image_url': node.get('ImageURL'),
        }

        # If the node has children, we will recursively process them into a nested dictionary
        if node.get('Children'):
            children_dict = {
                child['Text']: self._process_node(child) for child in node['Children']
            }
            parsed_node['children'] = children_dict
        else:
            parsed_node['children'] = {}

        return parsed_node


    # parsed_data['children']['HAWKING']['children']['AMD Radeon(TM) RX 7700S']['children']['Data']
