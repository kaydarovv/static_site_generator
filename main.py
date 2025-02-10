from src.static_to_public import source_to_destination

def main():
    static_path = "./static"
    public_path = "./public"
    source_to_destination(static_path, public_path)

if __name__ == "__main__":
    main()