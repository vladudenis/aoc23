import os
import subprocess

cd = os.getcwd()
ignore = [".git", ".idea", "venv"]

for item in os.listdir(cd):
    if os.path.isdir(item) and item not in ignore:
        dirname = os.path.abspath(item)
        filename = item.split(" - ")[0]

        os.chdir(dirname)
        path = os.path.join(os.getcwd(), filename)

        with subprocess.Popen(["python", f"{path}.py"], encoding="utf-8",
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            outs, errs = p.communicate()
            answers = outs.split("\n")[:-1]

            print(f"{item}:")
            for idx, answer in enumerate(answers):
                print(f"\tPART {idx + 1}: {answer}")
            print("")

        os.chdir(cd)
