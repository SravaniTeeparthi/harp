"""
Description
-----------

Example
-------
```
```
"""
import argparse
from argparse import RawTextHelpFormatter


description = ("""
Description
-----------
""")


def _arguments():
    """Parses input arguments."""

    # Initialize arguments instance
    args_inst = argparse.ArgumentParser(description=(description),
                                        formatter_class=RawTextHelpFormatter)

    # Adding arguments
    args_inst.add_argument("<pos arg name>", type=str, help=("<pos arg help>"))
    args = args_inst.parse_args()

    # Crate a dictionary having arguments and their values
    args_dict = {'<pos arg name>': args.rdir}

    # Return arguments as dictionary
    # Hello world how are you doing
    return args_dict


def main():
    """Main function."""
    argd = _arguments()
    print(argd)


# Execution starts here
if __name__ == "__main__":
    main()
