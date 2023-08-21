import argparse
import requests


def process_request(url, args):
    match args.action:
        case "post":
            fp = open(args.file, 'rb')
            resp = requests.post(url, files={'file': fp})
            fp.close()
            print("Status code: ", resp.status_code)
            print(resp.text)

        case "get":
            if args.file is None:
                resp = requests.get(url)
            else:
                header = {'file': args.file}
                if args.filter:
                    header['filter'] = ';'.join(map(str, args.filter))
                if args.sort:
                    header['sort'] = ';'.join(map(str, args.sort))
                resp = requests.get(url, headers=header)
            print("Status code: ", resp.status_code)
            print(resp.text)

        case "delete":
            if args.file:
                resp = requests.delete(url)
            else:
                header = {'file': args.file}
                resp = requests.delete(url, headers=header)
            print("Status code: ", resp.status_code)
            print(resp.text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='action: post, get, delete')
    parser.add_argument('-f', '--file', help='path to the input file')
    parser.add_argument('-fi', '--filter', action='append', help='data filter (input with \'\')')
    parser.add_argument('-s', '--sort', action='append', help='sort columns')
    process_request("http://127.0.0.1:8000", parser.parse_args())


if __name__ == "__main__":
    main()
