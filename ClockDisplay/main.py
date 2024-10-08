from window import window
from get_config import get_config


def main() -> None:
    configs: list = get_config()
    wn = window(configs)
    wn.root.attributes('-topmost', True)
    print(wn.root.winfo_screenwidth())
    wn.root.mainloop()


if __name__ == '__main__':
    main()
