import unittest
import testing_file

if __name__ == '__main__':
    test_suite = unittest.TestSuite()
    
    test_suite.addTest(testing_file.Scenario1TestCase('test_scenario1'))
    test_suite.addTest(testing_file.Scenario2TestCase('test_scenario2'))
    test_suite.addTest(testing_file.Scenario3TestCase('test_scenario3'))
    test_suite.addTest(testing_file.Scenario4TestCase('test_scenario4'))


    runner = unittest.TextTestRunner()
    output = runner.run(test_suite)
    print(type(output))
    print(output)    


#unittest.TextTestRunner(): This is the default text-based test runner that displays test results in the console.
#test_suite is a container that holds the specified test cases from the sample_main

# dates(start_date, end_date)