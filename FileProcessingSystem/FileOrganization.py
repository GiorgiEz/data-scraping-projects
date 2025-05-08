from collections import defaultdict
from pathlib import Path
import logging



class FileOrganization:
    def __init__(self, directory):
        self.directory = directory
        logging.basicConfig(
            filename="logs/file_operations.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    def list_files(self):
        """Lists all files in the given directory."""
        try:
            dir_path = Path(self.directory)
            if not dir_path.exists() or not dir_path.is_dir():
                logging.error(f"Listing files failed, directory doesn't exist: {self.directory}")
                return f"Directory '{self.directory}' does not exist."

            files = [f for f in dir_path.iterdir() if f.is_file()]
            return files if files else "No files found in the directory."

        except Exception as e:
            logging.exception(f"Error listing files in: {self.directory}")
            return f"Error listing files: {e}"

    def list_and_sort_files(self, sort_by="name", reverse=False):
        """Lists and sorts files in a directory.
        Args:
            sort_by (str): Sorting criteria ("name", "type", "date").
            reverse (bool): If True, sorts in descending order. Default is False (ascending).
        """
        try:
            files = self.list_files()
            if isinstance(files, str):  # If an error message is returned
                logging.error(f"Files sorting failed in: {self.directory}")
                return files

            if sort_by == "name":
                sorted_files = sorted(files, key=lambda f: f.name.lower(), reverse=reverse)
            elif sort_by == "type":
                sorted_files = sorted(files, key=lambda f: f.suffix.lower(), reverse=reverse)
            elif sort_by == "date":
                sorted_files = sorted(files, key=lambda f: f.stat().st_mtime, reverse=reverse)
            else:
                logging.error(f"Invalid sort option '{sort_by}' used in: {self.directory}")
                return f"Invalid sort option. Use 'name', 'type', or 'date'."

            logging.info(f"Files successfully sorted by {sort_by} in: {self.directory}")
            return [f.name for f in sorted_files]

        except Exception as e:
            logging.exception(f"Error sorting files in: {self.directory}")
            return f"Error sorting files: {e}"

    def file_categories(self):
        """ Groups files by their extension """
        try:
            files = self.list_files()
            if isinstance(files, str):  # If an error message is returned
                logging.error(f"Files grouping failed in: {self.directory} directory")
                return f"Files grouping failed in: {self.directory} directory"

            file_groups = defaultdict(list)
            for file in files:
                name, extension = file.name.split('.')
                file_groups[extension].append(file.name)

            logging.info(f"Files grouped successfully: {self.directory} directory")
            return file_groups
        except Exception as e:
            logging.exception(f"File grouping failed at: {self.directory} directory")
            return f"Error grouping files: {e}"

    def search_files(self, searched_file):
        """ Simple search function to find files containing given searched_file
            Args: searched_file: file user trying to search for
        """
        try:
            files = self.list_files()
            if type(files) == str:
                logging.error(f"Files searching failed in: {self.directory} directory")
                return f"Files searching failed in: {self.directory} directory"

            logging.info(f"Searching files successful: {self.directory} directory")
            return [file_name.name for file_name in files if searched_file in file_name.name]
        except Exception as e:
            logging.exception(f"Searching files failed: {self.directory} directory")
            return f"Error searching files: {e}"
