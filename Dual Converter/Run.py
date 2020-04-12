from Dual_Converter import *

def main():
    try:
        exec(open("Dual_Converter.py").read())
    except FileNotFoundError:
        print("Converter file not found")
        os.system("pause")
        system.exit(0)
    except FileExistsError:
        print("Converter file does not exists")
        os.system("pause")
        system.exit(0)
    except SystemExit:
        pass

    choice = str(input("Do you want to run the converter again? (y = Yes, n + No) ")).lower()

    while choice == "y":
        try:
            exec(open("Dual_Converter.py").read())
        except FileNotFoundError:
            print("Converter file not found")
            os.system("pause")
            system.exit(0)
        except FileExistsError:
            print("Converter file does not exists")
            os.system("pause")
            system.exit(0)
        except SystemExit:
            pass
        choice = str(input("Do you want to run the converter again? (y = Yes, n + No) ")).lower()
        while choice != "y" and choice != "n":
            print("Please type a valid character (y or n)")
            choice = str(input("Do you want to run the converter again? (y = Yes, n + No) ")).lower()
        if choice == "n":
            break

    try:
        shutil.rmtree("__pycache__")
    except OSError as e:
        pass


if __name__ == "__main__":
     main()