from models import B,C,D,E

def main():
    print("Hello from syncspec!")

    e = E(d=[
        D(x={'t': 'b', 'b_field': 'hello'}),
        D(x={'t': 'c', 'c_field': 10})
    ])
    e.execute()


if __name__ == "__main__":
    main()
