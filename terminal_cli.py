from providers import YellowPagesCanada, YellowPagesSpain
from analyzer import AnalyzeWeb
import argparse

providers = {
    'CA': YellowPagesCanada(),
    'ES': YellowPagesSpain()
}

parser = argparse.ArgumentParser()
parser.add_argument('--provider', type=str, help='ES or CA (Default: ES)', default='ES')
parser.add_argument('category', type=str, help='category to search')
parser.add_argument('location', type=str, help='city name')
parser.add_argument('n_pages', type=int, help='N pages to scan')
args = parser.parse_args()

for b in providers[args.provider].GetBusiness(args.category, args.location, args.n_pages):
    if b.website:
        print(f'[i] Analyzing {b.name}..')
        score = 0
        try:
            score = AnalyzeWeb(b.website)['lighthouseResult']['categories']['performance']['score']
        except KeyError:
            pass
        print(f'{b.website} -> {score}')