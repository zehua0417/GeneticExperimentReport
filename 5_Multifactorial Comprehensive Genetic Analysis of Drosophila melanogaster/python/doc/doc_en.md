# Fruit Fly Phenotypic Data Management

## Introduction

This document provides an overview of the Python code that manages phenotypic data for fruit flies, specifically focusing on the F1 and F2 generations. The code includes two classes: `PhenotypicFruitData` and `GroupData`, each serving a distinct purpose in organizing and analyzing fruit fly genetic data.

## PhenotypicFruitData Class

### Purpose

The `PhenotypicFruitData` class is designed to represent individual fruit fly phenotypic data, encapsulating attributes such as body color, eye color, wing shape, bristle type, gender, and count.

### Attributes

* `m_body_color`: integer representing body color (0 for grey, 1 for black).
* `m_eye_color`: integer representing eye color (0 for white, 1 for red).
* `m_wing_shape`: integer representing wing shape (0 for short, 1 for long).
* `m_bristle_type`: integer representing bristle type (0 for curly, 1 for straight).
* `m_gender`: integer representing gender (0 for female, 1 for male).
* `m_count`: integer representing the count of fruit flies with the given phenotype.

### Methods

#### Getters

* `get_body_color()`: Returns the string representation of body color.
* `get_eye_color()`: Returns the string representation of eye color.
* `get_wing_shape()`: Returns the string representation of wing shape.
* `get_bristle_type()`: Returns the string representation of bristle type.
* `get_gender()`: Returns the string representation of gender.
* `get_count()`: Returns the count of fruit flies with the given phenotype.
* `get_phenotype()`: Returns the complete phenotype as a list.

#### Setters

* `set_count(count)`: Sets the count of fruit flies with the given phenotype.

## GroupData Class

### Purpose

The `GroupData` class manages a group of fruit fly data, distinguishing between F1 and F2 generations. It includes methods for loading F1 and F2 data, generating binary lists, obtaining specific counts based on traits, and filtering data based on validity checks.

### Attributes

* `binary_combinations`: List of binary combinations representing all possible phenotypic traits.
* `m_orthogonal`: List of `PhenotypicFruitData` objects representing orthogonal data.
* `m_complementary`: List of `PhenotypicFruitData` objects representing complementary data.
* `m_generation`: Integer representing the generation (1 for F1, 2 for F2).

### Methods

#### Initialization

* `__init__(data: np.ndarray, generation)`: Initializes the class with input data and generation information.

#### Loading Data

* `__load_f1_data__(data: np.ndarray)`: Loads F1 generation data into the class.
* `__load_f2_data__(data: np.ndarray)`: Loads F2 generation data into the class.

#### Data Manipulation

* `__set_specific_data__(phenotype: list, type, count)`: Sets count for specific phenotypic data.
* `generate_bin_list(trait, trait_id)`: Generates a binary list based on a specific trait.

#### Getters

* Various methods (`get_specific_count`, `get_gender_count`, `get_body_color_count`, `get_eye_color_count`, `get_wing_shape_count`, `get_bristle_type_count`) to obtain specific counts based on traits.

#### Data Management

* `clear(type="both")`: Clears data based on the specified type (orthogonal, complementary, or both).
* `check_data_validity(type="both")`: Checks the validity of data based on the generation and type.
* `filter_data(type="both")`: Filters data based on validity checks.

## Conclusion

The provided Python code facilitates the organization and analysis of fruit fly phenotypic data, particularly in the context of F1 and F2 generations. The `PhenotypicFruitData` class represents individual phenotypic data, while the `GroupData` class manages groups of data, including methods for loading, manipulation, and analysis.

## Usage

The following section outlines the basic usage of these classes, including instantiation, data loading, and common data analysis tasks.

### Instantiation

```python
# Example instantiation of PhenotypicFruitData
fruit_data = PhenotypicFruitData(body_color=0, eye_color=1, wing_shape=0, bristle_type=1, gender=1, count=10)

# Example instantiation of GroupData for F1 generation
f1_data = np.array([...])  # Provide F1 data as a NumPy array
group_f1 = GroupData(data=f1_data, generation=1)

# Example instantiation of GroupData for F2 generation
f2_data = np.array([...])  # Provide F2 data as a NumPy array
group_f2 = GroupData(data=f2_data, generation=2)
```

### Data Loading and Analysis

```python
# Example loading F1 data into GroupData
group_f1.__load_f1_data__(f1_data)

# Example loading F2 data into GroupData
group_f2.__load_f2_data__(f2_data)

# Example obtaining specific counts
count_female = group_f2.get_gender_count("female", type="both")
count_black_flies = group_f2.get_body_color_count("black", type="both")

# Example data filtering
is_data_valid = group_f2.filter_data(type="both")

# Additional analysis and data manipulation as needed
```