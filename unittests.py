import unittest
import Parser
import tempfile
import MMPoseExtractor
import os
import torch


class ParserTester(unittest.TestCase):
    def setUp(self):
        self.test_parser = Parser.Parser()
        self.working_xml_test_file_path = (
            "test_files/Parser_test_files/working_xml_test_file.xml"
        )
        self.working_json_test_file_path = (
            "test_files/Parser_test_files/working_json_test_file.json"
        )
        self.invalid_file_type_test_path = (
            "test_files/Parser_test_files/invalid_file_type.txt"
        )
        self.empty_file_path = ""
        self.same_uid_json_file_path = (
            "test_files/Parser_test_files/same_uid_json_file.json"
        )
        self.same_uid_xml_file_path = (
            "test_files/Parser_test_files/same_uid_xml_file.xml"
        )
        self.non_string_split_value_json_file_path = (
            "test_files/Parser_test_files/non_string_split_value_json_file.json"
        )
        self.malformed_json_test_file_path = (
            "test_files/Parser_test_files/malformed_json_file.json"
        )
        self.empty_json_test_file_path = (
            "test_files/Parser_test_files/empty_json_test_file.json"
        )
        self.empty_xml_test_file_path = (
            "test_files/Parser_test_files/empty_xml_test_file.xml"
        )
        self.missing_split_key_json_test_file_path = (
            "test_files/Parser_test_files/missing_split_key_json_test_file.json"
        )
        self.missing_split_key_xml_test_file_path = (
            "test_files/Parser_test_files/missing_split_key_xml_test_file.xml"
        )
        self.missing_uid_key_json_test_file_path = (
            "test_files/Parser_test_files/missing_uid_key_json_test_file.json"
        )
        self.missing_uid_key_xml_test_file_path = (
            "test_files/Parser_test_files/missing_uid_key_xml_test_file.xml"
        )
        self.correct_dict_mapping_json_test_file_path = (
            "test_files/Parser_test_files/correct_dict_mapping_json_test_file.json"
        )
        self.correct_dict_mapping_xml_test_file_path = (
            "test_files/Parser_test_files/correct_dict_mapping_xml_test_file.xml"
        )
        self.only_target_split_values_json_test_file_path = (
            "test_files/Parser_test_files/only_target_split_values_json_test_file.json"
        )
        self.only_target_split_values_xml_test_file_path = (
            "test_files/Parser_test_files/only_target_split_values_xml_test_file.xml"
        )
        self.only_dict_json_test_file_path = (
            "test_files/Parser_test_files/only_dict_json_test_file.json"
        )

    def test_parser_valid_target_inputs(self):
        self.assertIsInstance(self.test_parser.target_split_keys, tuple)
        self.assertIsInstance(self.test_parser.target_split_values, tuple)
        self.assertIsInstance(self.test_parser.target_uid_keys, tuple)

        self.assertTrue(
            all(isinstance(item, str) for item in self.test_parser.target_split_keys),
            "Not all elements in target_split_keys are strings",
        )
        self.assertTrue(
            all(isinstance(item, str) for item in self.test_parser.target_split_values),
            "Not all elements in target_split_values are strings",
        )
        self.assertTrue(
            all(isinstance(item, str) for item in self.test_parser.target_uid_keys),
            "Not all elements in target_uid_keys are strings",
        )

    def test_parser_deeply_nested_json(self):
        depth = 4000
        json_parts = []
        for _ in range(depth):
            json_parts.append('{"nested":')

        json_parts.append('{"video_id": "deep_uid", "split": "train"}')
        json_parts.append("}" * depth)
        deep_json_str = "".join(json_parts)

        with tempfile.NamedTemporaryFile(
            delete=False, mode="w", suffix=".json"
        ) as tmp_file:
            tmp_file.write(deep_json_str)
            file_path = tmp_file.name

        try:
            with self.assertRaises(RecursionError):
                self.test_parser.decide_parser(file_path)

        finally:
            os.remove(file_path)

    def test_parser_decide_parser_invalid_file_type(self):
        self.assertRaises(
            ValueError, self.test_parser.decide_parser, self.invalid_file_type_test_path
        )

    def test_parser_decide_parser_empty_file_path(self):
        self.assertRaises(
            FileNotFoundError, self.test_parser.decide_parser, self.empty_file_path
        )

    def test_parser_returns_dict(self):
        result_json = self.test_parser.decide_parser(self.working_json_test_file_path)
        self.assertIsInstance(result_json, dict)

        result_xml = self.test_parser.decide_parser(self.working_xml_test_file_path)
        self.assertIsInstance(result_xml, dict)

    def test_parser_returns_correct_dict_mapping(self):
        expected_json = {
            "69241_correct_dict_mapping_json_test_file.json": "train",
            "65225_correct_dict_mapping_json_test_file.json": "val",
        }

        result_json = self.test_parser.decide_parser(
            self.correct_dict_mapping_json_test_file_path
        )
        self.assertEqual(result_json, expected_json)

        expected_xml = {
            "69241_correct_dict_mapping_xml_test_file.xml": "train",
            "65225_correct_dict_mapping_xml_test_file.xml": "val",
        }

        result_xml = self.test_parser.decide_parser(
            self.correct_dict_mapping_xml_test_file_path
        )
        self.assertEqual(result_xml, expected_xml)

    def test_parser_with_malformed_file(self):
        self.assertRaises(
            ValueError,
            self.test_parser.decide_parser,
            self.malformed_json_test_file_path,
        )

    def test_parser_only_target_split_values(self):
        expected_json = {
            "69241_only_target_split_values_json_test_file.json": "train",
            "65225_only_target_split_values_json_test_file.json": "val",
        }
        result_json = self.test_parser.decide_parser(
            self.only_target_split_values_json_test_file_path
        )
        self.assertEqual(result_json, expected_json)

        expected_xml = {
            "69241_only_target_split_values_xml_test_file.xml": "train",
            "65225_only_target_split_values_xml_test_file.xml": "val",
        }
        result_xml = self.test_parser.decide_parser(
            self.only_target_split_values_xml_test_file_path
        )
        self.assertEqual(result_xml, expected_xml)

    def test_parser_with_empty_file(self):
        self.assertRaises(
            ValueError, self.test_parser.decide_parser, self.empty_json_test_file_path
        )
        self.assertRaises(
            ValueError, self.test_parser.decide_parser, self.empty_xml_test_file_path
        )

    def test_parser_same_uid_file(self):
        self.assertRaises(
            ValueError, self.test_parser.decide_parser, self.same_uid_json_file_path
        )
        self.assertRaises(
            ValueError, self.test_parser.decide_parser, self.same_uid_xml_file_path
        )

    def test_parser_non_string_value_for_split(self):
        self.assertRaises(
            TypeError,
            self.test_parser.decide_parser,
            self.non_string_split_value_json_file_path,
        )

    def test_parser_missing_uid_key_in_file(self):
        self.assertRaises(
            ValueError,
            self.test_parser.decide_parser,
            self.missing_uid_key_json_test_file_path,
        )
        self.assertRaises(
            ValueError,
            self.test_parser.decide_parser,
            self.missing_uid_key_xml_test_file_path,
        )

    def test_parser_missing_split_key_in_file(self):
        self.assertRaises(
            ValueError,
            self.test_parser.decide_parser,
            self.missing_split_key_json_test_file_path,
        )
        self.assertRaises(
            ValueError,
            self.test_parser.decide_parser,
            self.missing_split_key_xml_test_file_path,
        )

    def test_parser_only_dict_json(self):
        expected_json = {"69241_only_dict_json_test_file.json": "train"}
        result_json = self.test_parser.decide_parser(self.only_dict_json_test_file_path)
        self.assertEqual(result_json, expected_json)


class MMPoseExtractorTester(unittest.TestCase):
    def setUp(self):
        self.checkpoint_file_path = (
            "test_files/MMPoseExtractor_test_files/checkpoint_test_file.json" 
        )
        self.config_file_path = "test_files/MMPoseExtractor_test_files/config_file.json"
        self.input_files_path = "test_files/MMPoseExtractor_test_files/input_Files"
        self.output_files_path = "test_files/MMPoseExtractor_test_files/output_Files"
        self.MMPoseExtractorTester = MMPoseExtractor.MMPoseExtractor(
            self.checkpoint_file_path,
            self.config_file_path,
        )
        self.non_string_checkpoint_file_path = 1234
        self.non_string_config_file_path = True

    def test_create_mmpose_extractor_object(self):
        self.assertIsInstance(
            self.MMPoseExtractorTester, MMPoseExtractor.MMPoseExtractor
        )

    def test_mmpose_extractor_non_string_config_file_path(self):
        with self.assertRaises(TypeError) as config_file_path_type_error:
            MMPoseExtractor.MMPoseExtractor(
                self.non_string_config_file_path,
                self.checkpoint_file_path,
            )
        self.assertIn(
            f"expected string type for config_file_path got {type(self.non_string_config_file_path)}",
            str(config_file_path_type_error.exception),
        )

    def test_mmpose_extractor_non_string_checkpoint_file_path(self):
        with self.assertRaises(TypeError) as checkpoint_file_path_type_error:
            MMPoseExtractor.MMPoseExtractor(
                self.config_file_path,
                self.non_string_checkpoint_file_path,
            )

        self.assertIn(
            f"expected string type for checkpoint_file_path got {type(self.non_string_checkpoint_file_path)}",
            str(checkpoint_file_path_type_error.exception),
        )

    def test_mppose_extractor_model_initalization(self):
        self.assertIsInstance(
            self.MMPoseExtractorTester.model,
            torch.nn.modules.module.Module,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
