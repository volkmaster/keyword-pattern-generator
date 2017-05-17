import api_caller


__author__ = 'Ziga Vucko'


def main():
    keywords = ['Coexistence (exhibition)', 'Frankenstein', 'Exquisite corpse', 'Mutation', 'Interpassivity',
                'Interpretation (philosophy)', 'Identity (philosophy)', 'Kiosk', 'Ruin', 'Mashup (education)',
                'Diversification (marketing strategy)', 'Recycling', 'Entropy']

    for keyword in keywords:
        api_caller.run(keyword)


if __name__ == '__main__':
    main()
