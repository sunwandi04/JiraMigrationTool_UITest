#!/usr/bin/env zsh
echo "-> Removing old Allure results"
rm -rf  allure-results/* || echo "No results"
echo "-> Start tests"
pytest  tests --alluredir allure-results
echo "-> Test finished"
echo "-> Generating report"
allure generate allure-results --clean -o allure-report
echo "-> Execute 'allure serve' in the command line"
# allure serve allure-results
exit 0