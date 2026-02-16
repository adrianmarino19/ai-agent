from functions.get_files_info import get_files_info


def test():
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result)
    print("")

    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(result)

    result = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(result)

    result = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(result)


if __name__ == "__main__":
    test()


# import unittest
# # from unittest import main, TestCase
# from get_files_info import get_files_info

# class TestGetInfo(unittest.TestCase):
#     # def setUp(self):
#     #     self.get_files_info = get_files_info()

#     def test_current_directory(self):
#         result = get_files_info("calculator", ".")
#         expected_result = """
#         - tests.py: file_size=1354 bytes, is_dir=False
#         - main.py: file_size=741 bytes, is_dir=False
#         - pkg: file_size=160 bytes, is_dir=True
#         """
#         self.assertEqual(result, expected_result)

# if __name__ == "__main__":
#     unittest.main()
