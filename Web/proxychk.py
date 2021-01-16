from proxy_checker import ProxyChecker
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from pathlib import Path
import argparse
import sys


parser = argparse.ArgumentParser(description='Check some proxy.')
parser.add_argument('proxy', nargs='*',
                    help='Proxy in format: ip:port ip:port...')
parser.add_argument('-i', '--infile', nargs='?', help='Read proxy from file.')
parser.add_argument('-o', '--outfile', action='store_true',
                    help='Write good proxy to file.')
parser.add_argument('-w', '--workers', action='count',
                    default=20, help='Count of threads.')
args = parser.parse_args()


if not (args.proxy or args.infile):
    parser.print_help()
    sys.exit(0)

if args.infile:
    proxy_path = Path(args.infile)

    if not proxy_path.is_file():
        raise Exception(
            'Proxyfile not exists. Please run with correct file path.')

    if args.outfile:
        good_proxy_path = proxy_path.parent.joinpath('good_proxy.csv')
else:
    if args.outfile:
        good_proxy_path = Path.cwd().joinpath('good_proxy.csv')


checker = ProxyChecker()


def proxy_handler(proxy_str):
    resp = checker.check_proxy(proxy_str)
    if resp:
        resp['protocols'] = '/'.join(resp['protocols'])
        resp_vals = list(str(i) for i in resp.values())
        return f'{proxy_str},{",".join(resp_vals)}\n'


if __name__ == '__main__':
    data = 'ip:port,protocols,anonymity,timeout,country,country_code\n'
    print('  '.join(i if n % 2 == 0 else f'\033[95m{i}\033[0m'
                    for n, i in enumerate(data.strip().split(','))))

    if args.outfile:
        with open(good_proxy_path, 'a') as f:
            f.write(data)

    if args.infile:
        with open(proxy_path) as f:
            proxies = [row.strip() for row in f]
    else:
        proxies = [row.strip() for row in args.proxy]

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        f = [executor.submit(proxy_handler, proxy) for proxy in proxies]
        for future in concurrent.futures.as_completed(f):
            try:
                data = future.result()
            except Exception as e:
                print(e)
            else:
                if not data:
                    continue

                print('  '.join(i if n % 2 == 0 else f'\033[95m{i}\033[0m'
                                for n, i in enumerate(data.strip().split(','))))

                if args.outfile:
                    with open(good_proxy_path, 'a') as f:
                        f.write(data)
