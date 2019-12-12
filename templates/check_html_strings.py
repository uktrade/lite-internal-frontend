import importlib
import inspect
import os
import re

LCS_PATTERN = "{% lcs '(.*)' %}"


def get_strings_package(base_dir):
    """
    Uses BASE_DIR to get the lite_content package
    i.e. /Users/user/lite-internal-frontend = lite_internal_frontend
    :return: strings package name
    """
    project_name = os.path.basename(base_dir)
    return project_name.replace("-", "_", 2)


def get_base_dir():
    """
    Get's the BASE_DIR from settings.
    Accounts for this file being called externally
    :return: str BASE_DIR value
    """
    try:
        from conf.settings import BASE_DIR
    except ModuleNotFoundError:
        # Fix for calling python file externally
        import sys
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(parent_dir)
        from conf.settings import BASE_DIR
    return BASE_DIR


def get_all_html_strings(templates_folder):
    """
    Get all LCS strings from the HTML files in the given folder
    :param templates_folder: string path for the HTML folders
    :return: set of found LCS strings
    """
    strings = set()

    for root, _, files in os.walk(templates_folder):
        for file_name in files:
            if file_name.endswith(".html"):
                with open(f"{root}/{file_name}") as f:
                    lcs_strings = re.findall(LCS_PATTERN, f.read())
                    strings.update(lcs_strings)

    return strings


def get_all_lite_strings(lite_strings, module, path):
    """
    Recursive function to load all properies in a given module
    :param lite_strings: set of strings found
    :param module: the current module to search
    :param path: the string path to the current module (dot seperated)
    :return: set of all string paths for lite_content
    """
    for key, obj in inspect.getmembers(module):
        # Ignore hidden properties
        if "__" not in key:

            # Uses isupper to ensure we do not assess both the import and the definition (definition is uppercase)
            if inspect.isclass(obj) or (inspect.ismodule(obj) and key.isupper()):
                get_all_lite_strings(lite_strings, obj, f"{path}.{key}")

            # Saves path. Removes leading .
            elif isinstance(obj, str):
                lite_strings.add(f"{path}.{key}"[1:])

    return lite_strings


if __name__ == "__main__":
    not_found = []

    base_dir = get_base_dir()
    # Load strings package
    strings_package_name = get_strings_package(base_dir)
    strings_module = importlib.import_module(f"lite_content.{strings_package_name}.strings")

    # Get all HTML strings (LCS)
    html_strings = get_all_html_strings(f"{base_dir}/templates")

    # Get all lite_content strings
    lite_strings = get_all_lite_strings(set(), strings_module, "")

    if html_strings != lite_strings:
        errors = []
        # Get differences between the two sets
        invalid_html_strings = html_strings - lite_strings
        unused_lite_strings = lite_strings - html_strings

        if invalid_html_strings:
            errors.append(f"\n\nThe following HTML strings couldn't be found: {invalid_html_strings}")
        if unused_lite_strings:
            errors.append(f"\n\nThe following strings in lite_content are unused: {unused_lite_strings}")
        raise Exception("".join(errors))
    
    else:
        print("All LITE strings valid")
