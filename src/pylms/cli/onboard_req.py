
import pandas as pd

from pylms.cli.input_with_quit import input_fn
from pylms.utils import paths


def confirm_onboard_req() -> None:
    """
    prints a warning message to the user listing out all the requirements for cleaning the registration data for the new cohort. after which the user is asked to confirm if these requirements are met.

        - If the user specifies 'y' or 'yes', the program continues to confirm if the requirements are met. Else it exits the program with a warning.
        - Using a defined function `checks` it validates if all requirements are met, and for each requirement that is failed, it prints out a warning, before it forcefully exits the program.

    :return: a None value
    :rtype: None
    """
    
    warning: str = """
Before going ahead, please confirm that the following requirements are met. 
If these requirements are not met, your code will not run successfully.
These requirements are:
    1. That in the `data` folder which is a subdirectory of the project folder, you have saved the following folder called `excel` inside it
    2. The registration data is stored with the name `Registration.xlsx`
    3. That the `Registration.xlsx` file is not open in any program.
    4. That in the same `data` folder, you do not have any file called `dates.json` saved in
    either a sub-directory or `data` itself.
If any of these requirements are not met for you
Enter 'N' or 'No', then fix the issues and then rerun the program 
Are all these requirements met for you [y/N]? """
    # prompt the user with the warning message defined above
    response: str = input_fn(warning)
    # get user input
    response = response.lower().strip()

    def checks() -> bool:
        """
        checks that the following requirements for cleaning the registration date for a new cohort are met. These requirements are:

            - **Registration.xlsx** must exist in a path defined as `data/excel/Registration.xlsx` where **data** is a direct child directory of the project folder.
            - No **dates.json** file must exist in a path defined as `data/json/dates.json` where **data** has the same meaning as defined above.

        :return: True if all requirements are met, False otherwise.
        :rtype: bool
        """
        # check if requirement 1 and 2 is met as defined in the outer scope `warning`
        test1: bool = paths.get_paths_excel()["Registration"].exists()

        # check if requirement 4 is met
        test2: bool = not paths.get_paths_json()["Date"].exists()

        try:
            # check if requirement 3 is met
            pd.read_excel(paths.get_paths_excel()["Registration"])
            test3: bool = True
        except (FileNotFoundError, PermissionError):
            if test1:
                # requirement 3 failed
                print(
                    f"{paths.get_paths_excel()["Registration"]} is open in another process"
                )
                test3 = False
            else:
                # requirements 1 and 2 failed
                print(f"{paths.get_paths_excel()["Registration"]} does not exist.")
                test3 = False

        if not test2:
            # requirement 4 failed
            print(
                f"{paths.get_paths_json()["Date"]} exists contrary to the cleaning requirements."
            )

        return test1 and test2 and test3

    # continue if user specifies that the requirements are met else exit
    if response == "y" or response == "yes":
        pass
    else:
        exit(
            "You have specified that the cleaning requirements are not met. Please fix those issues and rerun the program"
        )

    # continue if the user actually meets the requirements else exit
    if checks():
        pass
    else:
        exit(
            "Cleaning Requirements Failed. Please fix the highlighted issues and then rerun the program."
        )
