while True:
    try:
        line = input(">>> ")
        result = eval(line)
        print(result)
    except Exception as e:
        print("Error:", e)