import os, csv, json
import shutil
import logging



class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path
        logging.basicConfig(
            filename="logs/file_operations.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    def validate_file(self):
        """Check if the file exists and is accessible."""
        return os.path.isfile(self.file_path)

    def read_file(self):
        """Read the content of a text file."""
        try:
            if not self.validate_file():
                logging.error(f"File not found: {self.file_path}")
                raise FileNotFoundError("File does not exist.")

            with open(self.file_path, 'r', encoding='utf-8') as file:
                logging.info(f"File read successfully: {self.file_path}")
                return '\n' + file.read()
        except Exception as e:
            logging.exception(f"Error reading file: {self.file_path}")
            return f"Error reading file: {e}"

    def write_file(self, data, mode='w'):
        """Write data to a text file."""
        try:
            with open(self.file_path, mode, encoding='utf-8') as file:
                logging.info(f"File written successfully: {self.file_path}")
                file.write(data)
            return "Write operation successful."
        except Exception as e:
            logging.exception(f"Error writing to file {self.file_path}: {e}")
            return f"Error writing to file: {e}"

    def append_to_file(self, data):
        """Append data to a new line in a text file."""
        return self.write_file('\n' + data, mode='a')

    def create_backup(self, backup_dir='backups'):
        """Create a backup of the file."""
        try:
            if not self.validate_file():
                logging.exception(f"File {self.file_path} does not exist, backup failed")
                raise FileNotFoundError("File does not exist. Backup failed.")

            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            backup_path = os.path.join(backup_dir, os.path.basename(self.file_path) + '.bak')
            shutil.copy2(self.file_path, backup_path)
            logging.info(f"Backup created successfully for file {self.file_path}")
            return f"Backup created at {backup_path}"
        except Exception as e:
            return f"Error creating backup: {e}"

    def parse_file(self):
        """Reads a CSV or JSON file and returns structured data."""
        try:
            if not self.validate_file():
                logging.exception('File not found while parsing')
                raise FileNotFoundError("File does not exist.")

            file_extension = os.path.splitext(self.file_path)[-1].lower()

            with open(self.file_path, 'r', encoding='utf-8') as file:
                if file_extension == ".csv":
                    reader = csv.DictReader(file)
                    data = [row for row in reader]
                    # Converting files to integer (In this case "Age"), since csv only supports strings
                    for item in data:
                        if "Age" in item:
                            try:
                                item["Age"] = int(item["Age"])  # Convert Age to int
                            except ValueError:
                                item["Age"] = None  # Handle invalid numbers
                    logging.info(f"File parsed successfully {self.file_path}")
                    return data

                elif file_extension == ".json":
                    logging.info(f"File parsed successfully {self.file_path}")
                    return json.load(file)  # Load JSON file as list of dictionaries
                else:
                    logging.exception(f"Unsupported file extension: {file_extension}")
                    return "Unsupported file format. Only CSV and JSON are allowed."
        except Exception as e:
            logging.exception(f"File parsing failed for file {self.file_path}")
            return f"Error parsing file: {e}"

    def manipulate_text(self, operation, *args):
        """Perform string manipulations on the text file."""
        try:
            if not self.validate_file():
                raise FileNotFoundError("File does not exist.")

            with open(self.file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            if operation == "uppercase":
                text = text.upper()
            elif operation == "lowercase":
                text = text.lower()
            elif operation == "replace":
                old, new = args
                text = text.replace(old, new)
            elif operation == "strip_spaces":
                text = " ".join(text.split())  # Removes extra spaces and newlines
            elif operation == "count_word":
                word = args[0]
                return text.lower().split().count(word.lower())  # Case-insensitive count
            else:
                return "Invalid operation."

            # Write the manipulated text back to the file
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write(text)

            return "Successful."
        except Exception as e:
            return f"Error manipulating text: {e}"

    def validate_data(self, required_fields=None, data_types=None):
        """Validates data against required fields and data types."""
        data = self.parse_file()
        try:
            if not isinstance(data, list):
                raise ValueError("Data should be a list of dictionaries.")

            for item in data:
                if not isinstance(item, dict):
                    raise ValueError("Each item in data should be a dictionary.")

                if required_fields:
                    missing_fields = [field for field in required_fields if field not in item]
                    if missing_fields:
                        return f"Missing required fields: {missing_fields}"

                if data_types:
                    for field, expected_type in data_types.items():
                        if field in item:
                            actual_type = type(item[field])
                            if actual_type is not expected_type:
                                return (f"Field '{field}' should be of type {expected_type.__name__}, "
                                        f"but got {actual_type.__name__}")

            return "Data validation successful."
        except Exception as e:
            return f"Error validating data: {e}"

    def filter_data(self, field, value):
        """Filter data based on an exact match."""
        data = self.parse_file()
        return [item for item in data if item.get(field) == value]

    def filter_data_range(self, field, min_value=None, max_value=None):
        """Filter data based on a numeric range."""
        data = self.parse_file()
        filtered_data = []

        for item in data:
            if field in item and isinstance(item[field], (int, float)):
                if (min_value is None or item[field] >= min_value) and (max_value is None or item[field] <= max_value):
                    filtered_data.append(item)

        return filtered_data

    def filter_data_contains(self, field, substring):
        """Filter data where a field contains a substring (case insensitive)."""
        data = self.parse_file()
        return [item for item in data if field in item and
                isinstance(item[field], str) and substring.lower() in item[field].lower()]
