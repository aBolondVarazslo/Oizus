import sys
import os


main_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'MAIN'))

if main_path not in sys.path:
    sys.path.insert(0, main_path)


from main import tokenize, evaluate


def run_oizys_file(filename):
    with open(filename, 'r') as f:
        code = f.read()

    tokens = tokenize(code)
    result = evaluate(tokens)
    print(result)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: oizys <filename.oizys>")
        sys.exit(1)

    run_oizys_file(sys.argv[1])
