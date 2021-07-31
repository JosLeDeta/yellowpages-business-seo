from providers import YellowPagesCanada, YellowPagesSpain
import sys

providers = {
    'CA': YellowPagesCanada(),
    'ES': YellowPagesSpain()
}

if len(sys.argv) == 5:
    if not sys.argv[1] in providers.keys():
        print(f'Error! No website found to country: {sys.argv[1]}')
    else:
        for b in providers[sys.argv[1]].GetBusiness(sys.argv[2], sys.argv[3], int(sys.argv[4])):
            print(b)
else:
    usage = '''Usage: python main.py <provider> <category> <city> <pages>
    <provider> CA/ES
    <category> plumber
    <city> madrid
    <pages> 1'''
    print(usage)