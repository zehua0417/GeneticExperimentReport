# 果蝇表型数据管理

## 简介

本文档提供了有关 Python 代码的概述，该代码用于管理果蝇的表型数据，特别关注 F1 和 F2 代。代码包括两个类：`PhenotypicFruitData` 和 `GroupData`，每个类在组织和分析果蝇基因数据方面都有着不同的用途。

## PhenotypicFruitData 类

### 目的

`PhenotypicFruitData` 类旨在表示单个果蝇表型数据，封装了身体颜色、眼睛颜色、翅膀形状、毛刺类型、性别和数量等属性。

### 属性

* `m_body_color`：表示身体颜色的整数（0 为灰色，1 为黑色）。
* `m_eye_color`：表示眼睛颜色的整数（0 为白色，1 为红色）。
* `m_wing_shape`：表示翅膀形状的整数（0 为短，1 为长）。
* `m_bristle_type`：表示毛刺类型的整数（0 为卷曲，1 为直立）。
* `m_gender`：表示性别的整数（0 为雌性，1 为雄性）。
* `m_count`：表示具有给定表型的果蝇数量的整数。

### 方法

#### 获取器

* `get_body_color()`：返回身体颜色的字符串表示。
* `get_eye_color()`：返回眼睛颜色的字符串表示。
* `get_wing_shape()`：返回翅膀形状的字符串表示。
* `get_bristle_type()`：返回毛刺类型的字符串表示。
* `get_gender()`：返回性别的字符串表示。
* `get_count()`：返回具有给定表型的果蝇数量。
* `get_phenotype()`：返回完整表型的列表。

#### 设置器

* `set_count(count)`：设置具有给定表型的果蝇数量。

## GroupData 类

### 目的

`GroupData` 类管理一组果蝇数据，区分 F1 和 F2 代。它包括用于加载 F1 和 F2 数据、生成二进制列表、基于特征获取特定计数以及基于有效性检查过滤数据的方法。

### 属性

* `binary_combinations`：包含所有可能表型特征的二进制组合的列表。
* `m_orthogonal`：包含表示正交数据的 `PhenotypicFruitData` 对象的列表。
* `m_complementary`：包含表示补充数据的 `PhenotypicFruitData` 对象的列表。
* `m_generation`：表示代数的整数（1 为 F1，2 为 F2）。

### 方法

#### 初始化

* `__init__(data: np.ndarray, generation)`：使用输入数据和代数信息初始化类。

#### 加载数据

* `__load_f1_data__(data: np.ndarray)`：将 F1 代数据加载到类中。
* `__load_f2_data__(data: np.ndarray)`：将 F2 代数据加载到类中。

#### 数据操作

* `__set_specific_data__(phenotype: list, type, count)`：设置特定表型数据的计数。
* `generate_bin_list(trait, trait_id)`：基于特定特征生成二进制列表。

#### 获取器

* 多个方法（`get_specific_count`、`get_gender_count`、`get_body_color_count`、`get_eye_color_count`、`get_wing_shape_count`、`get_bristle_type_count`）以获取基于特征的特定计数。

#### 数据管理

* `clear(type="both")`：根据指定的类型（正交、补充或两者）清除数据。
* `check_data_validity(type="both")`：根据代数和类型检查数据的有效性。
* `filter_data(type="both")`：根据有效性检查过滤数据。

## 结论

提供的 Python 代码简化了果蝇表型数据的组织和分析，特别是在 F1 和 F2 代的背景下。`PhenotypicFruitData` 类表示个体表型数据，而 `GroupData` 类管理数据组，包括加载、操作和分析的方法。

## 用法

以下部分概述了这些类的基本用法，包括实例化、数据加载和常见数据分析任务。

### 实例化

```python
# 示例实例化 PhenotypicFruitData
fruit_data = PhenotypicFruitData(body_color=0, eye_color=1, wing_shape=0, bristle_type=1, gender=1, count=10)

# 示例实例化 F1 代的 GroupData
f1_data = np.array([...])  # 提供 F1 数据作为 NumPy 数组
group_f1 = GroupData(data=f1_data, generation=1)

# 示例实例化 F2 代的 GroupData
f2_data = np.array([...])  # 提供 F2 数据作为 NumPy 数组
group_f2 = GroupData(data=f2_data, generation=2)
```

### 数据加载和分析

```python
# 示例将 F1 数据加载到 GroupData 中
group_f1.__load_f1_data__(f1_data)

# 示例将 F2 数据加载到 GroupData 中
group_f2.__load_f2_data__(f2_data)

# 示例获取特定计数
count_female = group_f2.get_gender_count("female", type="both")
count_black_flies = group_f2.get_body_color_count("black", type="both")

# 示例数据过滤
is_data_valid = group_f2.filter_data(type="both")

# 根据需要进行额外的分析和数据操作
```