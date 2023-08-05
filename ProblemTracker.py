import os
import configparser

class ProblemTracker:
    # Read the text files to get the problem names and categories
    def readFiles(self):
        # Open the text file with the solved problems' names 
        with open(self.solved_dir_path, 'r') as f:
            # Add to the set of solved problems each of the read lines
            lines = f.readlines()
            for l in lines:
                self.solved_problems_set.add(l.strip().lower())

        # Get all the names of the categories by listing the names of the
        # text files
        for path in os.listdir(self.problems_dir_path):
            # If it is a text file, you append it to the list that stores
            # the names of the categories. To each of the strings we're
            # removing the last 4 chars which contain ".txt"
            if os.path.isfile(os.path.join(self.problems_dir_path, path)):
                self.problems_categories.append(path[:-4])

        # For each category, we open the text files that contain the problems
        # in that category and add them to a dictionary. The dictionary uses
        # as a key the category, and a list with the names of the problems
        # as the value
        for category in self.problems_categories:
            # For each category, we open the text file and store the problem
            # names
            with open(self.problems_dir_path + category + ".txt", 'r') as f:
                # Read the lines and store them as a list of strings
                lines = f.readlines()

                # As the strings contain break lines, we iterate over the list
                # to strip each string
                for l in lines:
                    # Get the list from the dict of problems (if the list still
                    # doesn't exist, we get an empty list) 
                    lst = self.problems.get(category, [])
                    # Append to the list the stripped string
                    lst.append(l.strip())
                    # Change the value of the dictionary
                    self.problems[category] = lst

                    if l.strip().lower() in self.solved_problems_set:
                        # Get the list from the dict of solved problems (if the
                        # list still doesn't exist, we get an empty list) 
                        lst = self.solved_problems.get(category, [])
                        # Append to the list the stripped string
                        lst.append(l.strip())
                        # Change the value of the dictionary
                        self.solved_problems[category] = lst

        # Get all the names of the lists of problems by listing the names of the
        # folders
        for path in os.listdir(self.lists_dir_path):
            # Dictionary that will store the problems on each category and then
            # will be added to the dictionary of the list of problems
            temp_dict = {}

            # Get all the names of the categories by listing the names of the
            # text files
            for category in os.listdir(os.path.join(self.lists_dir_path, path)):
                # Path to the category text file
                text_file_path = os.path.join(self.lists_dir_path, path, category)
                # Remove the last 4 chars which contain ".txt"
                category = category[:-4]

                # If it is a text file
                if os.path.isfile(text_file_path):
                    # For each category, we open the text file and store the problem
                    # names
                    with open(text_file_path, 'r') as f:
                        # Read the lines and store them as a list of strings
                        lines = f.readlines()

                        # As the strings contain break lines, we iterate over the list
                        # to strip each string
                        for l in lines:
                            # Get the list from the dict of problems (if the list still
                            # doesn't exist, we get an empty list) 
                            lst = temp_dict.get(category, [])
                            # Append to the list the stripped string
                            lst.append(l.strip())
                            # Change the value of the dictionary
                            temp_dict[category] = lst

                # Stores the dictionary of problems on each list of problems
                self.problems_lists[path] = temp_dict

        # Read the config file
        self.config = configparser.ConfigParser()
        self.config.read(self.config_dir_path)
        self.github_profile = self.config.get('GITHUB', 'profile')
        self.github_repo = self.config.get('GITHUB', 'repo_name')
        self.output_dir_path = self.config.get('DIR_PATHS', 'output_dir')
        self.auto_push = True if self.config.get('MISC', 'auto_push').lower() == "true" else False
        self.repo_dir += self.config.get('DIR_PATHS', 'repo_dir')

    # Constructor
    def __init__(self):
        # Initialize the needed lists/sets
        self.problems_categories = []
        self.problems = {}
        self.solved_problems = {}
        self.solved_problems_set = set()
        self.problems_lists = {}
        self.github_profile = ""
        self.github_repo = ""
        self.auto_push = False
        self.config = None

        # Path to the directory of the project
        self.package_dir = os.getcwd()
        # Path to the problems directory
        self.problems_dir_path = os.path.join(self.package_dir, 'Problems\\')
        # Path to the solved file
        self.solved_dir_path = os.path.join(self.package_dir, 'Config\\Solved.txt')
        # Path to config file
        self.config_dir_path = os.path.join(self.package_dir, 'Config\\config.cfg')
        # Path to the lists of problems
        self.lists_dir_path = os.path.join(self.package_dir, 'Lists\\')
        # Path to the local repository (will append to it from config file)
        self.repo_dir = self.package_dir

        # Read the files
        self.readFiles()

        # Needed to ensure the colors are displayed in the console correctly
        os.system("color")

    # Functions to assign green color when printing to the console
    def green(self, doPrint=True):
        # It always return the value in case you want to use it as an
        # intext modifier, but can also print it so it affects all
        # after it
        if doPrint:
            print('\x1b[1;32;40m', end="")
        return '\x1b[1;32;40m'

    # Functions to assign white/black color when printing to the console
    def normal(self, doPrint=True):
        # It always return the value in case you want to use it as an
        # intext modifier, but can also print it so it affects all
        # after it
        if doPrint:
            print('\033[0m', end="")
        return '\033[0m'

    # Functions to assign cyan color when printing to the console
    def cyan(self, doPrint=True):
        # It always return the value in case you want to use it as an
        # intext modifier, but can also print it so it affects all
        # after it
        if doPrint:
            print('\033[96m', end="")
        return '\033[96m'

    # Functions to assign red color when printing to the console
    def red(self, doPrint=True):
        # It always return the value in case you want to use it as an
        # intext modifier, but can also print it so it affects all
        # after it
        if doPrint:
            print('\033[91m', end="")
        return '\033[91m'

    # Print the problem with certain format
    def printProblem(self, i, p, bullet):
        print(f"{bullet}{i+1}) {p}")

    # Displays all the problems available (solved and unsolved)
    def displayAllProblems(self):
        # Each item of the problems contains the category and a list with
        # the problem names in the category.
        for category, p in self.problems.items():
                # Print the category
                print(f'{category} [{len(self.solved_problems.get(category, []))}/{len(p)}]')
                # Iterate over the list with the problems' names
                for i, p in enumerate(p):
                    # If the problems is already solved, print it in green
                    if p.lower() in self.solved_problems_set:
                        self.green()
                        self.printProblem(i, p, "\t")
                        self.normal()
                    # If not, print it normally
                    else:
                        self.printProblem(i, p, "\t")
                # Space between each category
                print()

    # Displays only the solved problems without any color
    def displaySolved(self):
        # Each item of the problems contains the category and a list with
        # the problem names in the category.
        for category, p in self.solved_problems.items():
                # Print the category
                print(f'{category} [{len(p)}/{len(self.problems.get(category, []))}]')
                # Iterate over the list with the problems' names
                for i, p in enumerate(p):
                    # Print each problem with a certain format
                    self.printProblem(i, p, "\t")
                # Space between each category
                print()

    # Display the category names which have at least one problem solved
    def displaySolvedCategories(self):
        # Stores the index of the categories that have a problem solved
        # With this, we can check if the number input is a valid category
        categories_index = set()
        # Iterate over the problems, checking if for each category there's
        # at least one problem solved, if so, print the category and break
        # the loop
        for category, p in self.problems.items():
                # Check the problems in the category
                for i, p in enumerate(p):
                    # If the problem is solved
                    if p.lower() in self.solved_problems_set:
                        # Print the category and add the index to the set
                        print(category)
                        # For the index, we take the first 2 chars convert
                        # them to integer and add it to the set
                        categories_index.add(int(category[:2]))
                        # Break the cycle so we can check another category
                        # and don't print the same category more than once
                        break
        # Return the set with the indexes 
        return categories_index

    # Display the category names which have no problems solved
    def displayUnsolvedCategories(self):
        # Stores the index of the categories that have no problem solved
        # With this, we can check if the number input is a valid category
        categories_index = set()
        # Iterate over the problems, checking if for each category there's
        # at least one problem solved, if so, print the category and break
        # the loop
        for category, p in self.problems.items():
            # Check the problems in the category
            for problem in p:
                # If the problem is not solved
                if problem.lower() not in self.solved_problems_set:
                    # Print the category and add the index to the set
                    print(category)
                    # For the index, we take the first 2 chars convert
                    # them to integer and add it to the set
                    categories_index.add(int(category[:2]))
                    # Break the cycle so we can check another category
                    # and don't print the same category more than once
                    break
        # Return the set with the indexes 
        return categories_index

    # Gets the category name by the index
    def getCategoryName(self, categoryIndex):
        # Iterate over the problems
        for category in self.problems:
            # If the index of the category is the same as the
            # received one, we return the name of the category
            if categoryIndex == int(category[:2]):
                return category

    # Gets the problems that have been solved from the received
    # category
    def getSolvedProblemsByCategory(self, categoryIndex):
        # Stores the problems that meet the condition
        solved = []

        # Get the problems from the dictionary
        p = self.problems.get(self.getCategoryName(categoryIndex))

        for problem in p:
            #If the problem has been solved, append it
            if problem.lower() in self.solved_problems_set:
                solved.append(problem)
        # Return the list with the solved problems
        return solved

    # Gets the problems that haven't been solved from the received
    # category
    def getUnsolvedProblemsByCategory(self, categoryIndex):
        # Stores the problems that meet the condition
        unsolved_problems = []
        
        # Get the problems from the dictionary
        p = self.problems.get(self.getCategoryName(categoryIndex))

        for problem in p:
            #If the problem hasn't been solved, append it
            if problem.lower() not in self.solved_problems_set:
                unsolved_problems.append(problem)
        # Return the list with the solved problems
        return unsolved_problems

    # Displays the problems from a specific list
    def displayProblems(self, problems):
        for i, p in enumerate(problems):
            self.printProblem(i, p, "")

    # Adds a problem to the set of solved problems and updates the
    # file containing the names of the solved problems
    def addSolved(self, problem, category_index):
        # If the problem hasn't been solved (it's redundant as there
        # are other measures to ensure that no solved problem gets
        # here, but just in case), adds it to the set and file
        if problem.lower() not in self.solved_problems_set:
            # Get the category name from its index
            category_name = self.getCategoryName(category_index)
            # Get the list stored in the dict of solved problems and
            # append to it the problem
            lst = self.solved_problems.get(category_name, [])
            lst.append(problem)
            self.solved_problems[category_name] = lst

            # Add the problem name to the set
            self.solved_problems_set.add(problem.lower())
            # Append the problem to the file
            with open(self.solved_dir_path, 'a') as f:
                f.write(f"\n{problem.lower()}")

    # Removes a problem from the set of solved problems and updates
    # the file containing the names of the solved problems
    def removeSolved(self, problem, category_index):
        # If the problem has been solved (it's redundant as there
        # are other measures to ensure that no unsolved problem
        # gets here, but just in case), removes it from the set
        # and file
        if problem.lower() in self.solved_problems_set:
            # Get the category name from its index
            category_name = self.getCategoryName(category_index)
            # Get the list stored in the dict of solved problems and
            # remove from it the problem
            lst = self.solved_problems.get(category_name, [])
            # Check if the problem is in the list so there's no error
            # in case the list is empty. This should be redundant as
            # you shouldn't be able to remove a solved problem if it
            # wasn't added in the first place, but still, just in case
            if problem in lst:
                lst.remove(problem)
            self.solved_problems[category_name] = lst

            # Remove the problem name from the set
            self.solved_problems_set.remove(problem.lower())
            # Iterate over the set of solved problems rewriting the
            # solved problems' file
            with open(self.solved_dir_path, 'w') as f:
                for i, p in enumerate(self.solved_problems_set):
                    f.write(f"{p}")
                    # To prevent writing an extra line jump at the end
                    # of the file
                    if i != len(self.solved_problems_set)-1:
                        f.write("\n")

    def markAsSolved(self):
        # Get the indexes of the categories that have at least one problem
        # solved to check the input index. Also print the categories so the
        # user can choose the category from which he wants to mark a problem
        # as solved
        categories_index = self.displayUnsolvedCategories()
        # Ask the user the category
        c_index = int(input("\nIndex of category (0 to return to menu): "))
        # Check if the category is not 0 (returns to menu) and that it's
        # included in the available categories. If not, clear the console
        # and return
        if c_index == 0 or c_index not in categories_index:
            os.system('cls')
            return

        # Get in a list the problems that haven't been solved in the specified
        # category
        p = self.getUnsolvedProblemsByCategory(c_index)
        # Display the problems in the previous list
        self.displayProblems(p)
        # Ask the user the problem to mark as solved
        p_index = int(input("\nIndex of problem (0 to return to menu): "))
        # Check if the problem is not 0 (returns to menu) and that it's
        # included in the available problems. If not, clear the console
        # and return
        if p_index <= 0 or p_index > len(p):
            os.system('cls')
            return

        # Ask for a confirmation
        ans = input(f'\nAre you sure you want to mark as solved the problem: "{p[p_index-1]}" (y/n): ')
        # If they accept, mark the problem as solved
        if ans.lower() in ["yes", "y"]:
            self.addSolved(p[p_index-1], c_index)

            if self.auto_push:
                os.system('cls')
                print(f'{self.cyan(False)}Updating README.md{self.normal(False)}')
                self.createReadme()
                print(f'{self.cyan(False)}Pushing changes to remote repository{self.normal(False)}')
                print(f'{self.cyan(False)}git -C "{self.repo_dir}" add .{self.normal(False)}')
                os.system(f'git -C "{self.repo_dir}" add .')
                print(f'{self.cyan(False)}git -C "{self.repo_dir}" commit -m "Add \'{p[p_index-1]}\' solution"{self.normal(False)}')
                os.system(f'git -C "{self.repo_dir}" commit -m "Add \'{p[p_index-1]}\' solution"')
                print(f'{self.cyan(False)}git -C "{self.repo_dir}" push origin main{self.normal(False)}')
                os.system(f'git -C "{self.repo_dir}" push origin main')
                print()

    def markAsUnsolved(self):
        # Get the indexes of the categories that have no solved problem and
        # print them
        categories_index = self.displaySolvedCategories()
        # Ask the user the category
        c_index = int(input("\nIndex of category (0 to return to menu): "))
        # Check if the category is not 0 (returns to menu) and that it's
        # included in the available categories. If not, clear the console
        # and return
        if c_index == 0 or c_index not in categories_index:
            os.system('cls')
            return

        # Get in a list the problems that haven't been solved in the specified
        # category
        p = self.getSolvedProblemsByCategory(c_index)
        # Display the problems in the previous list
        self.displayProblems(p)
        # Ask the user the problem to mark as solved
        p_index = int(input("\nIndex of problem (0 to return to menu): "))
        # Check if the problem is not 0 (returns to menu) and that it's
        # included in the available problems. If not, clear the console
        # and return
        if p_index <= 0 or p_index > len(p):
            os.system('cls')
            return

        # Ask for a confirmation
        ans = input(f'\nAre you sure you want to mark as unsolved the problem: "{p[p_index-1]}" (y/n): ')
        # If they accept, mark the problem as solved
        if ans.lower() in ["yes", "y"]:
            self.removeSolved(p[p_index-1], c_index)

            if self.auto_push:
                os.system('cls')
                print(f'{self.cyan(False)}Updating README.md{self.normal(False)}')
                self.createReadme()
                print(f'{self.cyan(False)}Pushing changes to remote repository{self.normal(False)}')
                print(f'{self.cyan(False)}cd {self.repo_dir}{self.normal(False)}')
                os.system(f'cd {self.repo_dir}')
                print(f'{self.cyan(False)}git add .{self.normal(False)}')
                os.system('git add .')
                print(f'{self.cyan(False)}git commit -m "Add \'{p[p_index-1]}\' solution"{self.normal(False)}')
                os.system(f'git commit -m "Add \'{p[p_index-1]}\' solution"')
                print(f'{self.cyan(False)}git push origin main{self.normal(False)}')
                os.system('git push origin main')
                print()

    def getSolvedProblemsByList(self, list_name):
        solved = 0
        total = 0
        for problems_lists in self.problems_lists.get(list_name, {}).values():
            total += len(problems_lists)
            for problem in problems_lists:
                if problem.lower() in self.solved_problems_set:
                    solved += 1
        return {'solved':solved, 'total': total}

    def displayReadme(self):
        print(f"![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/w/{self.github_profile}/{self.github_repo})")
        print()
        print("# LeetCodeProblems")
        print()
        print("## Overall progress")

        # For each problem list get the solved and total count
        for list_name in self.problems_lists:
            solved_count = self.getSolvedProblemsByList(list_name)['solved']
            total_count = self.getSolvedProblemsByList(list_name)['total']
            print(f"![](https://progress-bar.dev/{solved_count}/?scale={total_count}&suffix=/{total_count}) **{list_name}**")
            print()
        print("## Progress per list of problems")
        print()
        print("| Topic |", end="")

        # Print the titles of each problem list
        for list_name in self.problems_lists:
            print(f" {list_name} |", end="")
        print()
        for i in range(len(self.problems_lists)+1):
            print(f"| :---:", end="")
        print(" |")

        # Iterate over the categories of the problems
        for category in self.problems:
            link = f"https://github.com/{self.github_profile}/{self.github_repo}/tree/main/{category}"
            # Replace characters that usually are replaced in links
            link = link.replace(" ", "%20")
            link = link.replace("&", "%26")
            print(f"| ![{category}]({link}) |", end="")

            # Iterate over the lists of problems
            for list_name, problems_lst_list in self.problems_lists.items():
                # Count the solved problems that are also part of the current list
                counter = 0
                for sp in self.solved_problems.get(category, []):
                    if sp in problems_lst_list.get(category, []):
                        counter += 1
                total = len(problems_lst_list.get(category, []))
                print(f" ![](https://progress-bar.dev/{counter}/?scale={total}&suffix=/{total}) |", end="")
            print()
        print()
        print("Made with ![LeetCode Progress Tracker](https://github.com/christopher-pedraza/leetcode-problem-tracker/)")

    def createReadme(self):
        with open(self.output_dir_path, 'w') as f:
            f.write(f"![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/w/{self.github_profile}/{self.github_repo})\n")
            f.write("\n")
            f.write("# LeetCodeProblems\n")
            f.write("\n")
            f.write("## Overall progress\n")

            # For each problem list get the solved and total count
            for list_name in self.problems_lists:
                solved_count = self.getSolvedProblemsByList(list_name)['solved']
                total_count = self.getSolvedProblemsByList(list_name)['total']
                f.write(f"![](https://progress-bar.dev/{solved_count}/?scale={total_count}&suffix=/{total_count}) **{list_name}**\n")
                f.write("\n")
            f.write("## Progress per list of problems\n")
            f.write("\n")
            f.write("| Topic |")

            # Print the titles of each problem list
            for list_name in self.problems_lists:
                f.write(f" {list_name} |")
            f.write("\n")
            for i in range(len(self.problems_lists)+1):
                f.write(f"| :---:")
            f.write(" |\n")

            # Iterate over the categories of the problems
            for category in self.problems:
                link = f"https://github.com/{self.github_profile}/{self.github_repo}/tree/main/{category}"
                # Replace characters that usually are replaced in links
                link = link.replace(" ", "%20")
                link = link.replace("&", "%26")
                f.write(f"| ![{category}]({link}) |")

                # Iterate over the lists of problems
                for list_name, problems_lst_list in self.problems_lists.items():
                    # Count the solved problems that are also part of the current list
                    counter = 0
                    for sp in self.solved_problems.get(category, []):
                        if sp in problems_lst_list.get(category, []):
                            counter += 1
                    total = len(problems_lst_list.get(category, []))
                    f.write(f" ![](https://progress-bar.dev/{counter}/?scale={total}&suffix=/{total}) |")
                f.write("\n")
            f.write("\n")
            f.write("Made with ![LeetCode Progress Tracker](https://github.com/christopher-pedraza/leetcode-problem-tracker/)\n")
            
    def toggleAutoPush(self):
        if self.auto_push:
            print(f'Set Auto Push to {self.red()}False{self.normal()}')
            self.config.set('MISC', 'auto_push','FALSE')
            self.auto_push = False
        else:
            print(f'Set Auto Push to {self.green()}True{self.normal()}')
            self.config.set('MISC', 'auto_push','TRUE')
            self.auto_push = True
        print()

        with open(self.config_dir_path, 'w') as configfile:
            self.config.write(configfile)


pt = ProblemTracker()

while True:
    print("1. Mark problem as solved")
    print("2. Mark problem as unsolved")
    print("3. Update README.md file")
    print("4. Display all problems")
    print("5. Display solved problems")
    print("6. Print README.md content")
    print("7. Toggle auto push to remote repository")
    print("0. Exit")

    op = input("Option: ")
    os.system('cls')

    if op == '0':
        break
    elif op == '1':
        pt.markAsSolved()
    elif op == '2':
        pt.markAsUnsolved()
    elif op == '3':
        pt.createReadme()
    elif op == '4':
        pt.displayAllProblems()
    elif op == '5':
        pt.displaySolved()
    elif op == '6':
        pt.displayReadme()
    elif op == '7':
        pt.toggleAutoPush()