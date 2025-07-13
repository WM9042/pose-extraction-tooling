import json
import os
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Union


class Parser:
    def __init__(self):
        ###########################
        # CHANGE PARSING TARGETS HERE
        ###########################
        self.target_split_keys = ("split",)
        self.target_split_values = (
            "train",
            "test",
            "val",
            "validation",
        )
        self.target_uid_keys = ("video_id", "uid")

    def decide_parser(self, split_file_path: str) -> Dict[str, str]:
        """
        Public Strategy Method for parsing xml or json files.
        Decides the file type and calls the appropiate parser.

        Args:
            split_file_path: a string denoting the path to the to be parsed file

        Returns:
            A dictionary that has a mapping of a uid with an appended file name to split value.

        Raises:
            TypeError: If split_file_path is not a string.
            ValueError: If the passed file is neither proper json or xml.
            PermissionError: If user does not have permission to read passed file.

        Warning:
            This implementation assumes that any uid key and its corresponding split value key are present
            within the same parent element.
        """
        if not isinstance(split_file_path, str):
            raise TypeError(f"split_file_path {split_file_path} is not a string.")
        try:
            file_name_to_append = os.path.basename(split_file_path)
            with open(split_file_path, "r") as f:
                file_content = f.read()
                parsed_data = json.loads(file_content)
                return self._parse_json(parsed_data, file_name_to_append)
        except json.JSONDecodeError:
            try:
                parsed_data = ET.parse(split_file_path)
                return self._parse_xml(parsed_data, file_name_to_append)
            except ET.ParseError:
                raise ValueError(
                    f"Failed to parse file at {split_file_path}. Please make sure file is valid json or xml."
                )
        except PermissionError:
            raise PermissionError(f"Permission denied for file: {split_file_path}")
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Could not find any file at {split_file_path}. Please double check file path."
            )

    def _parse_json(
        self, json_data: Union[Dict[str, Any], List[Dict]], file_name_to_append: str
    ) -> Dict[str, str]:
        """
        Initiates the JSON parsing process to extract uid and split value pairs.

        This function validates that the provided JSON data is either a dictionary or list, then delegates
        the extraction to the _traverse_json_helper method. Each extracted UID is appended with the
        given file_name_to_append to form a unique key in the returned dictionary.

        Args:
            json_data: A JSON structure (dict or list) containing uid and split value pairs.
            file_name_to_append: A string appended to each uid to ensure unique identification.

         Returns:
            A dictionary mapping each unique key (constructed as "uid_file_name_to_append")
            to its corresponding split value.

        Raises:
            TypeError: If json_data is not a dict or list.
            ValueError: If no valid uid-split pair is found.

        Warning:
            This implementation assumes that any uid key and its corresponding split value key are present
            within the same parent element.
        """
        if not isinstance(json_data, (dict, list)):
            raise TypeError(
                f"Json file {file_name_to_append} is not a dict or list. Please verify data integrity."
            )

        json_split_dict = {}
        self._traverse_json_helper(json_data, file_name_to_append, json_split_dict)

        if not json_split_dict:
            raise ValueError(
                f"Missing required uid or split key in file: {file_name_to_append}"
            )
        return json_split_dict

    def _traverse_json_helper(
        self,
        json_data: Union[Dict[str, Any], List[Any]],
        file_name_to_append: str,
        json_split_dict: Dict[str, str],
    ):
        """
        Recursively traverses the JSON structure to extract uid and split value pairs,
        appending the provided file name to the uid to generate unique keys.


        Args:
            json_data: JSON Dict or JSON List to parse
            file_name_to_append: A string to append to the UID.
            json_split_dict: Mutable dict mapping UID_with_appended_file_name to split value.

        Raises:
            TypeError: If json_data is not a dict or list, or if an extracted split value is not a string.
            ValueError: If one element of a pair (uid or split value) is missing or if a duplicate uid key is detected.
            RecursionError: If maximum recursion depth is exceeded.


        Warning:
            This implementation assumes that any uid key and its corresponding split value key are present
            within the same parent element.
        """
        try:
            if isinstance(json_data, dict):
                uid_value = None
                split_value = None

                for key, value in json_data.items():
                    if key in self.target_uid_keys:
                        uid_value = value

                    if key in self.target_split_keys or (
                        isinstance(value, str) and value in self.target_split_values
                    ):
                        split_value = value

                if uid_value is not None or split_value is not None:
                    if uid_value is None or split_value is None:
                        raise ValueError(
                            f"Missing required uid or split key in file: {file_name_to_append}"
                        )

                    if not isinstance(uid_value, str):
                        uid_value = str(uid_value)

                    if not isinstance(split_value, str):
                        raise TypeError(
                            f"Split value is not a string in file: {file_name_to_append}"
                        )

                    key_with_file = f"{uid_value}_{file_name_to_append}"

                    if key_with_file in json_split_dict:
                        raise ValueError(
                            f"Duplicate uid encountered: {uid_value} in file: {file_name_to_append}"
                        )
                    json_split_dict[key_with_file] = split_value

                for value in json_data.values():
                    self._traverse_json_helper(
                        value, file_name_to_append, json_split_dict
                    )

            elif isinstance(json_data, list):
                for item in json_data:
                    self._traverse_json_helper(
                        item, file_name_to_append, json_split_dict
                    )
        except RecursionError:
            raise RecursionError(
                f"Recursion depth exceeded while parsing file: {file_name_to_append}. "
                "Ensure the JSON structure is not excessively deep or circular."
            )

    def _parse_xml(
        self, xml_data: ET.ElementTree, file_name_to_append: str
    ) -> Dict[str, str]:
        """
        Parse the XML data to extract UID and split values.

        Args:
            xml_data: An XML ElementTree object.
            file_name_to_append: A string to append to the UID.

        Returns:
            A dictionary mapping UID_with_appended_file_name to split value.

        Raises:
            ValueError: If duplicate UIDs are found.
            ValueError: If no split keys/values are found.
            ValueError: If no uids are found.

        Warning:
            This implementation assumes that any uid key and its corresponding split value key are present
            within the same parent element.
        """

        xml_split_dict = {}
        root = xml_data.getroot()
        uid_value = None
        split_value = None
        found_uid_value_flag = False
        found_split_value_flag = False

        for element in root.iter():
            tag = element.tag
            if element.text is None:
                continue
            text = element.text.strip()

            if tag in self.target_uid_keys:
                uid_value = text
                found_uid_value_flag = True
            if tag in self.target_split_keys or text in self.target_split_values:
                split_value = text
                found_split_value_flag = True

            if uid_value is not None and split_value is not None:
                uid_value_with_appended_file_name = (
                    uid_value + "_" + file_name_to_append
                )
                if uid_value_with_appended_file_name in xml_split_dict:
                    raise ValueError(
                        f"Duplicate UID: {uid_value} in file at {file_name_to_append}"
                    )
                xml_split_dict[uid_value_with_appended_file_name] = split_value
                uid_value = None
                split_value = None

        if found_uid_value_flag is False:
            raise ValueError(f"Did not find any uids in {file_name_to_append}")
        if found_split_value_flag is False:
            raise ValueError(
                f"Did not find any target split value in {file_name_to_append}"
            )

        return xml_split_dict
