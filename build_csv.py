#
# file: build_csv.py
# date: 20200816
# use: python build_csv.py
# version: 0.1
#

import os
import csv
import hashlib

def get_md5(string):
    byte_string = string.encode("utf-8")
    md5 = hashlib.md5()
    md5.update(byte_string)
    result = md5.hexdigest()
    return result

def build_executive_cayley(executive_prep, executive_import):
    with open(executive_prep, 'r', encoding='utf-8') as file_prep, open(executive_import, 'a', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=' ')

        for i, row in enumerate(file_prep_csv):
            if i == 0 or len(row) < 3:
                continue

            info_id = get_md5('{},{},{}'.format(row[0], row[1], row[2]))
            relation = [info_id, '<Person_ID>', row[0], "."]
            file_import_csv.writerow(relation)

    print('build executive cayley done.')


def build_stock_cayley(stock_industry_prep, stock_concept_prep, stock_import):

    stock = set()  # 'code,name'

    with open(stock_industry_prep, 'r', encoding='utf-8') as file_prep:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            code_name = '{},{}'.format(row[0], row[1].replace(' ', ''))
            stock.add(code_name)

    with open(stock_concept_prep, 'r', encoding='utf-8') as file_prep:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            code_name = '{},{}'.format(row[0], row[1].replace(' ', ''))
            stock.add(code_name)

    with open(stock_import, 'w', encoding='utf-8') as file_import:
        file_import_csv = csv.writer(file_import, delimiter=',')
        headers = ['stock_id:ID', 'name', 'code', ':LABEL']
        file_import_csv.writerow(headers)
        for s in stock:
            split = s.split(',')
            ST = False  # ST flag
            states = ['*ST', 'ST', 'S*ST', 'SST']
            info = []
            for state in states:
                if split[1].startswith(state):
                    ST = True
                    split[1] = split[1].replace(state, '')
                    info = [split[0], split[1], split[0], 'Company;ST']
                    break
                else:
                    info = [split[0], split[1], split[0], 'Company']
            file_import_csv.writerow(info)

    print('build stock cayley done.')


def build_concept_cayley(stock_concept_prep, concept_import):
    with open(stock_concept_prep, 'r', encoding='utf-8') as file_prep, open(concept_import, 'a', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=' ')

        concepts = set()
        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            concepts.add(row[2])
        for concept in concepts:
            concept_id = get_md5(concept)
            relation = [concept, '<Concept_ID>', concept_id, "."]
            file_import_csv.writerow(relation)

    print('build concept cayley done.')


def build_industry_cayley(stock_industry_prep, industry_import):
    with open(stock_industry_prep, 'r', encoding="utf-8") as file_prep, open(industry_import, 'a', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=' ')

        industries = set()
        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            industries.add(row[2])
        for industry in industries:
            industry_id = get_md5(industry)
            relation = [industry_id, '<Industry_ID>', industry, "."]
            file_import_csv.writerow(relation)

    print('build industry cayley done.')


def build_executive_stock_cayley(executive_prep, relation_import):
    with open(executive_prep, 'r', encoding='utf-8') as file_prep, open(relation_import, 'a', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=' ')

        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            # generate md5 according to 'name' 'gender' and 'age'
            start_id = get_md5('{},{},{}'.format(row[0], row[1], row[2]))
            end_id = row[3]  # code
            relation = [start_id, '<employ_of>', end_id, "."]
            file_import_csv.writerow(relation)

    print('build executive stock cayley done.')


def build_stock_industry_cayley(stock_industry_prep, relation_import):
    with open(stock_industry_prep, 'r', encoding='utf-8') as file_prep, \
        open(relation_import, 'a', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=' ')

        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            industry = row[2]
            start_id = row[0] #code
            end_id = get_md5(industry)
            relation = [start_id, '<industry_of>', end_id, "."]
            file_import_csv.writerow(relation)

        print('build stock->industry cayley done.')


def build_stock_concept_cayley(stock_concept_prep, relation_import):
    with open(stock_concept_prep, 'r', encoding='utf-8') as file_prep, \
        open(relation_import, 'a', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=' ')

        # headers = [':START_ID', ':END_ID', ':TYPE']
        # file_import_csv.writerow(headers)

        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            concept = row[2]
            start_id = row[0]  # code
            end_id = get_md5(concept)
            relation = [start_id, '<concept_of>', end_id, "."]
            file_import_csv.writerow(relation)


if __name__ == '__main__':
    import_path = 'data/import'
    if not os.path.exists(import_path):
        os.makedirs(import_path)

    build_stock_cayley('data/stock_industry_prep.csv', 'data/stock_concept_prep.csv', 'data/import/stock.csv')
    build_executive_cayley('data/executive_prep.csv', 'data/import/cayley.nq')
    build_concept_cayley('data/stock_concept_prep.csv', 'data/import/cayley.nq')
    build_industry_cayley('data/stock_industry_prep.csv', 'data/import/cayley.nq')
    build_executive_stock_cayley('data/executive_prep.csv', 'data/import/cayley.nq')
    build_stock_industry_cayley('data/stock_industry_prep.csv', 'data/import/cayley.nq')
    build_stock_concept_cayley('data/stock_concept_prep.csv', 'data/import/cayley.nq')

