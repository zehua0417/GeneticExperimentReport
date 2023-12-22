import numpy as np
from itertools import product

__f2_least_valid_num__ = 0.3


class PhenotypicFruitData:
    """
    PhenotypicFruitData类, 用于存储果蝇表型数据

    Attributes:
        m_body_color: 身体颜色, int, 0->灰色, 1->黑色
        m_eye_color: 眼睛颜色, int, 0->白色, 1->红色
        m_wing_shape: 翅膀形状, int, 0->短, 1->长
        m_bristle_type: 毛刺类型, int, 0->卷曲, 1->直立
        m_gender: 性别, int, 0->雌性, 1->雄性
        m_count: 数量, int
    """

    # Constructor #################
    def __init__(self,
                 body_color,
                 eye_color,
                 wing_shape,
                 bristle_type,
                 gender,
                 count=0,
                 ):
        self.m_body_color = body_color
        self.m_eye_color = eye_color
        self.m_wing_shape = wing_shape
        self.m_bristle_type = bristle_type
        self.m_gender = gender
        self.m_count = count

    # getters #####################
    def get_body_color(self):
        if self.m_body_color == 0:
            return "grey"
        elif self.m_body_color == 1:
            return "black"
        else:
            return "unknown"

    def get_eye_color(self):
        if self.m_eye_color == 0:
            return "white"
        elif self.m_eye_color == 1:
            return "red"
        else:
            return "unknown"

    def get_wing_shape(self):
        if self.m_wing_shape == 0:
            return "short"
        elif self.m_wing_shape == 1:
            return "long"
        else:
            return "unknown"

    def get_bristle_type(self):
        if self.m_bristle_type == 0:
            return "curly"
        elif self.m_bristle_type == 1:
            return "straight"
        else:
            return "unknown"

    def get_gender(self):
        if self.m_gender == 0:
            return "female"
        elif self.m_gender == 1:
            return "male"
        else:
            return "unknown"

    def get_count(self):
        return self.m_count

    def get_phenotype(self):
        """
        获取表型
        :return: 表型, list
        """
        phenotype = []
        phenotype.extend(
            [self.m_body_color, self.m_eye_color, self.m_wing_shape, self.m_bristle_type, self.m_gender]
        )
        return phenotype

    # setters #####################
    def set_count(self, count):
        """
        设置数量
        :param count: 数量
        """
        self.m_count = count


class GroupData:
    """
    GroupData类, 用于存储一组果蝇数据

    Attributes:
        binary_combinations: 二进制组合, list, (0, 0, 0, 0, 0)~(1, 1, 1, 1, 1)
        m_orthogonal: 正交数据, list
        m_complementary: 反交数据, list
        m_generation: 代数, int, 1->f1, 2->f2
    """

    # Constructor #################
    def __init__(self, data: np.ndarray, generation):
        # mylist = [myclass(*params) for params in binary_combinations]
        self.binary_combinations = list(product([0, 1], repeat=5))
        self.m_orthogonal = [PhenotypicFruitData(*params) for params in self.binary_combinations]
        self.m_complementary = [PhenotypicFruitData(*params) for params in self.binary_combinations]
        self.m_generation = generation
        if generation == 1:
            self.__load_f1_data__(data)
        elif generation == 2:
            self.__load_f2_data__(data)
        else:
            return

    def __set_specific_data__(self, phenotype: list, type, count):
        if len(phenotype) != 5:
            return
        index = self.binary_combinations.index(tuple(phenotype))
        if type == "orth":
            self.m_orthogonal[index].set_count(count)
        elif type == "comp":
            self.m_complementary[index].set_count(count)
        else:
            return

    def __load_f1_data__(self, data: np.ndarray):
        """
        加载f1数据
        :param data: f1数据
        """
        if self.m_generation != 1:
            return
        for i in range(0, 16):
            try:
                num = int(data[i])
            except:
                num = 0

            phenotype = []
            phenotype.append(1 ^ (i % 8 // 4))  # body color
            phenotype.append(1 ^ (i % 4 // 2))  # eye color
            phenotype.append(1 ^ (i % 4 // 2))  # wing shape
            phenotype.append(1 ^ (i % 4 // 2))  # bristle type
            phenotype.append((i + 1) % 2)  # gender

            if i < 8:
                self.__set_specific_data__(phenotype, "orth", num)
            else:
                self.__set_specific_data__(phenotype, "comp", num)

    def __load_f2_data__(self, data: np.ndarray):
        """
        加载f2数据
        :param data: f2数据
        """
        if self.m_generation != 2:
            return
        for i in range(data.shape[0]):
            for j in range(0, 8):
                try:
                    num = int(data[i][j])
                except:
                    num = 0

                phenotype = []
                phenotype.append(1 ^ (j % 4 // 2))  # body color
                # eye color, wing shape, bristle type
                # ugly code, but it works
                if i == 0:
                    phenotype.extend([1, 1, 1])
                elif i == 1:
                    phenotype.extend([0, 0, 0])
                elif i == 2:
                    phenotype.extend([0, 1, 1])
                elif i == 3:
                    phenotype.extend([1, 0, 0])
                elif i == 4:
                    phenotype.extend([1, 1, 0])
                elif i == 5:
                    phenotype.extend([0, 0, 1])
                elif i == 6:
                    phenotype.extend([1, 0, 1])
                elif i == 7:
                    phenotype.extend([0, 1, 0])
                else:
                    print("index error")
                    return  # error
                phenotype.append((j + 1) % 2)  # gender

                if j < 4:
                    self.__set_specific_data__(phenotype, "orth", num)
                else:
                    self.__set_specific_data__(phenotype, "comp", num)

    def __generate_bin_list__(self, trait, trait_id):
        trait_dic = {
            "body_color": 0,
            "eye_color": 1,
            "wing_shape": 2,
            "bristle_type": 3,
            "gender": 4
        }
        trait_position = trait_dic[trait]
        list1 = list(product([0, 1], repeat=trait_position))
        list2 = [trait_id]
        list3 = list(product([0, 1], repeat=4 - trait_position))
        result = []
        for item1 in list1:
            for item2 in list2:
                for item3 in list3:
                    # 将元组连接并添加到结果列表中
                    result.append(item1 + (item2,) + item3)
        return result

    def __generate_motify_bin_list__(self, trait_list: list, phenotype: list):
        head = 0
        phen = []
        count = 0
        for i in range(0, 5):
            if trait_list[i] == 1:
                temp = []
                if not phen:
                    add_list = list(product([0, 1], repeat=i - head))
                    phen = add_list
                    for item in phen:
                        temp.append(item + (phenotype[count],))
                    phen = temp
                    count = count + 1
                else:
                    add_list = list(product([0, 1], repeat=i - 1 - head))
                    temp = []
                    for item in phen:
                        for add in add_list:
                            temp.append(item + add + (phenotype[count],))
                    phen = temp
                    count = count + 1
                head = i

        add_list = list(product([0, 1], repeat=4 - head))
        temp = []
        for item in phen:
            for add in add_list:
                temp.append(item + add)
        phen = temp
        return phen

    # getters #####################
    def get_specific_count(self, phenotype: list, type):
        """
        获取特定数据
        :param phenotype: 表型, list
        :param type: 数据类型, str, "orth"->正交数据, "comp"->反交数据
        :return: 特定数据, int
        """
        if len(phenotype) != 5:
            print("phenotype length error")
            return
        index = self.binary_combinations.index(tuple(phenotype))
        if type == "orth":
            return self.m_orthogonal[index].get_count()
        elif type == "comp":
            return self.m_complementary[index].get_count()
        else:
            print("type error")
            return

    def get_motify_specific_count(self, trait_list: list, phenotype: list, type="both"):
        count = 0
        bin_list = self.__generate_motify_bin_list__(trait_list, phenotype)
        for item in bin_list:
            if type == "orth" or type == "both":
                count = count + self.get_specific_count(item, "orth")
            if type == "comp" or type == "both":
                count = count + self.get_specific_count(item, "comp")
        return count

    def get_count(self, type="both"):
        """
        获取数量
        :param type: 数据类型, str, "orth"->正交数据, "comp"->反交数据, "both"->正交和反交数据
        :return: 数量, int
        """
        count = 0
        if type == "orth" or type == "both":
            for item in self.m_orthogonal:
                count = count + item.get_count()
        if type == "comp" or type == "both":
            for item in self.m_complementary:
                count = count + item.get_count()
        return count

    def get_gender_count(self, gender, type="both"):
        """
        :param gender: 性别
        :param type: 筛选类型
        :return: count 性别数量
        """
        count = 0
        if gender == "male":
            gender_id = 0
        elif gender == "female":
            gender_id = 1
        else:
            return
        phenotype = self.__generate_bin_list__("gender", gender_id)
        if type == "orth" or type == "both":
            for phen in phenotype:
                count = count + self.get_specific_count(phen, "orth")
        if type == "comp" or type == "both":
            for phen in phenotype:
                count = count + self.get_specific_count(phen, "comp")
        return count

    def get_body_color_count(self, body_color, type="both"):
        """
        :param body_color: 身体颜色
        :param type: 筛选类型
        :return: count 身体颜色数量
        """
        count = 0
        if body_color == "grey":
            body_color_id = 1
        elif body_color == "black":
            body_color_id = 0
        else:
            return
        phenotype = self.__generate_bin_list__("body_color", body_color_id)
        if type == "orth" or type == "both":
            for phen in phenotype:
                count = count + self.get_specific_count(phen, "orth")
        if type == "comp" or type == "both":
            for phen in phenotype:
                count = count + self.get_specific_count(phen, "comp")
        return count

    def get_eye_color_count(self, eye_color, type="both"):
        """
        :param eye_color: 眼睛颜色
        :param type: 筛选类型
        :return: count 眼睛颜色数量
        """
        count = 0
        if eye_color == "white":
            eye_color_id = 0
        elif eye_color == "red":
            eye_color_id = 1
        else:
            return
        phenotype = self.__generate_bin_list__("eye_color", eye_color_id)
        if type == "orth" or type == "both":
            for phen in phenotype:
                count = count + self.get_specific_count(phen, "orth")
        if type == "comp" or type == "both":
            for phen in phenotype:
                count = count + self.get_specific_count(phen, "comp")
        return count

    def get_wing_shape_count(self, wing_shape, type="both"):
        """
        :param wing_shape: 翅膀形状
        :param type: 筛选类型
        :return: count 翅膀形状数量
        """
        count = 0
        if wing_shape == "short":
            wing_shape_id = 0
        elif wing_shape == "long":
            wing_shape_id = 1
        else:
            return
        phenotype = self.__generate_bin_list__("wing_shape", wing_shape_id)
        if type == "orth" or type == "both":
            for phen in phenotype:
                count = count + self.get_specific_count(phen, "orth")
        if type == "comp" or type == "both":
            for phen in phenotype:
                count = count + self.get_specific_count(phen, "comp")
        return count

    def get_bristle_type_count(self, bristle_type, type="both"):
        """
        :param bristle_type: 毛刺类型
        :param type: 筛选类型
        :return: count 毛刺类型数量
        """
        count = 0
        if bristle_type == "curly":
            bristle_type_id = 0
        elif bristle_type == "straight":
            bristle_type_id = 1
        else:
            return
        phenotype = self.__generate_bin_list__("bristle_type", bristle_type_id)
        if type == "orth" or type == "both":
            for phen in phenotype:
                count = count + self.get_specific_count(phen, "orth")
        if type == "comp" or type == "both":
            for phen in phenotype:
                count = count + self.get_specific_count(phen, "comp")
        return count

    # clear ########################
    def clear(self, type="both"):
        """
        清空数据
        :param type: 数据类型, str, "orth"->正交数据, "comp"->反交数据, "both"->正交和反交数据
        """
        if type == "both":
            for item in self.m_orthogonal:
                item.set_count(0)
            for item in self.m_complementary:
                item.set_count(0)
        elif type == "orth":
            for item in self.m_orthogonal:
                item.set_count(0)
        elif type == "comp":
            for item in self.m_complementary:
                item.set_count(0)
        else:
            return

    def check_data_validity(self, type="both"):
        """
       检查数据是否有效
       :param type: 数据类型, str, "orth"->正交数据, "comp"->反交数据, "both"->正交和反交数据
       :return: 数据是否有效, bool
       """
        count = 0
        if self.m_generation == 1:
            if type == "orth" or type == "both":
                valid_list = [[1, 1, 1, 1, 1], [1, 0, 0, 0, 0]]
                for item in self.m_orthogonal:
                    if not item.get_phenotype() in valid_list and item.get_count() > 0:
                        return False
            if type == "comp" or type == "both":
                valid_list = [[1, 1, 1, 1, 1], [1, 1, 1, 1, 0]]
                for item in self.m_complementary:
                    if not item.get_phenotype() in valid_list and item.get_count() > 0:
                        return False
        if self.m_generation == 2:
            # f2反交雌性应该只有黑/灰红直长(0, 1, 1, 1, 1)/(1, 1, 1, 1, 1)
            # if type == "orth" or type == "both":
            if type == "comp" or type == "both":
                valid_list = [[0, 1, 1, 1, 1], [1, 1, 1, 1, 1]]
                count = 0
                for item in self.m_complementary:
                    if item.get_gender() == "female" and not item.get_phenotype() in valid_list:
                        f2_comp_female = self.get_gender_count("female", "comp")
                        if f2_comp_female == 0:
                            continue
                        if (item.get_count() / f2_comp_female) > __f2_least_valid_num__:
                            return False
        return True

    def filter_data(self, type="both"):
        flag = 0
        if (type == "orth" or type == "both") and not self.check_data_validity("orth"):
            self.clear("orth")
            flag = flag + 1
        if (type == "comp" or type == "both") and not self.check_data_validity("comp"):
            self.clear("comp")
            flag = flag + 1
        if flag != 0:
            return False
        else:
            return True
