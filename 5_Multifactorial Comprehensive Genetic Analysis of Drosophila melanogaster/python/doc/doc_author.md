# 果蝇多因素遗传数据分析代码文档

## 用于存储数据的数据类型
```txt
f1_data, f2_data =
[
  GroupData(  
    [PhenotypicFruitFlyCount1, PhenotypicFruitFlyCount2, ...]  
  ), GroupData(...), ...  
]  
```

## class
### PhenotypicFruitFlyCount:
* 简介: 
  * 用于统计单个表现型果蝇的数量
  * 位置: "./flydataclass.py"
* 类成员: 
  * m_body_color, 体色, string; 0 -> 黑色, 1 -> 灰色.
  * m_eye_color, 眼色, string; 0 -> 白色, 1 -> 红色.
  * m_wing_shape, 翅型, string; 0 -> 短翅, 1 -> 长翅.
  * m_bristle_type: 刚毛, string; 0 -> 焦刚毛, 1 -> 直刚毛.
  * m_gender: 性别, string; 0 -> 雄性, 1 -> 雌性.
  * m_count: 计数, int; -1 -> 无数据, * -> 该表现型的果蝇的数目.
* 类方法:
  * __init__:
    * 简介: 构造函数, 用于初始化类成员.
    * @param body_color eye_color wing_shape bristle_type gender count
  * getter:
    * 简介: 用于获取类成员.
    * @return 类成员值对应的英文(str), eg: "black", "straight"

### GroupData:
* 简介: 
  * 用于统计单个组的f1或f2果蝇统计情况
  * 位置: "./flydataclass.py"
* 类成员:
  * m_orthogonal: list, 用于存储正交表的数据.
  * m_complementary: list, 用于存储反交表的数据.
  * m_generation: string, 用于存储代数, "f1" or "f2".
* 列表成员属性与索引时间的关系:
```txt
m_orthogonal = m_complementary = list[
    1. (0, 0, 0, 0, 0), 黑白短焦雄
    2. (0, 0, 0, 0, 1), 黑白短焦雌
    3. (0, 0, 0, 1, 0), 黑白短直雄
    4. (0, 0, 0, 1, 1), 黑白短直雌
    5. (0, 0, 1, 0, 0), 黑白长焦雄
    6. (0, 0, 1, 0, 1), 黑白长焦雌
    7. (0, 0, 1, 1, 0), 黑白长直雄
    8. (0, 0, 1, 1, 1), 黑白长直雌
    9. (0, 1, 0, 0, 0), 黑红短焦雄
    10. (0, 1, 0, 0, 1), 黑红短焦雌
    11. (0, 1, 0, 1, 0), 黑红短直雄
    12. (0, 1, 0, 1, 1), 黑红短直雌
    13. (0, 1, 1, 0, 0), 黑红长焦雄
    14. (0, 1, 1, 0, 1), 黑红长焦雌
    15. (0, 1, 1, 1, 0), 黑红长直雄
    16. (0, 1, 1, 1, 1), 黑红长直雌 # f2_comp
    17. (1, 0, 0, 0, 0), 灰白短焦雄 # f1_orth
    18. (1, 0, 0, 0, 1), 灰白短焦雌
    19. (1, 0, 0, 1, 0), 灰白短直雄
    20. (1, 0, 0, 1, 1), 灰白短直雌
    21. (1, 0, 1, 0, 0), 灰白长焦雄
    22. (1, 0, 1, 0, 1), 灰白长焦雌
    23. (1, 0, 1, 1, 0), 灰白长直雄
    24. (1, 0, 1, 1, 1), 灰白长直雌
    25. (1, 1, 0, 0, 0), 灰红短焦雄
    26. (1, 1, 0, 0, 1), 灰红短焦雌
    27. (1, 1, 0, 1, 0), 灰红短直雄
    28. (1, 1, 0, 1, 1), 灰红短直雌
    29. (1, 1, 1, 0, 0), 灰红长焦雄
    30. (1, 1, 1, 0, 1), 灰红长焦雌
    31. (1, 1, 1, 1, 0), 灰红长直雄 # f1_comp
    32. (1, 1, 1, 1, 1)  灰红长直雌 # f1_orth & f1_comp & f2_comp
](32)
```
* 类方法:
  * __init__:
    * 简介: 构造函数, 用于初始化类成员.
    * @param data(np.array)
    * @param generation(string)
    * @example: GroupData(np.array([[1, 2], [3, 4]]), "f1")
  * getter:
    * 简介: 用于获取类成员, m_orthogonal, m_complementary, m_generation.
  * filter:
    * 简介: 用于过滤数据, 选择特定表现型的果蝇数据.
    * 方法名: filter_[body_color, eye_color, wing_color, bristle_type, gender]
    * @param: feature(string), 用于选择的表现型, eg: "black", "straight".
    * @return: GroupData, 过滤后的数据.
    * 状态: TODO
