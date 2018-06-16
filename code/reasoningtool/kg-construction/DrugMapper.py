from QueryMyChem import QueryMyChem
from SynonymMapper import SynonymMapper


class DrugMapper:

    @staticmethod
    def map_drug_to_hp(chembl_id):
        """
        mapping between a drug and human phenotypes corresponding to side effects

        :param chembl_id: The CHEMBL ID for a drug

        :return: A set of strings containing the found hp ids or empty set if none where found
        """
        hp_set = set()
        if not isinstance(chembl_id, str):
            return hp_set
        umls_array = QueryMyChem.get_drug_side_effects(chembl_id)
        if len(umls_array) == 0:
            return hp_set
        sm = SynonymMapper()
        for umls_id in umls_array:
            hp_ids = sm.get_all_from_oxo(umls_id, 'HP')
            if hp_ids != None:
                for hp_id in hp_ids:
                    hp_set.add(hp_id)
        return hp_set


if __name__ == '__main__':
    hp_set = DrugMapper.map_drug_to_hp("KWHRDNMACVLHCE-UHFFFAOYSA-N")
    print(hp_set)
    print(len(hp_set))

    hp_set = DrugMapper.map_drug_to_hp("CHEMBL521")
    print(hp_set)
    print(len(hp_set))