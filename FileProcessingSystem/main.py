from FileManager import FileManager
from FileOrganization import FileOrganization



def task1():
    file_manager = FileManager('files/example.txt')

    print("Validating the file: ", file_manager.validate_file(), '\n')  # checks if file exists
    print("Reading the file: ", file_manager.read_file(), '\n')  # reads the file
    print("Writing to file: ", file_manager.write_file(data='python'), '\n')  # writes data, but removes previous data
    print("Appending to file: ", file_manager.append_to_file(data='python'), '\n')  # appends without removing data
    print("Creating a backup: ", file_manager.create_backup(), '\n')  # creates backup file in 'backups' directory

def task2():
    file_manager_csv = FileManager("files/data.csv")
    file_manager_json = FileManager("files/data.json")
    file_manager_txt = FileManager("files/example.txt")

    print("Parsing CSV file:", file_manager_csv.parse_file(), '\n')  # parses csv file
    print("Parsing JSON file:", file_manager_json.parse_file(), '\n')  # parses json file

    print("Converting to uppercase:", file_manager_txt.manipulate_text("uppercase"), '\n')
    print("Replacing word:", file_manager_txt.manipulate_text("replace", "PYTHON", "java"), '\n')

    word = 'java'
    count = file_manager_txt.manipulate_text("count_word", word)  # Count occurrences of a word
    print(f"word '{word}' appears {count} times.", '\n')

    print("Removing extra spaces:", file_manager_txt.manipulate_text("strip_spaces"), '\n')  # Remove extra spaces

    required_fields = ['Name', 'Age', 'Occupation']  # defining the fields for files
    data_types = {'Name': str, 'Age': int, 'Occupation': str}  # defining the data types for fields
    print("Validating json data: ", file_manager_json.validate_data(required_fields, data_types))
    print("Validating csv data: ", file_manager_csv.validate_data(required_fields, data_types))

    print("Filter by Occupation: ", file_manager_json.filter_data('Occupation', 'Engineer'))
    print("Filter by Age range: ", file_manager_json.filter_data_range('Age', 28, 45))
    print("Filter by Name: ", file_manager_json.filter_data_contains('Name', 'ice'))

def task3():
    file_organization = FileOrganization('files')
    print(f"List all the files in directory 'files': ", file_organization.list_files(), '\n')

    print('Sorted in Ascending order by date: ', file_organization.list_and_sort_files(sort_by='date'))
    print('Sorted in Ascending order by type: ', file_organization.list_and_sort_files(sort_by='type'))
    print('Sorted in Descending order by name: ', file_organization.list_and_sort_files(reverse=True))
    print('Organizing files into categories: ', file_organization.file_categories(), '\n')
    print('Searching files: ', file_organization.search_files('exa'), '\n')



if __name__ == '__main__':
    task1()
    task2()
    task3()
