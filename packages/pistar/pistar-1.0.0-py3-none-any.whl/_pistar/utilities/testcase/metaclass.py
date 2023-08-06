"""
description: this module provides class MetaTestCase.
"""

BASE_TEST_CASE = "BaseTestCase"


class MetaTestCase(type):
    """
    description: this class is the meta class of BastTestCase.
    """

    def __init__(cls, *args, **kwargs):
        """
        description: this function is used to execute testcase automatically
        """
        super().__init__(*args, **kwargs)

        return

    def __new__(mcs, name, bases, class_dict):
        bases = (object,) if name == BASE_TEST_CASE else bases

        new_class = type.__new__(mcs, name, bases, class_dict)

        return new_class

    def __call__(cls, *args, **kwargs):
        """
        description: this function is used for testcase introspection.
        """
        testcase = type.__call__(cls, *args, **kwargs)

        if not testcase.failure:

            def failure():
                return testcase.teardown()

            testcase.failure = failure

        return testcase
